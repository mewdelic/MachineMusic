/*
 Race Condition - SuperCollider Physical Model
 競合状態が生む偶然のハーモニー
 SuperColliderによるマルチスレッド音響合成
*/

// サーバー起動確認
s.waitForBoot {

    // 競合状態を模倣したシンセ定義
    SynthDef(\raceCondition, {
        arg freq=440, pan=0, amp=0.1, gate=1, 
            conflictRate=10, spatialSpread=0.5, releaseTime=0.1;
        
        // 2つのプロセスが異なるタイミングで実行
        var sig1, sig2, sig3, conflictNoise, conflictDetect;
        var env = EnvGen.kr(Env.asr(0.01, 1, releaseTime), gate, doneAction: 2);
        
        // プロセス1: サイン波による安定した基音
        sig1 = SinOsc.ar(freq * [1, 1.01, 0.99], 0, amp * 0.3);
        
        // プロセス2: パルス波によるリズミックな要素
        sig2 = Pulse.ar(freq * [0.5, 2, 1.5], Rand(0.2, 0.8), amp * 0.2);
        
        // プロセス3: ノコギリ波による複雑な倍音
        sig3 = Saw.ar(freq * [1.5, 0.75, 3], amp * 0.15);
        
        // 競合による衝突検出（ノイズとして表現）
        conflictNoise = WhiteNoise.ar(amp * 0.1) * LFNoise0.kr(conflictRate).range(0, 1);
        
        // 競合検出器（信号の急激な変化を検出）
        conflictDetect = (sig1 * sig2 * sig3) * Dust.kr(conflictRate * 2);
        
        // すべての信号を混合
        var mixedSignal = (sig1 + sig2 + sig3 + conflictNoise + conflictDetect) * env;
        
        // 競合による空間的な揺らぎ
        var panNoise = LFNoise1.kr(0.5).range(-spatialSpread, spatialSpread);
        var finalSignal = Splay.ar(mixedSignal, panNoise);
        
        // 出力
        Out.ar(0, finalSignal);
        
    }).add;
    
    // 衝突音用の追加シンセ
    SynthDef(\raceConflict, {
        arg freq=880, pan=0, amp=0.2, gate=1;
        var env = EnvGen.kr(Env.perc(0.001, 0.1), gate, doneAction: 2);
        var sig = LPF.ar(WhiteNoise.ar(amp), freq) * env;
        Out.ar(0, Pan2.ar(sig, pan));
    }).add;
    
    // 低周波の競合振動
    SynthDef(\raceVibration, {
        arg freq=110, amp=0.1, gate=1;
        var env = EnvGen.kr(Env.adsr(0.1, 0.3, 0.7, 1.0), gate, doneAction: 2);
        var sig = SinOsc.ar(freq, 0, amp) * env;
        Out.ar(0, Pan2.ar(sig, 0));
    }).add;
    
    // メインの競合状態生成ルーチン
    ~raceConditionRoutine = Routine({
        var duration = 60; // 60秒の演奏
        var baseFreq = 220; // A3
        
        // メインのプロセス開始
        var mainProcess = Synth(\raceCondition, [
            \freq, baseFreq,
            \amp, 0.3,
            \conflictRate, 8,
            \spatialSpread, 0.8
        ]);
        
        // 競合状態の時間変化
        duration.do({ |i|
            var progress = i / duration;
            var conflictIntensity = sin(progress * 8pi).abs;
            
            // 競合が激しくなるにつれて衝突音を発生
            if(conflictIntensity > 0.7, {
                Synth(\raceConflict, [
                    \freq, baseFreq * [1.5, 2, 0.5].choose,
                    \pan, 1.0.rand2,
                    \amp, conflictIntensity * 0.3
                ]);
            });
            
            // 低周波の振動を加える
            if(i % 10 == 0, {
                Synth(\raceVibration, [
                    \freq, baseFreq * 0.25,
                    \amp, conflictIntensity * 0.2
                ]);
            });
            
            // メインプロセスのパラメータを更新
            mainProcess.set(
                \freq, baseFreq * (1 + (progress * 0.5)),
                \conflictRate, 8 + (conflictIntensity * 12)
            );
            
            0.1.wait; // 100ms間隔で更新
        });
        
        // 演奏終了
        mainProcess.release(2);
        "Race Condition performance completed".postln;
    });
    
    // 演奏開始
    ~raceConditionRoutine.play;
    
    // 録音設定（オプション）
    s.record;
    s.waitForRecording({
        "Recording saved".postln;
        s.stopRecording;
    });
}

/*
 解説:
 このアルゴリズムはRace Condition（競合状態）を音楽的に表現しています。
 
 技術的特徴:
 - 複数のシンセが同時に実行され、互いに干渉
 - 確率的な衝突がノイズや突然の音として表現
 - 空間的な広がりで競合の緊張感を視覚化
 - 非決定的な結果（毎回異なる演奏）
 
 物理モデル:
 - 競合: シグナルの乗算による衝突検出
 - 振動: 低周波でのシステムの不安定性
 - 衝突: ノイズと突然のパルス音
 
 データソニフィケーション:
 - 競合率 → 衝突音の頻度
 - 進捗度 → 周波数と空間の変化
 - 競合強度 → 音量とエフェクトの深さ
 
 このコードをSuperColliderで実行すると、毎回異なる Race Condition の音楽が生成されます。
*/