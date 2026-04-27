#!/usr/bin/env python3
"""
Null Pointer Dreams Advanced
~~~~~~~~~~~~~~~~~~~~~~~~~~~

何も指さないポインタが見る夢を音楽的に表現。

- メモリ空間の空虚さを音響化
- Nullポインタアクセスの不安定さ
- 断片化された情報の再構成
- 確率的要素と構造的要素の融合

Concept: 「何も指さないポインタが見る夢」
"""

import numpy as np
import scipy.signal as signal
import scipy.fft as fft
import soundfile as sf
import matplotlib.pyplot as plt
import json
from datetime import datetime
import random

class NullPointerDreamsAdvanced:
    def __init__(self, duration=60, sample_rate=48000):
        self.duration = duration
        self.sample_rate = sample_rate
        self.samples = int(duration * sample_rate)
        
        # 音響パラメータ
        self.base_freq = 220.0  # A3
        self.memory_size = 1024  # 仮想メモリサイズ
        self.null_probability = 0.3  # Nullアクセス確率
        self.fragmentation_rate = 0.15  # 断片化率
        
        # 空間化パラメータ
        self.spatial_range = 60.0  # 空間範囲（度）
        self.movement_speed = 0.1  # 空間移動速度
        
        # ランダムシード（再現性のため）
        np.random.seed(42)
        random.seed(42)
        
    def generate_memory_map(self):
        """仮想メモリマップの生成"""
        # メモリアドレス空間（0x0000-0x0400）
        addresses = np.arange(0x0000, 0x0400, dtype=np.uint16)
        
        # メモリの状態を表現
        # 0: 空き（未使用）
        # 1: 有効データ
        # 2: 解放済み（ゴミデータ）
        # 3: Nullポインタ（特別な状態）
        
        memory_state = np.zeros(self.memory_size, dtype=np.int8)
        
        # 有効データの配置（ランダムだがクラスター化）
        valid_regions = []
        for _ in range(random.randint(8, 16)):
            start = random.randint(0, self.memory_size - 64)
            size = random.randint(8, 64)
            if start + size <= self.memory_size:
                memory_state[start:start+size] = 1
                valid_regions.append((start, start+size))
        
        # 解放済み領域の配置
        for _ in range(random.randint(4, 8)):
            start = random.randint(0, self.memory_size - 32)
            size = random.randint(4, 32)
            if start + size <= self.memory_size:
                memory_state[start:start+size] = 2
        
        # Nullポインタの配置（特別な場所）
        null_positions = random.sample(range(self.memory_size), 
                                     int(self.memory_size * 0.02))
        memory_state[null_positions] = 3
        
        return memory_state, addresses
    
    def null_pointer_access_sounds(self, memory_state, time_points):
        """Nullポインタアクセス時の音響生成"""
        null_sounds = np.zeros(len(time_points))
        
        # メモリ状態に基づいた音響パターン
        for i, t in enumerate(time_points):
            # 仮想アドレスの生成
            address = int(t * self.memory_size) % self.memory_size
            state = memory_state[address]
            
            # 状態に応じた音響生成
            if state == 0:  # 空きメモリ
                # 静寂に近いノイズ
                amplitude = 0.05 * np.random.normal(0, 0.1)
                frequency = self.base_freq * 0.5
                
            elif state == 1:  # 有効データ
                # 安定した音響
                amplitude = 0.3 * (1 + 0.1 * np.sin(2 * np.pi * t * 2))
                frequency = self.base_freq * (1 + 0.2 * np.sin(2 * np.pi * t * 0.5))
                
            elif state == 2:  # 解放済みメモリ
                # 不安定な音響
                amplitude = 0.2 * np.random.normal(1, 0.3)
                frequency = self.base_freq * (1 + 0.5 * np.random.normal(0, 0.2))
                
            else:  # state == 3: Nullポインタ
                # 衝撃音と共鳴
                if np.random.random() < self.null_probability:
                    # Nullアクセス発生
                    amplitude = 0.8 * np.exp(-t * 10)  # 減衰
                    frequency = self.base_freq * 2 * np.random.uniform(0.5, 3.0)
                else:
                    amplitude = 0.1
                    frequency = self.base_freq
            
            null_sounds[i] = amplitude * np.sin(2 * np.pi * frequency * t)
        
        return null_sounds
    
    def fragmentation_effects(self, audio_signal, fragmentation_positions):
        """断片化効果の適用"""
        fragmented_audio = audio_signal.copy()
        
        # 断片化によるランダムな切断と再配置
        fragment_size = int(self.sample_rate * self.fragmentation_rate)
        num_fragments = len(audio_signal) // fragment_size
        
        fragments = []
        for i in range(num_fragments):
            start = i * fragment_size
            end = start + fragment_size
            if end <= len(audio_signal):
                fragment = audio_signal[start:end]
                
                # 断片化処理
                if np.random.random() < 0.3:  # 30%の確率で断片化
                    # ランダムな時間的反転
                    if np.random.random() < 0.5:
                        fragment = fragment[::-1]
                    
                    # ランダムなピッチシフト
                    shift_factor = np.random.uniform(0.8, 1.2)
                    fragment = self.pitch_shift(fragment, shift_factor)
                    
                    # ランダムなゲイン調整
                    gain = np.random.uniform(0.3, 1.5)
                    fragment *= gain
                
                fragments.append(fragment)
        
        # 断片を再構成
        if fragments:
            try:
                fragmented_audio = np.concatenate(fragments)
                # オリジナルの長さに合わせる
                if len(fragmented_audio) > len(audio_signal):
                    fragmented_audio = fragmented_audio[:len(audio_signal)]
                elif len(fragmented_audio) < len(audio_signal):
                    # ゼロパディング
                    padding = np.zeros(len(audio_signal) - len(fragmented_audio))
                    fragmented_audio = np.concatenate([fragmented_audio, padding])
            except:
                fragmented_audio = audio_signal
        
        return fragmented_audio
    
    def pitch_shift(self, audio, factor):
        """簡易的なピッチシフト"""
        # リサンプリングによるピッチシフト
        indices = np.arange(0, len(audio), factor)
        indices = indices[indices < len(audio)].astype(int)
        if len(indices) > 0:
            return audio[indices]
        else:
            return audio
    
    def spatialization_3d(self, audio, azimuth, elevation=0):
        """3D空間化処理（バイノーラル）"""
        # 簡易的なバイノーラル処理
        # 実際のHRTFを使用するとより高度な効果が得られます
        
        left_channel = audio.copy()
        right_channel = audio.copy()
        
        # 頭部遮蔽効果のシミュレーション
        # 方位角に応じた時間差と音量差
        # azimuthが配列の場合、平均値を使用
        if hasattr(azimuth, '__len__') and len(azimuth) > 0:
            azimuth_avg = np.mean(azimuth)
        else:
            azimuth_avg = azimuth
        
        azimuth_rad = np.radians(azimuth_avg)
        
        # 時間差（ITD: Interaural Time Difference）
        max_delay = 0.0007  # 最大遅延700μs
        itd = max_delay * np.sin(azimuth_rad)
        itd_samples = int(itd * self.sample_rate)
        
        # レベル差（ILD: Interaural Level Difference）
        max_attenuation = 0.7  # 最大減衰量
        ild = max_attenuation * np.abs(np.sin(azimuth_rad))
        
        # チャンネル間の調整
        if azimuth_avg > 0:  # 右側
            # 左チャンネル：遅延と減衰
            if itd_samples > 0:
                left_channel = np.pad(left_channel, (itd_samples, 0))[:-itd_samples]
            left_channel *= (1 - ild)
            
            # 右チャンネル：増幅
            right_channel *= (1 + ild * 0.3)
            
        else:  # 左側
            # 左チャンネル：増幅
            left_channel *= (1 + ild * 0.3)
            
            # 右チャンネル：遅延と減衰
            if itd_samples > 0:
                right_channel = np.pad(right_channel, (itd_samples, 0))[:-itd_samples]
            right_channel *= (1 - ild)
        
        # ステレオ音声の生成
        stereo_audio = np.column_stack((left_channel, right_channel))
        
        return stereo_audio
    
    def memory_error_sounds(self, memory_state):
        """メモリアクセスエラー音の生成"""
        error_sounds = np.zeros(self.samples)
        
        # 時間軸の生成
        time = np.linspace(0, self.duration, self.samples)
        
        # セグメンテーションフォルトのシミュレーション
        segfault_positions = []
        for _ in range(random.randint(3, 7)):
            position = random.randint(0, self.samples - 1000)
            duration = random.randint(100, 500)
            segfault_positions.append((position, position + duration))
        
        # セグメンテーションフォルト音の重畳
        for start, end in segfault_positions:
            if start < self.samples and end <= self.samples:
                # 衝撃音の生成
                impact_sound = np.zeros(self.samples)
                impact_sound[start:end] = np.random.normal(0, 0.3, end - start)
                impact_sound = signal.lfilter([1, -0.9], [1], impact_sound)  # リバーブ効果
                
                error_sounds += impact_sound
        
        # バスアクセスエラーのシミュレーション
        bus_error_freq = 0.1  # 0.1Hzの周期で発生
        bus_error_mask = np.sin(2 * np.pi * bus_error_freq * time) > 0.9
        
        bus_errors = np.zeros(self.samples)
        bus_errors[bus_error_mask] = np.random.normal(0, 0.2, np.sum(bus_error_mask))
        
        error_sounds += bus_errors
        
        return error_sounds
    
    def generate_composition(self):
        """主要なコンポジション生成"""
        print("Null Pointer Dreams Advanced: 生成開始")
        
        # メモリマップの生成
        memory_state, addresses = self.generate_memory_map()
        print(f"メモリ状態: 有効={np.sum(memory_state==1)}, 解放済={np.sum(memory_state==2)}, Null={np.sum(memory_state==3)}")
        
        # 時間軸の生成
        time = np.linspace(0, self.duration, self.samples)
        
        # 基本音響の生成
        print("基本音響生成中...")
        base_sounds = self.null_pointer_access_sounds(memory_state, time)
        
        # 断片化効果の適用
        print("断片化処理中...")
        fragmentation_positions = np.where(np.random.random(len(time)) < self.fragmentation_rate)[0]
        fragmented_sounds = self.fragmentation_effects(base_sounds, fragmentation_positions)
        
        # メモリエラー音の追加
        print("メモリエラー音追加中...")
        error_sounds = self.memory_error_sounds(memory_state)
        
        # 音響の合成
        print("音響合成中...")
        combined_sounds = fragmented_sounds + error_sounds * 0.5
        
        # エンベロープの適用
        envelope = self.create_envelope(time)
        combined_sounds *= envelope
        
        # ノーマライズ
        combined_sounds = self.normalize_audio(combined_sounds)
        
        # 3D空間化
        print("3D空間化処理中...")
        # アジマスの時間変化（円運動）
        azimuth = self.spatial_range * np.sin(2 * np.pi * self.movement_speed * time)
        
        # 立体音響の生成
        stereo_audio = self.spatialization_3d(combined_sounds, azimuth)
        
        print("生成完了")
        
        return stereo_audio, memory_state, azimuth
    
    def create_envelope(self, time):
        """エンベロープの生成"""
        # ADSR風のエンベロープ
        attack_time = self.duration * 0.1
        decay_time = self.duration * 0.2
        sustain_level = 0.7
        release_time = self.duration * 0.3
        
        envelope = np.ones_like(time)
        
        # Attack
        attack_mask = time <= attack_time
        envelope[attack_mask] = time[attack_mask] / attack_time
        
        # Decay
        decay_start = attack_time
        decay_end = decay_start + decay_time
        decay_mask = (time > decay_start) & (time <= decay_end)
        decay_time_norm = (time[decay_mask] - decay_start) / decay_time
        envelope[decay_mask] = 1 - (1 - sustain_level) * decay_time_norm
        
        # Sustain
        sustain_start = decay_end
        sustain_end = self.duration - release_time
        sustain_mask = (time > sustain_start) & (time <= sustain_end)
        envelope[sustain_mask] = sustain_level
        
        # Release
        release_mask = time > sustain_end
        release_time_norm = (time[release_mask] - sustain_end) / release_time
        envelope[release_mask] = sustain_level * (1 - release_time_norm)
        
        return envelope
    
    def normalize_audio(self, audio):
        """音声のノーマライズ"""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val * 0.9  # 0.9で少し余裕を持たせる
        else:
            return audio
    
    def create_visualization(self, memory_state, azimuth, time):
        """可視化の作成"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # メモリマップの可視化
        ax1.plot(memory_state, marker='o', markersize=1)
        ax1.set_title('Memory State Map')
        ax1.set_xlabel('Address')
        ax1.set_ylabel('State (0:Empty, 1:Valid, 2:Freed, 3:Null)')
        ax1.grid(True, alpha=0.3)
        
        # アジマスの時間変化
        ax2.plot(time, azimuth)
        ax2.set_title('Spatial Azimuth Movement')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Azimuth (degrees)')
        ax2.grid(True, alpha=0.3)
        
        # メモリ状態のヒストグラム
        states = ['Empty', 'Valid', 'Freed', 'Null']
        counts = [np.sum(memory_state==i) for i in range(4)]
        ax3.bar(states, counts)
        ax3.set_title('Memory State Distribution')
        ax3.set_ylabel('Count')
        
        # スペクトログラム（サンプル）
        sample_size = min(48000, len(azimuth))
        sample_signal = np.sin(2 * np.pi * 440 * time[:sample_size]) * 0.1
        
        f, t, Sxx = signal.spectrogram(sample_signal, self.sample_rate)
        ax4.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        ax4.set_title('Sample Spectrogram')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Frequency (Hz)')
        ax4.set_ylim(0, 2000)
        
        plt.tight_layout()
        return fig
    
    def save_audio(self, audio, filename):
        """音声ファイルの保存"""
        sf.write(filename, audio, self.sample_rate)
        print(f"音声ファイルを保存: {filename}")
    
    def save_metadata(self, memory_state, filename):
        """メタデータの保存"""
        metadata = {
            "title": "Null Pointer Dreams Advanced",
            "artist": "MachineMusic Project",
            "album": "Error Garden (Advanced)",
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "memory_size": self.memory_size,
            "null_probability": self.null_probability,
            "fragmentation_rate": self.fragmentation_rate,
            "spatial_range": self.spatial_range,
            "memory_stats": {
                "empty_addresses": int(np.sum(memory_state == 0)),
                "valid_addresses": int(np.sum(memory_state == 1)),
                "freed_addresses": int(np.sum(memory_state == 2)),
                "null_addresses": int(np.sum(memory_state == 3))
            },
            "generation_time": datetime.now().isoformat(),
            "technical_notes": "Advanced algorithm featuring memory access error simulation, 3D spatialization, and fragmentation effects"
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"メタデータを保存: {filename}")

def main():
    """メイン実行関数"""
    print("Null Pointer Dreams Advanced - 生成開始")
    print("=" * 50)
    
    # インスタンスの生成
    composer = NullPointerDreamsAdvanced(duration=60, sample_rate=48000)
    
    # コンポジションの生成
    stereo_audio, memory_state, azimuth = composer.generate_composition()
    
    # 音声ファイルの保存
    audio_filename = "03_null_pointer_dreams_advanced.wav"
    composer.save_audio(stereo_audio, audio_filename)
    
    # 可視化の作成と保存
    print("可視化を作成中...")
    time = np.linspace(0, composer.duration, composer.samples)
    fig = composer.create_visualization(memory_state, azimuth, time)
    viz_filename = "null_pointer_dreams_advanced_visualization.png"
    fig.savefig(viz_filename, dpi=300, bbox_inches='tight')
    print(f"可視化を保存: {viz_filename}")
    plt.close(fig)
    
    # メタデータの保存
    metadata_filename = "null_pointer_dreams_advanced_metadata.json"
    composer.save_metadata(memory_state, metadata_filename)
    
    print("=" * 50)
    print("Null Pointer Dreams Advanced - 生成完了")
    print(f"生成ファイル:")
    print(f"  音声: {audio_filename}")
    print(f"  可視化: {viz_filename}")
    print(f"  メタデータ: {metadata_filename}")
    
    # 音響仕様のサマリー
    print(f"\n音響仕様:")
    print(f"  収録時間: {composer.duration}秒")
    print(f"  サンプルレート: {composer.sample_rate}Hz")
    print(f"  メモリサイズ: {composer.memory_size}アドレス")
    print(f"  Nullアクセス確率: {composer.null_probability}")
    print(f"  断片化率: {composer.fragmentation_rate}")
    print(f"  空間範囲: ±{composer.spatial_range}°")

if __name__ == "__main__":
    main()