#!/usr/bin/env python3
"""
Deadlock Dance Advanced - テストバージョン
"""

import numpy as np
from scipy.io import wavfile
import soundfile as sf
import matplotlib.pyplot as plt

def test_deadlock_dance_advanced():
    """テスト用の短いバージョン"""
    print("=== Deadlock Dance Advanced テスト開始 ===")
    
    # 基本パラメータ
    sample_rate = 44100
    duration = 10  # 10秒のテスト
    time = np.linspace(0, duration, int(sample_rate * duration))
    
    # 簡単なデッドロック信号生成
    # 2つのプロセスが互いに待機する様子を表現
    process1 = np.sin(2 * np.pi * 60 * time)  # 60Hz
    process2 = np.sin(2 * np.pi * 90 * time)  # 90Hz
    
    # 相互干渉（デッドロックの結合）
    coupling = 0.3
    interference1 = process1 + coupling * process2
    interference2 = process2 + coupling * process1
    
    # ステレオ信号
    left_channel = interference1
    right_channel = interference2
    stereo_signal = np.column_stack([left_channel, right_channel])
    
    # 正規化
    stereo_signal = stereo_signal / np.max(np.abs(stereo_signal)) * 0.8
    
    # 音声ファイルの保存
    output_file = "07_deadlock_dance_advanced_test.wav"
    sf.write(output_file, stereo_signal, sample_rate)
    
    print(f"テスト音声ファイルを保存: {output_file}")
    
    # 簡単な可視化
    plt.figure(figsize=(10, 6))
    plt.plot(time[:1000], process1[:1000], label='Process 1', alpha=0.7)
    plt.plot(time[:1000], process2[:1000], label='Process 2', alpha=0.7)
    plt.title('Deadlock Dance Advanced - Test Visualization')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('deadlock_dance_advanced_test.png', dpi=150)
    plt.close()
    
    print("テスト可視化を保存: deadlock_dance_advanced_test.png")
    print("=== テスト完了 ===")

if __name__ == "__main__":
    test_deadlock_dance_advanced()