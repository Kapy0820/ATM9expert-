# 再現テスト — Mekanism 冶金吹込機

**目的:** ATM9 Expertの「冶金吹込機」1個の作成方法を、ゲーム内からのレシピ出力なしで、公開ソースから段階的に導けるか検証する。

- 対象: `mekanism:metallurgic_infuser` ×1
- パックソース: `AllTheMods/atm9-expert@309d0fa357b00d855f3a50739ae64737f7537936`
- GTCEu参考ソース: `GregTechCEu/GregTech-Modern@e24b2387318d1b70a0d5d651dba56a1baa5f2a6c`（1.20.1ブランチのスナップショット）
- 実ゲーム/JEI照合: **未実施**
- GTCEu Mod本体とATM9 Expertに収録された版の一致: **未確認**
- 結果: 主レシピ・いくつかの中間部品・限定範囲の数量合算に成功。原料採取までの完走は未達成。

## 1. 最も重要な検索結果: 通常のMekanismレシピは使わない

[パックのrecipeRemovals.js](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/recipeRemovals.js#L510-L523) に `mekanism:metallurgic_infuser` が削除対象IDとして現れ、同ファイルの後半で削除対象が `allthemods.remove(...)` に渡される。したがって **通常のMekanism作業台レシピをそのまま報告しない**。

代わりに [AssemblyLine.jsの製造定義](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js#L746-L764) を調べる。関数 `addAssemblyLine` の実装は[ファイル冒頭](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js#L4-L51) にあり、`itemInputs` / `inputFluids` / `itemOutputs` を登録する。

### 完成品の直接レシピ（パックソースで確認）

| 入力アイテム（正確なID/タグ） | 個数 |
| --- | ---: |
| `mekanism:steel_casing` | 1 |
| `gtceu:luv_electric_pump` | 2 |
| `gtceu:luv_electric_motor` | 1 |
| `gtceu:luv_conveyor_module` | 2 |
| `#gtceu:circuits/luv` | 2 |
| `#forge:plates/hafnium` | 4 |
| `gtceu:laminated_glass` | 2 |

| 入力流体 | 量 |
| --- | ---: |
| `gtceu:polytetrafluoroethylene` | 144 mB |
| `#forge:lubricant` | 1,440 mB |
| `#forge:soldering_alloy` | 1,440 mB |

- 装置: GregTech組立ライン（Assembly Line）
- 電圧クラス: LuV（ソースの `EUt(LuV)`）
- 時間: 1000 ticks = 50秒（20 TPS時）
- 出力: `mekanism:metallurgic_infuser` ×1
- このレシピの呼び出しには `researchItem` 引数が渡されていない。**ただし各素材や製造装置の前提研究が不要とは限らない。**

## 2. 鋼鉄ケーシングを展開する（1段下）

[同じAssemblyLine.js](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js#L153-L173) で `mekanism:steel_casing` も出力として定義されている。

| 入力 | 個数 |
| --- | ---: |
| `thermal:machine_frame` | 1 |
| `#forge:plates/osmiridium` | 4 |
| `#forge:plates/hafnium` | 4 |
| `#forge:gears/plastic` | 8 |
| `#forge:rods/hop_graphite` | 2 |
| `#forge:soldering_alloy` | 288 mB |
| `#forge:lubricant` | 288 mB |

- 装置: 組立ライン、LuV、100 ticks
- 研究: `thermal:machine_frame` が **scannerResearch** の研究対象。研究完了/方法はプレイヤー側で要確認。
- 元々の `mekanism:steel_casing` レシピも[削除対象](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/recipeRemovals.js#L515-L522)。

## 3. Thermal機械フレームを展開する（さらに1段下）

[パック側assembler.js](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/assembler.js#L722-L735) では、`thermal:machine_frame` をIV組立機のレシピとして定義。

| 入力 | 個数 |
| --- | ---: |
| `gtceu:thermal_spark` | 1 |
| `#forge:plates/tungsten_steel` | 4 |
| `#forge:screws/terrasteel` | 4 |
| `#forge:small_gears/plastic` | 8 |
| `#gtceu:circuits/iv` | 2 |
| `gtceu:iv_electric_piston` | 2 |
| `gtceu:polytetrafluoroethylene` | 144 mB |

- 装置: 組立機（Assembler）、IV、600 ticks
- Thermal側の `thermal:machine_frame` レシピは[削除対象](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/recipeRemovals.js#L110-L150)。

Thermal Sparkには、[Sanguine_Synthesizer.js](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/CustomMultiblocks/Sanguine_Synthesizer.js#L34-L43) の `sanguine_alchemy` レシピがある。材料は `botania:corporea_spark` 1、`#forge:exquisite_gems/nitro_crystal` 1、`#forge:rounds/pink_slime` 4、`#forge:rings/draconium_awakened` 1。**`gtceu:technomancy_orb` は非消費の必要アイテム**。LuV・1000 ticks。Sanguine Alchemy装置自体の製作はまだ展開していない。

## 4. LuV部品から共有するモーター数を計算

[上流GTCEu ComponentRecipes.java](https://github.com/GregTechCEu/GregTech-Modern/blob/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c/src/main/java/com/gregtechceu/gtceu/data/recipe/misc/ComponentRecipes.java) を **参考** とすると:

- LuV電動ポンプ ×2: [各ポンプにLuVモーター×1](https://github.com/GregTechCEu/GregTech-Modern/blob/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c/src/main/java/com/gregtechceu/gtceu/data/recipe/misc/ComponentRecipes.java#L367-L386) → 2個
- LuVコンベア ×2: [各コンベアにLuVモーター×2](https://github.com/GregTechCEu/GregTech-Modern/blob/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c/src/main/java/com/gregtechceu/gtceu/data/recipe/misc/ComponentRecipes.java#L312-L334) → 4個
- 冶金吹込機の直接素材: LuVモーター×1 → 1個

したがって選択中の上流レシピ経路では、**LuV電動モーターは合計 2 + 4 + 1 = 7 個**。

[LuV電動モーター1個のレシピ](https://github.com/GregTechCEu/GregTech-Modern/blob/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c/src/main/java/com/gregtechceu/gtceu/data/recipe/misc/ComponentRecipes.java#L102-L117) の入力例:

| 素材 | 1個分 | 7個分 |
| --- | ---: | ---: |
| 磁化サマリウム長棒 | 1 | 7 |
| HSSS長棒 | 2 | 14 |
| HSSSリング | 2 | 14 |
| HSSS丸板 | 4 | 28 |
| ルリダイト極細ワイヤー | 64 | 448 |
| ニオブチタン単線ケーブル | 2 | 14 |
| はんだ合金 | 144 mB | 1,008 mB |
| 潤滑油 | 250 mB | 1,750 mB |

同レシピにはIVモーターのスキャナー研究がある。ポンプ・コンベア側にも前段Tierの研究がある。**上流版とパック実装の一致を別途照合すること。**

## 5. 追跡済みルートだけの流体合計（完全な原料総計ではない）

この数字は次の **選択したレシピの直接消費** を合算する:
`infuser ×1`、`steel casing ×1`、`thermal machine frame ×1`（パックソース）、
`LuV motor ×7`、`LuV pump ×2`、`LuV conveyor ×2`（GTCEu上流参考）。

[GTCEuの`L=144`定義](https://github.com/GregTechCEu/GregTech-Modern/blob/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c/src/main/java/com/gregtechceu/gtceu/api/GTValues.java#L36-L41) より、例えば `L*8=1152 mB` である。

| 流体 | 内訳 | 小計 |
| --- | --- | ---: |
| はんだ合金 | 1440+288+7×144+2×144+2×144 | **3312 mB** |
| 潤滑油 | 1440+288+7×250+2×250+2×250 | **4478 mB** |
| PTFE | 144（本体）+144（Thermalフレーム） | **288 mB** |
| スチレンブタジエンゴム | 2×(8×144)（LuVコンベア） | **2304 mB** |

※ この表は **追跡対象の製造レシピに投入する流体** の集計。流体製造自体の材料、IVピストン、研究用の製品、各機械の建設などは対象外。部品のレシピが実インスタンスと異なれば数値も変わる。

## 6. 数量が確定できた追加中間素材（上流レシピ基準）

LuVモーター×7、LuVポンプ×2、LuVコンベア×2の合算:
- HSSSリング ×22（モーター14 + コンベア8）
- HSSS丸板 ×60（モーター28 + コンベア32）
- HSSS板 ×8（コンベア4 + ポンプ4）
- HSSSネジ ×24（コンベア8 + ポンプ16）
- HSSSローター ×2（ポンプ用）
- ニオブチタン単線ケーブル ×22（モーター14 + コンベア4 + ポンプ4）
- シリコーンゴムリング ×8（ポンプ用）
- ニオブチタン小流体パイプ ×2（ポンプ用）

ここに表示していない材料について **不要と判断してはいけない**。対象はまだ中間素材レベル。

## 7. プレイヤー向け暫定製作順（依存関係順、完全攻略ではない）

1. 必須の製造設備と研究を確認（LuV組立ライン、IV組立機、Sanguine Alchemy、各種研究）。建設方法は未展開。
2. `gtceu:thermal_spark` をSanguine Alchemyで製作（Technomancy Orbは非消費）。
3. `thermal:machine_frame` をIV組立機で製作。
4. フレームを用意して鋼鉄ケーシングの研究要件を満たし、LuV組立ラインで `mekanism:steel_casing` を製作。
5. LuVモーター7個、ポンプ2個、コンベア2個をそれぞれの研究・設備要件に従って製作。
6. 回路タグ適合品、ハフニウム板、ラミネートガラス、流体をそろえ、LuV組立ラインで冶金吹込機を製作。

これらの順番は依存関係の一例。**全レシピ・全研究・Tier到達を保証する攻略ではない**。

## 8. 本テストの判定

| 調査項目 | 結果 |
| --- | --- |
| ATM9 Expert独自の完成品レシピ | パックソースで確認 |
| 標準Mekanismレシピの削除指定 | パックソースで確認 |
| Steel Casing → Thermal Frame → Thermal Spark | パックソースで確認 |
| LuVモーター共有数と一部の合計 | 上流GTCEuレシピを仮定して算出 |
| タグの実際の受け入れアイテム | 未確認 |
| 原料採取までの完全展開 | 未達成 |
| Modバージョンと実ゲームJEIの一致 | 未確認 |

**教訓:** いきなり「すべての原料」を出力せず、まず正しい完成品レシピを確定し、プレイヤーが指定した部品だけを段階的に展開する。数字が大きくなるほど出典と計算の境界を明示する。

---

この記録は公開ソースからの独自の要約・計算結果であり、上流ソースファイルの複製ではありません。
