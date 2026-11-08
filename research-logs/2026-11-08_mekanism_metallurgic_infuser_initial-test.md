# 調査ログ（再構成）: Mekanism 冶金吹込機

> **注意**: これは2026-11-08の既存の対話ベースの調査結果から復元した要約であり、独立したAI実行の完全な操作ログではない。検索履歴や所要時間を捏造しない。

## 0. メタデータ

- 日付: 2026-11-08 JST
- 担当: 初回AI調査（対話ベース・要約）
- 対象: `mekanism:metallurgic_infuser` ×1
- 状態: 完了（部分的）
- パック参照コミット: `309d0fa357b00d855f3a50739ae64737f7537936`
- GregTech本体参考コミット: `e24b2387318d1b70a0d5d651dba56a1baa5f2a6c`（パック収録バージョンとの照合なし）
- 実ゲームJEI: 未確認

## 1. 追跡できた検索経路

| 順番 | 検索対象 | 発見・判断 |
| ---: | --- | --- |
| 1 | ATM9 Expertで`metallurgic_infuser`を検索 | レシピ削除指定と、別の製造定義を発見 |
| 2 | `recipeRemovals.js` | 標準MekanismレシピID `mekanism:metallurgic_infuser` は削除対象 |
| 3 | `Gregification/Machine_Recipes/AssemblyLine.js` | 組立ライン（LuV）の完成品レシピが存在する |
| 4 | 同ファイルの`mekanism:steel_casing`出力 | 前段部品に`thermal:machine_frame`が必要と判明 |
| 5 | `Gregification/Machine_Recipes/assembler.js` | `thermal:machine_frame`には`gtceu:thermal_spark`とIV部品が必要 |
| 6 | `Gregification/CustomMultiblocks/Sanguine_Synthesizer.js` | `gtceu:thermal_spark`はSanguine Alchemyで作る |
| 7 | GregTech Modern `ComponentRecipes.java` | LuVポンプ・コンベア・モーターを展開。**上流ソース参考に留まる** |

### 参照ソース（コミット固定）

- パックの削除指定: [recipeRemovals.js](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/recipeRemovals.js#L515-L523)
- 冶金吹込機: [AssemblyLine.js L746–764](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js#L746-L764)
- 鋼鉄ケーシング: [AssemblyLine.js L153–173](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/AssemblyLine.js#L153-L173)
- Thermal機械フレーム: [assembler.js L722–735](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/Machine_Recipes/assembler.js#L722-L735)
- Thermal Spark: [Sanguine_Synthesizer.js L34–43](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/server_scripts/Gregification/CustomMultiblocks/Sanguine_Synthesizer.js#L34-L43)
- 上流GregTech部品: [ComponentRecipes.java](https://github.com/GregTechCEu/GregTech-Modern/blob/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c/src/main/java/com/gregtechceu/gtceu/data/recipe/misc/ComponentRecipes.java)

## 2. 得られた判断

- 完成品は**作業台ではなくLuV組立ライン**で製作。
- `mekanism:steel_casing` → `thermal:machine_frame` → `gtceu:thermal_spark` と依存関係が延びる。
- GT部品の選択経路では、ポンプ2個でLuVモーター2個、コンベア2個でLuVモーター4個、完成品へ直接1個、合計 **LuVモーター7個**。
- 公開ソース由来の数量計算は、他Modの収録バージョンやタグが一致する前提の**暫定値**。

## 3. 未解決・今後の調査

- ATM9 Expertに含まれるGregTechの**厳密なModバージョン**と使用した参考コードの一致。
- レシピ削除・上書きが実ゲームに反映されるかどうか。
- `#gtceu:circuits/luv` 等のタグに含まれる実際の素材。
- LuV組立ラインやSanguine Alchemyなど必要機械の建設・研究。
- 原料・流体の製造、代替経路、全レシピの循環依存の有無。

## 4. 成果物

- [人間向け調査結果](../examples/mekanism_metallurgic_infuser.md)
- [構造化レシピと部分計算](../examples/mekanism_metallurgic_infuser.json)

他AIは本ログを**再開地点**として使い、出典の再確認と未解決点の検証から始めること。
