/*
 Floating Point Anxiety - SuperCollider Physical Model
 浮動小数点の精度が失われる不安
 SuperColliderによる数値不安定性の表現
*/

// サーバー起動確認
s.waitForBoot {

    // 浮動小数点誤差を模倣したシンセ定義
    SynthDef(\floatingPoint, {
        arg freq=440, pan=0, amp=0.1, gate=1, 
            precisionLoss=0.0, roundingError=0.01, driftRate=0.1, releaseTime=0.1;
        
        var env = EnvGen.kr(Env.asr(0.01, 1, releaseTime), gate, doneAction: 2);
        
        // 基本信号（徐々に精度が落ちる）
        var baseFreq = freq * (1 + (precisionLoss * LFNoise1.kr(driftRate).range(-0.1, 0.1)));
        
        // 高精度なサイン波（正常状態）
        var preciseSignal = SinOsc.ar(baseFreq, 0, amp * 0.4);
        
        // 量子化された信号（精度低下）
        var quantizedSignal = (SinOsc.ar(baseFreq * 1.001, 0, amp * 0.3) * (1 / roundingError)).floor * roundingError;
        
        // 丸め誤差ノイズ（量子化誤差として表現）
        var roundingNoise = WhiteNoise.ar(amp * 0.15) * (precisionLoss * LFNoise1.kr(2).range(0.5, 1.5));
        
        // 演算誤差（オーバーフロー・アンダーフローを表現）
        var arithmeticError = LPF.ar(
            WhiteNoise.ar(amp * 0.2),
            freq * (2 - precisionLoss)  // 精度が落ちるとカットオフ周波数も不安定に
        ) * precisionLoss;
        
        // 微小な周波数ドリフト（数値不安定性）
        var drift = LFNoise2.kr(driftRate * 10).range(-5, 5);
        var driftedSignal = SinOsc.ar(baseFreq + drift, 0, amp * 0.2);
        
        // すべての信号を混合
        var mixedSignal = (preciseSignal + quantizedSignal + roundingNoise + arithmeticError + driftedSignal) * env;
        
        // ステレオパン（不安定さを表現）
        var panDrift = LFNoise1.kr(0.3).range(-0.8, 0.8) * precisionLoss;
        var finalSignal = Pan2.ar(mixedSignal, panDrift);
        
        // 出力
        Out.ar(0, finalSignal);
        
    }).add;
    
    // 精度喪失警告音
    SynthDef(\precisionWarning, {
        arg freq=880, pan=0, amp=0.15, gate=1;
        var env = EnvGen.kr(Env.perc(0.001, 0.05), gate, doneAction: 2);
        var sig = Saw.ar([freq, freq * 1.01], amp) * env;  // 微小なズレで不安定さを表現
        Out.ar(0, Pan2.ar(sig, pan));
    }).add;
    
    // オーバーフローの爆発音
    SynthDef(\overflowExplosion, {
        arg freq=220, pan=0, amp=0.3, gate=1;
        var env = EnvGen.kr(Env.perc(0.001, 0.3), gate, doneAction: 2);
        var sig = PinkNoise.ar(amp) * env;
        sig = LPF.ar(sig, freq * 4);
        Out.ar(0, Pan2.ar(sig, pan));
    }).add;
    
    // 低周波の不安定な揺らぎ
    SynthDef(\anxietyBass, {
        arg freq=110, amp=0.15, gate=1, instability=0.0;
        var env = EnvGen.kr(Env.adsr(0.2, 0.5, 0.6, 1.0), gate, doneAction: 2);
        var freqDrift = LFNoise2.kr(0.5).range(freq * 0.95, freq * 1.05) * (1 + instability);
        var sig = SinOsc.ar(freqDrift, 0, amp) * env;
        Out.ar(0, Pan2.ar(sig, 0));
    }).add;
    
    // メインの浮動小数点不安定性生成ルーチン
    ~floatingPointRoutine = Routine({
        var duration = 60; // 60秒の演奏
        var baseFreq = 330; // E4
        
        // メインのプロセス開始（最初は高精度）
        var mainProcess = Synth(\floatingPoint, [
            \freq, baseFreq,
            \amp, 0.25,
            \precisionLoss, 0.05,
            \roundingError, 0.001,
            \driftRate, 0.1
        ]);
        
        // 低周波の不安定なベース
        var bass = Synth(\anxietyBass, [
            \freq, baseFreq * 0.5,
            \amp, 0.1,
            \instability, 0.1
        ]);
        
        // 浮動小数点誤差の時間変化
        duration.do({ |i|
            var progress = i / duration;
            var precisionLoss = 0.05 + (progress * 0.85);  // 5% → 90% まで精度が落ちる
            var roundingError = 0.001 + (progress * 0.099);  // 量子化誤差が増大
            var driftRate = 0.1 + (progress * 2.0);  // ドリフトが激しくなる
            
            // 精度警告音（精度が落ちるタイミングで）
            if((i % 10 == 0) && (precisionLoss > 0.3), {
                Synth(\precisionWarning, [
                    \freq, baseFreq * [1.5, 2, 0.75].choose,
                    \pan, 1.0.rand2,
                    \amp, precisionLoss * 0.2
                ]);
            });
            
            // オーバーフロー爆発音（精度が極端に落ちた時）
            if(precisionLoss > 0.7, {
                if(0.1.rand < (precisionLoss - 0.7), {
                    Synth(\overflowExplosion, [
                        \freq, baseFreq * [0.5, 1, 2].choose,
                        \pan, 1.0.rand2,
                        \amp, (precisionLoss - 0.7) * 0.5
                    ]);
                });
            });
            
            // メインプロセスのパラメータを更新（精度が徐々に低下）
            mainProcess.set(
                \freq, baseFreq * (1 + (progress * 0.3)),  // 周波数も不安定に
                \precisionLoss, precisionLoss,
                \roundingError, roundingError,
                \driftRate, driftRate
            );
            
            // ベースの不安定性も増加
            bass.set(\instability, precisionLoss);
            
            0.1.wait; // 100ms間隔で更新
        });
        
        // 演奏終了
        mainProcess.release(3);
        bass.release(3);
        "Floating Point Anxiety performance completed".postln;
    });
    
    // 演奏開始
    ~floatingPointRoutine.play;
    
    // 録音設定（オプション）
    s.record;
    s.waitForRecording({
        "Recording saved".postln;
        s.stopRecording;
    });
}

/*
 解説:
 このアルゴリズムはFloating Point Anxiety（浮動小数点の不安）を音楽的に表現しています。
 
 技術的特徴:
 - 精度の低下: 精度が落ちるにつれて信号が歪む
 - 量子化誤差: .floor * step で量子化をシミュレート
 - 丸め誤差ノイズ: 精度損失に比例してノイズが増大
 - 周波数ドリフト: 数値不安定性によるピッチの揺らぎ
 - オーバーフロー/アンダーフロー: 突然の爆発音として表現
 
 物理モデル:
 - 精度損失: 信号品質の劣化をシミュレート
 - 量子化: デジタル信号の離散化を表現
 - 数値不安定性: 演算誤差の蓄積
 
 データソニフィケーション:
 - 精度損失率 → 信号歪みとノイズの増大
 - 量子化誤差 → ノコギリ波状の歪み
 - ドリフトレート → 周波数の不安定さ
 - 進捗度 → 全体的な不安定性の増大
 
 このコードをSuperColliderで実行すると、徐々に精度が落ちていく浮動小数点の不安を表現した音楽が生成されます。
*/