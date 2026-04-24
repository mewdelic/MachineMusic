#!/usr/bin/env python3
"""
Memory Leak Lullaby Advanced Simplified - 軽量版

複雑系理論のコンセプトを維持しつつ、計算負荷を軽減したバージョン。
主要な構造は維持しつつ、リアルタイム処理を可能にする最適化。
"""

import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

class MemoryLeakLullabySimplified:
    def __init__(self, duration=60, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.total_samples = int(duration * sample_rate)
        
        # 音響パラメータ
        self.base_frequency = 220.0
        self.memory_decay_rate = 0.995
        
        # 出力配列
        self.left_channel = np.zeros(self.total_samples)
        self.right_channel = np.zeros(self.total_samples)
        
    def generate_quantum_memory_interference(self, start_time, end_time):
        """セクション1: 量子記憶干渉の簡易版"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # 簡易的な量子干渉（正弦波の重ね合わせ）
        signal = np.zeros(samples)
        for i in range(5):  # 量子状態を5個に制限
            freq = self.base_frequency * (1 + 0.1 * i)
            phase = np.random.uniform(0, 2 * np.pi)
            amplitude = np.exp(-0.1 * t) * np.random.uniform(0.1, 0.5)
            signal += amplitude * np.sin(2 * np.pi * freq * t + phase)
        
        # メモリリーク効果
        leak_factor = 1 - (t / (end_time - start_time)) ** 2
        signal *= leak_factor
        
        return signal * 0.2
    
    def generate_spin_glass_memory_relaxation(self, start_time, end_time):
        """セクション2: スピングラス緩和の簡易版"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # 温度減少
        temperature = 2.0 * np.exp(-t / 10)
        
        # 擬似的な磁化（ランダムウォーク）
        magnetization = np.cumsum(np.random.normal(0, 0.1, samples)) * 0.01
        magnetization = np.tanh(magnetization)  # [-1, 1]にクリップ
        
        # 磁化を周波数にマッピング
        signal = np.sin(2 * np.pi * self.base_frequency * (1 + 0.3 * magnetization) * t)
        
        # 温度によるノイズ
        noise = np.random.normal(0, temperature * 0.01, samples)
        signal += noise
        
        # メモリ減衰
        signal *= np.exp(-0.3 * t / (end_time - start_time))
        
        return signal * 0.3
    
    def generate_phase_transition_cleanup(self, start_time, end_time):
        """セクション3: 相転移クリーンアップの簡易版"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # 温度スケジューリング
        critical_temp = 0.5
        temperatures = np.linspace(1.0, 0.1, samples)
        
        signal = np.zeros(samples)
        
        for i, temp in enumerate(temperatures):
            if temp > critical_temp:
                # 高温相：ノイズ
                signal[i] = np.random.normal(0, temp * 0.05)
            else:
                # 低温相：調和音
                order = 1 - temp / critical_temp
                freq = self.base_frequency * (1 + order)
                signal[i] = order * np.sin(2 * np.pi * freq * t[i])
        
        # 臨界領域での増幅
        critical_region = (temperatures > critical_temp - 0.1) & (temperatures < critical_temp + 0.1)
        signal[critical_region] *= 1.5
        
        return signal * 0.25
    
    def generate_chaotic_memory_tracking(self, start_time, end_time):
        """セクション4: カオス的記憶トラッキングの簡易版"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # ヘノンアトラクタ（簡易版）
        x, y = 0.1, 0.1
        trajectory_x = []
        
        for _ in range(samples // 10):  # ダウンサンプリング
            x_new = 1 - 1.4 * x**2 + y
            y_new = 0.3 * x
            x, y = x_new, y_new
            trajectory_x.append(x)
        
        # 軌道を補間
        trajectory = np.interp(np.linspace(0, len(trajectory_x) - 1, samples), 
                             np.arange(len(trajectory_x)), trajectory_x)
        
        # 周波数にマッピング
        freq = self.base_frequency * (1 + 0.5 * trajectory)
        signal = np.sin(2 * np.pi * freq * t)
        
        # カオス的減衰
        signal *= np.exp(-0.2 * t / (end_time - start_time))
        
        return signal * 0.2
    
    def generate_fractal_memory_space(self, start_time, end_time):
        """セクション5: フラクタル記憶空間の簡易版"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        # 1/fノイズ（ピンクノイズ）の簡易生成
        white_noise = np.random.normal(0, 1, samples)
        
        # 移動平均による簡易的1/f特性
        filtered_noise = np.convolve(white_noise, np.ones(10)/10, mode='same')
        
        # 時間変化
        t = np.linspace(0, 1, samples)
        growth_factor = 1 + 0.5 * t
        
        signal = filtered_noise * growth_factor
        
        return signal * 0.1
    
    def generate_self_organized_memory_garbage(self, start_time, end_time):
        """セクション6: 自己組織的記憶ゴミ集積の簡易版"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # 簡易的なクラスタリングモデル
        num_clusters = 5
        cluster_positions = np.random.uniform(0, 1, num_clusters)
        cluster_strengths = np.random.uniform(0.1, 0.5, num_clusters)
        
        signal = np.zeros(samples)
        
        for i, (pos, strength) in enumerate(zip(cluster_positions, cluster_strengths)):
            # クラスタの周波数
            freq = self.base_frequency * (1 + pos)
            cluster_signal = strength * np.sin(2 * np.pi * freq * t)
            
            # クラスタの時間変化
            evolution = np.sin(2 * np.pi * 0.1 * t + i * np.pi / num_clusters)
            cluster_signal *= (1 + 0.5 * evolution)
            
            signal += cluster_signal
        
        # 断続的バースト
        burst_times = np.random.random(samples) < 0.002
        signal[burst_times] *= 3.0
        
        # 全体の減衰
        signal *= np.exp(-0.1 * t / (end_time - start_time))
        
        return signal * 0.15
    
    def generate_stereo_signal(self):
        """ステレオ信号生成"""
        sections = [
            (0, 10, self.generate_quantum_memory_interference),
            (10, 20, self.generate_spin_glass_memory_relaxation),
            (20, 30, self.generate_phase_transition_cleanup),
            (30, 40, self.generate_chaotic_memory_tracking),
            (40, 50, self.generate_fractal_memory_space),
            (50, 60, self.generate_self_organized_memory_garbage)
        ]
        
        for start_time, end_time, generator in sections:
            print(f"Generating section {start_time}-{end_time}s...")
            
            # モノラル信号生成
            mono_signal = generator(start_time, end_time)
            
            # ステレオ配置
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            
            # パンニング
            pan_position = (start_time / 60.0) * 2 - 1  # -1 から 1
            
            # 左右チャンネルに分配
            left_gain = np.sqrt((1 - pan_position) / 2)
            right_gain = np.sqrt((1 + pan_position) / 2)
            
            self.left_channel[start_sample:end_sample] = mono_signal * left_gain
            self.right_channel[start_sample:end_sample] = mono_signal * right_gain
    
    def apply_mastering(self):
        """簡易マスタリング"""
        # ノーマライズ
        max_left = np.max(np.abs(self.left_channel))
        max_right = np.max(np.abs(self.right_channel))
        max_level = max(max_left, max_right)
        
        if max_level > 0:
            self.left_channel /= max_level
            self.right_channel /= max_level
        
        # ソフトクリップ
        def soft_clip(signal, threshold=0.8):
            return np.tanh(signal / threshold) * threshold
        
        self.left_channel = soft_clip(self.left_channel * 0.8)
        self.right_channel = soft_clip(self.right_channel * 0.8)
        
        # 最終ノーマライズ
        max_left = np.max(np.abs(self.left_channel))
        max_right = np.max(np.abs(self.right_channel))
        max_level = max(max_left, max_right)
        
        if max_level > 0:
            self.left_channel = self.left_channel / max_level * 0.9
            self.right_channel = self.right_channel / max_level * 0.9
    
    def save_audio(self, filename):
        """オーディオ保存"""
        audio_data = np.column_stack((self.left_channel, self.right_channel))
        audio_data = (audio_data * 32767).astype(np.int16)
        wavfile.write(filename, self.sample_rate, audio_data)
        print(f"Audio saved to: {filename}")

def main():
    """メイン処理"""
    print("Memory Leak Lullaby Advanced Simplified")
    print("=" * 50)
    
    mll = MemoryLeakLullabySimplified()
    
    print("1. Generating stereo signal...")
    mll.generate_stereo_signal()
    
    print("2. Applying mastering...")
    mll.apply_mastering()
    
    print("3. Saving audio...")
    filename = "05_memory_leak_lullaby_advanced_simplified.wav"
    mll.save_audio(filename)
    
    print("=" * 50)
    print("✅ Generation complete!")
    print(f"File: {filename}")
    print(f"Duration: {mll.duration}s")
    print(f"Sample rate: {mll.sample_rate}Hz")
    print("Format: Stereo WAV")
    print()
    print("🎵 Sections:")
    print("1. Quantum Memory Interference (0-10s)")
    print("2. Spin Glass Relaxation (10-20s)")
    print("3. Phase Transition Cleanup (20-30s)")
    print("4. Chaotic Memory Tracking (30-40s)")
    print("5. Fractal Memory Space (40-50s)")
    print("6. Self-Organized Memory Garbage (50-60s)")
    print()
    print("🔧 Simplified for faster computation")
    print("while maintaining artistic concept.")

if __name__ == "__main__":
    main()