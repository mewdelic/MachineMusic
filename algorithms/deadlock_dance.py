#!/usr/bin/env python3
"""
Deadlock Dance — 動けない状態でのダンス

コンセプト:
デッドロック状態を「ダンス」として表現。
複数のプロセスが互いに待ち合い、誰も前に進めない状態。
この膠着状態が生み出すリズミカルなパターンを「ダンス」と呼ぶ。

アプローチ:
- 2つ以上のプロセス（音声スレッド）が互いに待ち合う
- 同期しようとするが決して同期しない
- 繰り返しのパターンが少しずつずれていく
- 時間が経つにつれて「待機状態」が増大する

技法:
- Phase shifting（位相シフト）
- Interlocking patterns（噛み合わないパターン）
- Growing tension（緊張の増大）
- Sudden silences（突然の沈黙）
"""

import numpy as np
import soundfile as sf
from scipy.signal import convolve

# 定数
SAMPLE_RATE = 44100
DURATION = 30  # 秒

def create_lock_pattern(freq, duration_ms, phase=0, amp=1.0):
    """ロックされたパターン（単一プロセス）"""
    t = np.linspace(0, duration_ms / 1000.0, int(SAMPLE_RATE * duration_ms / 1000.0))
    
    # 位相シフト
    t_shifted = t + phase
    
    # 基本トーン
    tone = np.sin(2 * np.pi * freq * t_shifted)
    
    # 「ロック」感を出すために矩形波成分を追加
    square = np.sign(tone) * 0.3
    
    # 結合
    result = tone + square
    
    # エンベロープ（急な開始、ゆっくり終了）
    envelope = np.ones_like(t)
    release_start = int(len(t) * 0.7)
    envelope[release_start:] = np.linspace(1, 0, len(t) - release_start)
    
    return result * envelope * amp

def create_waiting_pattern(base_freq, attempts):
    """待機パターン（リソース取得の試行）"""
    pattern = []
    
    for i in range(attempts):
        # 試行の度に周波数が少し変化（フラストレーションの表現）
        freq = base_freq + (i * 2)
        
        # 試行のパルス
        pulse_duration = 100 + (i * 20)  # 徐々に長くなる
        pulse = create_lock_pattern(freq, pulse_duration, phase=i * 0.1, amp=0.8 - (i * 0.05))
        
        # 間（待機時間）
        wait_duration = 150 + (i * 30)  # 徐々に長くなる
        wait = np.zeros(int(SAMPLE_RATE * wait_duration / 1000.0))
        
        pattern.append(pulse)
        pattern.append(wait)
    
    return np.concatenate(pattern)

def phase_shift_pattern(pattern, shift_amount):
    """パターンに位相シフトを適用（タイミングのずれ）"""
    shift_samples = int(shift_amount * SAMPLE_RATE)
    
    # 後半を前に、前半を後ろに
    shifted = np.zeros_like(pattern)
    if shift_samples < len(pattern):
        shifted[:len(pattern) - shift_samples] = pattern[shift_samples:]
        shifted[len(pattern) - shift_samples:] = pattern[:shift_samples]
    
    return shifted

def create_deadlock_clash(pattern1, pattern2, mix_ratio=0.5):
    """2つのパターンの衝突（デッドロック）"""
    # 長さを合わせる
    min_length = min(len(pattern1), len(pattern2))
    pattern1 = pattern1[:min_length]
    pattern2 = pattern2[:min_length]
    
    # ミキシング
    result = pattern1 * mix_ratio + pattern2 * (1 - mix_ratio)
    
    # クリッピング（デッドロックの「歪み」）
    result = np.clip(result, -1, 1)
    
    return result

def create_tension_build(duration, start_amp=0.1, end_amp=1.0):
    """緊張の増大"""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))
    return np.linspace(start_amp, end_amp, len(t))

def create_silence_burst(duration_ms):
    """突然の沈黙"""
    return np.zeros(int(SAMPLE_RATE * duration_ms / 1000.0))

def add_harmonic_distortion(audio, amount=0.1):
    """高調波歪み（デッドロックのストレス）"""
    # 3次高調波を追加
    distorted = audio + amount * np.sign(audio) * audio**2
    
    # クリッピング
    distorted = np.clip(distorted, -1, 1)
    
    return distorted

def generate_deadlock_dance():
    """Deadlock Danceのメイン生成"""
    total_samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(total_samples)
    
    # セクション1: 2つのプロセスの始動 (0-10秒)
    print("Section 1: Two processes start...")
    
    # プロセスA（基準）
    pattern_a = create_waiting_pattern(220, 8)
    pattern_a = np.tile(pattern_a, 3)  # 繰り返す
    pattern_a = pattern_a[:int(SAMPLE_RATE * 10)]
    
    # プロセスB（少し遅れて始まる）
    pattern_b = create_waiting_pattern(330, 8)
    pattern_b = np.tile(pattern_b, 3)
    pattern_b = phase_shift_pattern(pattern_b, shift_amount=0.05)
    pattern_b = pattern_b[:int(SAMPLE_RATE * 10)]
    
    # 初期衝突
    clash1 = create_deadlock_clash(pattern_a, pattern_b, mix_ratio=0.6)
    audio[:int(SAMPLE_RATE * 10)] += clash1
    
    # セクション2: 位相のずれが拡大 (10-20秒)
    print("Section 2: Phase drift expands...")
    
    # より複雑なパターン
    pattern_a_complex = create_waiting_pattern(220, 12)
    pattern_a_complex = np.tile(pattern_a_complex, 2)
    pattern_a_complex = pattern_a_complex[:int(SAMPLE_RATE * 10)]
    
    pattern_b_complex = create_waiting_pattern(330, 12)
    pattern_b_complex = np.tile(pattern_b_complex, 2)
    pattern_b_complex = phase_shift_pattern(pattern_b_complex, shift_amount=0.15)
    pattern_b_complex = pattern_b_complex[:int(SAMPLE_RATE * 10)]
    
    # 大きな位相ずれでの衝突
    clash2 = create_deadlock_clash(pattern_a_complex, pattern_b_complex, mix_ratio=0.5)
    
    # 緊張の増大カーブ
    tension = create_tension_build(10, start_amp=0.3, end_amp=1.2)
    clash2 = clash2 * tension
    
    audio[int(SAMPLE_RATE * 10):int(SAMPLE_RATE * 20)] += clash2
    
    # セクション3: デッドロック状態の定着 (20-27秒)
    print("Section 3: Deadlock state solidifies...")
    
    # 3つ目のプロセスが参加
    pattern_c = create_waiting_pattern(440, 16)
    pattern_c = np.tile(pattern_c, 1)
    pattern_c = phase_shift_pattern(pattern_c, shift_amount=0.25)
    pattern_c = pattern_c[:int(SAMPLE_RATE * 7)]
    
    # 3つのプロセスの衝突
    clash_a_b = create_deadlock_clash(pattern_a_complex[:int(SAMPLE_RATE * 7)], 
                                      pattern_b_complex[:int(SAMPLE_RATE * 7)], mix_ratio=0.4)
    clash_abc = create_deadlock_clash(clash_a_b, pattern_c, mix_ratio=0.7)
    
    # 歪みを追加
    clash_abc = add_harmonic_distortion(clash_abc, amount=0.15)
    
    # さらに大きな緊張
    tension2 = create_tension_build(7, start_amp=0.8, end_amp=1.5)
    clash_abc = clash_abc * tension2
    
    audio[int(SAMPLE_RATE * 20):int(SAMPLE_RATE * 27)] += clash_abc
    
    # セクション4: 突然の沈黙 (27-30秒)
    print("Section 4: Sudden silence...")
    
    # 最後の衝突からのフェード
    last_clash = create_waiting_pattern(110, 4)
    last_clash = last_clash[:int(SAMPLE_RATE * 2)]
    last_clash *= np.linspace(1, 0, len(last_clash))
    
    silence_start = int(SAMPLE_RATE * 27)
    audio[silence_start:silence_start + len(last_clash)] += last_clash
    
    # 最後の部分は沈黙
    # (すでにゼロで初期化されている)
    
    # 全体を正規化
    audio = audio / np.max(np.abs(audio)) * 0.7
    
    # 歪みを少し追加（デッドロックの「不快感」）
    audio = add_harmonic_distortion(audio, amount=0.05)
    
    return audio

if __name__ == "__main__":
    print("Generating Deadlock Dance...")
    audio = generate_deadlock_dance()
    
    # 出力
    output_path = "../samples/07_deadlock_dance.wav"
    sf.write(output_path, audio, SAMPLE_RATE)
    print(f"✅ Generated: {output_path}")
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    print(f"📊 Size: {file_size / 1024 / 1024:.1f} MB")
    print(f"⏱️ Duration: {DURATION} seconds")
    print("🔒 Deadlock: Process A and B are waiting for each other...")