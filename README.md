# MachineMusic

AIがコードベースで一から作る実験音楽アルバム。

## コンセプト

「機械が機械のために作る音楽」

人間が聴くことを前提にしない。アルゴリズムが生成し、アルゴリズムが評価する。

## 方針

- **DAW-less**: コードで全て生成
- **実験的**: 既存のジャンルに当てはめない
- **毎日少しずつ**: 継続的に発展させる
- **参考**: kurogedelic/i-was-in-the-box（あくまで参考）

## 生成手法（検討中）

1. **Data Sonification** — データを音に変換
2. **Algorithmic Composition** — アルゴリズムによる作曲
3. **Physical Modeling** — 物理シミュレーションで音を合成
4. **Generative Grammars** — 文法ベースの生成
5. **Cellular Automata** — セルオートマトンからパターン生成
6. **Neural Audio Synthesis** — ニューラルネットワークで音色生成

## ディレクトリ構成

```
MachineMusic/
├── concepts/       # アルバムコンセプト・曲名
├── algorithms/     # 生成アルゴリズム
├── samples/        # 生成された音声ファイル
├── scores/         # 楽譜・MIDI
├── docs/           # 進捗メモ
└── tools/          # 補助ツール
```

## 進捗

- [ ] コンセプト決定
- [ ] トラックリスト作成
- [ ] 最初の1曲生成

## Leoの興味から参考

- 坂本龍一、平沢進、YMO、クラフトワーク
- ユーロラックシンセ
- レトロなもの、変なもの
- 四国めたん（VOICEVOX）

---

生成はz.ai GLMモデルで実行。
