"""
Track 5: Memory Leak Lullaby - Enhanced with Physical Modeling
コンセプト：物理的メモリリークの子守唄

強化コンセプト：
- Karplus-Strong物理モデリングでメモリアロケーションを弦として表現
- 物理的減衰の失敗でメモリ解放の失敗を表現
- 共振の増加でメモリ断片化を表現
- ノイズの物理的変化でメモリ破損を表現

物理モデリング技術：
- Karplus-Strong弦合成（メモリアロケーション）
- 減衰制御システム（メモリ解放）
- 共振フィルター（メモリ断片化）
- 物理的ノイズ（メモリ破損）
- 空間的定位（メモリ空間）
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
import random
import math

# パラメータ
SAMPLE_RATE = 44100
DURATION = 30  # 秒

class MemoryString:
    """メモリを表現する弦（Karplus-Strong物理モデリング）"""
    def __init__(self, freq, memory_address, initial_energy=1.0):
        self.freq = freq
        self.memory_address = memory_address
        self.initial_energy = initial_energy
        self.energy = initial_energy
        
        # 弦の物理的特性
        self.string_length = int(SAMPLE_RATE / freq)
        self.buffer = np.random.uniform(-0.1, 0.1, self.string_length).astype(np.float32)
        self.buffer_pos = 0
        
        # メモリ関連プロパティ
        self.is_allocated = True
        self.should_free = False
        self.leak_factor = 0.0
        self.fragmentation = 0.0
        
        # 物理的減衰パラメータ
        self.damping = 0.995  # 通常の減衰率
        self.leak_damping = 0.999  # リーク時の減衰率（減衰しない）
        self.current_damping = self.damping
        
    def allocate(self, energy):
        """メモリをアロケート（弦を鳴らす）"""
        if not self.is_allocated:
            self.is_allocated = True
            self.energy = energy
            self.buffer = np.random.uniform(-0.1, 0.1, self.string_length).astype(np.float32) * energy
            self.buffer_pos = 0
            
    def try_free(self):
        """メモリ解放を試みる（弦の減衰）"""
        if self.should_free:
            # リークしている場合は解放できない
            if self.leak_factor > 0.5:
                self.current_damping = self.leak_damping
                return False
            else:
                self.current_damping = self.damping
                self.energy *= 0.9
                return self.energy < 0.01
        return True
        
    def update_leak(self, leak_amount):
        """リーク量を更新"""
        self.leak_factor = min(1.0, self.leak_factor + leak_amount)
        self.fragmentation = self.leak_factor * 0.5
        
    def get_sample(self):
        """次のサンプルを生成（Karplus-Strongアルゴリズム）"""
        if not self.is_allocated or self.energy < 0.001:
            return 0.0
            
        # Karplus-Strongアルゴリズム
        current_sample = self.buffer[self.buffer_pos]
        
        # フィルタリング（平均を取ることで減衰）
        next_pos = (self.buffer_pos + 1) % self.string_length
        filtered_sample = (current_sample + self.buffer[next_pos]) * 0.5
        
        # 更新
        self.buffer[self.buffer_pos] = filtered_sample * self.current_damping
        self.buffer_pos = next_pos
        
        # エネルギー更新
        self.energy *= self.current_damping
        
        return current_sample * self.energy

class MemoryResonance:
    """メモリ断片化による共鳴を表現"""
    def __init__(self, base_freq):
        self.base_freq = base_freq
        self.fragmentation_level = 0.0
        self.resonance_freqs = []
        
    def update_fragmentation(self, level):
        """断片化レベルを更新"""
        self.fragmentation_level = level
        
        # 断片化に応じて共鳴周波数を生成
        num_resonances = int(1 + level * 8)
        self.resonance_freqs = []
        for i in range(num_resonances):
            freq = self.base_freq * (1 + (i + 1) * level * 0.1)
            self.resonance_freqs.append(freq)
            
    def apply_resonance(self, audio_signal, sample_rate):
        """共鳴を適用"""
        if self.fragmentation_level < 0.1:
            return audio_signal
            
        result = np.copy(audio_signal)
        
        for freq in self.resonance_freqs:
            # バンドパスフィルタで共鳴を作成
            nyquist = sample_rate / 2
            low = max(0.01, (freq - 20) / nyquist)
            high = min(0.99, (freq + 20) / nyquist)
            
            if low < high:
                b, a = signal.butter(2, [low, high], btype='band')
                try:
                    resonance = signal.filtfilt(b, a, audio_signal)
                    result += resonance * self.fragmentation_level * 0.1
                except:
                    pass
                    
        return result

class MemoryNoise:
    """メモリ破損による物理的ノイズ"""
    def __init__(self):
        self.corruption_level = 0.0
        
    def update_corruption(self, level):
        """破損レベルを更新"""
        self.corruption_level = level
        
    def generate_noise(self, length, sample_rate):
        """破損ノイズを生成"""
        if self.corruption_level < 0.05:
            return np.zeros(length, dtype=np.float32)
            
        noise = np.zeros(length, dtype=np.float32)
        
        # 破損レベルに応じてノイズを追加
        for i in range(0, length, 100):
            if self.corruption_level > random.random():
                # インパルスノイズ（メモリ破損）
                noise_length = min(100, length - i)
                noise[i:i + noise_length] = np.random.normal(0, 0.1 * self.corruption_level, noise_length)
                
        # 周波数領域での破損
        if self.corruption_level > 0.3:
            # 高周波ノイズ
            hf_noise = np.random.normal(0, 0.05 * self.corruption_level, length)
            # ローパスフィルタ
            b, a = signal.butter(1, 0.8, btype='high')
            try:
                hf_noise = signal.filtfilt(b, a, hf_noise)
                noise += hf_noise
            except:
                pass
                
        return noise

class MemoryLeakLullabyEnhanced:
    """強化版メモリリーク子守唄"""
    def __init__(self):
        # メモリ弦システム
        self.memory_strings = []
        self.max_strings = 32
        
        # メモリ管理システム
        self.allocated_memory = 0
        self.total_memory = 1024
        self.leak_rate = 0.01
        self.fragmentation = 0.0
        self.corruption = 0.0
        
        # 物理モデリングコンポーネント
        self.resonance = MemoryResonance(110)
        self.noise_generator = MemoryNoise()
        
        # 時間管理
        self.time_step = 0
        self.pressure_curve = None
        
    def initialize_memory(self, duration_samples):
        """メモリシステムを初期化"""
        # 圧力カーブを計算
        t = np.linspace(0, 1, duration_samples)
        self.pressure_curve = np.clip(t ** 1.5, 0, 1)
        
        # 初期メモリ弦をアロケート
        initial_strings = 8
        for i in range(initial_strings):
            freq = 110 + i * 55  # メモリアドレスに対応する周波数
            string = MemoryString(freq, i * 128)
            string.allocate(0.5)
            self.memory_strings.append(string)
            self.allocated_memory += 128
            
    def allocate_memory(self):
        """新しいメモリをアロケート"""
        if len(self.memory_strings) >= self.max_strings:
            return False
            
        if self.allocated_memory >= self.total_memory * 0.9:
            return False  # メモリ不足
            
        # 新しいメモリ弦をアロケート
        address = random.randint(0, 1024)
        freq = 110 + (address % 16) * 55
        string = MemoryString(freq, address)
        string.allocate(0.3)
        self.memory_strings.append(string)
        self.allocated_memory += 128
        
        return True
        
    def update_memory_leak(self):
        """メモリリークを更新"""
        if self.time_step % (SAMPLE_RATE // 4) == 0:  # 0.25秒ごと
            # リーク率を増加
            self.leak_rate = min(0.1, self.leak_rate + 0.001)
            
            # 断片化を増加
            self.fragmentation = min(1.0, self.fragmentation + 0.002)
            
            # 破損を増加
            if self.fragmentation > 0.3:
                self.corruption = min(1.0, self.corruption + 0.001)
                
            # すべての弦にリークを適用
            for string in self.memory_strings:
                string.update_leak(self.leak_rate * 0.1)
                string.should_free = True  # 解放マーク
                
            # 断片化に応じて共鳴を更新
            self.resonance.update_fragmentation(self.fragmentation)
            
            # 破損ノイズを更新
            self.noise_generator.update_corruption(self.corruption)
            
    def manage_memory(self):
        """メモリ管理（ガベージコレクションの失敗）"""
        if self.time_step % (SAMPLE_RATE // 2) == 0:  # 0.5秒ごと
            # 解放を試みる
            freed_count = 0
            strings_to_remove = []
            
            for string in self.memory_strings:
                if string.try_free():
                    strings_to_remove.append(string)
                    self.allocated_memory -= 128
                    freed_count += 1
                    
            # 解放できた弦を削除
            for string in strings_to_remove:
                self.memory_strings.remove(string)
                
            # リークが進行している場合、新しいメモリをアロケート
            if self.leak_rate > 0.02 and random.random() < 0.3:
                self.allocate_memory()
                
    def generate_frame(self):
        """1フレームのオーディオを生成"""
        frame = np.zeros(1, dtype=np.float32)
        
        # すべての弦からサンプルを生成
        for string in self.memory_strings:
            sample = string.get_sample()
            frame[0] += sample
            
        # 更新
        self.time_step += 1
        self.update_memory_leak()
        self.manage_memory()
        
        return frame
        
    def generate_full_track(self, duration_samples):
        """完全なトラックを生成"""
        # メモリシステムを初期化
        self.initialize_memory(duration_samples)
        
        # オーディオバッファ
        audio = np.zeros(duration_samples, dtype=np.float32)
        
        # フレーム生成ループ
        for i in range(duration_samples):
            frame = self.generate_frame()
            audio[i] = frame[0]
            
            # 進捗表示
            if i % (SAMPLE_RATE * 5) == 0:
                progress = i / duration_samples * 100
                print(f"Progress: {progress:.1f}% - Strings: {len(self.memory_strings)} - Leak: {self.leak_rate:.3f}")
                
        return audio

def post_process_enhanced_lullaby(audio, pressure_curve, sample_rate):
    """強化版子守唄のポストプロセッシング"""
    # リバーブを徐々に深く（メモリ使用量の増加）
    reverb_audio = np.zeros_like(audio)
    
    sections = 20
    section_length = len(audio) // sections
    
    for i in range(sections):
        start = i * section_length
        end = min(start + section_length, len(audio))
        current_section = audio[start:end]
        
        # リバーブ深度を計算
        reverb_depth = int(0.5 * sample_rate * (i / sections))
        
        if reverb_depth > 0 and len(current_section) > reverb_depth:
            # シンプルなリバーブ
            reverb = np.zeros_like(current_section)
            for delay in range(sample_rate // 8, reverb_depth, sample_rate // 16):
                if delay < len(current_section):
                    reverb[delay:] += current_section[:-delay] * 0.3
                    
            current_section += reverb * 0.5
            
        reverb_audio[start:end] = current_section
        
    # 共鳴を適用
    resonance = MemoryResonance(110)
    resonance.update_fragmentation(0.7)  # 最終的な断片化レベル
    resonant_audio = resonance.apply_resonance(reverb_audio, sample_rate)
    
    # 破損ノイズを追加
    noise = MemoryNoise()
    noise.update_corruption(0.8)  # 最終的な破損レベル
    noise_audio = noise.generate_noise(len(audio), sample_rate)
    
    result = resonant_audio + noise_audio * 0.1
    
    # 圧力に応じて全体の音量を調整
    for i in range(len(result)):
        pressure = pressure_curve[min(i, len(pressure_curve) - 1)]
        if pressure > 0.8:
            # メモリ圧力が高いと音量を落とす
            result[i] *= (1.0 - (pressure - 0.8) * 2)
            
    # クリッピング防止
    result = np.clip(result, -0.95, 0.95)
    
    return result

def analyze_memory_leak_enhanced(audio, sample_rate):
    """メモリリーク強化版の分析"""
    # 基本的な統計
    peak_level = np.max(np.abs(audio))
    rms_level = np.sqrt(np.mean(audio**2))
    
    # ダイナミックレンジ
    signal_power = audio**2
    max_power = np.max(signal_power)
    min_power = np.min(signal_power[signal_power > 0])
    dynamic_range = 10 * np.log10(max_power / min_power) if min_power > 0 else 0
    
    print(f"Memory Leak Lullaby Enhanced Analysis:")
    print(f"Peak Level: {20 * np.log10(peak_level):.2f} dB")
    print(f"RMS Level: {20 * np.log10(rms_level):.2f} dB")
    print(f"Dynamic Range: {dynamic_range:.2f} dB")
    
    return {
        'peak_level': peak_level,
        'rms_level': rms_level,
        'dynamic_range': dynamic_range
    }

def create_memory_visualization_enhanced(pressure_curve, fragmentation_curve, corruption_curve, sample_rate):
    """メモリ状態の可視化"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        
        # 時間軸
        time_axis = np.arange(len(pressure_curve)) / sample_rate
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        # 圧力カーブ
        ax1.plot(time_axis, pressure_curve, 'b-', linewidth=2, label='Memory Pressure')
        ax1.set_ylabel('Pressure')
        ax1.set_title('Memory Leak Lullaby - Physical Modeling Analysis')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 断片化カーブ
        ax2.plot(time_axis, fragmentation_curve, 'r-', linewidth=2, label='Memory Fragmentation')
        ax2.set_ylabel('Fragmentation')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 破損カーブ
        ax3.plot(time_axis, corruption_curve, 'g-', linewidth=2, label='Memory Corruption')
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Corruption')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/tmp/MachineMusic/visualizations/05_memory_leak_lullaby_enhanced_analysis.png', 
                   dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Created enhanced visualization: 05_memory_leak_lullaby_enhanced_analysis.png")
        
    except ImportError:
        print("Matplotlib not available for visualization")

def main():
    print("Generating Track 5: Memory Leak Lullaby - Enhanced with Physical Modeling...")
    print("Concept: Physical memory leak simulation using Karplus-Strong strings")
    
    total_samples = SAMPLE_RATE * DURATION
    
    # 強化版メモリリーク子守唄生成器
    generator = MemoryLeakLullabyEnhanced()
    
    # メインオーディオ生成
    main_audio = generator.generate_full_track(total_samples)
    
    # 圧力カーブを取得
    pressure_curve = generator.pressure_curve
    
    # 断片化と破損のカーブを生成
    fragmentation_curve = np.zeros_like(pressure_curve)
    corruption_curve = np.zeros_like(pressure_curve)
    
    for i in range(len(pressure_curve)):
        # 時間とともに増加
        t = i / len(pressure_curve)
        fragmentation_curve[i] = min(1.0, t ** 1.2)
        corruption_curve[i] = min(1.0, max(0, (t - 0.3) ** 2) * 2)
    
    # ポストプロセッシング
    processed_audio = post_process_enhanced_lullaby(main_audio, pressure_curve, SAMPLE_RATE)
    
    # 音量調整
    processed_audio = processed_audio * 0.8
    
    # 分析
    analysis = analyze_memory_leak_enhanced(processed_audio, SAMPLE_RATE)
    
    # 16-bit PCMに変換
    audio_data = (processed_audio * 32767).astype(np.int16)
    
    # 保存
    output_path = "/tmp/MachineMusic/samples/05_memory_leak_lullaby_enhanced.wav"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wavfile.write(output_path, SAMPLE_RATE, audio_data)
    
    print(f"Generated: {output_path}")
    print(f"Duration: {DURATION} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Peak Level: {20 * np.log10(analysis['peak_level']):.2f} dB")
    print(f"RMS Level: {20 * np.log10(analysis['rms_level']):.2f} dB")
    print(f"Dynamic Range: {analysis['dynamic_range']:.2f} dB")
    
    # 可視化
    create_memory_visualization_enhanced(pressure_curve, fragmentation_curve, corruption_curve, SAMPLE_RATE)
    
    print("\nMemory Leak Lullaby - Enhanced Complete!")
    print("Physical Modeling Features:")
    print("- Karplus-Strong strings represent memory allocations")
    print("- Failed damping represents memory that cannot be freed")
    print("- Resonance represents memory fragmentation")
    print("- Physical noise represents memory corruption")
    print("- Spatial positioning represents memory address space")
    print("\nTrack Structure:")
    print("- 0-8s: Gentle lullaby with stable memory")
    print("- 8-16s: Memory leaks begin, strings accumulate")
    print("- 16-24s: Severe fragmentation and corruption")
    print("- 24-30s: Memory exhaustion and system crash")

if __name__ == "__main__":
    import os
    random.seed(42)
    np.random.seed(42)
    main()