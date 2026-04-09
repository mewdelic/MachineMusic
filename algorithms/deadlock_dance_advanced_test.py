#!/usr/bin/env python3
"""
Deadlock Dance Advanced Test - 短いテストバージョン
"""

import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import soundfile as sf

def main():
    print("Testing Deadlock Dance Advanced...")
    
    # 基本パラメータ
    duration = 10  # 10秒のテスト
    sample_rate = 44100
    samples = int(duration * sample_rate)
    time = np.linspace(0, duration, samples)
    
    # シンプルなデッドロック音響生成
    output = np.zeros((samples, 2))  # ステレオ
    
    # 4つのスレッドを表す4つの周波数
    frequencies = [220, 330, 440, 550]  # A3, E4, A4, C#5
    
    for i, freq in enumerate(frequencies):
        # 各スレッドの音
        thread_signal = np.sin(2 * np.pi * freq * time) * 0.1
        
        # パンニング
        pan = (i - 1.5) / 1.5
        left_gain = np.sqrt((1.0 - pan) / 2.0)
        right_gain = np.sqrt((1.0 + pan) / 2.0)
        
        output[:, 0] += thread_signal * left_gain
        output[:, 1] += thread_signal * right_gain
    
    # デッドロック検出パターン（シンプル）
    detection = np.sin(2 * np.pi * 0.5 * time)  # 0.5Hzのゆっくりした変化
    detection = (detection + 1) / 2  # 0-1に正規化
    
    output *= (1 + 0.3 * detection.reshape(-1, 1))
    
    # ノーマライズ
    max_val = np.max(np.abs(output))
    if max_val > 0:
        output = output / max_val * 0.8
    
    # 保存
    sf.write("07_deadlock_dance_advanced_test.wav", output, sample_rate)
    print("Test audio saved: 07_deadlock_dance_advanced_test.wav")
    
    # ビジュアライズ
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.plot(time, output[:, 0], 'r-', label='Left Channel')
    plt.plot(time, output[:, 1], 'b-', label='Right Channel')
    plt.title('Deadlock Dance Advanced Test - Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(3, 1, 2)
    f, t, Sxx = scipy.signal.spectrogram(output[:, 0], sample_rate, nperseg=1024)
    plt.pcolormesh(t, f/1000, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
    plt.title('Spectrogram')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (kHz)')
    
    plt.subplot(3, 1, 3)
    plt.plot(time, detection, 'g-', linewidth=2)
    plt.title('Deadlock Detection Pattern')
    plt.xlabel('Time (s)')
    plt.ylabel('Detection Level')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("07_deadlock_dance_advanced_test_visualization.png", dpi=300)
    print("Test visualization saved: 07_deadlock_dance_advanced_test_visualization.png")
    
    print("Test completed successfully!")

if __name__ == "__main__":
    main()