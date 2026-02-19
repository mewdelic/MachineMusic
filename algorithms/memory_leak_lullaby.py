"""
Track 5: Memory Leak Lullaby
コンセプト：徐々に失われる記憶の子守唄

メモリリークを音で表現：
- 最初はシンプルで美しい旋律（子守唄）
- 時間が経つにつれて、前の音符が残り始める（リーク）
- 徐々に多くの層が重なり、音楽が重く、濁っていく
- 最終的に「メモリ不足」で終了するようなフェードアウト
- リバーブ、レイヤー増加、ノイズ、不協和音、リズム遅延
"""

import numpy as np
from scipy.io import wavfile
import random

# パラメータ
SAMPLE_RATE = 44100
DURATION = 30  # 秒

def simple_tone(freq, duration_samples, amplitude=0.5, fade_in=0.01, fade_out=0.01):
    """基本的なサイン波（フェード付き）"""
    t = np.linspace(0, duration_samples / SAMPLE_RATE, duration_samples, dtype=np.float32)
    
    # フェードイン/フェードアウト
    fade_in_samples = int(duration_samples * fade_in)
    fade_out_samples = int(duration_samples * fade_out)
    
    tone = amplitude * np.sin(2 * np.pi * freq * t)
    
    # フェード適用
    if fade_in_samples > 0:
        tone[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    if fade_out_samples > 0:
        tone[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    
    return tone

def simple_melody(base_freq, num_notes=8, note_duration=0.5):
    """シンプルな子守唄風メロディ"""
    melody = np.zeros(int(SAMPLE_RATE * num_notes * note_duration), dtype=np.float32)
    
    # 子守唄風のスケール（ペンタトニック風）
    scale_ratios = [1, 1.125, 1.25, 1.5, 1.667, 2, 2.25, 2.5]
    
    current_pos = 0
    for i in range(num_notes):
        freq = base_freq * random.choice(scale_ratios)
        note_samples = int(SAMPLE_RATE * note_duration)
        
        note = simple_tone(freq, note_samples, amplitude=0.3, fade_in=0.1, fade_out=0.2)
        
        if current_pos + len(note) <= len(melody):
            melody[current_pos:current_pos + len(note)] = note
        
        current_pos += int(SAMPLE_RATE * note_duration * 0.9)  # 少し重ねる
    
    return melody

def accumulate_layers(base_melody, accumulation_factor, max_layers=10):
    """前の音が残っていく（メモリリークの表現）"""
    result = np.copy(base_melody)
    melody_length = len(base_melody)
    
    # 徐々に前のレイヤーを追加
    for i in range(1, max_layers):
        delay = int(melody_length * 0.1 * i * accumulation_factor)
        if delay >= melody_length:
            break
        
        delayed_start = delay
        delayed_end = min(delay + melody_length, melody_length)
        source_start = 0
        source_end = min(melody_length, melody_length - delay)
        
        if source_end > source_start:
            delayed_layer = base_melody[source_start:source_end] * (0.5 / i)
            result[delayed_start:delayed_end] += delayed_layer
    
    return result

def memory_leak_drone(base_freq, duration_samples, leak_rate=0.05):
    """メモリリークするドローン - 徐々に複雑化"""
    t = np.linspace(0, duration_samples / SAMPLE_RATE, duration_samples, dtype=np.float32)
    
    # 基本ドローン
    drone = np.zeros(duration_samples, dtype=np.float32)
    
    # 徐々に周波数層を追加（リーク）
    num_layers = int(duration_samples / SAMPLE_RATE * leak_rate) + 1
    for i in range(num_layers):
        layer_start = int(duration_samples * (i / num_layers))
        layer_freq = base_freq * (1 + (i % 5) * 0.1)
        
        if layer_start < duration_samples:
            t_layer = t[layer_start:]
            layer = 0.15 * np.sin(2 * np.pi * layer_freq * t_layer)
            layer *= (1 + i * 0.05)  # 徐々に大きく
            layer *= np.exp(-t_layer * 0.3)  # 各レイヤーはフェードアウト
            
            drone[layer_start:] += layer[:len(t_layer)]
    
    return drone

def growing_reverb(signal, max_depth_samples):
    """時間とともにリバーブが深くなる（メモリ使用量の増加）"""
    signal_length = len(signal)
    result = np.zeros(signal_length, dtype=np.float32)
    
    # セクションごとにリバーブ深度を変える
    sections = 20
    section_length = signal_length // sections
    
    for i in range(sections):
        section_start = i * section_length
        section_end = min(section_start + section_length, signal_length)
        current_section = signal[section_start:section_end]
        
        # 深さが徐々に増える
        current_depth = int(max_depth_samples * (i / sections))
        
        # シンプルなリバーブ（遅延の重ね）
        reverb = np.copy(current_section)
        for delay in range(SAMPLE_RATE // 10, current_depth, SAMPLE_RATE // 20):
            if section_start + delay < signal_length:
                delayed_start = delay
                delayed_end = min(delayed_start + len(current_section), len(reverb))
                if delayed_end > delayed_start:
                    source_length = min(len(current_section), delayed_end - delayed_start)
                    reverb[delayed_start:delayed_start + source_length] += \
                        current_section[:source_length] * 0.3 / (delay / (SAMPLE_RATE // 10))
        
        result[section_start:section_end] = current_section + reverb[:len(current_section)] * 0.5
    
    return result

def memory_pressure_noise(duration_samples, pressure_curve):
    """メモリ圧力によるノイズの導入"""
    noise = np.zeros(duration_samples, dtype=np.float32)
    
    # 圧力曲線に沿ってノイズを追加
    for i in range(0, duration_samples, 100):
        pressure = pressure_curve[i] if i < len(pressure_curve) else 0
        if pressure > 0.3:
            # 圧力が高いとノイズが増える
            noise[i:min(i + 100, duration_samples)] = \
                np.random.normal(0, 0.05 * (pressure - 0.3), min(100, duration_samples - i)).astype(np.float32)
    
    return noise

def slowing_down(base_rhythm, slowdown_factor):
    """リズムが徐々に遅くなる（CPU負荷上昇の比喩）"""
    result = np.zeros(len(base_rhythm), dtype=np.float32)
    
    # 音の位置をスライドさせながらコピー
    position = 0
    i = 0
    while position < len(result) and i < len(base_rhythm):
        # 徐々に遅延が増える
        current_delay = int(slowdown_factor * (i / len(base_rhythm))**2)
        
        # コピー範囲
        chunk_size = min(100, len(result) - position)
        if chunk_size > 0 and i + chunk_size < len(base_rhythm):
            result[position:position + chunk_size] = base_rhythm[i:i + chunk_size]
        
        position += chunk_size + current_delay
        i += chunk_size
    
    return result

def dissonant_intrusion(duration_samples, intrusion_start_time):
    """不協和音の侵入（メモリ汚染）"""
    signal = np.zeros(duration_samples, dtype=np.float32)
    
    start_sample = int(intrusion_start_time * SAMPLE_RATE)
    if start_sample >= duration_samples:
        return signal
    
    # 不協和音の周波数比
    dissonant_ratios = [1.04, 1.06, 1.08, 1.1, 1.15]
    
    for ratio in dissonant_ratios:
        base_freq = 110
        freq = base_freq * ratio
        
        t = np.linspace(0, (duration_samples - start_sample) / SAMPLE_RATE, 
                       duration_samples - start_sample, dtype=np.float32)
        
        # 徐々に大きくなる不協和音
        amplitude = 0.1 * (1 + 2 * t / DURATION) * np.exp(-t * 0.2)
        
        tone = amplitude * np.sin(2 * np.pi * freq * t)
        
        signal[start_sample:] += tone[:len(signal[start_sample:])]
    
    return signal

def memory_leak_lullaby(total_samples):
    """メモリリークの子守唄メインシーケンス"""
    sequence = np.zeros(total_samples, dtype=np.float32)
    
    # 圧力カーブ（0から1へ徐々に上昇）
    t = np.linspace(0, 1, total_samples)
    pressure_curve = np.clip(t**1.5, 0, 1)
    
    # セクション1: シンプルな子守唄（0-8秒）
    section1_end = SAMPLE_RATE * 8
    section1_duration = section1_end
    
    # 基本メロディ
    melody = simple_melody(220, num_notes=16, note_duration=0.4)
    melody_duration = len(melody)
    
    # セクション1にはまだリークは少ない
    for i in range(0, min(melody_duration, section1_duration), SAMPLE_RATE):
        if i + SAMPLE_RATE <= section1_duration and i + SAMPLE_RATE <= melody_duration:
            sequence[i:i + SAMPLE_RATE] += melody[i:i + SAMPLE_RATE] * 0.4
    
    # ドローン
    drone1 = memory_leak_drone(110, section1_duration, leak_rate=0.02)
    sequence[:section1_duration] += drone1 * 0.3
    
    # セクション2: リークの開始（8-16秒）
    section2_start = section1_end
    section2_end = SAMPLE_RATE * 16
    section2_duration = section2_end - section2_start
    
    # レイヤーが蓄積し始める
    melody2 = simple_melody(220, num_notes=16, note_duration=0.4)
    accumulated2 = accumulate_layers(melody2, accumulation_factor=0.3, max_layers=3)
    
    for i in range(min(section2_duration, len(accumulated2))):
        sequence[section2_start + i] += accumulated2[i] * 0.3
    
    # ドローンにリーク
    drone2 = memory_leak_drone(110, section2_duration, leak_rate=0.05)
    sequence[section2_start:section2_end] += drone2 * 0.35
    
    # セクション3: リークが進行（16-24秒）
    section3_start = section2_end
    section3_end = SAMPLE_RATE * 24
    section3_duration = section3_end - section3_start
    
    # 多くのレイヤー
    melody3 = simple_melody(220, num_notes=16, note_duration=0.4)
    accumulated3 = accumulate_layers(melody3, accumulation_factor=0.5, max_layers=6)
    
    for i in range(min(section3_duration, len(accumulated3))):
        sequence[section3_start + i] += accumulated3[i] * 0.35
    
    # ドローンにさらにリーク
    drone3 = memory_leak_drone(110, section3_duration, leak_rate=0.08)
    sequence[section3_start:section3_end] += drone3 * 0.4
    
    # 不協和音の侵入開始
    dissonant = dissonant_intrusion(section3_duration, intrusion_start_time=0.3)
    sequence[section3_start:section3_end] += dissonant * 0.15
    
    # セクション4: メモリ不足のフェードアウト（24-30秒）
    section4_start = section3_end
    section4_end = total_samples
    section4_duration = section4_end - section4_start
    
    # 濁った、重いサウンド
    melody4 = simple_melody(220, num_notes=12, note_duration=0.5)
    accumulated4 = accumulate_layers(melody4, accumulation_factor=0.7, max_layers=10)
    
    # スローにする
    slowed4 = slowing_down(accumulated4, slowdown_factor=0.5)
    
    for i in range(min(section4_duration, len(slowed4))):
        sequence[section4_start + i] += slowed4[i] * 0.25
    
    # 最後のドローン
    drone4 = memory_leak_drone(110, section4_duration, leak_rate=0.12)
    sequence[section4_start:section4_end] += drone4 * 0.3
    
    # 不協和音が増える
    dissonant4 = dissonant_intrusion(section4_duration, intrusion_start_time=0.1)
    sequence[section4_start:section4_end] += dissonant4 * 0.2
    
    # 最後はフェードアウト（メモリ不足で終了）
    fade_start = int(section4_start + section4_duration * 0.7)
    fade_duration = section4_end - fade_start
    if fade_duration > 0:
        fade_curve = np.linspace(1, 0, fade_duration)
        sequence[fade_start:section4_end] *= fade_curve
    
    return sequence

def main():
    print("Generating Track 5: Memory Leak Lullaby...")
    
    total_samples = SAMPLE_RATE * DURATION
    
    # 圧力カーブ（メモリ使用量の増加）
    t = np.linspace(0, 1, total_samples)
    pressure_curve = t ** 1.5
    
    # メインシーケンス生成
    main_sequence = memory_leak_lullaby(total_samples)
    
    # リバーブを徐々に深く
    reverb = growing_reverb(main_sequence, max_depth_samples=SAMPLE_RATE * 2)
    main_sequence += reverb * 0.3
    
    # ノイズの追加（メモリ圧力）
    noise = memory_pressure_noise(total_samples, pressure_curve)
    main_sequence += noise * 0.2
    
    # ベースレイヤー
    bass = memory_leak_drone(55, total_samples, leak_rate=0.03) * 0.25
    main_sequence += bass
    
    # 高音の不協和音（最後に強くなる）
    high_dissonance = np.zeros(total_samples, dtype=np.float32)
    for i in range(0, total_samples, SAMPLE_RATE // 2):
        pressure = pressure_curve[i]
        if pressure > 0.5:
            start = i
            end = min(i + SAMPLE_RATE // 4, total_samples)
            if end > start:
                t_high = np.linspace(0, (end - start) / SAMPLE_RATE, end - start, dtype=np.float32)
                freq = random.choice([880, 1100, 1320, 1760])
                high_dissonance[start:end] = 0.08 * pressure * np.sin(2 * np.pi * freq * t_high)
    
    main_sequence += high_dissonance
    
    # 全体的な音量調整
    main_sequence = main_sequence * 0.6
    
    # 最終的なクリッピング防止
    main_sequence = np.clip(main_sequence, -0.95, 0.95)
    
    # 16-bit PCMに変換
    audio_data = (main_sequence * 32767).astype(np.int16)
    
    # WAVファイルとして保存
    output_path = "/tmp/MachineMusic/samples/05_memory_leak_lullaby.wav"
    wavfile.write(output_path, SAMPLE_RATE, audio_data)
    
    print(f"Generated: {output_path}")
    print(f"Duration: {DURATION} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print("\nMemory Leak Lullaby complete!")
    print("- Starts with a simple, gentle lullaby melody")
    print("- Previous notes accumulate (memory leak)")
    print("- Layers build up, creating heaviness and murkiness")
    print("- Gradually slows down (CPU pressure)")
    print("- Dissonance and noise increase")
    print("- Fades out into 'out of memory' silence")

if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()
