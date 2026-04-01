#!/usr/bin/env python3
"""
Race Condition - Python/SuperCollider Hybrid Implementation
競合状態が生む偶然のハーモニーをPythonで生成し、SuperColliderで音響化
"""

import numpy as np
import scipy.signal
import soundfile as sf
import os
from datetime import datetime

class RaceConditionGenerator:
    def __init__(self, duration=60, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.num_samples = int(duration * sample_rate)
        
        # 競合状態のパラメータ
        self.base_frequency = 220.0  # A3
        self.conflict_rate = 0.1  # 競合発生確率
        self.process_count = 3  # 同時実行プロセス数
        
        print(f"Race Condition Generator: {duration}s at {sample_rate}Hz")
        
    def generate_process_signal(self, process_id, time_array):
        """各プロセスの信号生成"""
        frequency = self.base_frequency * (1 + process_id * 0.1)
        
        # プロセスごとに異なる波形
        if process_id == 0:
            # サイン波：安定した基音
            signal = np.sin(2 * np.pi * frequency * time_array)
        elif process_id == 1:
            # パルス波：リズミックな要素
            signal = scipy.signal.square(2 * np.pi * frequency * time_array)
        else:
            # ノコギリ波：複雑な倍音
            signal = scipy.signal.sawtooth(2 * np.pi * frequency * time_array)
            
        return signal
    
    def generate_conflict_noise(self, time_array):
        """競合によるノイズ生成"""
        # 競合がランダムに発生
        conflict_events = np.random.random(self.num_samples) < self.conflict_rate
        
        # 白色ノイズを競合イベントに乗せる
        noise = np.random.normal(0, 0.1, self.num_samples)
        conflict_noise = noise * conflict_events
        
        return conflict_noise
    
    def detect_conflicts(self, signals):
        """プロセス間の競合を検出"""
        # 信号の急激な変化を競合として検出
        combined_signal = np.sum(signals, axis=0)
        gradient = np.gradient(combined_signal)
        
        # 勾配が大きいところを競合としてマーク
        conflict_threshold = np.std(gradient) * 3
        conflicts = np.abs(gradient) > conflict_threshold
        
        return conflicts
    
    def apply_spatial_effects(self, signal, time_array):
        """空間的な広がりを適用"""
        # パンの揺らぎを生成
        pan_lfo = 0.3 * np.sin(2 * np.pi * 0.5 * time_array)
        
        # ステレオ信号に分割
        left_channel = signal * (1 + pan_lfo) / 2
        right_channel = signal * (1 - pan_lfo) / 2
        
        return np.column_stack([left_channel, right_channel])
    
    def generate_race_condition(self):
        """競合状態の音響を生成"""
        print("Generating race condition signals...")
        
        # 時間配列
        time_array = np.linspace(0, self.duration, self.num_samples)
        
        # 各プロセスの信号を生成
        process_signals = []
        for i in range(self.process_count):
            signal = self.generate_process_signal(i, time_array)
            process_signals.append(signal)
        
        # 競合ノイズを生成
        conflict_noise = self.generate_conflict_noise(time_array)
        
        # 競合を検出
        conflicts = self.detect_conflicts(process_signals)
        
        # 競合が発生した箇所でインパクト音を生成
        conflict_impact = np.zeros(self.num_samples)
        conflict_impact[conflicts] = np.random.normal(0, 0.5, np.sum(conflicts))
        
        # 全信号を混合
        mixed_signal = np.sum(process_signals, axis=0)
        mixed_signal += conflict_noise
        mixed_signal += conflict_impact
        
        # 競合の激しさに応じて振幅調整
        intensity_envelope = 1 + 0.5 * np.sin(2 * np.pi * 0.1 * time_array)
        mixed_signal *= intensity_envelope
        
        # 正規化
        max_amplitude = np.max(np.abs(mixed_signal))
        if max_amplitude > 0:
            mixed_signal = mixed_signal / max_amplitude * 0.8
        
        # 空間効果を適用
        stereo_signal = self.apply_spatial_effects(mixed_signal, time_array)
        
        return stereo_signal
    
    def save_audio(self, signal, filename):
        """音声ファイルとして保存"""
        # 出力ディレクトリの確認
        output_dir = "../samples"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        sf.write(filepath, signal, self.sample_rate)
        print(f"Audio saved to: {filepath}")
        
        return filepath
    
    def generate_visualization_data(self, signals, conflicts):
        """可視化用のデータ生成"""
        time_array = np.linspace(0, self.duration, self.num_samples)
        
        # 競合の時間的分布
        conflict_times = time_array[conflicts]
        
        # 各プロセスの周波数分析
        freq_data = []
        for signal in signals:
            fft = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(len(signal), 1/self.sample_rate)
            power_spectrum = np.abs(fft)**2
            freq_data.append({
                'frequencies': frequencies[:len(frequencies)//2],
                'power': power_spectrum[:len(power_spectrum)//2]
            })
        
        return {
            'time_array': time_array,
            'conflict_times': conflict_times,
            'frequency_data': freq_data
        }

def main():
    """メイン実行関数"""
    print("=== Race Condition Generator ===")
    print("競合状態が生む偶然のハーモニーを生成します...")
    
    # ジェネレーターの初期化
    generator = RaceConditionGenerator(duration=60, sample_rate=44100)
    
    # 競合状態の音響生成
    audio_signal = generator.generate_race_condition()
    
    # 保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"04_race_condition_supercollider_{timestamp}.wav"
    
    filepath = generator.save_audio(audio_signal, filename)
    
    # 可視化データの生成
    process_signals = []
    time_array = np.linspace(0, generator.duration, generator.num_samples)
    for i in range(generator.process_count):
        signal = generator.generate_process_signal(i, time_array)
        process_signals.append(signal)
    
    conflicts = generator.detect_conflicts(process_signals)
    viz_data = generator.generate_visualization_data(process_signals, conflicts)
    
    print(f"\n=== 生成完了 ===")
    print(f"ファイル: {filename}")
    print(f"再生時間: {generator.duration}秒")
    print(f"サンプルレート: {generator.sample_rate}Hz")
    print(f"競合検出数: {np.sum(conflicts)}回")
    
    # 競合統計
    conflict_rate = np.sum(conflicts) / len(conflicts) * 100
    print(f"競合発生率: {conflict_rate:.2f}%")
    
    print(f"\nこの音響はRace Condition（競合状態）を表現しています。")
    print(f"- 複数のプロセスが同時に実行され、互いに干渉")
    print(f"- 確率的な衝突がノイズや突然の音として表現")
    print(f"- 空間的な広がりで競合の緊張感を視覚化")
    print(f"- 非決定的な結果（毎回異なる演奏）")

if __name__ == "__main__":
    main()