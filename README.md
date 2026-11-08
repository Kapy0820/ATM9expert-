# ATM9 Expert Recipe Research / AI Crafting Guide

ATM9 Expert の公開ソースから、AIエージェントがアイテムの製作手順を **根拠付きで** 調査・説明するための作業リポジトリです。

> **現在は調査手順と再現テストのプロトタイプです。** 全レシピ収録済みのデータベースでも、実ゲームのJEIを取得したデータでもありません。

## 目標

プレイヤーが「○○を作りたい」と入力すると、Modpack独自の削除・上書きを優先して調査し、必要な素材、製作機械、流体、技術段階、研究条件、依存部品、素材数、出典を示します。

ATM9 Expertは依存関係が非常に深いため、**最初は直接素材だけを表示し、要求された中間素材だけを追加展開する** 方針です。すでに所持している素材・機械は展開の停止点にできます。

## AIエージェントへ（ここから読む）

1. **[AGENTS.md](AGENTS.md)** — 調査時の必須ルール、検索順序、禁止事項、回答書式
2. **[docs/RESEARCH_PROTOCOL.md](docs/RESEARCH_PROTOCOL.md)** — 公開ソースを使う再現可能な調査手順、数量計算、検証方法
3. **[examples/mekanism_metallurgic_infuser.md](examples/mekanism_metallurgic_infuser.md)** — 実際に調査したMekanism「冶金吹込機」の例
4. **[examples/mekanism_metallurgic_infuser.json](examples/mekanism_metallurgic_infuser.json)** — 上記テストの機械可読な記録

### 次のAIに与える依頼例

```text
このリポジトリの AGENTS.md と docs/RESEARCH_PROTOCOL.md を先に読んでください。
ATM9 Expert の [アイテム名または item ID] を1個作る手順を公開ソースから調査してください。
まず直接レシピを提示し、中間素材は深さ2まで展開してください。
Modpack側の recipeRemovals / KubeJS / datapack を先に確認し、
次にMod本体のレシピを調べてください。
各レシピは出典URL、参照コミット、根拠の確度、
未確認点、必要な機械・流体・研究条件も記載してください。
ゲーム内で検証していないものを「確定」と呼ばないでください。
```

## 調査した実例：冶金吹込機

- `mekanism:metallurgic_infuser` のMekanism標準レシピは ATM9 Expert で削除対象。
- パック独自レシピはGregTech **組立ライン（LuV）**。鋼鉄ケーシング、LuVポンプ2、LuVモーター1、LuVコンベア2、LuV回路2、ハフニウム板4、ラミネートガラス2、および流体を要求。
- 鋼鉄ケーシングはさらにThermal機械フレームを要求し、機械フレームはThermal Sparkを要求。そこでBotaniaやBlood Magicを含む別経路へ依存が伸びる。
- 詳細な出典・検証範囲・計算結果は [テスト記録](examples/mekanism_metallurgic_infuser.md) を参照。

## 参照ソース（再現性のため固定）

| 対象 | 参照コミット | 用途 |
| --- | --- | --- |
| [ATM9 Expert 公開リポジトリ](https://github.com/AllTheMods/atm9-expert) | [`309d0fa357b00d855f3a50739ae64737f7537936`](https://github.com/AllTheMods/atm9-expert/commit/309d0fa357b00d855f3a50739ae64737f7537936) | KubeJSによるパック固有レシピ・削除・追加 |
| [GregTech Modern](https://github.com/GregTechCEu/GregTech-Modern) | [`e24b2387318d1b70a0d5d651dba56a1baa5f2a6c`](https://github.com/GregTechCEu/GregTech-Modern/commit/e24b2387318d1b70a0d5d651dba56a1baa5f2a6c)（1.20.1ブランチから取得） | GregTech標準部品レシピの**参考** |

**重要:** GregTech側コミットがATM9 Expertに実際に収録されているModバージョンと一致するかは未照合です。したがって、GregTech由来の展開結果は「上流ソース参考・ゲーム未検証」と区別してください。パックのコミットもゲームインスタンスのバージョン一致を保証しません。

## ライセンス・注意

このリポジトリは非公式の研究メモです。ATM9 Expert / 各Modとは無関係です。公開ソースを参照・リンクし、各ソースの著作権・ライセンスに従ってください。**他リポジトリの大量のレシピファイルやプログラム本体を無断複製しない** 方針です。説明・出典・独自構造化データを中心に扱います。
