#!/usr/bin/env python3
"""
Deadlock Dance Enhanced — 動けない状態でのダンス（簡易物理モデリング版）

コンセプト:
デッドロック状態を「ダンス」として表現。
複数のプロセスが互いに待ち合い、誰も前に進めない状態。
この膠着状態が生み出すリズミカルなパターンを「ダンス」と呼ぶ。

Enhanced版の特徴:
- 物理モデリングによる現実的な音響表現
- 空間的な広がりを持つサウンドスケープ
- プロセス間の相互作用を音響化

アプローチ:
- 2つ以上のプロセス（音声スレッド）が互いに待ち合う
- 同期しようとするが決して同期しない
- 時間が経つにつれて「待機状態」が増大する
"""

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter

# 定数
SAMPLE_RATE = 44100
DURATION = 35  # 秒

class PhysicalResonator:
    """物理的な共鳴体モデル"""
    def __init__(self, fundamental_freq, damping=0.999, nonlinear=0.0001):
        self.freq = fundamental_freq
        self.damping = damping
        self.nonlinear = nonlinear
        self.phase = 0
        self.amplitude = 1.0
        
    def generate(self, n_samples, tension=1.0):
        """共鳴音を生成"""
        t = np.arange(n_samples) / SAMPLE_RATE
        
        # 基本周波数
        omega = 2 * np.pi * self.freq * (1 + tension * 0.1)
        
        # 位相の進行
        self.phase += omega / SAMPLE_RATE
        
        # 非線形効果
        self.amplitude *= self.damping
        signal = self.amplitude * np.sin(self.phase + self.nonlinear * self.phase**3)
        
        return signal

class DeadlockPhysicalModel:
    """デッドロックの物理モデル"""
    def __init__(self):
        # プロセスAの共鳴体
        self.resonator_a = PhysicalResonator(220.0, damping=0.998, nonlinear=0.0002)
        # プロセスBの共鳴体
        self.resonator_b = PhysicalResonator(330.0, damping=0.997, nonlinear=0.0003)
        
    def create_process_signal(self, base_freq, duration, tension=1.0, phase_shift=0):
        """プロセスの信号を生成"""
        resonator = PhysicalResonator(base_freq, damping=0.998, nonlinear=0.0002)
        
        t = np.arange(duration) / SAMPLE_RATE
        signal = np.zeros(duration)
        
        # テンションに基づいた周波数変調
        freq_mod = 1 + tension * 0.2 * np.sin(2 * np.pi * 0.5 * t)
        
        for i in range(duration):
            # 周波数変調
            current_freq = base_freq * freq_mod[i]
            
            # 信号生成
            omega = 2 * np.pi * current_freq / SAMPLE_RATE
            resonator.phase += omega
            signal[i] = resonator.amplitude * np.sin(resonator.phase + resonator.nonlinear * resonator.phase**3)
            
            # ダンピング
            resonator.amplitude *= resonator.damping
            
        # 位相シフト
        if phase_shift > 0:
            shift_samples = int(phase_shift * SAMPLE_RATE)
            signal = np.roll(signal, shift_samples)
        
        return signal
    
    def create_interaction_signal(self, signal1, signal2):
        """2つの信号の相互作用"""
        # 非線形相互作用
        interaction = signal1 * signal2 * 0.1
        
        # 結合
        result = signal1 + signal2 + interaction
        
        # リミッター
        result = np.clip(result, -1, 1)
        
        return result

def apply_spatial_effects(signal, position):
    """空間効果の適用"""
    # 簡易的なステレオ化
    delay_samples = int(SAMPLE_RATE * 0.02)  # 20ms delay
    
    left_delay = int(delay_samples * position)
    right_delay = int(delay_samples * (1 - position))
    
    # 左チャンネル
    left_signal = np.roll(signal, left_delay)
    left_signal[:left_delay] = 0
    
    # 右チャンネル
    right_signal = np.roll(signal, -right_delay)
    right_signal[-right_delay:] = 0
    
    # モノラルにミックス
    spatial_signal = (left_signal + right_signal) * 0.5
    
    return spatial_signal

def generate_deadlock_dance_enhanced():
    """Enhanced版 Deadlock Danceの生成"""
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)
    
    # 物理モデルの初期化
    model = DeadlockPhysicalModel()
    
    # セクション1: 2つのプロセスの対立 (0-10秒)
    print("Section 1: Two processes confrontation...")
    
    section1_duration = int(SAMPLE_RATE * 10)
    
    # プロセスA（220Hz）
    signal_a = model.create_process_signal(220, section1_duration, tension=0.3)
    
    # プロセスB（330Hz） - 位相をずらす
    signal_b = model.create_process_signal(330, section1_duration, tension=0.4, phase_shift=0.1)
    
    # 相互作用
    clash1 = model.create_interaction_signal(signal_a, signal_b)
    
    # 空間効果
    spatial1 = apply_spatial_effects(clash1, 0.3)
    
    audio[:section1_duration] = spatial1 * 0.8
    
    # セクション2: テンションの増大 (10-20秒)
    print("Section 2: Tension buildup...")
    
    section2_duration = int(SAMPLE_RATE * 10)
    
    # テンションを増大
    signal_a_tense = model.create_process_signal(220, section2_duration, tension=0.6)
    signal_b_tense = model.create_process_signal(330, section2_duration, tension=0.8, phase_shift=0.2)
    
    # 相互作用
    clash2 = model.create_interaction_signal(signal_a_tense, signal_b_tense)
    
    # テンションカーブを適用
    tension_curve = np.linspace(1.0, 1.5, section2_duration)
    clash2 = clash2 * tension_curve
    
    # 空間効果
    spatial2 = apply_spatial_effects(clash2, 0.5)
    
    start2 = section1_duration
    audio[start2:start2 + section2_duration] = spatial2 * 0.9
    
    # セクション3: 第3のプロセスが加わり完全なデッドロック (20-30秒)
    print("Section 3: Third process joins, complete deadlock...")
    
    section3_duration = int(SAMPLE_RATE * 10)
    
    # 第3のプロセス（440Hz）
    signal_c = model.create_process_signal(440, section3_duration, tension=1.0, phase_shift=0.3)
    
    # 3つのプロセスの相互作用
    clash_ab = model.create_interaction_signal(signal_a_tense[:section3_duration], signal_b_tense[:section3_duration])
    clash_abc = model.create_interaction_signal(clash_ab, signal_c)
    
    # さらに大きなテンション
    tension_curve2 = np.linspace(1.5, 2.0, section3_duration)
    clash_abc = clash_abc * tension_curve2
    
    # 空間効果
    spatial3 = apply_spatial_effects(clash_abc, 0.7)
    
    start3 = start2 + section2_duration
    audio[start3:start3 + section3_duration] = spatial3 * 1.0
    
    # セクション4: 緊張の頂点と解放 (30-35秒)
    print("Section 4: Tension peak and release...")
    
    section4_duration = int(SAMPLE_RATE * 5)
    
    # 最後の衝突
    final_freq = 110.0  # 低い周波数で緊張感を表現
    final_signal = model.create_process_signal(final_freq, section4_duration, tension=1.5)
    
    # 急激な減衰
    decay = np.exp(-np.linspace(0, 3, section4_duration))
    final_signal = final_signal * decay
    
    start4 = start3 + section3_duration
    audio[start4:start4 + section4_duration] = final_signal
    
    # 全体を正規化
    audio = audio / np.max(np.abs(audio)) * 0.7
    
    # マスタリングエフェクト
    audio = apply_mastering_effects(audio)
    
    return audio

def apply_mastering_effects(audio):
    """マスタリングエフェクトの適用"""
    # 低域フィルター（不要な低域をカット）
    from scipy.signal import butter, lfilter
    b, a = butter(2, 0.05, btype='high')
    audio = lfilter(b, a, audio)
    
    # 高域フィルター（不要な高域をカット）
    b, a = butter(2, 0.95, btype='low')
    audio = lfilter(b, a, audio)
    
    # コンプレッション（簡易）
    threshold = 0.5
    ratio = 4.0
    compressed = np.where(np.abs(audio) > threshold, 
                        np.sign(audio) * (threshold + (np.abs(audio) - threshold) / ratio),
                        audio)
    
    # ミックス
    audio = audio * 0.8 + compressed * 0.2
    
    # リミッター
    max_amp = np.max(np.abs(audio))
    if max_amp > 0.95:
        audio = audio * 0.95 / max_amp
    
    return audio

if __name__ == "__main__":
    print("Generating Enhanced Deadlock Dance...")
    print("🎼 Physical modeling synthesis activated...")
    print("🌐 Spatial audio processing...")
    
    audio = generate_deadlock_dance_enhanced()
    
    # 出力
    output_path = "../samples/07_deadlock_dance_enhanced.wav"
    sf.write(output_path, audio, SAMPLE_RATE)
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    duration = len(audio) / SAMPLE_RATE
    
    print(f"✅ Generated: {output_path}")
    print(f"📊 Size: {file_size / 1024 / 1024:.1f} MB")
    print(f"⏱️ Duration: {duration:.1f} seconds")
    print(f"🎹 Sample Rate: {SAMPLE_RATE} Hz")
    print(f"🔒 Deadlock: Physical processes are locked in resonance...")
    print(f"🎼 Features: Physical Modeling, Spatial Audio, Mastering")