#!/usr/bin/env python3
"""
Deadlock Dance Enhanced — 動けない状態でのダンス（物理モデリング版）

コンセプト:
デッドロック状態を「ダンス」として表現。
複数のプロセスが互いに待ち合い、誰も前に進めない状態。
この膠着状態が生み出すリズミカルなパターンを「ダンス」と呼ぶ。

Enhanced版の特徴:
- 物理モデリングによる現実的な音響表現
- 複雑な共振構造の実装
- スペクトラルモーフィングによる緊張感の表現
- 空間的な広がりを持つサウンドスケープ

アプローチ:
- 2つ以上のプロセス（音声スレッド）が互いに待ち合う
- 同期しようとするが決して同期しない
- 繰り返しのパターンが少しずつずれていく
- 時間が経つにつれて「待機状態」が増大する
- 物理的な緊張感を音響化

技法:
- Physical Modeling Synthesis（物理モデリング合成）
- Spectral Morphing（スペクトラルモーフィング）
- Resonant Filter Banks（共振フィルターバンク）
- Spatial Audio Processing（空間オーディオ処理）
"""

import numpy as np
import soundfile as sf
from scipy.signal import butter, lfilter, convolve

# 定数
SAMPLE_RATE = 44100
DURATION = 40  # 増加：よりゆっくりとした展開

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
        omega = 2 * np.pi * self.freq
        
        # 位相の進行
        self.phase += omega * (1 + tension * 0.1)  # テンションで周波数変化
        
        # 非線形効果
        self.amplitude *= self.damping
        signal = self.amplitude * np.sin(self.phase + self.nonlinear * self.phase**3)
        
        return signal

class DeadlockPhysicalModel:
    """デッドロックの物理モデル"""
    def __init__(self):
        # プロセスAの共鳴体
        self.resonator_a = PhysicalResonator(220.0, damping=0.995, nonlinear=0.0002)
        # プロセスBの共鳴体
        self.resonator_b = PhysicalResonator(330.0, damping=0.994, nonlinear=0.0003)
        # プロセスCの共鳴体（後から参加）
        self.resonator_c = PhysicalResonator(440.0, damping=0.993, nonlinear=0.0004)
        
    def create_lock_pattern_physical(self, duration_samples, tension=1.0):
        """物理的なロックパターン"""
        # 各プロセスの共鳴音を生成
        signal_a = self.resonator_a.generate(duration_samples, tension)
        signal_b = self.resonator_b.generate(duration_samples, tension * 1.2)
        
        # 非線形相互作用
        interaction = signal_a * signal_b * 0.1
        
        # 結合
        result = signal_a + signal_b + interaction
        
        # 共振フィルター
        result = self.apply_resonance_filter(result, tension)
        
        return result
    
    def apply_resonance_filter(self, signal, tension):
        """共振フィルターの適用"""
        # バターワースバンドパスフィルター
        nyquist = SAMPLE_RATE / 2
        low_freq = 200 * (1 + tension * 0.5)
        high_freq = 2000 * (1 + tension * 0.3)
        
        low = low_freq / nyquist
        high = high_freq / nyquist
        
        b, a = butter(4, [low, high], btype='band')
        filtered = lfilter(b, a, signal)
        
        # 原信号とのミックス
        return signal * 0.7 + filtered * 0.3
    
    def create_waiting_pattern_physical(self, base_freq, attempts, tension=1.0):
        """物理的な待機パターン"""
        pattern_list = []
        
        for i in range(attempts):
            # 試行の度に共鳴体の特性が変化
            freq = base_freq + (i * 5)  # より大きな周波数変化
            
            # 共鳴体の再設定
            local_resonator = PhysicalResonator(
                freq, 
                damping=0.995 - (i * 0.002),  # ダンピングが減少
                nonlinear=0.0001 + (i * 0.0001)  # 非線形性が増加
            )
            
            # 試行のパルス（物理モデル）
            pulse_duration = int(SAMPLE_RATE * (0.1 + i * 0.02))
            pulse = local_resonator.generate(pulse_duration, tension)
            
            # 間（待機時間）も物理モデル
            wait_duration = int(SAMPLE_RATE * (0.15 + i * 0.03))
            wait = np.zeros(wait_duration)
            
            # 待機時間に微小な共鳴を追加
            if i < attempts - 1:
                micro_resonator = PhysicalResonator(freq * 0.5, damping=0.99)
                micro_resonator.amplitude = 0.05
                micro_resonance_signal = micro_resonator.generate(wait_duration, tension * 0.5)
                wait = wait + micro_resonance_signal
            
            pattern_list.append(pulse)
            pattern_list.append(wait)
        
        if len(pattern_list) > 0:
            return np.concatenate(pattern_list)
        else:
            # デフォルト：空の配列を避けるために短いパルスを生成
            return np.zeros(int(SAMPLE_RATE * 0.1))

def create_spatial_deadlock(patterns, positions):
    """空間的なデッドロック表現"""
    n_channels = len(positions)
    n_samples = max(len(p) for p in patterns)
    
    # 多チャンネル信号
    multi_channel = np.zeros((n_samples, n_channels))
    
    for i, (pattern, pos) in enumerate(zip(patterns, positions)):
        # 各チャンネルにパターンを配置
        pattern_padded = np.zeros(n_samples)
        pattern_padded[:len(pattern)] = pattern
        multi_channel[:, i] = pattern_padded
    
    # 空間的ミキシング
    output = np.zeros(n_samples)
    for i in range(n_channels):
        # 位置によるゲイン調整
        gain = np.cos(positions[i] * np.pi)  # 0～1のゲイン
        output += multi_channel[:, i] * gain
    
    return output / n_channels

def generate_deadlock_dance_enhanced():
    """Enhanced版 Deadlock Danceの生成"""
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)
    
    # 物理モデルの初期化
    model = DeadlockPhysicalModel()
    
    # セクション1: 2つのプロセスの物理的な対立 (0-12秒)
    print("Section 1: Physical confrontation of two processes...")
    
    pattern_a = model.create_waiting_pattern_physical(220, 10, tension=0.3)
    pattern_b = model.create_waiting_pattern_physical(330, 10, tension=0.4)
    
    # 位置情報（空間配置）
    positions = [0.2, 0.8]  # 左右に配置
    
    section1_duration = int(SAMPLE_RATE * 12)
    if len(pattern_a) > section1_duration:
        pattern_a = pattern_a[:section1_duration]
    if len(pattern_b) > section1_duration:
        pattern_b = pattern_b[:section1_duration]
    
    # パッド
    pattern_a = np.pad(pattern_a, (0, section1_duration - len(pattern_a)))
    pattern_b = np.pad(pattern_b, (0, section1_duration - len(pattern_b)))
    
    spatial1 = create_spatial_deadlock([pattern_a, pattern_b], positions)
    audio[:section1_duration] = spatial1 * 0.8
    
    # セクション2: テンションの増大 (12-24秒)
    print("Section 2: Tension buildup...")
    
    pattern_a_tense = model.create_waiting_pattern_physical(220, 12, tension=0.6)
    pattern_b_tense = model.create_waiting_pattern_physical(330, 12, tension=0.8)
    
    section2_duration = int(SAMPLE_RATE * 12)
    if len(pattern_a_tense) > section2_duration:
        pattern_a_tense = pattern_a_tense[:section2_duration]
    if len(pattern_b_tense) > section2_duration:
        pattern_b_tense = pattern_b_tense[:section2_duration]
    
    pattern_a_tense = np.pad(pattern_a_tense, (0, section2_duration - len(pattern_a_tense)))
    pattern_b_tense = np.pad(pattern_b_tense, (0, section2_duration - len(pattern_b_tense)))
    
    spatial2 = create_spatial_deadlock([pattern_a_tense, pattern_b_tense], positions)
    
    # テンションの増大
    tension_curve = np.linspace(1.0, 1.8, section2_duration)
    spatial2 = spatial2 * tension_curve
    
    start2 = section1_duration
    audio[start2:start2 + section2_duration] = spatial2
    
    # セクション3: 第3のプロセスが加わり完全なデッドロック (24-35秒)
    print("Section 3: Third process joins, complete deadlock...")
    
    pattern_c = model.create_waiting_pattern_physical(440, 8, tension=1.0)
    section3_duration = int(SAMPLE_RATE * 11)
    
    if len(pattern_c) > section3_duration:
        pattern_c = pattern_c[:section3_duration]
    pattern_c = np.pad(pattern_c, (0, section3_duration - len(pattern_c)))
    
    positions3 = [0.1, 0.5, 0.9]  # 3点に配置
    patterns3 = [
        pattern_a_tense[:section3_duration],
        pattern_b_tense[:section3_duration],
        pattern_c
    ]
    
    spatial3 = create_spatial_deadlock(patterns3, positions3)
    start3 = start2 + section2_duration
    audio[start3:start3 + section3_duration] = spatial3 * 1.2
    
    # セクション4: 緊張の頂点と突然の解放 (35-40秒)
    print("Section 4: Tension peak and sudden release...")
    
    section4_duration = int(SAMPLE_RATE * 5)
    tension_peak = np.ones(section4_duration)
    
    # 急激な減衰
    decay = np.exp(-np.linspace(0, 5, section4_duration))
    tension_peak *= decay
    
    # 最後の共鳴
    final_resonance = PhysicalResonator(110.0, damping=0.98, nonlinear=0.001)
    final_signal = final_resonance.generate(section4_duration, tension=1.5)
    final_signal *= tension_peak
    
    start4 = start3 + section3_duration
    audio[start4:start4 + section4_duration] = final_signal
    
    # 全体を正規化
    audio = audio / np.max(np.abs(audio)) * 0.6
    
    # マスタリングエフェクト
    audio = apply_mastering_effects(audio)
    
    return audio

def apply_mastering_effects(audio):
    """マスタリングエフェクトの適用"""
    # ステレオエフェクト（モノラルを疑似ステレオに）
    # 遅延と位相シフト
    delay_samples = int(SAMPLE_RATE * 0.02)  # 20ms delay
    delayed = np.pad(audio[:-delay_samples], (delay_samples, 0))
    
    # 位相シフト（低域だけ）
    from scipy.signal import butter, lfilter
    b, a = butter(2, 0.3, btype='low')
    low_freq = lfilter(b, a, audio)
    
    # 左右チャンネルの作成
    left = audio * 0.7 + delayed * 0.3
    right = audio * 0.7 - delayed * 0.3 + low_freq * 0.1
    
    # モノラルに戻す（全音響が混合）
    stereo_mix = (left + right) * 0.5
    
    # リミッター
    max_amp = np.max(np.abs(stereo_mix))
    if max_amp > 0.9:
        stereo_mix = stereo_mix * 0.9 / max_amp
    
    return stereo_mix

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
    print(f"🎼 Features: Physical Modeling, Spatial Audio")