#!/usr/bin/env python3
"""
Deadlock Dance Advanced Test - 簡易版テスト
"""

import numpy as np
import scipy.signal
import soundfile as sf
import matplotlib.pyplot as plt

def test_deadlock_dance():
    """簡易版デッドロックダンスの生成"""
    print("Starting Deadlock Dance Advanced Test...")
    
    # 基本パラメータ
    sample_rate = 44100
    duration = 30  # 30秒テスト
    num_samples = int(duration * sample_rate)
    
    # 時間軸
    time_array = np.linspace(0, duration, num_samples)
    
    # プロセス数
    num_processes = 4
    
    # 基本周波数
    base_freqs = [110.0, 165.0, 220.0, 330.0]
    
    print(f"Generating {num_processes} processes...")
    
    # 各プロセスの信号生成
    signals = []
    for i in range(num_processes):
        # 基本信号
        signal = np.sin(2 * np.pi * base_freqs[i] * time_array)
        
        # デッドロックパターン（矩形波による変調）
        cycle_period = 2.0 + i * 0.5
        pattern = scipy.signal.square(2 * np.pi * time_array / cycle_period, duty=0.3)
        
        # 強度の時間変化
        intensity = 1.0 + 0.5 * (time_array / duration) ** 2
        
        # パターンの適用
        signal = signal * pattern * intensity
        
        signals.append(signal)
    
    print("Mixing signals...")
    
    # 信号のミックス
    mixed_signal = np.sum(signals, axis=0)
    
    # エンベロープ
    envelope = np.ones_like(time_array)
    
    # 構造的エンベロープ
    # 導入部
    intro_end = int(0.2 * num_samples)
    envelope[:intro_end] = np.linspace(0, 1, intro_end)
    
    # 終結部
    outro_start = int(0.8 * num_samples)
    envelope[outro_start:] = np.linspace(1, 0, num_samples - outro_start)
    
    # エンベロープ適用
    mixed_signal = mixed_signal * envelope
    
    # ステレオ化
    stereo_signal = np.zeros((2, num_samples))
    
    # 簡単なパンニング
    for i, signal in enumerate(signals):
        pan_pos = i / (num_processes - 1)  # 0 to 1
        left_gain = np.sqrt(1 - pan_pos)
        right_gain = np.sqrt(pan_pos)
        
        stereo_signal[0] += signal * left_gain
        stereo_signal[1] += signal * right_gain
    
    # ミックス信号も追加
    stereo_signal[0] += mixed_signal * 0.5
    stereo_signal[1] += mixed_signal * 0.5
    
    # 正規化
    stereo_signal = stereo_signal / np.max(np.abs(stereo_signal) + 1e-10)
    
    print("Creating visualization...")
    
    # 可視化
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    
    # 波形
    axes[0].plot(time_array[:1000], stereo_signal[0, :1000], 'b-', alpha=0.7)
    axes[0].plot(time_array[:1000], stereo_signal[1, :1000], 'r-', alpha=0.7)
    axes[0].set_ylabel('Amplitude')
    axes[0].set_title('Deadlock Dance Advanced Test - Waveform')
    axes[0].legend(['Left', 'Right'])
    axes[0].grid(True, alpha=0.3)
    
    # スペクトログラム
    f, t, Sxx = scipy.signal.spectrogram(stereo_signal[0], sample_rate, 
                                        nperseg=1024, noverlap=512)
    im = axes[1].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
    axes[1].set_ylabel('Frequency [Hz]')
    axes[1].set_xlabel('Time [s]')
    axes[1].set_title('Spectrogram')
    plt.colorbar(im, ax=axes[1], label='Power [dB]')
    
    plt.tight_layout()
    
    # 保存
    print("Saving files...")
    
    # 音声ファイル
    sf.write('samples/07_deadlock_dance_advanced_test.wav', 
             stereo_signal.T, sample_rate)
    print("Audio saved to: samples/07_deadlock_dance_advanced_test.wav")
    
    # 可視化
    fig.savefig('samples/07_deadlock_dance_advanced_test_visualization.png', 
                dpi=150, bbox_inches='tight')
    print("Visualization saved to: samples/07_deadlock_dance_advanced_test_visualization.png")
    
    print("Test completed successfully!")
    
    return True

if __name__ == "__main__":
    test_deadlock_dance()