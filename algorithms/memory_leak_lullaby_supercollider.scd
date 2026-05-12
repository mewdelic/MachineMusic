/*
Track 5: Memory Leak Lullaby - SuperCollider version
コンセプト：徐々に失われる記憶の子守唄

メモリリークを音で表現：
- 最初はシンプルで美しい旋律（子守唄）
- 時間が経つにつれて、前の音符が残り始める（リーク）
- 徐々に多くの層が重なり、音楽が重く、濁っていく
- 最終的に「メモリ不足」で終了するようなフェードアウト
- リバーブ、レイヤー増加、ノイズ、不協和音、リズム遅延
*/

s.waitForBoot {

    // === シンセ定義 ===

    // シンプルな子守唄風トーン
    SynthDef(\lullabyTone, {
        arg freq = 440, amp = 0.3, attack = 0.1, release = 0.3, pan = 0;
        var sig, env;

        env = EnvGen.kr(Env([0, 1, 0], [attack, release]), doneAction: 2);

        // シンプルなサイン波
        sig = SinOsc.ar(freq);

        // ソフトなディストーション（暖かみのあるサウンド）
        sig = sig.tanh;

        // パン
        sig = Pan2.ar(sig, pan);

        Out.ar(0, sig * amp * env);
    }).add;

    // ドローンシンセ（メモリリークする）
    SynthDef(\leakyDrone, {
        arg freq = 110, amp = 0.2, leakRate = 0.05, leakDecay = 3;
        var sig, leak, env;

        // 基本ドローン
        sig = SinOsc.ar(freq);

        // リーク層（徐々に蓄積）
        leak = Mix.fill(10, { |i|
            var leakFreq = freq * (1 + (i % 5) * 0.1);
            var leakAmp = 0.1 * (1 + i * 0.05);
            var leakEnv = EnvGen.kr(Env([0, leakAmp, 0], [0.1, leakDecay + i * 0.5]));
            SinOsc.ar(leakFreq) * leakEnv;
        });

        sig = sig + leak;

        // パン
        sig = Pan2.ar(sig, 0);

        Out.ar(0, sig * amp);
    }).add;

    // 不協和音侵入シンセ
    SynthDef(\dissonantIntrusion, {
        arg baseFreq = 110, amp = 0.1, attack = 2, release = 3, pan = 0;
        var sig, env;

        env = EnvGen.kr(Env([0, 1, 0], [attack, release]), doneAction: 2);

        // 不協和音の周波数比
        var ratios = [1.04, 1.06, 1.08, 1.1, 1.15];

        sig = Mix.fill(ratios.size, { |i|
            SinOsc.ar(baseFreq * ratios[i]) * (1.0 / ratios.size);
        });

        // ノイズ要素
        sig = sig + (PinkNoise.ar() * 0.2);

        // パン
        sig = Pan2.ar(sig, pan);

        Out.ar(0, sig * amp * env);
    }).add;

    // ノイズパートシンセ
    SynthDef(\memoryPressureNoise, {
        arg amp = 0.05, pressure = 0.5;
        var sig;

        // 圧力に応じてノイズを調整
        sig = PinkNoise.ar() * (pressure ** 1.5);

        // ローパスフィルター（圧力が高いとより広帯域）
        sig = LPF.ar(sig, 2000 + pressure * 4000);

        // パン
        sig = Pan2.ar(sig, 0);

        Out.ar(0, sig * amp);
    }).add;

    // リバーブ
    SynthDef(\memoryLeakReverb, {
        arg inBus = 0, outBus = 0, amp = 0.3, reverbTime = 2, mix = 0.3;
        var input, sig;

        input = In.ar(inBus, 2);

        // リバーブ
        sig = FreeVerb2.ar(input[0], input[1],
            mix: mix,
            room: reverbTime,
            damp: 0.5
        );

        Out.ar(outBus, sig * amp);
    }).add;

    // === メインシーケンス ===

    s.sync;

    // 全体のリバーブバス
    ~reverbBus = Bus.audio(s, 2);
    ~reverbSynth = Synth(\memoryLeakReverb, [
        \inBus, ~reverbBus.index,
        \outBus, 0,
        \amp, 0.4,
        \reverbTime, 2,
        \mix, 0.2
    ], addAction: \addToTail);

    // 子守唄のスケール（ペンタトニック風）
    ~lullabyScale = [0, 2, 4, 7, 9, 12, 14, 16];

    // メロディを演奏する関数
    ~playMelody = {
        arg baseFreq = 220, duration = 10, numNotes = 8, noteDuration = 0.8,
            leakAccumulation = 0, leakDepth = 0;

        var task, accumulatedBuffer, bufferIndex;

        // リークバッファ
        accumulatedBuffer = Array.new;

        task = Task({
            var i, freq, freqRatio, leakTask;

            for (0, numNotes - 1, { |i|
                // 周波数選択（ペンタトニック風）
                freqRatio = 2 ** (~lullabyScale[i % ~lullabyScale.size] / 12);
                freq = baseFreq * freqRatio;

                // 新しい音符
                Synth(\lullabyTone, [
                    \freq, freq,
                    \amp, 0.3,
                    \attack, 0.1,
                    \release, 0.4,
                    \pan, rrand(-0.3, 0.3)
                ]);

                // リークされた音符を再生（バッファから）
                if (accumulatedBuffer.size > 0 && leakDepth > 0) {
                    leakTask = Task({
                        var j, leakFreq;
                        accumulatedBuffer.do({ |storedFreq, j|
                            if ((j / accumulatedBuffer.size).coin) { // ランダムに選択
                                leakFreq = storedFreq;
                                Synth(\lullabyTone, [
                                    \freq, leakFreq,
                                    \amp, 0.2 * (1.0 / (j + 1)) * leakDepth,
                                    \attack, 0.05,
                                    \release, 0.3,
                                    \pan, rrand(-0.5, 0.5)
                                ]);
                            };
                        });
                    });
                    leakTask.play;
                };

                // バッファに周波数を追加
                accumulatedBuffer.add(freq);

                // 次の音符までの待機
                (noteDuration * (1 + leakAccumulation * i)).wait;
            });
        });

        task.play;
    };

    // === 楽曲構成 ===

    Routine({

        // セクション1: シンプルな子守唄（0-8秒）
        "Section 1: Simple Lullaby".postln;

        // ベースドローン
        ~drone1 = Synth(\leakyDrone, [
            \freq, 55,
            \amp, 0.25,
            \leakRate, 0.02,
            \leakDecay, 4
        ]);

        // メロディ
        ~playMelody.value(
            baseFreq: 220,
            duration: 8,
            numNotes: 8,
            noteDuration: 0.8,
            leakAccumulation: 0,
            leakDepth: 0
        );

        8.wait;

        // セクション2: リークの開始（8-16秒）
        "Section 2: Leak Begins".postln;

        // ドローンのリーク率を上げる
        ~drone1.set(\leakRate, 0.05, \leakDecay, 3);

        // メロディ（少しリーク）
        ~playMelody.value(
            baseFreq: 220,
            duration: 8,
            numNotes: 8,
            noteDuration: 0.8,
            leakAccumulation: 0.05,
            leakDepth: 0.3
        );

        8.wait;

        // セクション3: リークが進行（16-24秒）
        "Section 3: Leak Progressing".postln;

        // ドローンのリーク率をさらに上げる
        ~drone1.set(\leakRate, 0.08, \leakDecay, 2.5);

        // メロディ（さらにリーク）
        ~playMelody.value(
            baseFreq: 220,
            duration: 8,
            numNotes: 8,
            noteDuration: 0.85, // 少し遅くなる
            leakAccumulation: 0.08,
            leakDepth: 0.5
        );

        // 不協和音の侵入
        ~dissonant1 = Synth(\dissonantIntrusion, [
            \baseFreq, 110,
            \amp, 0.12,
            \attack, 3,
            \release, 4,
            \pan, rrand(-0.3, 0.3)
        ]);

        // ノイズ開始
        ~noise1 = Synth(\memoryPressureNoise, [
            \amp, 0.03,
            \pressure, 0.3
        ]);

        // リバーブを深く
        ~reverbSynth.set(\reverbTime, 2.5, \mix, 0.3);

        8.wait;

        // セクション4: メモリ不足のフェードアウト（24-30秒）
        "Section 4: Out of Memory Fade Out".postln;

        // ドローンのリーク率を最大に
        ~drone1.set(\leakRate, 0.12, \leakDecay, 2, \amp, 0.15);

        // メロディ（重く、遅く）
        ~playMelody.value(
            baseFreq: 220,
            duration: 6,
            numNotes: 6,
            noteDuration: 0.9, // さらに遅くなる
            leakAccumulation: 0.12,
            leakDepth: 0.7
        );

        // 不協和音の増加
        ~dissonant2 = Synth(\dissonantIntrusion, [
            \baseFreq, 110 * 1.1,
            \amp, 0.15,
            \attack, 2,
            \release, 5,
            \pan, rrand(-0.4, 0.4)
        ]);

        // 高音の不協和音
        ~dissonantHigh = Synth(\dissonantIntrusion, [
            \baseFreq, 880,
            \amp, 0.08,
            \attack, 1,
            \release, 6,
            \pan, rrand(-0.5, 0.5)
        ]);

        // ノイズの増加
        ~noise1.set(\amp, 0.06, \pressure, 0.6);

        // リバーブを最深に
        ~reverbSynth.set(\reverbTime, 3, \mix, 0.4);

        6.wait;

        // フェードアウト（メモリ不足）
        "Final Fade Out...".postln;

        // 全体をフェードアウト
        ~fadeOutTask = Task({
            var fadeTime = 4;
            var steps = 20;
            var stepDuration = fadeTime / steps;

            for (0, steps, { |i|
                var currentAmp = 1 - (i / steps);
                ~drone1.set(\amp, 0.15 * currentAmp);
                ~noise1.set(\amp, 0.06 * currentAmp);
                stepDuration.wait;
            });

            // 全てのシンセを解放
            ~drone1.free;
            ~noise1.free;
            ~reverbSynth.set(\amp, 0);
        });

        ~fadeOutTask.play;

        4.wait;

        "Memory Leak Lullaby Complete!".postln;
        "\nTrack Summary:".postln;
        "- Simple lullaby melody at start".postln;
        "- Previous notes accumulate (memory leak)".postln;
        "- Layers build up, creating heaviness".postln;
        "- Rhythm gradually slows down".postln;
        "- Dissonance and noise increase".postln;
        "- Fades out into 'out of memory' silence".postln;

    }).play;

}
