"""
Track 3: Null Pointer Dreams
コンセプト：何も指さないポインタが見る夢

NULL状態を音で表現：
- 値が突然NULLになる感覚
- 音が途中で消える、途切れる、虚空へ
- 期待していた音が来ない不安
- サイレンスと突然のノイズ
- デリファレンスの瞬間のクラッシュ
"""

import numpy as np
from scipy.io import wavfile
import random

# パラメータ
SAMPLE_RATE = 44100
DURATION = 30  # 秒

def generate_silence(duration_samples):
    """完全な静寂"""
    return np.zeros(duration_samples)

def generate_tone(freq, duration_samples, amplitude=0.5):
    """基本的なサイン波"""
    t = np.linspace(0, duration_samples / SAMPLE_RATE, duration_samples, dtype=np.float32)
    return amplitude * np.sin(2 * np.pi * freq * t)

def sudden_cutoff(signal, cutoff_point):
    """突然の途切れ - NULLへのデリファレンス"""
    result = np.copy(signal)
    result[cutoff_point:] = 0
    return result

def expected_sound_missing(duration_samples, expected_start, expected_duration):
    """期待していた音が来ない - その場所だけ静寂"""
    silence = np.zeros(duration_samples, dtype=np.float32)
    # 期待される場所に微かな「ノイズの影」を入れる（音そのものは来ない）
    ghost_noise = np.random.normal(0, 0.001, expected_duration).astype(np.float32)
    silence[expected_start:expected_start + expected_duration] = ghost_noise
    return silence

def null_burst(position, total_samples, burst_duration=2000):
    """NULLポインタからのノイズバースト - クラッシュの瞬間"""
    signal = np.zeros(total_samples, dtype=np.float32)
    # 急激に立ち上がり、すぐに消える
    t = np.linspace(0, burst_duration / SAMPLE_RATE, burst_duration, dtype=np.float32)
    
    # 複数の周波数が衝突するノイズ
    burst = np.zeros(burst_duration, dtype=np.float32)
    for freq in [100, 250, 400, 800, 1200, 2000]:
        burst += 0.15 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 50)
    
    # ホワイトノイズを混ぜる
    burst += 0.2 * np.random.normal(0, 1, burst_duration).astype(np.float32) * np.exp(-t * 80)
    
    # クリッピング（デジタル歪み）
    burst = np.clip(burst, -0.9, 0.9)
    
    if position + burst_duration < total_samples:
        signal[position:position + burst_duration] = burst
    
    return signal

def dereference_echo(original_signal, echo_position, decay_rate=0.3):
    """デリファレンス時の残響 - NULLに到達した音の反響"""
    echo = original_signal * decay_rate
    echo_duration = len(echo)
    
    if echo_position + echo_duration < len(original_signal):
        result = np.copy(original_signal)
        result[echo_position:echo_position + echo_duration] += echo
        return result
    return original_signal

def void_drone(base_freq, duration_samples, drift_rate=0.001):
    """虚空へのドローン - 徐々にNULLへ向かう"""
    t = np.linspace(0, duration_samples / SAMPLE_RATE, duration_samples, dtype=np.float32)
    
    # 周波数が徐々に不安定になる
    freq_variation = base_freq * (1 + drift_rate * np.cumsum(np.random.randn(duration_samples) * 0.01))
    
    # 位相の累積
    phase = np.cumsum(2 * np.pi * freq_variation / SAMPLE_RATE)
    
    # 振幅も徐々に消えていく
    amplitude = 0.3 * np.exp(-t * 0.3) * (1 + 0.5 * np.sin(t * 0.5))
    
    drone = amplitude * np.sin(phase)
    
    # 時々断絶
    for i in range(0, duration_samples, SAMPLE_RATE // 2):
        if random.random() < 0.15:  # 15%の確率で断絶
            gap_duration = random.randint(100, 500)
            drone[i:min(i + gap_duration, duration_samples)] = 0
    
    return drone

def pointer_arithmetic_melody(base_freq, num_notes=12):
    """ポインタ演算のような不規則なメロディ - アドレス計算の誤差"""
    total_samples = SAMPLE_RATE * 3  # 3秒
    melody = np.zeros(total_samples, dtype=np.float32)
    
    # 「ポインタ」のような不規則なジャンプ
    current_pos = 0
    for i in range(num_notes):
        # ポインタ演算：時には大きなジャンプ、時には小さなステップ
        if random.random() < 0.2:
            # NULLポインタ参照 - 音が飛ぶ
            current_pos += random.randint(SAMPLE_RATE // 4, SAMPLE_RATE // 2)
        else:
            current_pos += random.randint(SAMPLE_RATE // 20, SAMPLE_RATE // 8)
        
        if current_pos >= total_samples:
            break
        
        # メモリアクセスのような音
        note_duration = random.randint(1000, 5000)
        freq = base_freq * (random.choice([0.5, 1, 1.5, 2, 3]))  # 不規則なオクターブ
        
        t = np.linspace(0, note_duration / SAMPLE_RATE, note_duration, dtype=np.float32)
        note = 0.2 * np.sin(2 * np.pi * freq * t)
        
        # 50%の確率で途中で途切れる（NULL参照）
        if random.random() < 0.5:
            cutoff = random.randint(note_duration // 4, note_duration // 2)
            note[cutoff:] = 0
        
        end_pos = min(current_pos + note_duration, total_samples)
        actual_duration = end_pos - current_pos
        if actual_duration > 0:
            melody[current_pos:end_pos] = note[:actual_duration]
    
    return melody

def segmentation_violation(total_samples, num_violations=5):
    """セグメンテーション違反 - アクセスしてはいけない領域への侵入"""
    signal = np.zeros(total_samples, dtype=np.float32)
    
    for _ in range(num_violations):
        # 違反の位置
        position = random.randint(0, total_samples - 5000)
        
        # 違反のサイズ（小さなバースト）
        violation_duration = random.randint(500, 3000)
        
        # 短い高周波ノイズ
        t = np.linspace(0, violation_duration / SAMPLE_RATE, violation_duration, dtype=np.float32)
        freq = random.choice([2000, 3000, 4000, 5000])
        
        violation = 0.4 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 200)
        violation += 0.3 * np.random.normal(0, 1, violation_duration).astype(np.float32) * np.exp(-t * 300)
        
        end_pos = min(position + violation_duration, total_samples)
        actual_duration = end_pos - position
        if actual_duration > 0:
            signal[position:end_pos] += violation[:actual_duration]
    
    return signal

def null_dream_sequence(total_samples):
    """NULLポインタが見る夢のシーケンス"""
    sequence = np.zeros(total_samples, dtype=np.float32)
    
    # セクション1: 安定した開始（0-8秒）
    section1_end = SAMPLE_RATE * 8
    drone1 = void_drone(110, section1_end, drift_rate=0.0005)
    sequence[:section1_end] += drone1 * 0.4
    
    # セクション2: 不安定化（8-16秒）
    section2_start = section1_end
    section2_end = SAMPLE_RATE * 16
    
    # メロディが途中で消える
    melody1 = pointer_arithmetic_melody(220, num_notes=15)
    melody1_with_cutoff = sudden_cutoff(melody1, len(melody1) * 2 // 3)
    sequence[section2_start:section2_start + len(melody1_with_cutoff)] += melody1_with_cutoff * 0.3
    
    # 期待された音が来ない
    missing = expected_sound_missing(section2_end - section2_start, 
                                      SAMPLE_RATE * 2, 
                                      SAMPLE_RATE)
    sequence[section2_start:section2_end] += missing * 0.5
    
    # ドローンも不安定に
    drone2 = void_drone(165, section2_end - section2_start, drift_rate=0.002)
    sequence[section2_start:section2_end] += drone2 * 0.3
    
    # セクション3: クラッシュと静寂（16-24秒）
    section3_start = section2_end
    section3_end = SAMPLE_RATE * 24
    
    # NULLバースト
    for i in range(3):
        burst_pos = section3_start + i * SAMPLE_RATE * 2 + random.randint(0, SAMPLE_RATE)
        burst = null_burst(burst_pos, total_samples, burst_duration=random.randint(1000, 4000))
        sequence += burst * 0.5
    
    # セグメンテーション違反
    seg_violations = segmentation_violation(section3_end - section3_start, num_violations=7)
    sequence[section3_start:section3_end] += seg_violations * 0.4
    
    # 長い静寂
    silence_duration = SAMPLE_RATE * 2
    silence_start = section3_start + SAMPLE_RATE * 3
    sequence[silence_start:silence_start + silence_duration] = 0
    
    # セクション4: 終わりのない夢（24-30秒）
    section4_start = section3_end
    section4_end = total_samples
    
    # 最後のドローン - 徐々に虚空へ
    drone3 = void_drone(130, section4_end - section4_start, drift_rate=0.005)
    sequence[section4_start:section4_end] += drone3 * 0.25
    
    # 断続的な音
    for i in range(5):
        frag_start = section4_start + i * SAMPLE_RATE + random.randint(-SAMPLE_RATE // 4, SAMPLE_RATE // 4)
        if frag_start < total_samples:
            frag_duration = random.randint(500, 2000)
            freq = random.choice([180, 220, 270, 330])
            t = np.linspace(0, frag_duration / SAMPLE_RATE, frag_duration, dtype=np.float32)
            fragment = 0.15 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 20)
            
            end_pos = min(frag_start + frag_duration, total_samples)
            actual_duration = end_pos - frag_start
            if actual_duration > 0:
                sequence[frag_start:end_pos] += fragment[:actual_duration]
    
    return sequence

def main():
    print("Generating Track 3: Null Pointer Dreams...")
    
    total_samples = SAMPLE_RATE * DURATION
    
    # メインシーケンス生成
    main_sequence = null_dream_sequence(total_samples)
    
    # 追加のレイヤー
    # 低音の不安定なベース
    bass = void_drone(55, total_samples, drift_rate=0.001) * 0.2
    
    # 予期しないクリック音（NULLチェックの失敗）
    clicks = np.zeros(total_samples, dtype=np.float32)
    for i in range(20):
        click_pos = random.randint(0, total_samples - 100)
        click_duration = random.randint(50, 200)
        click = 0.3 * np.random.choice([-1, 1]) * np.exp(-np.linspace(0, 5, click_duration))
        end_pos = min(click_pos + click_duration, total_samples)
        actual_duration = end_pos - click_pos
        if actual_duration > 0:
            clicks[click_pos:end_pos] += click[:actual_duration].astype(np.float32)
    
    # ミックス
    final_mix = main_sequence + bass + clicks * 0.3
    
    # 全体的な音量調整
    final_mix = final_mix * 0.7
    
    # 最終的なクリッピング防止
    final_mix = np.clip(final_mix, -0.95, 0.95)
    
    # 16-bit PCMに変換
    audio_data = (final_mix * 32767).astype(np.int16)
    
    # WAVファイルとして保存
    output_path = "/tmp/MachineMusic/samples/03_null_pointer_dreams.wav"
    wavfile.write(output_path, SAMPLE_RATE, audio_data)
    
    print(f"Generated: {output_path}")
    print(f"Duration: {DURATION} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print("\nNULL Pointer Dreams complete!")
    print("- Sounds cutting off into silence")
    print("- Expected sounds that never arrive")
    print("- Sudden noise bursts from dereferencing NULL")
    print("- The void where pointers point to nothing")

if __name__ == "__main__":
    random.seed(42)  # 再現性のため（でも常に少し違う）
    np.random.seed(42)
    main()
