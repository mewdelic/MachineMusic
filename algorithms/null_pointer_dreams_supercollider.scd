(
// Null Pointer Dreams - SuperCollider Version
// 何も指さないポインタが見る夢
// 空虚、無、ゼロからの浮遊する夢の断片

s.boot;

// 夢の断片 - 不完全な音の集合
(
SynthDef(\dreamFragment, { |out=0, freq=440, amp=0.3, pan=0, duration=4, detune=1.0, density=0.5|
    var env, sound, voices, fragmentEnv, voidSpace;

    // 空の包絡線 - 急に現れて急に消える夢の断片
    fragmentEnv = EnvGen.kr(
        Env([0, 1, 0.3, 0], [0.1, 0.5, duration], curve:\sin),
        timeScale: (1 + (Rand(-0.3, 0.3) * density))
    );

    // 複数の音声 - 未初期化メモリのノイズ
    voices = 4.collect({ |i|
        var detuneFreq = freq * (detune ** i);
        var phase = Rand(0, 2pi);
        var osc = SinOsc.ar(detuneFreq, phase) * Rand(0.5, 1.0);

        // 不完全な結合 - 偶然のハーモニー
        var partials = 3.collect({ |j|
            SinOsc.ar(detuneFreq * (j + 1), Rand(0, 2pi)) * (1 / (j + 2))
        }).sum;

        (osc + partials) * Rand(0.3, 0.7)
    }).sum;

    // 空虚な空間 - 広がりと深度
    voidSpace = GVerb.ar(
        voices * fragmentEnv * amp,
        roomsize: [20, 30].choose, // 大きな部屋
        revtime: [5, 8].choose, // 長い残響
        damping: 0.3,
        inputbw: 0.7,
        spread: 0.8,
        drylevel: 0.2,
        earlyreflevel: 0.4
    );

    // パンによる浮遊感
    Out.ar(out, Pan2.ar(voidSpace, pan + Rand(-0.2, 0.2)));
}).add;
);

// 空のポインタ - 静寂と微かな震え
(
SynthDef(\nullPointer, { |out=0, amp=0.15, baseFreq=60|
    var silence, tremble, voidNoise, envelope;

    // 静寂 - ほとんど音がしない状態
    silence = Silence.ar(2);

    // 微かな震え - 不安定な存在
    tremble = SinOsc.ar(baseFreq + Rand(-5, 5), 0) * Rand(0.01, 0.05);

    // 空のノイズ - メモリの空虚
    voidNoise = WhiteNoise.ar(Rand(0.001, 0.005)) * LFNoise1.kr(Rand(0.1, 0.5)).range(0.5, 1.0);

    // 包絡線 - 予兆と消滅
    envelope = EnvGen.kr(
        Env([0, 1, 0.5, 0], [0.3, 2, 1], curve:\sin),
        timeScale: 4
    );

    Out.ar(out, (silence + tremble + voidNoise) * envelope * amp);
}).add;
);

// ポインタの振動 - 無限の探索
(
SynthDef(\pointerVibration, { |out=0, baseFreq=80, amp=0.2, modRate=0.5|
    var vibration, lfo, drift, envelope;

    // LFOによる振動 - 探索の動き
    lfo = LFNoise2.kr(modRate).range(0.8, 1.2);

    // ドリフト - 定点を見つけられない動き
    drift = LFNoise1.kr(modRate * 2).range(-0.1, 0.1);

    // 振動する音
    vibration = SinOsc.ar(baseFreq * lfo + drift, 0) * lfo;

    // 包絡線 - 断続的な出現
    envelope = EnvGen.kr(
        Env([0, 1, 0], [0.1, Rand(2, 4)], curve:\exp),
        timeScale: Rand(0.5, 1.5)
    );

    Out.ar(out, vibration * envelope * amp);
}).add;
);

// 空の夢 - 背景のアンビエンス
(
SynthDef(\voidDream, { |out=0, amp=0.25, density=0.5|
    var harmonics, ambience, reverb, envelope;

    // 調和倍音 - 完全ではないコード
    harmonics = [1, 1.2, 1.5, 1.8, 2.2].collect({ |ratio|
        SinOsc.ar(110 * ratio, Rand(0, 2pi)) * Rand(0.2, 0.4)
    }).sum;

    // ドローン状のアンビエンス
    ambience = Splay.ar(harmonics, spread: 1.0, center: 0);

    // 広い空間のリバーブ
    reverb = FreeVerb.ar(
        ambience,
        mix: 0.6,
        room: 0.9,
        damp: 0.4
    );

    // 緩やかな包絡線
    envelope = EnvGen.kr(
        Env([0, 1, 1, 0], [5, 20, 5], curve:\sin),
        timeScale: (1 + (Rand(-0.2, 0.2) * density))
    );

    Out.ar(out, reverb * envelope * amp);
}).add;
);

// 未初期化メモリ - ランダムな断片
(
SynthDef(\uninitializedMemory, { |out=0, amp=0.18, activity=0.5|
    var noise, fragments, filter, envelope;

    // ノイズ - ゴミデータ
    noise = WhiteNoise.ar(0.3);

    // 断片的なフィルタリング
    fragments = LPF.ar(
        HPF.ar(noise, Rand(200, 800)),
        Rand(1000, 4000) * LFNoise1.kr(Rand(0.5, 2)).range(0.8, 1.2)
    );

    // アクティビティによる変調
    filter = LPF.ar(fragments, Rand(500, 2000)) * LFNoise2.kr(activity).range(0.2, 0.8);

    // 断続的な包絡線
    envelope = EnvGen.kr(
        Env([0, 1, 0], [0.05, Rand(0.1, 0.5)], curve:\exp),
        timeScale: (1 / activity)
    );

    Out.ar(out, filter * envelope * amp);
}).add;
);

// ==================== 演奏ルーチン ====================

// 全体の演奏時間（秒）
~totalDuration = 180; // 3分

// Null Pointer Dreams - メインルーチン
(
~nullPointerDreams = Routine({
    var currentTime = 0;

    // 序章 - 空虚な空間 (0-30秒)
    "Phase 1: Void Space - 空虚な空間".postln;

    // 空の夢から始める
    ~voidDream = Synth(\voidDream, [
        \amp, 0.25,
        \density, 0.5
    ]);

    // ポインタの振動を追加
    (10).wait;

    ~pointerVib1 = Synth(\pointerVibration, [
        \baseFreq, 80,
        \amp, 0.15,
        \modRate, 0.4
    ]);

    (8).wait;

    ~pointerVib2 = Synth(\pointerVibration, [
        \baseFreq, 60,
        \amp, 0.12,
        \modRate, 0.6
    ]);

    // 第2章 - 夢の断片 (30-90秒)
    "Phase 2: Dream Fragments - 夢の断片".postln;
    (7).wait;

    // 空のポインタ（静寂）
    ~nullPtr1 = Synth(\nullPointer, [\amp, 0.15]);
    (3).wait;

    // 夢の断片が現れ始める
    ~dreamFrag1 = Synth(\dreamFragment, [
        \freq, 330,
        \amp, 0.25,
        \pan, -0.6,
        \duration, 5,
        \detune, 1.02
    ]);
    (2).wait;

    ~dreamFrag2 = Synth(\dreamFragment, [
        \freq, 392,
        \amp, 0.2,
        \pan, 0.4,
        \duration, 6,
        \detune, 1.01
    ]);
    (3).wait;

    // 未初期化メモリの断片
    ~uninitMem1 = Synth(\uninitializedMemory, [\amp, 0.18, \activity, 0.4]);
    (1).wait;

    ~dreamFrag3 = Synth(\dreamFragment, [
        \freq, 262,
        \amp, 0.3,
        \pan, 0.2,
        \duration, 4,
        \detune, 1.03
    ]);
    (2).wait;

    ~nullPtr2 = Synth(\nullPointer, [\amp, 0.12]);
    (4).wait;

    ~dreamFrag4 = Synth(\dreamFragment, [
        \freq, 440,
        \amp, 0.22,
        \pan, -0.3,
        \duration, 5,
        \detune, 1.015
    ]);

    ~uninitMem2 = Synth(\uninitializedMemory, [\amp, 0.15, \activity, 0.6]);
    (3).wait;

    // 第3章 - 夢の深層 (90-150秒)
    "Phase 3: Deep Dreams - 夢の深層".postln;
    (5).wait;

    // より複雑な夢の断片
    ~dreamFrag5 = Synth(\dreamFragment, [
        \freq, 293,
        \amp, 0.28,
        \pan, -0.4,
        \duration, 6,
        \detune, 1.025,
        \density, 0.7
    ]);
    (2).wait;

    ~dreamFrag6 = Synth(\dreamFragment, [
        \freq, 349,
        \amp, 0.24,
        \pan, 0.5,
        \duration, 5,
        \detune, 1.018
    ]);
    (2).wait;

    ~pointerVib3 = Synth(\pointerVibration, [
        \baseFreq, 100,
        \amp, 0.18,
        \modRate, 0.3
    ]);

    ~uninitMem3 = Synth(\uninitializedMemory, [\amp, 0.2, \activity, 0.5]);
    (3).wait;

    ~nullPtr3 = Synth(\nullPointer, [\amp, 0.18]);
    (2).wait;

    ~dreamFrag7 = Synth(\dreamFragment, [
        \freq, 392,
        \amp, 0.26,
        \pan, -0.2,
        \duration, 7,
        \detune, 1.022
    ]);
    (2).wait;

    ~dreamFrag8 = Synth(\dreamFragment, [
        \freq, 330,
        \amp, 0.22,
        \pan, 0.3,
        \duration, 4,
        \detune, 1.012
    ]);

    (5).wait;

    // 終章 - 虚空への回帰 (150-180秒)
    "Phase 4: Return to Void - 虚空への回帰".postln;

    // 夢の断片が消えていく
    ~dreamFrag9 = Synth(\dreamFragment, [
        \freq, 262,
        \amp, 0.15,
        \pan, 0,
        \duration, 8,
        \detune, 1.02
    ]);

    (6).wait;

    ~nullPtr4 = Synth(\nullPointer, [\amp, 0.2]);
    (4).wait;

    // 全てのシンセを静かにフェードアウト
    ~voidDream.set(\amp, 0.15);
    (3).wait;

    ~pointerVib1.set(\amp, 0.08);
    ~pointerVib2.set(\amp, 0.06);
    (2).wait;

    ~voidDream.set(\amp, 0.08);
    (3).wait;

    ~voidDream.free;
    ~pointerVib1.free;
    ~pointerVib2.free;
    ~pointerVib3.free;

    "Null Pointer Dreams - 完了".postln;
}).play;
);

// 演奏開始（コメントアウトを解除して実行）
// ~nullPointerDreams.play;

// 停止用
(
~stopAll = {
    ~nullPointerDreams.stop;
    s.freeAll;
};
);

// ~stopAll.value; // 停止
)

/* ==================== コンセプト ====================

Null Pointer Dreams - 何も指さないポインタが見る夢

【表現の要素】

1. 空虚（Void）
   - 何も指さないポインタの無
   - GVerbによる広大な空間
   - 静寂と微かな震えの対比

2. 夢の断片（Dream Fragments）
   - 完全ではない音の集合
   - 偶然のハーモニー
   - 断続的な出現と消滅

3. 未初期化メモリ（Uninitialized Memory）
   - ランダムなノイズ断片
   - ゴミデータの音響表現
   - 不安定なアクティビティ

4. 探索（Exploration）
   - ポインタの振動
   - 定点を見つけられない動き
   - 無限の探索

【技術的特徴】

- リアルタイム音響合成
- 複数のシンセによる多層的表現
- 非決定的な演奏（毎回異なる結果）
- 広い空間のリバーブによる浮遊感
- 偶然性と予測不可能性

【演奏構成】

1. 序章（0-30秒）: 空虚な空間の提示
2. 第2章（30-90秒）: 夢の断片の現出
3. 第3章（90-150秒）: 夢の深層へ没入
4. 終章（150-180秒）: 虚空への回帰

【音楽的表現】

- 「何も指さない」 = 空虚、無、ゼロ
- 「夢」 = 幻想的、曖昧、断片的
- 空虚から生まれる幻影と、また虚空へ消える循環

"Nothing points to nothing, yet dreams emerge from the void"
*/
