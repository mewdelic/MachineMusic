/*
 Stack Overflow - SuperCollider Physical Model
 再帰が限界を超えた時の音
 SuperColliderによるスタックオーバーフローの表現
*/

// サーバー起動確認
s.waitForBoot {

    // スタックの層を模倣したシンセ定義
    SynthDef(\stackLayer, {
        arg freq=220, layerNum=0, totalLayers=20, amp=0.1, gate=1, 
            stackPressure=0.0, instability=0.0, releaseTime=0.1;
        
        var env = EnvGen.kr(Env.asr(0.01, 1, releaseTime), gate, doneAction: 2);
        
        // 層の高さに応じた周波数（高さが高いほど振動が遅くなる）
        var heightFactor = 1.0 - ((layerNum / totalLayers) * 0.8);
        var layerFreq = freq * heightFactor * (1 + (instability * LFNoise1.kr(0.5).range(-0.1, 0.1)));
        
        // 圧力による周波数シフト（スタックが圧迫される）
        var pressureShift = layerFreq * (1 - (stackPressure * 0.5));
        
        // 各層の振動モード
        var mode1 = SinOsc.ar(pressureShift, 0, amp * 0.4);
        var mode2 = SinOsc.ar(pressureShift * 1.5, 0, amp * 0.3);
        var mode3 = SinOsc.ar(pressureShift * 2.0, 0, amp * 0.2);
        
        // 層間の干渉（隣接する層からの影響）
        var interference = LFNoise2.kr(10).range(-1, 1) * amp * 0.1 * stackPressure;
        
        // 減衰（高さに応じて減衰が増大）
        var damping = 1.0 - ((layerNum / totalLayers) * 0.3);
        
        // 全信号を混合
        var mixedSignal = (mode1 + mode2 + mode3 + interference) * damping * env;
        
        // ステレオパン（層の位置で少しズレる）
        var panOffset = (layerNum / totalLayers - 0.5) * 0.3;
        var finalSignal = Pan2.ar(mixedSignal, panOffset);
        
        // 出力
        Out.ar(0, finalSignal);
        
    }).add;
    
    // 圧縮効果（ソフトクリッピング）
    SynthDef(\compressionEffect, {
        arg inBus=0, threshold=0.8, makeupGain=1.5;
        var input = In.ar(inBus, 2);
        var compressed = tanh(input / threshold) * threshold * makeupGain;
        ReplaceOut.ar(inBus, compressed);
    }).add;
    
    // 歪み効果
    SynthDef(\distortionEffect, {
        arg inBus=0, amount=0.3;
        var input = In.ar(inBus, 2);
        var distorted = input + (amount * sign(input) * pow(abs(input), 0.5));
        ReplaceOut.ar(inBus, distorted);
    }).add;
    
    // フィードバックノイズ（スタックオーバーフロー時）
    SynthDef(\feedbackOverflow, {
        arg freq=110, pan=0, amp=0.2, gate=1, chaosLevel=0.5;
        var env = EnvGen.kr(Env.perc(0.001, 0.5), gate, doneAction: 2);
        
        // カオス的フィードバック（ロジスティックマップのシミュレーション）
        var chaos = LFNoise0.kr(freq * 0.01).range(-1, 1) * chaosLevel;
        var sig = PinkNoise.ar(amp) * (1 + chaos) * env;
        
        // フィルタリング
        sig = LPF.ar(sig, freq * 4);
        sig = HPF.ar(sig, freq * 0.5);
        
        Out.ar(0, Pan2.ar(sig, pan));
    }).add;
    
    // スタック崩壊音（オーバーフローの瞬間）
    SynthDef(\stackCollapse, {
        arg freq=55, pan=0, amp=0.4, gate=1;
        var env = EnvGen.kr(Env.perc(0.001, 2.0), gate, doneAction: 2);
        
        // 複数のノイズ源を重ねる
        var noise1 = WhiteNoise.ar(amp);
        var noise2 = PinkNoise.ar(amp * 0.7);
        var noise3 = BrownNoise.ar(amp * 0.5);
        
        var sig = (noise1 + noise2 + noise3) * env;
        
        // 周波数モジュレーション（不安定さを表現）
        sig = sig * (1 + LFNoise2.kr(10).range(-0.3, 0.3));
        
        // フィルタリング
        sig = LPF.ar(sig, freq * 8);
        sig = HPF.ar(sig, freq);
        
        Out.ar(0, Pan2.ar(sig, pan));
    }).add;
    
    // 低周波のスタック振動
    SynthDef(\stackVibration, {
        arg freq=80, amp=0.15, gate=1;
        var env = EnvGen.kr(Env.adsr(0.1, 0.5, 0.7, 1.0), gate, doneAction: 2);
        
        // 複数の振動モード
        var mode1 = SinOsc.ar(freq, 0, amp * 0.5);
        var mode2 = SinOsc.ar(freq * 1.2, 0, amp * 0.3);
        var mode3 = SinOsc.ar(freq * 1.5, 0, amp * 0.2);
        
        var sig = (mode1 + mode2 + mode3) * env;
        
        Out.ar(0, Pan2.ar(sig, 0));
    }).add;
    
    // メインのスタックオーバーフロー生成ルーチン
    ~stackOverflowRoutine = Routine({
        var duration = 90; // 90秒の演奏
        var baseFreq = 110; // A2
        var stackSize = 20; // 20層のスタック
        var stackLayers = [];
        var effectBus = Bus.audio(s, 2);
        
        // 圧縮・歪みエフェクトの設定
        var compression = Synth(\compressionEffect, [\inBus, effectBus.index], addAction: \addToTail);
        var distortion = Synth(\distortionEffect, [\inBus, effectBus.index, \amount, 0.2], addAction: \addToTail);
        
        // 低周波の振動
        var vibration = Synth(\stackVibration, [
            \freq, baseFreq * 0.75,
            \amp, 0.15
        ]);
        
        // スタックの層を徐々に生成
        stackSize.do({ |i|
            var layer = Synth(\stackLayer, [
                \freq, baseFreq * (1 + (i * 0.1)),
                \layerNum, i,
                \totalLayers, stackSize,
                \amp, 0.15,
                \out, effectBus.index
            ]);
            stackLayers = stackLayers.add(layer);
            0.5.wait; // 各層を0.5秒間隔で追加
        });
        
        // スタック圧力の時間変化
        duration.do({ |i|
            var progress = i / duration;
            var stackPressure = progress * 0.8;  // 圧力が増大
            var instability = progress * 0.5;  // 不安定性が増大
            
            // 各層のパラメータを更新
            stackLayers.do({ |layer, j|
                layer.set(
                    \stackPressure, stackPressure * (1 + (j / stackSize) * 0.5),
                    \instability, instability * (1 + (j / stackSize) * 0.3)
                );
            });
            
            // 圧力が高まるとフィードバックノイズを発生
            if(stackPressure > 0.4, {
                if(0.1.rand < (stackPressure - 0.3), {
                    Synth(\feedbackOverflow, [
                        \freq, baseFreq * [0.5, 1, 1.5].choose,
                        \pan, 1.0.rand2,
                        \amp, (stackPressure - 0.3) * 0.3,
                        \chaosLevel, stackPressure
                    ]);
                });
            });
            
            // 圧力が極限に近いとき、崩壊音の予兆
            if(stackPressure > 0.7, {
                if(0.05.rand < (stackPressure - 0.65), {
                    Synth(\stackCollapse, [
                        \freq, baseFreq * 0.25,
                        \pan, 1.0.rand2,
                        \amp, (stackPressure - 0.65) * 0.4
                    ]);
                });
            });
            
            // 振動の不安定性を増加
            vibration.set(\freq, baseFreq * 0.75 * (1 + instability * 0.5));
            
            0.1.wait; // 100ms間隔で更新
        });
        
        // スタックオーバーフローの瞬間（崩壊）
        var collapseSound = Synth(\stackCollapse, [
            \freq, baseFreq * 0.125,
            \pan, 0,
            \amp, 0.6
        ]);
        
        // 追加のフィードバックノイズ
        5.do({ |i|
            Synth(\feedbackOverflow, [
                \freq, baseFreq * [0.25, 0.5, 1, 2, 4].choose,
                \pan, 1.0.rand2,
                \amp, 0.4,
                \chaosLevel, 0.8
            ]);
            0.2.wait;
        });
        
        // 全ての層を解放
        stackLayers.do({ |layer|
            layer.release(2);
        });
        vibration.release(2);
        compression.free;
        distortion.free;
        effectBus.free;
        
        // 崩壊音を再生した後に終了
        3.wait;
        "Stack Overflow performance completed".postln;
    });
    
    // 演奏開始
    ~stackOverflowRoutine.play;
    
    // 録音設定（オプション）
    s.record;
    s.waitForRecording({
        "Recording saved".postln;
        s.stopRecording;
    });
}

/*
 解説:
 このアルゴリズムはStack Overflow（スタックオーバーフロー）を音楽的に表現しています。
 
 技術的特徴:
 - スタックの層: 20層のスタックが徐々に生成
 - 圧力変化: 時間と共にスタックが圧迫される
 - 非線形効果: 圧縮と歪みによる音質変化
 - カオスフィードバック: ロジスティックマップのシミュレーション
 - 崩壊イベント: スタックオーバーフローの瞬間的な爆発音
 
 物理モデル:
 - 層の振動: 各層が異なる周波数で振動
 - 圧力: 層間の相互作用が増大
 - 減衰: 高さに応じて減衰が増加
 - 干渉: 隣接する層からの影響
 
 データソニフィケーション:
 - スタックの高さ → 周波数と減衰
 - 圧力 → 音量とエフェクトの深さ
 - 不安定性 → 周波数の揺らぎとノイズ
 - 進捗度 → 全体的なテンションの増大
 
 このコードをSuperColliderで実行すると、スタックが成長し、圧迫され、最終的に崩壊するプロセスを音楽的に表現した音が生成されます。
*/
