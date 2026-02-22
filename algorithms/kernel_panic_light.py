#!/usr/bin/env python3
"""
Kernel Panic (Reprise) - 簡易版

軽量バージョン：システム停止の基本構造に集中
"""

import numpy as np
from scipy.io import wavfile
import math

def generate_kernel_panic_light():
    sample_rate = 44100
    duration = 180  # 3分に短縮
    channels = 2
    
    print("Generating Kernel Panic (Reprise) - Light version...")
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros((len(t), channels))
    
    # 1. システム停止カーブ（指数関数的減衰）
    shutdown_curve = np.exp(-t / (duration * 0.4))
    
    # 2. 基本周波数の低下
    base_freq = 60
    freq_decay = base_freq * shutdown_curve
    
    # 3. 基本波形生成
    for ch in range(channels):
        # 低周波の基本波
        waveform = np.sin(2 * np.pi * base_freq * t)
        
        # 周波数モジュレーション
        modulation = np.sin(2 * np.pi * 0.1 * t) * 0.3
        waveform *= (1 + modulation)
        
        # シャットダウンカーブ適用
        waveform *= shutdown_curve
        
        # パニックメッセージ（不規則なノイズ）
        for i in range(0, len(t), 22050):  # 0.5秒ごと
            if i + 1000 < len(t):
                # ノイズバースト
                noise = np.random.normal(0, 0.2, 1000)
                waveform[i:i+1000] += noise * shutdown_curve[i]
        
        audio[:, ch] = waveform
    
    # 4. ノーマライズ
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8
    
    # 5. ファイル出力
    output_file = "../samples/10_kernel_panic_reprise.wav"
    wavfile.write(output_file, sample_rate, (audio * 32767).astype(np.int16))
    
    print(f"Kernel Panic (Reprise) track generated: {output_file}")
    return output_file

if __name__ == "__main__":
    generate_kernel_panic_light()