#!/usr/bin/env python3
"""Validate a versioned ATM9 Expert research fixture using Python's stdlib.

Usage:
    python scripts/validate_case.py examples/mekanism_metallurgic_infuser.json

This checks internal bookkeeping, NOT whether in-game/JEI recipes match source code.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


# Explicit grouping for report purposes only; tag membership is NOT verified.
FLUID_FAMILY = {
    "#forge:soldering_alloy": "soldering_alloy",
    "gtceu:soldering_alloy": "soldering_alloy",
    "#forge:lubricant": "lubricant",
    "gtceu:lubricant": "lubricant",
    "gtceu:polytetrafluoroethylene": "polytetrafluoroethylene",
    "gtceu:styrene_butadiene_rubber": "styrene_butadiene_rubber",
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate(data: dict) -> None:
    check(data["target"]["count"] > 0, "Target must be a positive quantity")
    recipes = {}
    for recipe in data["recipes"]:
        key = recipe["key"]
        check(key not in recipes, f"Duplicate recipe key: {key}")
        recipes[key] = recipe
        check(recipe["output"]["count"] > 0, f"{key}: invalid output count")
        check(recipe["duration_ticks"] > 0, f"{key}: invalid duration")
        check(recipe["source"]["commit"], f"{key}: missing source commit")
        check(recipe["source"]["path"], f"{key}: missing source path")
        check(recipe["evidence"] in ("pack_source_confirmed", "upstream_reference"),
              f"{key}: invalid evidence status")
        for form, amount in recipe["inputs"]:
            check(isinstance(form, str) and amount > 0,
                  f"{key}: invalid input")
        for form, amount in recipe["fluids_mb"]:
            check(isinstance(form, str) and amount > 0,
                  f"{key}: invalid fluid")

    plan = data["chosen_expansion"]
    counts = plan["production_counts"]
    for key, n in counts.items():
        check(key in recipes and isinstance(n, int) and n > 0,
              f"Invalid production count for {key}")
    check(counts["infuser"] == data["target"]["count"],
          "This fixture assumes one infuser recipe output per craft")

    # Verify the transitive motor requirement across all chosen consumers.
    motors_needed = sum(
        count * amount
        for key, count in counts.items()
        if key != "luv_motor"
        for form, amount in recipes[key]["inputs"]
        if form == "gtceu:luv_electric_motor"
    )
    check(motors_needed == counts["luv_motor"],
          f"LuV motors: declared {counts['luv_motor']}, inferred {motors_needed}")

    # Verify included fluid subtotals exactly match selected recipes.
    totals = defaultdict(int)
    for key in plan["inclusions"]:
        check(key in counts, f"Included recipe not in production plan: {key}")
        recipe = recipes[key]
        for name, amount in recipe["fluids_mb"]:
            check(name in FLUID_FAMILY,
                  f"{key}: no explicit fluid-family mapping for {name}")
            totals[FLUID_FAMILY[name]] += amount * counts[key]

    expected = plan["partial_consumed_fluid_totals_mb"]
    check(dict(totals) == expected,
          f"Fluid subtotals differ: calculated={dict(totals)}, recorded={expected}")

    # Check only the known tracked inter-recipe edges. Opaque items/tags remain unresolved.
    for child_id, child_key in (
        ("mekanism:steel_casing", "steel_casing"),
        ("thermal:machine_frame", "thermal_frame"),
        ("gtceu:thermal_spark", "thermal_spark"),
        ("gtceu:luv_electric_pump", "luv_pump"),
        ("gtceu:luv_conveyor_module", "luv_conveyor"),
    ):
        demand = sum(
            count * amount
            for parent_key, count in counts.items()
            if parent_key != child_key
            for form, amount in recipes[parent_key]["inputs"]
            if form == child_id
        )
        check(counts[child_key] * recipes[child_key]["output"]["count"] >= demand,
              f"Underproducing {child_id}: demand={demand}")

    check(not data["effective_recipe_status"]["runtime_verified"],
          "Fixture is a public-source-only test and must not imply runtime verification")

    print(f"VALID (source-only, partial expansion): {data['case_id']}")
    print(f"  Recipes: {len(recipes)}; LuV motors: {motors_needed}")
    for name, amount in sorted(totals.items()):
        print(f"  {name}: {amount} mB")
    print("  WARNING: Does not check GitHub contents, pack load order, or in-game JEI.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    validate(json.loads(args.fixture.read_text(encoding="utf-8")))


if __name__ == "__main__":
    main()
