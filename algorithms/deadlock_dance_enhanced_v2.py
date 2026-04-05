#!/usr/bin/env python3
"""
Deadlock Dance Enhanced — 動けない状態でのダンス（物理モデリング拡張版）

コンセプト:
デッドロック状態を「ダンス」として表現。
複数のプロセスが互いに待ち合い、誰も前に進めない状態。
この膠着状態が生み出すリズミカルなパターンを「ダンス」と呼ぶ。

Enhanced版の特徴:
- 物理モデリングによる現実的な楽器音響のシミュレーション
- フィルタバンクによる周波数帯域別のデッドロック表現
- スパースグランピングによるテクスチャの付加
- マルチバンドコンプレッションによる緊張感のコントロール
- モジュラー合成の要素を取り入れた複雑な音響生成

アプローチ:
- 2つ以上のプロセス（音声スレッド）が互いに待ち合う
- 同期しようとするが決して同期しない
- 繰り返しのパターンが少しずつずれていく
- 時間が経つにつれて「待機状態」が増大する

技法:
- 物理モデリング（ストリングス、パーカッション）
- フィルタバンク（デッドロックの周波数別表現）
- スパースグランピング（テクスチャと複雑さ）
- マルチバンドコンプレッション（緊張感のコントロール）
- モジュラー合成（複雑な音響生成）
- Phase shifting（位相シフト）
- Interlocking patterns（噛み合わないパターン）
- Growing tension（緊張の増大）
- Sudden silences（突然の沈黙）
"""

import numpy as np
import soundfile as sf
from scipy.signal import convolve, butter, filtfilt, sosfilt
from scipy.signal import hilbert
import matplotlib.pyplot as plt

# 定数
SAMPLE_RATE = 44100
DURATION = 45  # 秒（少し延長）

class PhysicalModeling:
    """物理モデリングによる楽器音響の生成"""
    
    @staticmethod
    def karplus_strong(frequency, duration, damping=0.99, stretch_factor=0.5):
        """Karplus-Strongアルゴリズムによるストリングス音響"""
        N = int(SAMPLE_RATE / frequency)
        samples = int(SAMPLE_RATE * duration)
        
        # 初期バッファ（ホワイトノイズ）
        buffer = np.random.uniform(-1, 1, N)
        
        # 出力バッファ
        output = np.zeros(samples)
        
        # Karplus-Strongループ
        for i in range(samples):
            if i < N:
                output[i] = buffer[i]
            else:
                # フィードバック
                feedback = (buffer[i % N] + buffer[(i + 1) % N]) * 0.5 * damping
                buffer[i % N] = feedback
                output[i] = feedback
                
        # ストレッチ（減衰の変更）
        envelope = np.exp(-np.linspace(0, 10, samples) * stretch_factor)
        output *= envelope
        
        return output
    
    @staticmethod
    def drum_model(frequency, duration, pitch_env=True):
        """ドラムの物理モデリング"""
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
        
        # 基本周波数
        if pitch_env:
            # ピッチエンベロープ
            pitch_curve = np.exp(-t * 5)
            freq_mod = frequency * (1 + pitch_curve * 0.5)
            
            # 周波数変調
            phase = 2 * np.pi * np.cumsum(freq_mod) / SAMPLE_RATE
            signal = np.sin(phase)
        else:
            signal = np.sin(2 * np.pi * frequency * t)
        
        # ノイズ成分（ドラムの打撃感）
        noise = np.random.normal(0, 0.1, len(t))
        noise_envelope = np.exp(-t * 100)
        noise *= noise_envelope
        
        # 結合
        drum = signal + noise
        
        # エンベロープ
        envelope = np.exp(-t * 20)
        drum *= envelope
        
        return drum
    
    @staticmethod
    def resonant_filter(audio, frequency, q=10):
        """レゾナントフィルタ"""
        # バターワースフィルタ
        nyquist = SAMPLE_RATE / 2
        normal_cutoff = frequency / nyquist
        
        # バンドパスフィルタ
        b, a = butter(2, [normal_cutoff * 0.8, normal_cutoff * 1.2], btype='band')
        filtered = filtfilt(b, a, audio)
        
        # レゾナンスブースト
        resonance_freq = frequency
        b_res, a_res = butter(2, [resonance_freq * 0.95 / nyquist, resonance_freq * 1.05 / nyquist], btype='band')
        resonance = filtfilt(b_res, a_res, audio) * q * 0.1
        
        return filtered + resonance

class FilterBank:
    """フィルタバンクによる周波数帯域別処理"""
    
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.bands = [
            {'freq': 100, 'q': 2, 'name': 'sub_bass'},
            {'freq': 300, 'q': 3, 'name': 'bass'},
            {'freq': 800, 'q': 4, 'name': 'low_mid'},
            {'freq': 2000, 'q': 5, 'name': 'mid'},
            {'freq': 5000, 'q': 6, 'name': 'high_mid'},
            {'freq': 12000, 'q': 8, 'name': 'high'}
        ]
    
    def apply_filter_bank(self, audio, gains=None):
        """フィルタバンクを適用"""
        if gains is None:
            gains = [1.0] * len(self.bands)
        
        nyquist = self.sample_rate / 2
        outputs = []
        
        for i, band in enumerate(self.bands):
            # バンドパスフィルタ
            freq = band['freq']
            q = band['q']
            
            # 帯域幅計算
            bandwidth = freq / q
            low_freq = max(20, freq - bandwidth/2)
            high_freq = min(nyquist - 20, freq + bandwidth/2)
            
            if low_freq < high_freq:
                b, a = butter(2, [low_freq/nyquist, high_freq/nyquist], btype='band')
                filtered = filtfilt(b, a, audio)
                filtered *= gains[i]
                outputs.append(filtered)
        
        # 全帯域を結合
        if outputs:
            return np.sum(outputs, axis=0)
        else:
            return audio

class SparseGranulation:
    """スパースグランピングによるテクスチャ生成"""
    
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
    
    def granulate(self, audio, grain_size=0.05, density=0.1, randomize=True):
        """オーディオをグレイン化"""
        grain_samples = int(grain_size * self.sample_rate)
        total_samples = len(audio)
        
        output = np.zeros(total_samples)
        
        # グレインの配置
        grain_positions = np.arange(0, total_samples, int(grain_samples / density))
        
        if randomize:
            # ランダム性を追加
            grain_positions += np.random.randint(-grain_samples//4, grain_samples//4, len(grain_positions))
        
        for pos in grain_positions:
            if pos + grain_samples < total_samples:
                # グレインを抽出
                grain = audio[pos:pos + grain_samples]
                
                # グレインのエンベロープ
                envelope = np.hanning(len(grain))
                grain *= envelope
                
                # 出力に追加
                output[pos:pos + grain_samples] += grain
        
        return output * 0.3  # 全体の音量を調整

class MultibandCompressor:
    """マルチバンドコンプレッションによる緊張感コントロール"""
    
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.bands = [
            {'low': 20, 'high': 200, 'ratio': 4, 'threshold': -20},
            {'low': 200, 'high': 2000, 'ratio': 3, 'threshold': -18},
            {'low': 2000, 'high': 8000, 'ratio': 2.5, 'threshold': -16},
            {'low': 8000, 'high': 20000, 'ratio': 2, 'threshold': -14}
        ]
    
    def compress(self, audio):
        """マルチバンドコンプレッションを適用"""
        nyquist = self.sample_rate / 2
        compressed_bands = []
        
        for band in self.bands:
            # バンド分離
            if band['high'] < nyquist:
                # ローパス（上限）
                b_hp, a_hp = butter(4, band['low']/nyquist, btype='high')
                b_lp, a_lp = butter(4, band['high']/nyquist, btype='low')
                
                # バンドパス
                high_passed = filtfilt(b_hp, a_hp, audio)
                band_signal = filtfilt(b_lp, a_lp, high_passed)
                
                # 簡易コンプレッション（ソフトクリッピング）
                threshold = 10 ** (band['threshold'] / 20)
                ratio = band['ratio']
                
                compressed = np.tanh(band_signal / threshold) * threshold * ratio
                
                compressed_bands.append(compressed)
        
        # バンドを結合
        if compressed_bands:
            return np.sum(compressed_bands, axis=0)
        else:
            return audio

def create_lock_pattern_enhanced(freq, duration_ms, phase=0, amp=1.0, physical=True):
    """強化版ロックパターン（物理モデリング付き）"""
    t = np.linspace(0, duration_ms / 1000.0, int(SAMPLE_RATE * duration_ms / 1000.0))
    
    # 位相シフト
    t_shifted = t + phase
    
    if physical:
        # 物理モデリング音響
        if freq < 200:  # 低域はドラム
            tone = PhysicalModeling.drum_model(freq, duration_ms / 1000.0)
        else:  # 中高域はストリングス
            tone = PhysicalModeling.karplus_strong(freq, duration_ms / 1000.0)
        
        # 長さを調整
        if len(tone) < len(t):
            tone = np.pad(tone, (0, len(t) - len(tone)))
        elif len(tone) > len(t):
            tone = tone[:len(t)]
    else:
        # 基本トーン
        tone = np.sin(2 * np.pi * freq * t_shifted)
        
        # 「ロック」感を出すために矩形波成分を追加
        square = np.sign(tone) * 0.3
        
        # 結合
        tone = tone + square
    
    # エンベロープ（急な開始、ゆっくり終了）
    envelope = np.ones_like(t)
    release_start = int(len(t) * 0.7)
    envelope[release_start:] = np.linspace(1, 0, len(t) - release_start)
    
    return tone * envelope * amp

def create_waiting_pattern_enhanced(base_freq, attempts, physical=True):
    """強化版待機パターン（物理モデリング付き）"""
    pattern = []
    
    for i in range(attempts):
        # 試行の度に周波数が少し変化（フラストレーションの表現）
        freq = base_freq + (i * 2)
        
        # 試行のパルス
        pulse_duration = 100 + (i * 20)  # 徐々に長くなる
        pulse = create_lock_pattern_enhanced(freq, pulse_duration, phase=i * 0.1, 
                                           amp=0.8 - (i * 0.05), physical=physical)
        
        # 間（待機時間）
        wait_duration = 150 + (i * 30)  # 徐々に長くなる
        wait = np.zeros(int(SAMPLE_RATE * wait_duration / 1000.0))
        
        pattern.append(pulse)
        pattern.append(wait)
    
    return np.concatenate(pattern)

def create_deadlock_clash_enhanced(pattern1, pattern2, pattern3=None, mix_ratios=None):
    """強化版デッドロック衝突（3つのプロセス対応）"""
    # 長さを合わせる
    min_length = min(len(pattern1), len(pattern2))
    if pattern3 is not None:
        min_length = min(min_length, len(pattern3))
    
    pattern1 = pattern1[:min_length]
    pattern2 = pattern2[:min_length]
    
    if mix_ratios is None:
        mix_ratios = [0.4, 0.4, 0.2]
    
    # 2つのパターンのミキシング
    result = pattern1 * mix_ratios[0] + pattern2 * mix_ratios[1]
    
    # 3つ目のパターンがあれば追加
    if pattern3 is not None:
        pattern3 = pattern3[:min_length]
        result += pattern3 * mix_ratios[2]
    
    # クリッピング（デッドロックの「歪み」）
    result = np.clip(result, -1, 1)
    
    return result

def generate_deadlock_dance_enhanced():
    """Deadlock Dance Enhancedのメイン生成"""
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)
    
    # 処理クラスの初期化
    filter_bank = FilterBank(SAMPLE_RATE)
    granulator = SparseGranulation(SAMPLE_RATE)
    compressor = MultibandCompressor(SAMPLE_RATE)
    
    # セクション1: 2つのプロセスの始動 (0-12秒)
    print("Section 1: Two processes start...")
    
    # プロセスA（基準）
    pattern_a = create_waiting_pattern_enhanced(220, 10, physical=True)
    pattern_a = np.tile(pattern_a, 3)
    pattern_a = pattern_a[:int(SAMPLE_RATE * 12)]
    
    # プロセスB（少し遅れて始まる）
    pattern_b = create_waiting_pattern_enhanced(330, 10, physical=True)
    pattern_b = np.tile(pattern_b, 3)
    pattern_b = phase_shift_pattern(pattern_b, shift_amount=0.05)
    pattern_b = pattern_b[:int(SAMPLE_RATE * 12)]
    
    # 初期衝突
    clash1 = create_deadlock_clash_enhanced(pattern_a, pattern_b, mix_ratios=[0.6, 0.4])
    
    # フィルタバンク処理
    clash1 = filter_bank.apply_filter_bank(clash1, gains=[0.5, 0.8, 1.0, 0.7, 0.5, 0.3])
    
    audio[:int(SAMPLE_RATE * 12)] += clash1
    
    # セクション2: 位相のずれが拡大 (12-24秒)
    print("Section 2: Phase drift expands...")
    
    # より複雑なパターン
    pattern_a_complex = create_waiting_pattern_enhanced(220, 15, physical=True)
    pattern_a_complex = np.tile(pattern_a_complex, 2)
    pattern_a_complex = pattern_a_complex[:int(SAMPLE_RATE * 12)]
    
    pattern_b_complex = create_waiting_pattern_enhanced(330, 15, physical=True)
    pattern_b_complex = np.tile(pattern_b_complex, 2)
    pattern_b_complex = phase_shift_pattern(pattern_b_complex, shift_amount=0.15)
    pattern_b_complex = pattern_b_complex[:int(SAMPLE_RATE * 12)]
    
    # 大きな位相ずれでの衝突
    clash2 = create_deadlock_clash_enhanced(pattern_a_complex, pattern_b_complex, mix_ratios=[0.5, 0.5])
    
    # 緊張の増大カーブ
    tension = create_tension_build(12, start_amp=0.3, end_amp=1.2)
    clash2 = clash2 * tension
    
    # スパースグランピング
    clash2 = granulator.granulate(clash2, grain_size=0.03, density=0.15)
    
    # フィルタバンク処理（異なる設定）
    clash2 = filter_bank.apply_filter_bank(clash2, gains=[0.3, 0.6, 1.0, 1.0, 0.8, 0.5])
    
    audio[int(SAMPLE_RATE * 12):int(SAMPLE_RATE * 24)] += clash2
    
    # セクション3: デッドロック状態の定着 (24-36秒)
    print("Section 3: Deadlock state solidifies...")
    
    # 3つ目のプロセスが参加
    pattern_c = create_waiting_pattern_enhanced(440, 20, physical=True)
    pattern_c = np.tile(pattern_c, 1)
    pattern_c = phase_shift_pattern(pattern_c, shift_amount=0.25)
    pattern_c = pattern_c[:int(SAMPLE_RATE * 12)]
    
    # 3つのプロセスの衝突
    clash_a_b = create_deadlock_clash_enhanced(pattern_a_complex[:int(SAMPLE_RATE * 12)], 
                                              pattern_b_complex[:int(SAMPLE_RATE * 12)], 
                                              mix_ratios=[0.4, 0.6])
    clash_abc = create_deadlock_clash_enhanced(clash_a_b, pattern_c, mix_ratios=[0.4, 0.4, 0.2])
    
    # 歪みを追加
    clash_abc = add_harmonic_distortion(clash_abc, amount=0.2)
    
    # さらに大きな緊張
    tension2 = create_tension_build(12, start_amp=0.8, end_amp=1.5)
    clash_abc = clash_abc * tension2
    
    # より密度の高いグランピング
    clash_abc = granulator.granulate(clash_abc, grain_size=0.02, density=0.25)
    
    # フィルタバンク処理（さらに複雑な設定）
    clash_abc = filter_bank.apply_filter_bank(clash_abc, gains=[0.4, 0.8, 1.2, 1.0, 0.6, 0.3])
    
    audio[int(SAMPLE_RATE * 24):int(SAMPLE_RATE * 36)] += clash_abc
    
    # セクション4: 緊張の頂点と解放 (36-45秒)
    print("Section 4: Tension climax and release...")
    
    # 4つ目のプロセスが参加
    pattern_d = create_waiting_pattern_enhanced(550, 25, physical=True)
    pattern_d = np.tile(pattern_d, 1)
    pattern_d = phase_shift_pattern(pattern_d, shift_amount=0.35)
    pattern_d = pattern_d[:int(SAMPLE_RATE * 9)]
    
    # 4つのプロセスの衝突
    clash_abcd = create_deadlock_clash_enhanced(
        pattern_a_complex[:int(SAMPLE_RATE * 9)], 
        pattern_b_complex[:int(SAMPLE_RATE * 9)],
        pattern_c[:int(SAMPLE_RATE * 9)],
        mix_ratios=[0.3, 0.3, 0.3, 0.1]
    )
    
    # 最大の緊張
    tension_max = create_tension_build(6, start_amp=1.0, end_amp=2.0)
    clash_abcd[:int(SAMPLE_RATE * 6)] *= tension_max
    
    # 急速な解放
    release_envelope = np.ones(int(SAMPLE_RATE * 9))
    release_start = int(SAMPLE_RATE * 6)
    release_envelope[release_start:] = np.linspace(1, 0, int(SAMPLE_RATE * 3))
    clash_abcd *= release_envelope
    
    # 最終処理
    clash_abcd = add_harmonic_distortion(clash_abcd, amount=0.15)
    
    audio[int(SAMPLE_RATE * 36):int(SAMPLE_RATE * 45)] += clash_abcd
    
    # 全体をマルチバンドコンプレッション
    audio = compressor.compress(audio)
    
    # 全体を正規化
    audio = audio / np.max(np.abs(audio)) * 0.7
    
    return audio

def phase_shift_pattern(pattern, shift_amount):
    """パターンに位相シフトを適用（タイミングのずれ）"""
    shift_samples = int(shift_amount * SAMPLE_RATE)
    
    # 後半を前に、前半を後ろに
    shifted = np.zeros_like(pattern)
    if shift_samples < len(pattern):
        shifted[:len(pattern) - shift_samples] = pattern[shift_samples:]
        shifted[len(pattern) - shift_samples:] = pattern[:shift_samples]
    
    return shifted

def create_tension_build(duration, start_amp=0.1, end_amp=1.0):
    """緊張の増大"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    return np.linspace(start_amp, end_amp, len(t))

def add_harmonic_distortion(audio, amount=0.1):
    """高調波歪み（デッドロックのストレス）"""
    # 3次高調波を追加
    distorted = audio + amount * np.sign(audio) * audio**2
    
    # クリッピング
    distorted = np.clip(distorted, -1, 1)
    
    return distorted

if __name__ == "__main__":
    print("Generating Deadlock Dance Enhanced...")
    audio = generate_deadlock_dance_enhanced()
    
    # 出力
    output_path = "../samples/07_deadlock_dance_enhanced.wav"
    sf.write(output_path, audio, SAMPLE_RATE)
    print(f"✅ Generated: {output_path}")
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    print(f"📊 Size: {file_size / 1024 / 1024:.1f} MB")
    print(f"⏱️ Duration: {DURATION} seconds")
    print("🔒🔒🔒 Deadlock: Multiple processes waiting for each other...")
    print("🎛️  Enhanced with Physical Modeling, Filter Banks, and Granulation")