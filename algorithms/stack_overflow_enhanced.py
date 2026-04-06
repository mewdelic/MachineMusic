#!/usr/bin/env python3
"""
Stack Overflow Enhanced — 物理モデリングによるスタックオーバーフローの表現深化

Concept:
- スタックオーバーフローを物理的な現象として表現
- Karplus-Strongアルゴリズムによる弦の振動のスタック
- 物理的な制約が破られる瞬間の音響化
- 複数の物理モデルが干渉し合う構造

Enhanced Features:
- 物理モデリング弦（Karplus-Strong）
- マルチレイヤーリバーブ
- フィルタバンクによる周波数帯域別処理
- 非線形歪みとサチュレーション
- スパースグランピングによるテクスチャ付加
- ステレオイメージングの強化

Algorithm:
1. 基本音源: Karplus-Strong物理モデルによる弦のスタック
2. 深度増加: 再帰的に層を追加、物理パラメータを変化
3. 制限突破: 物理的制約を超えた時の非線形現象
4. 崩壊: 物理モデルの破綻とカオスへの移行
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
import os
import soundfile as sf
from collections import deque

# Parameters
SAMPLE_RATE = 44100
DURATION = 45  # Enhanced to 45 seconds for more development
BASE_FREQ = 220  # A3

class KarplusStrongString:
    """Karplus-Strong物理モデルによる弦の実装"""
    
    def __init__(self, frequency, sample_rate, decay_factor=0.996, brightness=0.5):
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.decay_factor = decay_factor
        self.brightness = brightness
        self.buffer_size = int(sample_rate / frequency)
        self.buffer = deque(np.random.uniform(-0.5, 0.5, self.buffer_size))
        self.lowpass_filter = 0.5 * (1 - brightness)
        
    def get_sample(self):
        """次のサンプルを生成"""
        # バッファからサンプルを取得
        sample = self.buffer.popleft()
        
        # ローパスフィルタリング
        filtered = sample * (1 - self.lowpass_filter) + self.buffer[0] * self.lowpass_filter
        
        # 減衰を適用
        filtered *= self.decay_factor
        
        # バッファに戻す
        self.buffer.append(filtered)
        
        return sample
        
    def set_frequency(self, frequency):
        """周波数を変更"""
        if frequency != self.frequency:
            self.frequency = frequency
            new_size = int(self.sample_rate / frequency)
            if new_size != self.buffer_size:
                # バッファサイズの変更
                if new_size > self.buffer_size:
                    # バッファを延長
                    padding = np.random.uniform(-0.1, 0.1, new_size - self.buffer_size)
                    self.buffer.extend(padding)
                else:
                    # バッファを短縮
                    for _ in range(self.buffer_size - new_size):
                        self.buffer.pop()
                self.buffer_size = new_size

class PhysicalModelingStack:
    """物理モデリングによるスタックの実装"""
    
    def __init__(self, base_freq, sample_rate, max_layers=8):
        self.base_freq = base_freq
        self.sample_rate = sample_rate
        self.max_layers = max_layers
        self.strings = []
        self.layer_frequencies = []
        self.layer_amplitudes = []
        self.layer_decays = []
        
    def add_layer(self, layer_num):
        """新しいレイヤーを追加"""
        # 周波数の計算：ハーモニクスと微細なずれ
        freq_multiplier = 1 + (layer_num * 0.05) + np.random.uniform(-0.01, 0.01)
        frequency = self.base_freq * freq_multiplier
        
        # 物理パラメータの設定
        decay_factor = 0.998 - (layer_num * 0.0005)  # 上位レイヤーほど早く減衰
        brightness = 0.6 - (layer_num * 0.05)  # 上位レイヤーほど暗い
        
        # 弦を作成
        string = KarplusStrongString(frequency, self.sample_rate, decay_factor, brightness)
        self.strings.append(string)
        self.layer_frequencies.append(frequency)
        self.layer_amplitudes.append(0.8 ** layer_num)  # 上位レイヤーほど小さい振幅
        self.layer_decays.append(decay_factor)
        
    def generate_chunk(self, num_samples):
        """チャンクを生成"""
        chunk = np.zeros(num_samples)
        
        for i, string in enumerate(self.strings):
            layer_chunk = np.zeros(num_samples)
            for j in range(num_samples):
                layer_chunk[j] = string.get_sample()
            
            # 振幅を適用
            chunk += layer_chunk * self.layer_amplitudes[i]
        
        return chunk

class FilterBank:
    """マルチバンドフィルタバンク"""
    
    def __init__(self, sample_rate, num_bands=6):
        self.sample_rate = sample_rate
        self.num_bands = num_bands
        # より現実的な周波数帯域に調整
        self.crossover_freqs = np.logspace(np.log10(80), np.log10(min(8000, sample_rate/3)), num_bands + 1)
        
    def process(self, audio):
        """フィルタバンクで処理"""
        bands = []
        
        for i in range(self.num_bands):
            # バンドパスフィルタの設計
            low_freq = self.crossover_freqs[i]
            high_freq = self.crossover_freqs[i + 1]
            
            # バターハースフィルタで設計
            nyquist = self.sample_rate / 2
            low = max(0.01, min(0.99, low_freq / nyquist))  # 安全範囲に制限
            high = max(0.01, min(0.99, high_freq / nyquist))  # 安全範囲に制限
            
            # 確認：low < high
            if low >= high:
                # スキップまたは単純なローパス/ハイパスにフォールバック
                if i == 0:
                    # 最初のバンドはローパス
                    b, a = signal.butter(4, high, btype='low')
                elif i == self.num_bands - 1:
                    # 最後のバンドはハイパス
                    b, a = signal.butter(4, low, btype='high')
                else:
                    # 中間バンドはスキップ（前のバンドをコピー）
                    if bands:
                        bands.append(bands[-1].copy())
                        continue
                    else:
                        b, a = signal.butter(4, 0.1, btype='low')
            else:
                # バンドパスフィルタ
                b, a = signal.butter(4, [low, high], btype='band')
            
            try:
                band = signal.filtfilt(b, a, audio)
                bands.append(band)
            except:
                # エラー時は前のバンドをコピーまたはゼロ配列
                if bands:
                    bands.append(bands[-1].copy())
                else:
                    bands.append(np.zeros_like(audio))
        
        return bands

def create_distortion(audio, drive=1.0, tone=0.5):
    """非線形歪みとトーンコントロール"""
    # ドライブ適用
    driven = audio * drive
    # ソフクリッピング
    distorted = np.tanh(driven)
    
    # トーンコントロール（簡易的なハイパス）
    if tone > 0.1:
        b, a = signal.butter(2, tone * 0.1, btype='high')
        distorted = signal.filtfilt(b, a, distorted)
    
    return distorted

def create_sparse_granulation(audio, grain_size=0.05, density=0.3):
    """スパースグランピングによるテクスチャ付加"""
    samples = len(audio)
    grain_samples = int(grain_size * SAMPLE_RATE)
    result = np.zeros(samples)
    
    # グレインの配置
    grain_positions = np.random.choice(samples, int(samples * density / grain_samples), replace=False)
    
    for pos in grain_positions:
        if pos + grain_samples <= samples:
            # グレインの抽出
            grain = audio[pos:pos + grain_samples]
            # エンベロープ適用
            envelope = np.hanning(len(grain))
            grain *= envelope
            
            # 結果に加算
            end_pos = min(pos + len(grain), samples)
            result[pos:end_pos] += grain[:end_pos - pos]
    
    # オリジナルとミックス
    result = audio * 0.7 + result * 0.3
    
    return result

def create_reverb(audio, rt60=2.0, damping=0.5):
    """簡易的なリバーブの実装"""
    delay_lines = [0.03, 0.05, 0.07, 0.11, 0.13, 0.17]  # 秒
    gains = [0.5, 0.3, 0.25, 0.15, 0.1, 0.05]
    
    result = audio.copy()
    
    for delay, gain in zip(delay_lines, gains):
        delay_samples = int(delay * SAMPLE_RATE)
        delayed = np.zeros(len(audio))
        delayed[delay_samples:] = audio[:-delay_samples] * gain
        
        # 減衰係数
        decay = np.exp(-3 * delay / rt60)
        delayed *= decay
        
        result += delayed
    
    # 正規化
    max_val = np.max(np.abs(result))
    if max_val > 0:
        result /= max_val * 1.5
    
    return result

def create_stack_overflow_enhanced():
    """Enhanced版Stack Overflowトラックの作成"""
    print("Building enhanced physical modeling stack...")
    
    # セクションごとの時間設定
    section_duration = DURATION / 4  # 4セクション
    total_samples = int(SAMPLE_RATE * DURATION)
    
    # ステレオ用
    track_left = np.zeros(total_samples)
    track_right = np.zeros(total_samples)
    
    # 各セクションの処理
    for section in range(4):
        start_sample = int(section * section_duration * SAMPLE_RATE)
        end_sample = int((section + 1) * section_duration * SAMPLE_RATE)
        section_samples = end_sample - start_sample
        
        print(f"Processing section {section + 1}/4...")
        
        if section < 3:  # 最初の3セクションはスタックの成長
            # 物理モデリングスタックの作成
            stack = PhysicalModelingStack(BASE_FREQ, SAMPLE_RATE)
            
            # セクションごとにレイヤーを追加
            layers_per_section = 3
            for i in range(layers_per_section):
                layer_num = section * layers_per_section + i
                if layer_num < stack.max_layers:
                    stack.add_layer(layer_num)
            
            # セクションのオーディオ生成
            section_audio = stack.generate_chunk(section_samples)
            
            # セクションごとにエフェクトを強化
            if section == 0:
                # 第1セクション：クリーンな物理音
                pass
            elif section == 1:
                # 第2セクション：軽い歪み
                section_audio = create_distortion(section_audio, drive=1.5, tone=0.3)
            elif section == 2:
                # 第3セクション：強い歪みとフィルタバンク
                section_audio = create_distortion(section_audio, drive=3.0, tone=0.5)
                
                # フィルタバンク処理
                filter_bank = FilterBank(SAMPLE_RATE, 6)
                bands = filter_bank.process(section_audio)
                
                # バンドごとに異なる処理
                processed_bands = []
                for i, band in enumerate(bands):
                    if i < 2:  # 低域はブースト
                        processed_bands.append(band * 1.5)
                    elif i < 4:  # 中域はそのまま
                        processed_bands.append(band)
                    else:  # 高域はカット
                        processed_bands.append(band * 0.5)
                
                # 再合成
                section_audio = np.sum(processed_bands, axis=0)
            
        else:  # 最終セクションはオーバーフローの崩壊
            print("Creating overflow collapse...")
            # ホワイトノイズベース
            section_audio = np.random.uniform(-0.3, 0.3, section_samples)
            
            # スキャッタードトーンフラグメント
            num_fragments = 30
            for _ in range(num_fragments):
                start = np.random.randint(0, section_samples - 500)
                frag_len = np.random.randint(200, 3000)
                freq = np.random.choice([110, 220, 330, 440, 660]) * np.random.uniform(0.8, 1.2)
                fragment = np.sin(2 * np.pi * freq * np.linspace(0, frag_len/SAMPLE_RATE, frag_len))
                fragment *= np.hanning(frag_len) * 0.2
                end = min(start + frag_len, section_samples)
                section_audio[start:end] += fragment[:end-start]
            
            # デジタルデブリ（急峻な振幅スパイク）
            debris_count = 100
            for _ in range(debris_count):
                pos = np.random.randint(0, section_samples)
                spike = np.random.choice([-1, 1]) * np.random.uniform(0.7, 1.0)
                section_audio[pos] = spike
            
            # 強烈な歪み
            section_audio = create_distortion(section_audio, drive=5.0, tone=0.8)
        
        # リバーブの適用
        section_audio = create_reverb(section_audio, rt60=1.5, damping=0.6)
        
        # スパースグランピング（最終セクション以外）
        if section < 3:
            section_audio = create_sparse_granulation(section_audio, grain_size=0.03, density=0.4)
        
        # ステレオパンニングと広がり
        stereo_width = 0.3 + section * 0.2  # セクションが進むにつれて広がる
        mid_signal = section_audio * 0.7
        side_signal = section_audio * stereo_width
        
        # 左右チャンネルに分配
        track_left[start_sample:end_sample] = mid_signal - side_signal
        track_right[start_sample:end_sample] = mid_signal + side_signal
    
    # 全体のマスタリング
    print("Applying master processing...")
    
    # マルチバンドコンプレッション（簡易）
    filter_bank = FilterBank(SAMPLE_RATE, 4)
    left_bands = filter_bank.process(track_left)
    right_bands = filter_bank.process(track_right)
    
    processed_left = []
    processed_right = []
    
    for i, (left_band, right_band) in enumerate(zip(left_bands, right_bands)):
        if i == 0:  # 低域：控えめな圧縮
            threshold = 0.8
            ratio = 2.0
        elif i == 1:  # 低中域：標準的な圧縮
            threshold = 0.6
            ratio = 3.0
        elif i == 2:  # 高中域：強めの圧縮
            threshold = 0.5
            ratio = 4.0
        else:  # 高域：リミッター
            threshold = 0.4
            ratio = 10.0
        
        # 簡易コンプレッション
        left_abs = np.abs(left_band)
        right_abs = np.abs(right_band)
        
        left_gain = np.where(left_abs > threshold, threshold / left_abs * (1 - 1/ratio) + 1/ratio, 1.0)
        right_gain = np.where(right_abs > threshold, threshold / right_abs * (1 - 1/ratio) + 1/ratio, 1.0)
        
        processed_left.append(left_band * left_gain)
        processed_right.append(right_band * right_gain)
    
    # 再合成
    track_left = np.sum(processed_left, axis=0)
    track_right = np.sum(processed_right, axis=0)
    
    # 全体の正規化
    max_val = max(np.max(np.abs(track_left)), np.max(np.abs(track_right)))
    if max_val > 0:
        track_left /= max_val * 0.95
        track_right /= max_val * 0.95
    
    # フェードアウト
    fade_samples = int(SAMPLE_RATE * 3)
    if len(track_left) > fade_samples:
        fade = np.linspace(1, 0, fade_samples)
        track_left[-fade_samples:] *= fade
        track_right[-fade_samples:] *= fade
    
    return track_left, track_right

if __name__ == "__main__":
    print("=" * 60)
    print("Stack Overflow Enhanced - Track 1 of Error Garden")
    print("Physical Modeling Edition")
    print("=" * 60)
    
    track_left, track_right = create_stack_overflow_enhanced()
    
    # ステレオファイルとして保存
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", "01_stack_overflow_enhanced.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 16bit PCMに変換
    track_16bit_left = np.int16(track_left * 32767)
    track_16bit_right = np.int16(track_right * 32767)
    
    # ステレオ配列を作成
    stereo_track = np.column_stack((track_16bit_left, track_16bit_right))
    
    # 保存
    wavfile.write(output_path, SAMPLE_RATE, stereo_track)
    
    duration = len(track_left) / SAMPLE_RATE
    print(f"\nGenerated: {output_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Format: Stereo 16-bit PCM")
    print("\nEnhanced features:")
    print("- Karplus-Strong physical modeling")
    print("- Multi-band filter bank processing")
    print("- Sparse granulation texture")
    print("- Multi-band compression")
    print("- Stereo image enhancement")
    print("\nDone! The physical stack has overflowed with enhanced realism.")