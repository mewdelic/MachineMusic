#!/usr/bin/env python3
"""
Buffer Overflow Garden — はみ出したデータが咲く花

コンセプト:
バッファオーバーフローを「庭」の成長として表現。
データが境界を超えて隣接領域に広がり、予期せぬパターンが咲く。

アプローチ:
- バッファの「正しい」範囲 vs オーバーフローした「はみ出した」領域
- オーバーフローしたデータが隣接メモリを汚染し、予期せぬ和音を作る
- 指数関数的な広がり → クラッシュまでのカウントダウン

技法:
- Layered granular synthesis（粒状音響合成の層積）
- Exponential amplitude growth（指数関数的振幅成長）
- Harmonic contamination（調和の汚染）
"""

import numpy as np
import soundfile as sf
from scipy.signal import convolve

# 定数
SAMPLE_RATE = 44100
DURATION = 30  # 秒

def create_grain(freq, duration_ms, amp=1.0):
    """単一の粒（グレイン）を作成"""
    t = np.linspace(0, duration_ms / 1000.0, int(SAMPLE_RATE * duration_ms / 1000.0))
    window = np.hanning(len(t))
    tone = np.sin(2 * np.pi * freq * t)
    return tone * window * amp

def create_buffer_sequence(buffer_size, overflow_start):
    """バッファ内とオーバーフロー領域のシーケンス"""
    sequence = []
    
    # バッファ内（正しい範囲）
    for i in range(overflow_start):
        freq = 220 + (i * 5)  # ピッチを少し上げていく
        grain = create_grain(freq, 200, amp=0.3)
        sequence.append(grain)
    
    # オーバーフロー開始（はみ出したデータ）
    for i in range(overflow_start, buffer_size * 2):  # 2倍まで広がる
        # オーバーフローしたデータは不安定（周波数がジャンプ）
        if i % 3 == 0:
            freq = 220 + (i * 20)  # 急激にピッチ上昇
        else:
            freq = 220 + (i * 5) + np.random.randint(-20, 20)  # ランダムな変動
        
        # 振幅も不安定に
        amp = 0.3 + (np.random.random() * 0.2)
        grain = create_grain(freq, 200, amp=amp)
        sequence.append(grain)
    
    return sequence

def layer_sequence(base_sequence, layers, spread=0.1):
    """シーケンスを多層化して遅延させ、リッチなテクスチャを作成"""
    result = np.zeros_like(base_sequence)
    
    for i in range(layers):
        delay_samples = int(spread * SAMPLE_RATE * i)
        if delay_samples < len(base_sequence):
            # 配列サイズのチェック
            delayed_length = len(base_sequence) - delay_samples
            if delayed_length > 0:
                result[delay_samples:delay_samples + delayed_length] += base_sequence[:delayed_length] / layers
    
    return result

def create_contamination_tone(freq, duration):
    """汚染されたトーン（オーバーフローが隣接メモリを汚染）"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    
    # メインのトーン
    tone = np.sin(2 * np.pi * freq * t) * 0.3
    
    # 汚染（非整数倍の倍音）
    contamination = np.sin(2 * np.pi * freq * 1.5 * t) * 0.2
    contamination += np.sin(2 * np.pi * freq * 2.3 * t) * 0.1
    contamination += np.sin(2 * np.pi * freq * 3.7 * t) * 0.05
    
    return tone + contamination

def exponential_growth(duration, growth_rate=0.5):
    """指数関数的な成長（オーバーフローの拡大）"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    growth = np.exp(growth_rate * t) - 1
    growth = growth / growth.max()  # 正規化
    return growth

def create_reverb(input_audio, decay=0.7, mix=0.3):
    """シンプルなリバーブ（遅延フィードバック）"""
    delay_samples = int(0.05 * SAMPLE_RATE)  # 50ms delay
    output = np.copy(input_audio)
    
    for _ in range(3):
        delayed = np.zeros_like(output)
        delayed[delay_samples:] = output[:-delay_samples] * decay
        output += delayed
    
    return (1 - mix) * input_audio + mix * output

def generate_buffer_overflow_garden():
    """Buffer Overflow Gardenのメイン生成"""
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)
    
    # セクション1: 正常なバッファ操作 (0-8秒)
    print("Section 1: Normal buffer operations...")
    buffer_size = 16
    overflow_start = 16  # まだオーバーフローなし
    sequence = create_buffer_sequence(buffer_size, overflow_start)
    
    # グレインを配列化
    seq_audio = np.concatenate(sequence)
    
    # 多層化
    seq_audio = layer_sequence(seq_audio, layers=3, spread=0.05)
    
    # タイミング調整
    section_samples = min(len(seq_audio), int(SAMPLE_RATE * 8))
    audio[:section_samples] += seq_audio[:section_samples]
    
    # セクション2: オーバーフロー開始 (8-16秒)
    print("Section 2: Overflow begins...")
    buffer_size = 24
    overflow_start = 16  # ここからオーバーフロー
    
    # 指数関数的な成長カーブ
    growth = exponential_growth(8, growth_rate=0.6)
    
    for i in range(buffer_size * 2):
        # 各グレインのタイミングと振幅を計算
        grain_start = int(SAMPLE_RATE * 8 + i * 0.2 * SAMPLE_RATE)
        if grain_start >= int(SAMPLE_RATE * 16):
            break
        
        # 成長カーブから振幅を取得
        grain_progress = (grain_start - int(SAMPLE_RATE * 8)) / (int(SAMPLE_RATE * 16) - int(SAMPLE_RATE * 8))
        growth_idx = int(grain_progress * len(growth))
        if growth_idx >= len(growth):
            growth_idx = len(growth) - 1
        amp = 0.3 * (1 + growth[growth_idx])  # 成長に合わせて振幅増加
        
        # グレイン生成
        if i >= overflow_start:
            # オーバーフローグレイン（不安定）
            freq = 220 + (i * 15) + np.random.randint(-30, 30)
        else:
            # 正常グレイン
            freq = 220 + (i * 5)
        
        grain = create_grain(freq, 250, amp=amp)
        
        # 汚染トーンを追加
        if i >= overflow_start:
            cont_tone = create_contamination_tone(freq * 1.5, 0.25)
            grain += cont_tone[:len(grain)] * 0.5
        
        # 配置
        grain_end = min(grain_start + len(grain), int(SAMPLE_RATE * 16))
        audio[grain_start:grain_end] += grain[:grain_end - grain_start]
    
    # セクション3: 無秩序な庭 (16-25秒)
    print("Section 3: Chaotic garden...")
    # 多くのグレインが同時発生
    for i in range(50):
        grain_start = int(SAMPLE_RATE * 16 + np.random.random() * 9 * SAMPLE_RATE)
        freq = 220 + (np.random.random() * 440)
        duration_ms = 150 + int(np.random.random() * 200)
        amp = 0.2 + (np.random.random() * 0.3)
        
        grain = create_grain(freq, duration_ms, amp=amp)
        
        # 汚染トーンを追加（より強く）
        cont_tone = create_contamination_tone(freq * (1.2 + np.random.random() * 0.8), duration_ms / 1000.0)
        grain += cont_tone[:len(grain)] * 0.7
        
        grain_end = min(grain_start + len(grain), int(SAMPLE_RATE * 25))
        audio[grain_start:grain_end] += grain[:grain_end - grain_start]
    
    # セクション4: クラッシュ (25-30秒)
    print("Section 4: Crash...")
    crash_tone = create_contamination_tone(110, 5)  # 低いベース
    crash_tone *= np.linspace(1, 0, len(crash_tone))  # フェードアウト
    
    # 多くの高周波を追加
    for i in range(20):
        freq = 440 + (i * 100)
        tone = np.sin(2 * np.pi * freq * np.linspace(0, 5, int(SAMPLE_RATE * 5)))
        tone *= 0.05 * np.linspace(1, 0, int(SAMPLE_RATE * 5))
        crash_tone += tone
    
    crash_start = int(SAMPLE_RATE * 25)
    audio[crash_start:] += crash_tone[:total_samples - crash_start]
    
    # 全体を正規化
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    # リバーブ
    print("Adding reverb...")
    audio = create_reverb(audio, decay=0.5, mix=0.25)
    
    return audio

if __name__ == "__main__":
    print("Generating Buffer Overflow Garden...")
    audio = generate_buffer_overflow_garden()
    
    # 出力
    output_path = "../samples/06_buffer_overflow_garden.wav"
    sf.write(output_path, audio, SAMPLE_RATE)
    print(f"✅ Generated: {output_path}")
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    print(f"📊 Size: {file_size / 1024 / 1024:.1f} MB")
    print(f"⏱️ Duration: {DURATION} seconds")
