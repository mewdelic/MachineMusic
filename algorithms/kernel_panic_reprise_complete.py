#!/usr/bin/env python3
"""
Kernel Panic (Reprise) - 完全版

システム停止の全ての段階を表現する作品
1. 初期検出 (0:00-0:30)
2. パニック開始 (0:30-1:00)
3. カーネルスタックトレース (1:00-1:30)
4. メモリダンプ (1:30-2:00)
5. 完全停止 (2:00-3:00)
"""

import numpy as np
from scipy.io import wavfile
import math
import random

def generate_kernel_panic_reprise():
    sample_rate = 44100
    duration = 300  # 5分
    channels = 2
    
    print("Generating Kernel Panic (Reprise) - Complete version...")
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros((len(t), channels))
    
    # 1. 初期検出セクション (0:00-0:30)
    section1_end = int(30 * sample_rate)
    t1 = t[:section1_end]
    
    # 警告音の繰り返し
    warning_freq = 440  # A4
    for ch in range(channels):
        # 規則的な警告音
        warning_signal = np.sin(2 * np.pi * warning_freq * t1)
        
        # 2秒ごとに警告パルス
        for i in range(0, len(t1), int(2 * sample_rate)):
            if i + int(0.1 * sample_rate) < len(t1):
                pulse = 0.3 * np.sin(2 * np.pi * warning_freq * 2 * t1[i:i+int(0.1 * sample_rate)])
                warning_signal[i:i+int(0.1 * sample_rate)] += pulse
        
        audio[:section1_end, ch] = warning_signal * 0.5
    
    # 2. パニック開始セクション (0:30-1:00)
    section2_start = section1_end
    section2_end = int(60 * sample_rate)
    t2 = t[section2_start:section2_end]
    
    # 周波数の不安定化
    panic_freqs = [440, 523, 659, 784, 880]  # A4, C5, E5, G5, A5
    
    for ch in range(channels):
        panic_signal = np.zeros(len(t2))
        
        # 不規則な周波数変化
        for i, time_point in enumerate(t2):
            if i % int(0.1 * sample_rate) == 0:  # 0.1秒ごとに周波数変更
                freq = random.choice(panic_freqs)
            
            local_t = t2[i] % (1.0 / freq)
            panic_signal[i] = 0.3 * np.sin(2 * np.pi * freq * local_t)
        
        # ノイズの混入
        noise_level = 0.1
        panic_signal += np.random.normal(0, noise_level, len(t2))
        
        audio[section2_start:section2_end, ch] = panic_signal
    
    # 3. カーネルスタックトレースセクション (1:00-1:30)
    section3_start = section2_end
    section3_end = int(90 * sample_rate)
    t3 = t[section3_start:section3_end]
    
    # スタックトレースのリズミカルな表現
    stack_rhythm = [0.2, 0.1, 0.3, 0.1, 0.2, 0.1]  # リズムパターン
    
    for ch in range(channels):
        stack_signal = np.zeros(len(t3))
        
        # リズミカルな要素
        position = 0
        rhythm_index = 0
        
        while position < len(t3):
            duration_beat = int(stack_rhythm[rhythm_index % len(stack_rhythm)] * sample_rate)
            if position + duration_beat < len(t3):
                # ビート音
                beat_freq = 200 + rhythm_index * 50
                beat_t = np.linspace(0, stack_rhythm[rhythm_index % len(stack_rhythm)], duration_beat)
                beat_signal = 0.4 * np.sin(2 * np.pi * beat_freq * beat_t)
                beat_signal *= np.exp(-beat_t * 3)  # 減衰
                
                stack_signal[position:position + duration_beat] = beat_signal
            
            position += duration_beat
            rhythm_index += 1
        
        # 高周波の「文字」音
        for i in range(0, len(t3), int(0.05 * sample_rate)):
            if i + 200 < len(t3):
                char_freq = random.uniform(2000, 4000)
                char_signal = 0.1 * np.sin(2 * np.pi * char_freq * np.linspace(0, 0.005, 200))
                stack_signal[i:i+200] += char_signal
        
        audio[section3_start:section3_end, ch] = stack_signal
    
    # 4. メモリダンプセクション (1:30-2:00)
    section4_start = section3_end
    section4_end = int(120 * sample_rate)
    t4 = t[section4_start:section4_end]
    
    # メモリダンプのノイズ表現
    for ch in range(channels):
        # ベースノイズ
        base_noise = np.random.normal(0, 0.2, len(t4))
        
        # 周期的な「ダンプ」音
        dump_period = int(0.5 * sample_rate)  # 0.5秒ごと
        for i in range(0, len(t4), dump_period):
            if i + int(0.1 * sample_rate) < len(t4):
                dump_noise = np.random.normal(0, 0.5, int(0.1 * sample_rate))
                base_noise[i:i+int(0.1 * sample_rate)] += dump_noise
        
        # 低周波の「ダンプ」リズム
        dump_rhythm = 0.1 * np.sin(2 * np.pi * 2 * t4)  # 2Hzのリズム
        base_noise += dump_rhythm
        
        audio[section4_start:section4_end, ch] = base_noise
    
    # 5. 完全停止セクション (2:00-3:00)
    section5_start = section4_end
    t5 = t[section5_start:]
    
    # 指数関数的減衰
    shutdown_curve = np.exp(-t5 / (duration * 0.3))
    
    for ch in range(channels):
        # 最後の「ビープ」音
        final_beep = np.zeros(len(t5))
        
        # 10秒ごとにビープ
        for i in range(0, len(t5), int(10 * sample_rate)):
            if i + int(0.5 * sample_rate) < len(t5):
                beep_freq = 1000  # 高いビープ音
                beep_t = np.linspace(0, 0.5, int(0.5 * sample_rate))
                beep_signal = 0.6 * np.sin(2 * np.pi * beep_freq * beep_t)
                beep_signal *= shutdown_curve[i:i+int(0.5 * sample_rate)]
                final_beep[i:i+int(0.5 * sample_rate)] = beep_signal
        
        # 最後のノイズ
        final_noise = np.random.normal(0, 0.1, len(t5))
        final_noise *= shutdown_curve * 0.5
        
        final_beep += final_noise
        
        audio[section5_start:, ch] = final_beep
    
    # 全体的な処理
    # 1. ノーマライズ
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.7
    
    # 2. フェードイン・フェードアウト
    fade_duration = int(2 * sample_rate)  # 2秒
    
    # フェードイン
    for i in range(fade_duration):
        fade_factor = i / fade_duration
        audio[i, :] *= fade_factor
    
    # フェードアウト
    for i in range(len(t) - fade_duration, len(t)):
        fade_factor = (len(t) - i) / fade_duration
        audio[i, :] *= fade_factor
    
    # 3. ファイル出力
    output_file = "../samples/10_kernel_panic_reprise_complete.wav"
    wavfile.write(output_file, sample_rate, (audio * 32767).astype(np.int16))
    
    print(f"Kernel Panic (Reprise) Complete track generated: {output_file}")
    print("Track structure:")
    print("- 0:00-0:30: Initial Detection")
    print("- 0:30-1:00: Panic Beginning")
    print("- 1:00-1:30: Kernel Stack Trace")
    print("- 1:30-2:00: Memory Dump")
    print("- 2:00-3:00: Complete Shutdown")
    
    return output_file

if __name__ == "__main__":
    generate_kernel_panic_reprise()