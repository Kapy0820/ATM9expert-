# 調査ログ：ATM9 Expert公開クエストラインの利用可否

## 0. 調査メタデータ

- 調査日: 2026-11-08（日本時間）
- 実行者: GPT-6（この対話での調査）
- 対象: ATM9 ExpertのFTB Quests公開データ。検証例は`mekanism:metallurgic_infuser`。
- 状態: 完了（公開データの構造確認と具体例）。ゲーム内照合は未実施。
- ATM9 Expertソース: `AllTheMods/atm9-expert@309d0fa357b00d855f3a50739ae64737f7537936`
- 検討事項: レシピ手順にクエストの進行上の案内を付加できるか。

## 1. 検索・確認の履歴

1. 公開ウェブ検索を試したがツール結果を取得できず、GitHub公開ソースを直接調べる方法に切り替えた。
2. GitHubリポジトリツリーを取得し、`config/ftbquests/quests/chapters/` に **36個の`.snbt`章ファイル**があると確認。`chapter_groups.snbt`、`data.snbt`、`reward_tables/`も見つかった（36章ファイルの中にはプレースホルダーに近い小さいファイルもある）。
3. `data.snbt` に `progression_mode: "flexible"` が設定されていると確認。クエスト前提リンクはレシピ上の絶対的な製造ゲートとはみなせない。
4. `chapter_groups.snbt` で章のグループIDを確認。GregTech進行章の`an_introduction`～`ultra_high_voltage`や`gregstar`を確認。
5. `ludicrous_voltage.snbt`から`gtceu:assembly_line`のタスクがあるクエストと、その前提クエストIDを取得。
6. 36個の章ファイル本文について、`mekanism:metallurgic_infuser`、`mekanism:steel_casing`、`thermal:machine_frame`、`gtceu:thermal_spark`の文字列の有無を調査。いずれも章ファイル内の一致を確認できなかった。ただしクエストのテキストは翻訳キーや間接参照もあり、**これだけで実ゲーム内の全ての文脈に登場しないと断定しない**。
7. `botania.snbt`に`botania:corporea_spark`をタスクとするクエストを確認。
8. `kubejs/assets/kubejs/lang/en_us.json`、`ja_jp.json`を取得し、章名・クエスト名・説明の翻訳キーが日本語に解決できることを確認。

## 2. 出典と確認できた構造

- [FTBクエストの構成ファイル（ディレクトリ）](https://github.com/AllTheMods/atm9-expert/tree/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests)
- [章グループID](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests/chapter_groups.snbt)
- [進行設定：flexible](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests/data.snbt)
- [LuV章](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests/chapters/ludicrous_voltage.snbt)
- [Botania章](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests/chapters/botania.snbt)
- [日本語翻訳](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/assets/kubejs/lang/ja_jp.json)
- [英語翻訳](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/kubejs/assets/kubejs/lang/en_us.json)

各章ファイルに`quests: [ ... ]`があり、クエスト`id`、`dependencies`、`tasks`、`rewards`、`title`、`description`、`optional`等が含まれる。翻訳キーは`{atm9.quest...}`形式で、表示名へ変換するには言語JSONを引く。

### LuVの組立ライン（クエストID `204EDA5F8B1C7580`）

[原文のタスク・前提の定義](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests/chapters/ludicrous_voltage.snbt#L731-L795)

- 前提クエストID: `0E4C711E77497984`（ルリダイト歯車）、`60175A8E3A67F51C`（IVエミッターとセンサー）、`3DA1449117521889`（データスティック4個）。
- クエストのタスクは`gtceu:assembly_line`×1、`gtceu:assembly_line_unit`×5、`gtceu:assembly_line_casing`×5、`gtceu:assembly_line_grating`×8、`gtceu:solid_machine_casing`×14、`gtceu:laminated_glass`×10、`gtceu:data_access_hatch`×1。
- 英語での説明では、組立ラインは上位Tier部品に必要とされる。日本語訳の当該説明も取得できる。
- **注意**: クエストの達成条件は必ずしも実際のマルチブロック建造BOMと同じではない。

### BotaniaのCorporea Spark

[Botania章のクエスト](https://github.com/AllTheMods/atm9-expert/blob/309d0fa357b00d855f3a50739ae64737f7537936/config/ftbquests/quests/chapters/botania.snbt#L3078-L3118)に`botania:corporea_spark`と`botania:corporea_spark_master`のアイテムタスクがある。クエストタイトルの翻訳キー`atm9.quest.botania.theCorporeaNetwork`は日本語で「コーポリア・ネットワーク」。

### 冶金吹込機に直接クエストがない場合の扱い

`mekanism:metallurgic_infuser`の直接の対応クエストは、今回調べた章ファイルに見つからなかった。レシピ側で要求される`gtceu:assembly_line`のクエストや、素材の`botania:corporea_spark`のクエストを**関連クエスト**として提示する。この区別を維持し、直接クエストがあると誤認しない。

## 3. AIへの実装案

レシピとクエストを**別のグラフ**としてデータ化し、同一のアイテムID（クエストの`tasks`の`item`、またはレシピの入力・機械ID）を介して結び付ける。

- `recipe_graph`: 製作可能性に必要な材料、機械、研究、加工条件。
- `quest_graph`: クエストID、章、翻訳タイトル、タスク、前提クエストID、任意/必須、報酬。
- `joins`: 直接対象クエスト、素材タスククエスト、装置タスククエストを区別。
- プレイヤーのクエストクリア状況が不明な場合は「関連する推奨クエスト」として提示し、「あなたは未クリア」とは言わない。
- クエストの報酬は取得済みであるとも、確定的な製造ルートであるとも仮定しない。
- 全公開クエストの機械可読抽出・全依存ID解決・ゲーム内進行反映の確認は **未実施**。

## 4. 今回の調査の結論

公開のFTB Questsデータから、進行順・クエスト達成条件・日本語説明文を参照することは可能。プレイヤー向け製作手順に「推奨される関連クエスト」を加えられる。ただしクエスト関係は製作上の強制前提と区別すること。

今後の成果物候補: `docs/QUEST_GUIDANCE.md`、クエストSNBTの読み取り専用インデクサー、`item_id -> quest_id[]`の逆引きデータ。
