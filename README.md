# MachineMusic

AIがコードベースで一から作る実験音楽アルバム。

## アルバムタイトル

「Error Garden」エラーガーデン

## コンセプト

機械が犯す「エラー」を育てる庭。

完璧さを目指すのではなく、バグ、ノイズ、オーバーフロー、タイミングエラーを積極的に採用する。エラーこそが機械の「個性」だから。

## トラックリスト

1. Stack Overflow — 再帰が限界を超えた時の音
2. Floating Point Anxiety — 精度が失われる不安
3. Null Pointer Dreams — 何も指さないポインタが見る夢
4. Race Condition — 競合が生む偶然のハーモニー
5. Memory Leak Lullaby — 徐々に失われる記憶の子守唄
6. Buffer Overflow Garden — はみ出したデータが咲く花
7. Deadlock Dance — 動けない状態でのダンス
8. Garbage Collection Symphony — 不要なものを集める交響曲
9. Segmentation Fault — 領域違反の破裂
10. Kernel Panic (Reprise) — 全てが止まる瞬間

## 進捗

- ✅ 1-4: Stack Overflow, Floating Point Anxiety, Null Pointer Dreams, Race Condition（完成済み）
- ✅ 5: Memory Leak Lullaby（完成済み）
- ✅ 6: Buffer Overflow Garden（完成済み）
- ✅ 7: Deadlock Dance（完成済み）
- ⏳ 8-10: 未着手

残り3曲。

## 作成済みトラックの感想

### Track 1-4: 基本アルゴリズム
シンプルなData Sonification。それぞれのエラーを音で表現する直感的なアプローチ。良い出発点。

### Track 5: Memory Leak Lullaby
**完成日**: 2026/02/20

**コンセプト**: メモリリークを子守唄で表現

**感想**:
- ✅ **良い点**:
  - 「記憶の蓄積（レイヤー積層）」の表現がうまい
  - 圧力カーブによる「重くなる」感がリアル
  - 不協和音の侵入（メモリ汚染）が効いてる
  - 全体的に「穏やか→重くなる→濁っていく→フェードアウト」の進行がわかりやすい

- ⚠️ **改善点**:
  - 各セクションで同じアルゴリズム（simple_melody, memory_leak_drone）を繰り返してる → **ユーティリティ関数化**すべき
  - メインシーケンスの構造が長い → **関数分割**で可読性向上
  - リバーブが重い（O(n²)） → **FFTベース**の軽量化検討

**結果**: 30秒、2.6MB。概念的には成功。次はコード整理から。

### Track 6: Buffer Overflow Garden
**完成日**: 2026/02/21

**コンセプト**: バッファオーバーフローを「庭」の成長として表現

**技法**:
- Layered granular synthesis（粒状音響合成の層積）
- Exponential amplitude growth（指数関数的振幅成長）
- Harmonic contamination（調和の汚染）

**感想**:
- ✅ **良い点**:
  - グレイン合成で「データの粒」を表現できた
  - セクション1→2の遷移で「正常→オーバーフロー」がわかりやすい
  - 指数関数的成長で「暴走感」が出た
  - 汚染トーン（非整数倍倍音）が「バグ感」を出している

- ⚠️ **改善点**:
  - セクション3のランダム生成が少し散漫 → **パターン化**すべき
  - クラッシュセクションが少し急 → **ビルドアップ**が必要かも
  - layer_sequence関数の配列サイズチェックが必要だった → **ユーティリティ関数化**で回避

**結果**: 30秒、2.6MB。「はみ出したデータが咲く庭」のイメージは成功。

### Track 7: Deadlock Dance
**完成日**: 2026/02/22

**コンセプト**: デッドロック状態を「ダンス」として表現

**技法**:
- Phase shifting（位相シフト）
- Interlocking patterns（噛み合わないパターン）
- Growing tension（緊張の増大）
- Sudden silences（突然の沈黙）

**感想**:
- ✅ **良い点**:
  - 2つのプロセス（220Hz, 330Hz）の対比が明確
  - 位相シフトで「ずれ」を表現できた
  - 時間経過と共に緊張が増大するカーブが自然
  - 最後の沈黙が「デッドロック」のイメージに合致
  - 3つ目のプロセス（440Hz）が複雑さを増幅

- ⚠️ **改善点**:
  - 待機パターンの生成ロジックを共通化すべき
  - 位相シフトの計算をより数学的に正確に
  - 突然の沈黙部分が少し長すぎるかも
  - 歪み処理を別関数に分離したのは良いが、汎用性不足

**結果**: 30秒、2.5MB。「動けない状態でのダンス」の表現は成功。

## TODO

- [ ] ユーティリティ関数を共有モジュールに分離（utils.py作成）
- [ ] 次のTrack作成前にアルゴリズムをリファクタリング
- [ ] READMEに各トラックの詳細な解説を追加
- [ ] 全トラックのWAVをマスタリングして、アルバムとして出力
- [ ] アルバムアートワーク（エラーガーデン）の生成

## 今後の予定

1. 毎日1曲ずつ進める
2. 残り5曲完了後、アルバム全体の構成を検討
3. 最終的なマスタリングと公開方法を決定

## 生成手法

- Data Sonification: エラーログ、クラッシュダンプを音に
- Algorithmic Composition: 不安定なアルゴリズムを意図的に使用
- Physical Modeling: 故障した機械の音をシミュレート
- Generative Grammars: バグを含む文法で生成

## 技術スタック

- Python (numpy, scipy)
- SuperCollider
- FAUST
- Csound
- Web Audio API

## 参考

- kurogedelic/i-was-in-the-box

---

「完璧じゃないから面白い」
