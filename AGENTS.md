# AGENTS.md — ATM9 Expert recipe research instructions

## Your mission

Turn a requested item (e.g. `mekanism:metallurgic_infuser`) into a **source-grounded, versioned and progressively expandable crafting plan** for ATM9 Expert. The user wants actionable steps, not an unsourced generic wiki recipe.

**Read:** `docs/RESEARCH_PROTOCOL.md` and `examples/mekanism_metallurgic_infuser.md` before a new research task. Follow the pinned examples as methodology, not universal truth.

## Non-negotiable rules

1. **ATM9 Expert overrides generic mod recipes.** Look for pack recipe removal and additions first; a removed vanilla/Mekanism recipe must NOT be reported as the playable recipe.
2. **Source code is not the live game registry.** Distinguish `pack source confirmed`, `upstream source reference`, `derived`, and `unverified in game`. Do not claim JEI confirmation without actual in-game evidence.
3. **Use exact sources.** Provide repository, commit/ref, file path, preferably line range. Do not substitute an internet snippet for opening the definition.
4. **Follow recipe outputs, not merely filenames.** KubeJS can create outputs through helper functions such as `addAssemblyLine('mekanism:metallurgic_infuser', ...)`; generated recipe IDs may not be literal in any JSON file.
5. **Respect removal / replacement.** Check `kubejs/server_scripts/recipeRemovals.js`, other KubeJS scripts, datapack recipes, and matching output IDs, including dynamically constructed IDs.
6. **Never turn a tag into an unqualified fixed item.** `#gtceu:circuits/luv` means an accepted tag: record the tag, not an invented circuit item. Alternative materials or recipes are separate branches.
7. **Keep quantities and units precise.** Track item counts, fluid mB, output counts, electricity tier, time in ticks; use ceil(needed/output quantity). Include consumed / nonconsumed catalysts separately. Tool symbols in crafting grids are not automatically consumed.
8. **Don't hide prerequisites.** Record crafting machine, power tier, scanner/station research and its subject, cleanroom, circuit settings, non-consumed tools, multiblocks if relevant.
9. **Avoid invented completion.** Unknown steps remain `unresolved`. Do not guess basic-resource totals if dependency branches, material substitutions, or recipes are unknown.
10. **Avoid exhaustive expansion by default.** First show 1-hop recipe; then expand selected dependencies up to 2 hops. Stop at user's owned inventory/equipment and at explicit depth/cost limits.
11. **Check version compatibility.** Record pack commit and actual shipped Mod version when known; otherwise upstream reference remains provisional.
12. **Be efficient.** Find the likely source path once, use repository code search plus direct file fetch. Avoid repeatedly re-searching the whole web for a known output.

## Research order

1. Normalize requested Japanese/English name to the **exact namespace:item ID**. Check alternate meanings; do not silently select a different machine.
2. Record project target/version; locate the ATM9 Expert GitHub repository and pin a commit.
3. Search pack KubeJS/datapack for `item ID`, `addShaped`/`addAssembler`/`addAssemblyLine`, `itemOutputs` and recipe removal. Open matching files.
4. Check recipes that produce this item, not recipes merely using it as an input.
5. If no pack recipe defines it, inspect relevant Mod source / generated recipes at a matching version (if possible). Do not assume silence proves unmodified.
6. Normalize each viable recipe as: output ×count, input items, input fluids, nonconsumed items, tool requirements, machine, tier/EUt, time, research and evidence.
7. Expand dependencies selectively. Detect cycles and machine prerequisites; prefer feasible recipes that don't require the item being built.
8. Calculate resource totals for the **chosen path only**; don't add alternative recipes together. Exclude unknown branches from any claimed complete totals.
9. Report verified facts separately from inferred/transitive values and unknowns.
10. Finish with next actionable step and links.

## Required response format

- **Target:** item ID × desired quantity / game+pack commit / evidence status
- **Direct recipe:** method, tier, time, item table, fluid table, tools/research
- **Dependency tree:** 1–2 hops, shared ingredients deduplicated for totals
- **Ordered steps:** prerequisites before final assembly
- **Totals:** state which subrecipes and alternatives are included/excluded
- **Sources:** per-link fixed commit; pack vs upstream; explicitly unverified issues
- **Progress:** `confirmed` / `partial` / `unresolved`; never claim 100% without all branches

## Critical known example

`mekanism:metallurgic_infuser`:
- Pack removal: `kubejs/server_scripts/recipeRemovals.js` includes `mekanism:metallurgic_infuser`.
- Pack replacement: `kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js` has an `addAssemblyLine` output for it.
- It uses a `mekanism:steel_casing` which itself uses a `thermal:machine_frame` via a DIFFERENT assembly-line recipe.
- `thermal:machine_frame` is made in a GregTech assembler and uses `gtceu:thermal_spark`; `thermal_spark` has a separate Sanguine Alchemy path.
- LuV components depend on further LuV motors; do not count only the direct listed motor.
- Exact evidence and quantities: `examples/mekanism_metallurgic_infuser.md`.

## Mandatory research log (every research run)

Before beginning a new item investigation:
1. Open `research-logs/README.md` and check related previous logs.
2. Create a **new** log under `research-logs/YYYY-MM-DD_<namespace>_<item>_<agent-or-run>.md` based on `research-logs/TEMPLATE.md`. Do not overwrite another agent's log or the template.
3. As you search, record **actual** queries, file paths, fixed-commit URLs, hits and misses, source-vs-inference status, recipe decisions, and explicit unresolved items. Do not claim searches you didn't execute.
4. Close the log with status, next actionable steps, and a link to the final output under `examples/` (if created). Update `research-logs/README.md` index when practical; if multiple agents may edit it concurrently, save your unique log first to avoid conflicts.
5. If repository write access is unavailable, provide the log as Markdown for an authorized maintainer to commit; never claim you saved it remotely if you could not.

**A final recipe explanation in `examples/` is NOT a substitute for the chronological search log.** The log documents the reasoning path and dead ends, not just the final ingredients. If the user specifically requests a search history but not new recipe research, work in `research-logs/` only.

## Writing into this repo

When documenting new results, add a `examples/<namespace>_<item>.md` with pinned permalinks and a short confidence table. Optionally add JSON using the shape of the existing example. Do not edit upstream repositories. Do not label copied upstream code as ours. Preserve uncertainty and provenance, even if this makes the result less impressive.
