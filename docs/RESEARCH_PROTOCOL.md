# Public-source research protocol — ATM9 Expert

## Why this exists

ATM9 Expert is not just the union of individual Mod recipes. Pack KubeJS scripts may remove a Mod recipe, replace it with GregTech processing, introduce custom items, or link otherwise unrelated Mods. A credible guide must reconstruct the **effective recipe graph**, not copy a standard Mekanism wiki page.

A source-code-only answer is a **hypothesis about the effective game registry**, not evidence that the recipe was observed running in a particular game installation.

### Frozen reference set for the first test (2026-11-08)

- Pack: `AllTheMods/atm9-expert@309d0fa357b00d855f3a50739ae64737f7537936`.
- GregTech Modern: `GregTechCEu/GregTech-Modern@e24b2387318d1b70a0d5d651dba56a1baa5f2a6c` (1.20.1 branch snapshot; **version parity unverified**).
- Main test: `mekanism:metallurgic_infuser`.
- Always log the effective pack/Mod versions if later discovered from the target installation.

## Search checklist

### A. Confirm item identity and effective definition

- Search both exact `namespace:item` and unique suffix in the pack.
- Inspect `kubejs/server_scripts/recipeRemovals.js`. It contains arrays of recipe IDs later passed to `allthemods.remove`. Confirm the removal call executes; a list entry alone is not a complete execution trace.
- Search `kubejs/server_scripts/Gregification/`, other `kubejs/server_scripts/`, and `kubejs/data/**/recipes/`.
- A search result can be an **ingredient use**, not a **recipe output**: inspect context for `itemOutputs`, `output`, `addAssemblyLine`, `allthemods.shaped`, etc.
- For helper builders, open the function definition to confirm `itemInputs`, `inputFluids`, `duration`, `EUt`, and generated ID behavior.
- Inspect similarly named recipes, duplicates, alternatives, and global removal patterns. Flag uncertainty if all overrides cannot be enumerated.
- If pack definitions are absent, inspect the correct version of Mod source (generated JSON, Java datagen, or equivalent). Record the **version mismatch risk**.

### B. Prefer targeted source discovery

Example GitHub code-search terms:
```text
repo:AllTheMods/atm9-expert "mekanism:metallurgic_infuser"
repo:AllTheMods/atm9-expert "mekanism:steel_casing"
repo:AllTheMods/atm9-expert "thermal:machine_frame"
repo:GregTechCEu/GregTech-Modern "electric_motor_luv"
```
GitHub web/code-search syntax and connected search tools may differ. When using a connector that takes separate repository arguments, pass `repository_name` separately instead of query qualifiers. Use **one tree index / targeted file list**, then directly retrieve exact candidate files. Do not scan the same repository from scratch for every dependency.

Most useful locations:
- `kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js`
- `kubejs/server_scripts/Gregification/Machine_Recipes/assembler.js`
- `kubejs/server_scripts/Gregification/Mods/`
- `kubejs/server_scripts/recipeRemovals.js`
- GregTech upstream: `src/main/java/com/gregtechceu/gtceu/data/recipe/misc/ComponentRecipes.java`
- GregTech upstream: `src/main/java/com/gregtechceu/gtceu/data/recipe/misc/MetaTileEntityLoader.java`
- `config/ftbquests/` is useful progress **context**, but a quest or reward is NOT proof of an item crafting recipe.

### C. Extract a normalized recipe record

Each recipe should identify:
```json
{
  "output": {"id": "namespace:item", "count": 1},
  "machine": "machine_id_or_station",
  "inputs": [{"id_or_tag": "namespace:item OR #tag", "count": 2}],
  "fluids_mb": [{"id_or_tag": "namespace:fluid OR #tag", "amount": 144}],
  "nonconsumed": ["optional_catalyst_or_tool"],
  "processing": {"voltage_tier": "LuV", "duration_ticks": 1000},
  "research": {"type": "scanner|station|none|unknown", "subject": null},
  "source": {"repo": "owner/repo", "commit": "sha", "path": "file"},
  "evidence": "pack_source_confirmed|upstream_reference|unverified"
}
```
`#forge:...` and `#gtceu:...` are tags, not unique item IDs. Retain the source tag until mapping its valid members at the target version.

### D. Expand as a graph rather than a giant recursive essay

Recipe `R` with output count `o` and desired output `n`: `crafts = ceil(n / o)`. Every input count and consumed fluid amount is multiplied by `crafts`.

- Recipe choice: one result may have several recipes; record alternatives, but compute totals for **one explicit chosen branch**.
- Intermediate item: recurse only when within depth budget and not owned already.
- Reuse: add counts from independent branches before expanding common subrecipes (avoid double counting or undercounting).
- Cycle: mark any dependency leading back to an ancestor or requiring the currently unbuilt machine. Do not present a cyclic plan as feasible.
- Mechanism: distinguish an ingredient from the *machine/tool/research/catalyst required to perform* the recipe.
- Stop conditions: player already owns item, source not found, depth reached, known impossible dependency, missing Mod version, or alternative still undecided.
- Represent blockers as explicit `unresolved` nodes. Do not silently assume basic iron or steel is already available.
- Summation rule: label `direct inputs`, `expanded subtotal`, and `complete raw-material total` differently. A partial total MUST name excluded branches.

### E. Interpret source code cautiously

- KubeJS `allthemods.recipes.gtceu.assembly_line(...)` needs an assembly line; do not call this a normal crafting-table recipe.
- `GTValues.VA[LuV]` or a tier symbol means a voltage-tier requirement; do not guess exact EU/t if not checked.
- `duration(1000)` means 1000 game ticks; 50 seconds at 20 TPS, not a guaranteed real-world duration under lag.
- `scannerResearch`, `stationResearch`, `notConsumable`, `circuitMeta` and cleanroom are important player prerequisites.
- A displayed `#tag` may correspond to multiple usable items; never replace with a single unverified member.
- An all-rights-reserved pack can be linked and summarized; avoid copying bulk code/data into this repo.

## Verification and reporting levels

| Status | Means | Allowed wording |
| --- | --- | --- |
| `pack_source_confirmed` | Exact producer/removal/parameter visible in pinned pack source | 「公開ATM9 Expertソースに定義されている」 |
| `upstream_reference` | Recipe visible in another Mod's source but pack version/override not verified | 「Mod本体の参考レシピ」 |
| `derived` | Arithmetic/dependency inferred from identified source recipes | 「選んだレシピ経路から算出」 |
| `game_verified` | Personally supplied/verified in-game JEI or runtime registry data | 「ゲーム内で確認済み」 |
| `unresolved` | Source or effective behavior cannot yet be established | 「未確認」 |

A row with `pack_source_confirmed` must still not claim `game_verified`. Treat the pack source as a versioned input, not the final runtime oracle.

## Acceptance checklist before presenting any new item

- [ ] Exact item ID, target pack commit, upstream version status recorded
- [ ] Pack removal and matching producers checked
- [ ] Output vs input uses distinguished
- [ ] Main machine, voltage tier, processing time and fluids checked
- [ ] Research, nonconsumed catalysts and tools checked or explicitly unknown
- [ ] Every leaf in displayed dependency tree has a source or `unresolved` marker
- [ ] Alternative recipes are not mixed into one material total
- [ ] Quantities obey output yields and branching; material totals clearly scoped
- [ ] URLs point to exact files/commits rather than generic landing pages
- [ ] Proposed steps stop before unverified deadlocks or prerequisites

## Next data-collection milestone

Replace slow one-file-at-a-time agent browsing with **offline indexing** of allowed public recipe definitions (plus versioned provenance), then resolve dependency edges on demand. The long-term best source is an authorized **runtime recipe export from the same modpack instance**, when available; until then keep confidence labels. No runtime/JEI export is claimed for this project.
