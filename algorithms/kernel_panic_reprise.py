#!/usr/bin/env python3
"""
Kernel Panic (Reprise) - 全てが止まる瞬間

このトラックはカーネルパニックを音楽的に表現する。
システム全体の停止を、壮大な終焉として表現。

コンセプト:
- システムの完全停止
- 最後の息
- データの消失
- 暗転

技法:
- 周波数の低下（システムの停止）
- 音量の減衰（電源断）
- 最後のノイズバースト（パニックメッセージ）
- 完全なサイレンス（死）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import random
import math

class KernelPanicGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.duration = 240  # 4分（最長トラック）
        self.channels = 2  # ステレオ
        
    def create_system_shutdown(self, duration):
        """システムの停止プロセスを生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        shutdown_audio = np.zeros((len(t), self.channels))
        
        # システムの停止は指数関数的に進行
        shutdown_curve = np.exp(-t / (duration * 0.3))  # 30%の時間で急速に停止
        
        # 基本周波数の低下（クロック速度の低下）
        base_freq = 60  # 低い周波数から始める
        freq_decay = base_freq * shutdown_curve
        
        for ch in range(self.channels):
            # 基本波形
            waveform = np.sin(2 * np.pi * base_freq * t)
            
            # 周波数モジュレーション（不安定さ）
            modulation = np.sin(2 * np.pi * 0.1 * t) * shutdown_curve
            waveform *= (1 + 0.5 * modulation)
            
            # シャットダウンカーブを適用
            waveform *= shutdown_curve
            
            shutdown_audio[:, ch] = waveform
        
        return shutdown_audio
    
    def create_panic_messages(self, duration):
        """カーネルパニックメッセージの音響化"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        panic_audio = np.zeros((len(t), self.channels))
        
        # パニックメッセージは不規則に現れる
        panic_times = [
            (0.1, 0.15),   # 最初の警告
            (0.2, 0.25),   # エラーメッセージ
            (0.35, 0.4),   # スタックトレース
            (0.5, 0.55),   # 致命的エラー
            (0.7, 0.75),   # 最終メッセージ
        ]
        
        for start_time, end_time in panic_times:
            start_idx = int(start_time * duration * self.sample_rate)
            end_idx = int(end_time * duration * self.sample_rate)
            
            if end_idx > len(panic_audio):
                break
                
            segment_length = end_idx - start_idx
            
            # パニックメッセージのノイズ
            panic_noise = np.random.normal(0, 0.3, segment_length)
            
            # 文字コード的な周波数成分
            for i in range(segment_length):
                char_freq = 1000 + (i % 256) * 10  # 文字コードに基づく周波数
                char_wave = np.sin(2 * np.pi * char_freq * np.linspace(0, segment_length/self.sample_rate, segment_length))
                panic_noise[i] += char_wave[i] * 0.1
            
            # パニックオーディオに追加
            for ch in range(self.channels):
                panic_audio[start_idx:end_idx, ch] = panic_noise
        
        return panic_audio
    
    def create_data_loss(self, duration):
        """データ消失の音響化"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        loss_audio = np.zeros((len(t), self.channels))
        
        # データは断片的に消失
        data_blocks = 1000  # データブロック数
        
        for block in range(data_blocks):
            start_idx = (block * len(t)) // data_blocks
            end_idx = ((block + 1) * len(t)) // data_blocks
            
            # 時間と共に消失確率が増加
            loss_probability = (block / data_blocks) ** 2
            
            if random.random() < loss_probability:
                # このブロックは消失（サイレンス）
                continue
            else:
                # データが残っているブロック
                block_length = end_idx - start_idx
                
                # データの残骸ノイズ
                data_fragment = np.random.normal(0, 0.2, block_length)
                
                # 周波数成分（データの構造）
                data_freq = 200 + (block % 50) * 20
                data_wave = np.sin(2 * np.pi * data_freq * np.linspace(0, block_length/self.sample_rate, block_length))
                
                data_fragment += data_wave * 0.3
                
                for ch in range(self.channels):
                    loss_audio[start_idx:end_idx, ch] = data_fragment
        
        return loss_audio
    
    def create_final_silence(self, duration):
        """最後の完全なサイレンス"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        silence_audio = np.zeros((len(t), self.channels))
        
        # 最後の10%は完全なサイレンス
        silence_start = int(0.9 * len(t))
        
        # その前の段階で音量が急速に減衰
        fade_start = int(0.8 * len(t))
        fade_length = silence_start - fade_start
        
        if fade_length > 0:
            fade_curve = np.linspace(1, 0, fade_length)
            for ch in range(self.channels):
                silence_audio[fade_start:silence_start, ch] = fade_curve
        
        # 最後のガスプ（微かな音）
        last_breath_start = int(0.89 * len(t))
        last_breath_length = int(0.01 * len(t))  # 1%の時間
        
        if last_breath_start + last_breath_length < len(t):
            last_breath = np.random.normal(0, 0.05, last_breath_length)
            for ch in range(self.channels):
                silence_audio[last_breath_start:last_breath_start+last_breath_length, ch] = last_breath
        
        return silence_audio
    
    def create_reprise_elements(self, duration):
        """他のトラックからの要素を再利用（Reprise）"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        reprise_audio = np.zeros((len(t), self.channels))
        
        # 過去のトラックからの要素を薄く再現
        reprise_elements = [
            (0.05, 0.1, "stack_overflow"),      # Stack Overflowの要素
            (0.15, 0.2, "memory_leak"),        # Memory Leakの要素
            (0.25, 0.3, "deadlock"),          # Deadlockの要素
            (0.4, 0.45, "buffer_overflow"),   # Buffer Overflowの要素
        ]
        
        for start_time, end_time, element_type in reprise_elements:
            start_idx = int(start_time * duration * self.sample_rate)
            end_idx = int(end_time * duration * self.sample_rate)
            
            if end_idx > len(reprise_audio):
                break
                
            segment_length = end_idx - start_idx
            
            # 各要素の特性を再現
            if element_type == "stack_overflow":
                # スタックオーバーフロー：高周波の積層
                for layer in range(5):
                    layer_freq = 440 * (layer + 1)
                    layer_wave = np.sin(2 * np.pi * layer_freq * np.linspace(0, segment_length/self.sample_rate, segment_length))
                    reprise_audio[start_idx:end_idx, :] += layer_wave * 0.05
                    
            elif element_type == "memory_leak":
                # メモリリーク：重なる低音
                leak_wave = np.sin(2 * np.pi * 80 * np.linspace(0, segment_length/self.sample_rate, segment_length))
                reprise_audio[start_idx:end_idx, :] += leak_wave * 0.1
                
            elif element_type == "deadlock":
                # デッドロック：位相のずれ
                wave1 = np.sin(2 * np.pi * 220 * np.linspace(0, segment_length/self.sample_rate, segment_length))
                wave2 = np.sin(2 * np.pi * 330 * np.linspace(0, segment_length/self.sample_rate, segment_length) + np.pi/4)
                reprise_audio[start_idx:end_idx, :] += (wave1 + wave2) * 0.05
                
            elif element_type == "buffer_overflow":
                # バッファオーバーフロー：ノイズバースト
                noise = np.random.normal(0, 0.1, segment_length)
                reprise_audio[start_idx:end_idx, :] += noise
        
        return reprise_audio
    
    def generate_kernel_panic(self):
        """Kernel Panic (Reprise) トラックを生成"""
        print("Generating Kernel Panic (Reprise) track...")
        
        # 各コンポーネントを生成
        system_shutdown = self.create_system_shutdown(self.duration)
        panic_messages = self.create_panic_messages(self.duration)
        data_loss = self.create_data_loss(self.duration)
        final_silence = self.create_final_silence(self.duration)
        reprise_elements = self.create_reprise_elements(self.duration)
        
        # 全ての要素を合成
        final_audio = np.zeros((int(self.sample_rate * self.duration), self.channels))
        
        # 基本構造：システム停止
        final_audio += system_shutdown * 0.4
        
        # パニックメッセージを追加
        final_audio += panic_messages * 0.3
        
        # データ消失を追加
        final_audio += data_loss * 0.2
        
        # Reprise要素を追加
        final_audio += reprise_elements * 0.1
        
        # ファイナルサイレンスを適用
        final_audio *= final_silence
        
        # ノーマライズ
        max_val = np.max(np.abs(final_audio))
        if max_val > 0:
            final_audio = final_audio / max_val * 0.8
        
        # ファイル出力
        output_file = "10_kernel_panic_reprise.wav"
        wavfile.write(output_file, self.sample_rate, (final_audio * 32767).astype(np.int16))
        
        print(f"Kernel Panic (Reprise) track generated: {output_file}")
        
        # 可視化
        self.visualize_kernel_panic(final_audio, system_shutdown, panic_messages, data_loss)
        
        return output_file
    
    def visualize_kernel_panic(self, audio, shutdown, panic, loss):
        """Kernel Panic の可視化"""
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        t = np.linspace(0, self.duration, len(audio))
        
        # 1. システムシャットダウンカーブ
        axes[0].plot(t, shutdown[:, 0], 'r-', alpha=0.7, label='System Shutdown')
        axes[0].set_title('System Shutdown Curve (Exponential Decay)')
        axes[0].set_ylabel('Amplitude')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 2. パニックメッセージ
        axes[1].plot(t, panic[:, 0], 'orange', alpha=0.7, label='Panic Messages')
        axes[1].set_title('Kernel Panic Messages (Error Bursts)')
        axes[1].set_ylabel('Amplitude')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # 3. データ消失
        axes[2].plot(t, loss[:, 0], 'purple', alpha=0.7, label='Data Loss')
        axes[2].set_title('Data Loss (Fragmented Structure)')
        axes[2].set_ylabel('Amplitude')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # 4. 最終波形とスペクトログラム
        axes[3].plot(t, audio[:, 0], 'b-', alpha=0.7, label='Final Audio')
        axes[3].set_title('Final Audio - The Complete Shutdown')
        axes[3].set_ylabel('Amplitude')
        axes[3].set_xlabel('Time [sec]')
        axes[3].legend()
        axes[3].grid(True, alpha=0.3)
        
        # 最後の10%を強調（完全サイレンス）
        final_10_percent = int(0.9 * len(t))
        axes[3].axvline(x=t[final_10_percent], color='red', linestyle='--', alpha=0.7, label='Final Silence')
        axes[3].legend()
        
        plt.tight_layout()
        plt.savefig('10_kernel_panic_reprise_visualization.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Visualization saved: 10_kernel_panic_reprise_visualization.png")

def main():
    """Kernel Panic (Reprise) トラック生成のメイン関数"""
    generator = KernelPanicGenerator()
    output_file = generator.generate_kernel_panic()
    
    print(f"\n=== Kernel Panic (Reprise) Track Generated ===")
    print(f"File: {output_file}")
    print(f"Duration: {generator.duration} seconds")
    print(f"Sample Rate: {generator.sample_rate} Hz")
    print(f"Channels: {generator.channels}")
    print(f"\nConcept: Kernel Panic (Reprise) - 全てが止まる瞬間")
    print("This is the final track of the Error Garden album.")
    print("It represents the complete system shutdown,")
    print("incorporating elements from previous tracks as a reprise.")
    print("The gradual decay leads to ultimate silence - the end.")

if __name__ == "__main__":
    main()