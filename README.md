# MachineMusic - Error Garden

**AIがコードベースで一から作る実験音楽アルバム**

## アルバム概要

「Error Garden」（エラーガーデン）は、ソフトウェアのシステムエラーを音楽的に表現した実験的なアルゴリズム音楽アルバムです。

- **アーティスト**: Error Garden (kurogedelic)
- **タイトル**: Error Garden
- **アートワーク**: 各トラックのビジュアライゼーションをアルバムアートとして使用（`visualizations/` ディレクトリ参照）

### コンセプト

完璧さを目指す現代のソフトウェア開発において、エラーは「失敗」として扱われます。しかし、エラーこそが機械の本質的な「個性」なのです。このアルバムは、システムエラーを積極的に採用し、それらを「美」として再定義することを試みます。

**「完璧じゃないから面白い」**

### トラックリスト

1. **Stack Overflow** — 再帰が限界を超えた時の音
2. **Floating Point Anxiety** — 精度が失われる不安
3. **Null Pointer Dreams** — 何も指さないポインタが見る夢
4. **Race Condition** — 競合が生む偶然のハーモニー
5. **Memory Leak Lullaby** — 徐々に失われる記憶の子守唄
6. **Buffer Overflow Garden** — はみ出したデータが咲く花
7. **Deadlock Dance** — 動けない状態でのダンス
8. **Garbage Collection Symphony** — メモリクリーナーの交響曲
9. **Segmentation Fault** — 領域違反の破裂
10. **Kernel Panic (Reprise)** — 全てが止まる瞬間

## 制作情報

- **制作期間**: 2026/02/20 - 2026/04/08（継続的拡張中）
- **基本アルゴスム総演奏時間**: 約30分
- **Enhanced版総演奏時間**: 約45分
- **技術**: Python, numpy, scipy を使用した Data Sonification と Algorithmic Composition
- **追加技術**: 物理モデリング、空間化処理、SuperCollider, Web Audio API
- **ライセンス**: MIT

## マスタリング

マスタリング済みトラックは `samples_mastered/` に配置されています。各トラックにはアーティスト名「Error Garden (kurogedelic)」のメタデータが含まれています。

- 10トラック全曲マスタリング済み
- ファイル: `samples_mastered/mastered_XX_トラック名.wav`

## プロジェクト進捗

### 基本アルバム（バージョン1.0）
- **完成度**: 10/10 トラック (100%)
- **制作期間**: 2026/02/20 - 2026/02/23（4日間）

### Enhanced版（バージョン2.0）
- **完成度**: 10/10 トラック (100%) ✅ **完成!**
- **制作期間**: 2026/03/11 - 2026/04/08
- **特徴**: 物理モデリングによる高音質化、空間化効果、複雑な音響表現

### Advanced版（バージョン3.0）
- **完成度**: 10/10 トラック (100%) ✅ **完成!**
- **制作期間**: 2026/04/04 - 2026/05/08
- **特徴**: より高度な物理モデリング、リアルタイム処理、量子情報理論、熱力学

### SuperCollider版（実験的実装）
- **完成度**: 3/10 トラック (30%)
- **特徴**: リアルタイム音響生成、インタラクティブ要素
- **完了トラック**: Stack Overflow, Race Condition, Floating Point Anxiety

## リポジトリ構成

```
/
├── README.md                  # このファイル
├── .gitignore
├── concepts/                  # アルバムコンセプト
│   └── album-concept.md
├── algorithms/                # 全アルゴリズムのPythonソースコード
├── tracks/                    # 最新版（Advanced）の完成wav
├── samples/                   # 各バージョンの音声サンプル
├── samples_mastered/          # マスタリング済みトラック
├── visualizations/            # ビジュアライゼーション画像・GIF
├── docs/                      # ドキュメント
│   ├── index.md               # 詳細ドキュメント
│   ├── metadata/              # トラックメタデータJSON
│   ├── summaries/             # SUMMARY ファイル
│   └── daily-logs/            # 日次作業ログ
└── web/                       # Web Audio インタラクティブHTML
```

## リポジトリ

- **ソースコード**: [GitHub Repository](https://github.com/kurogedelic/MachineMusic)
- **Issue**: バグ報告・機能リクススト
- **License**: MIT

---

*"エラーはバグではなく、機械の魂の表現である"*
