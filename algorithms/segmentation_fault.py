#!/usr/bin/env python3
"""
Segmentation Fault - 領域違反の破裂

このトラックはセグメンテーション違反を音楽的に表現する。
メモリ領域への不正アクセスが引き起こす「破裂」的な音響を生成。

コンセプト:
- 不規則なメモリアクセスパターン
- 予期せぬクラッシュと再起動
- メモリ領域の境界違反
- システムの不安定さ

技法:
- 不規則なノイズバースト
- 周波数の急激な変化
- 断続的なサイレンス（クラッシュ状態）
- 徐々に不安定になる構造
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import random
import math

class SegmentationFaultGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.duration = 180  # 3分
        self.channels = 2  # ステレオ
        
    def generate_memory_access_pattern(self, duration):
        """不規則なメモリアクセスパターンを生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # 不規則なアクセスパターン（ランダムウォーク）
        memory_positions = np.zeros_like(t)
        current_pos = 0
        
        for i in range(len(t)):
            # ランダムなジャンプ（不正アクセス）
            jump = random.choice([-1000, -500, -100, 0, 100, 500, 1000])
            current_pos += jump
            
            # 境界チェックとオーバーフロー
            if abs(current_pos) > 32768:  # 16ビット整数の範囲を超える
                current_pos = random.randint(-32768, 32767)
            
            memory_positions[i] = current_pos
        
        return memory_positions
    
    def create_segmentation_noise(self, memory_positions, duration):
        """メモリ位置に基づくノイズを生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.zeros((len(t), self.channels))
        
        # メモリ位置を周波数にマッピング
        for i, pos in enumerate(memory_positions):
            if i % 1000 == 0:  # 1000サンプルごとに「アクセスイベント」
                # 不正アクセスによるノイズバースト
                noise_burst = np.random.normal(0, 0.3, 100)
                if i + len(noise_burst) < len(audio):
                    # 周波数シフト（位置に基づく）
                    freq_shift = abs(pos) / 32768.0 * 2000  # 0-2000Hz
                    
                    # バンドパスフィルタで特定の周波数帯を強調
                    for ch in range(self.channels):
                        audio[i:i+len(noise_burst), ch] = noise_burst * np.sin(2 * np.pi * freq_shift * np.linspace(0, len(noise_burst)/self.sample_rate, len(noise_burst)))
        
        return audio
    
    def create_crash_events(self, duration):
        """クラッシュイベント（突然のサイレンスと再起動）を生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        crash_mask = np.ones(len(t))
        
        # 不規則なクラッシュイベント
        crash_times = random.sample(range(int(duration * 10), int(duration * 90), 1000), 8)
        
        for crash_time in crash_times:
            crash_start = int(crash_time * self.sample_rate / 1000)
            crash_duration = random.randint(500, 2000)  # 0.5-2秒のクラッシュ
            
            crash_end = min(crash_start + crash_duration, len(crash_mask))
            crash_mask[crash_start:crash_end] = 0  # サイレンス
            
            # クラッシュ後の「再起動ノイズ」
            if crash_end + 500 < len(crash_mask):
                restart_noise = np.random.normal(0, 0.1, 500)
                crash_mask[crash_end:crash_end+500] = restart_noise
        
        return crash_mask
    
    def create_boundary_violations(self, duration):
        """境界違反による不規則な波形を生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        boundary_audio = np.zeros((len(t), self.channels))
        
        # 境界値付近での不安定な振る舞い
        for i in range(0, len(t), 4410):  # 100msごとに境界チェック
            segment_duration = min(4410, len(t) - i)
            
            # 境界値に近づくほど不安定に
            boundary_factor = (i / len(t)) * 2  # 時間と共に増加
            instability = np.sin(boundary_factor * np.pi)
            
            # 不規則な波形生成
            if random.random() < instability * 0.3:  # 境界違反確率
                # クリップノイズ
                noise = np.random.normal(0, 0.5, segment_duration)
                noise = np.clip(noise, -0.8, 0.8)  # クリップ
                
                for ch in range(self.channels):
                    boundary_audio[i:i+segment_duration, ch] = noise
            else:
                # 通常のサイン波（不安定さを含む）
                freq = 440 + instability * 100 * (random.random() - 0.5)
                normal_wave = np.sin(2 * np.pi * freq * t[i:i+segment_duration])
                
                for ch in range(self.channels):
                    boundary_audio[i:i+segment_duration, ch] = normal_wave * 0.3
        
        return boundary_audio
    
    def create_system_instability(self, duration):
        """システム全体の不安定さを表現"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        instability_audio = np.zeros((len(t), self.channels))
        
        # 時間と共に不安定さが増加
        instability_factor = np.linspace(0.1, 1.0, len(t))
        
        # 低周波の揺らぎ（システムの不安定さ）
        lfo = np.sin(2 * np.pi * 0.5 * t) * instability_factor
        
        # 不規則な変調
        for ch in range(self.channels):
            instability_audio[:, ch] = lfo * 0.2
        
        # 高周波の不安定性（メモリエラーによるノイズ）
        for i in range(0, len(t), 100):
            if instability_factor[i] > 0.7:  # 不安定さが高いほどノイズ増加
                noise = np.random.normal(0, instability_factor[i] * 0.1, 100)
                end_idx = min(i + 100, len(instability_audio))
                instability_audio[i:end_idx, ch] += noise
        
        return instability_audio
    
    def generate_segmentation_fault(self):
        """Segmentation Fault トラックを生成"""
        print("Generating Segmentation Fault track...")
        
        # 各コンポーネントを生成
        memory_positions = self.generate_memory_access_pattern(self.duration)
        segmentation_noise = self.create_segmentation_noise(memory_positions, self.duration)
        crash_events = self.create_crash_events(self.duration)
        boundary_violations = self.create_boundary_violations(self.duration)
        system_instability = self.create_system_instability(self.duration)
        
        # 全ての要素を合成
        final_audio = np.zeros((int(self.sample_rate * self.duration), self.channels))
        
        # 基本構造：境界違反
        final_audio += boundary_violations * 0.4
        
        # セグメンテーションノイズを追加
        final_audio += segmentation_noise * 0.3
        
        # システムの不安定さを追加
        final_audio += system_instability * 0.2
        
        # クラッシュイベントを適用
        for ch in range(self.channels):
            final_audio[:, ch] *= crash_events
        
        # ノーマライズ
        max_val = np.max(np.abs(final_audio))
        if max_val > 0:
            final_audio = final_audio / max_val * 0.8
        
        # ファイル出力
        output_file = "09_segmentation_fault.wav"
        wavfile.write(output_file, self.sample_rate, (final_audio * 32767).astype(np.int16))
        
        print(f"Segmentation Fault track generated: {output_file}")
        
        # 可視化
        self.visualize_segmentation_fault(final_audio, memory_positions, crash_events)
        
        return output_file
    
    def visualize_segmentation_fault(self, audio, memory_positions, crash_events):
        """Segmentation Fault の可視化"""
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        t = np.linspace(0, self.duration, len(audio))
        
        # 1. メモリアクセスパターン
        axes[0].plot(t[:len(memory_positions)], memory_positions, 'r-', alpha=0.7)
        axes[0].set_title('Memory Access Pattern (Irregular Jumps)')
        axes[0].set_ylabel('Memory Position')
        axes[0].grid(True, alpha=0.3)
        
        # 2. 音声波形（左チャンネル）
        axes[1].plot(t, audio[:, 0], 'b-', alpha=0.7)
        axes[1].set_title('Audio Waveform (Left Channel)')
        axes[1].set_ylabel('Amplitude')
        axes[1].grid(True, alpha=0.3)
        
        # 3. クラッシュイベント
        axes[2].plot(t, crash_events, 'r-', linewidth=2)
        axes[2].set_title('Crash Events (Silence Periods)')
        axes[2].set_ylabel('Audio Level')
        axes[2].set_ylim(-0.1, 1.1)
        axes[2].grid(True, alpha=0.3)
        
        # 4. スペクトログラム
        f, t_spec, Sxx = signal.spectrogram(audio[:, 0], self.sample_rate)
        axes[3].pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud', cmap='viridis')
        axes[3].set_title('Spectrogram (Showing "Bursts" and "Crashes")')
        axes[3].set_ylabel('Frequency [Hz]')
        axes[3].set_xlabel('Time [sec]')
        axes[3].set_ylim(0, 5000)
        
        plt.tight_layout()
        plt.savefig('09_segmentation_fault_visualization.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Visualization saved: 09_segmentation_fault_visualization.png")

def main():
    """Segmentation Fault トラック生成のメイン関数"""
    generator = SegmentationFaultGenerator()
    output_file = generator.generate_segmentation_fault()
    
    print(f"\n=== Segmentation Fault Track Generated ===")
    print(f"File: {output_file}")
    print(f"Duration: {generator.duration} seconds")
    print(f"Sample Rate: {generator.sample_rate} Hz")
    print(f"Channels: {generator.channels}")
    print(f"\nConcept: Segmentation Fault - 領域違反の破裂")
    print("This track represents the catastrophic failure when")
    print("a program accesses memory outside its allocated bounds.")
    print("The irregular jumps, crashes, and boundary violations")
    print("create a chaotic yet structured soundscape.")

if __name__ == "__main__":
    main()