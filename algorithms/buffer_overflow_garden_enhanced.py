#!/usr/bin/env python3
"""
Track 6: Buffer Overflow Garden - Enhanced with Physical Modeling
コンセプト：はみ出したデータが咲く花の物理的庭園

強化コンセプト：
- 物理的境界とバッファの相互作用を表現
- メモリレイアウトを物理的空間として表現
- データオーバーフローを物理的干渉として表現
- スタックヒープの物理的衝突を表現

物理モデリング技術：
- バッファ物理境界システム
- メモリレイアウトの物理的地形
- データフローの流体力学
- 衝突検知と反響
- 空間的メモリ配置
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.spatial import distance
import random
import math

# パラメータ
SAMPLE_RATE = 44100
DURATION = 30  # 秒

class MemoryBoundary:
    """メモリ境界を表現する物理的壁"""
    def __init__(self, position, strength=1.0):
        self.position = position
        self.strength = strength
        self.violations = 0
        self.resonance = 0.0
        
    def check_collision(self, data_pos):
        """データが境界を超えたかチェック"""
        if data_pos > self.position:
            self.violations += 1
            self.resonance = min(1.0, self.resonance + 0.1)
            return True
        return False
    
    def get_resonance_freq(self):
        """境界の反響周波数"""
        base_freq = 220 + (self.position * 10)
        return base_freq + (self.resonance * 50)

class BufferRegion:
    """バッファ領域を表現する物理的容器"""
    def __init__(self, start_pos, size, region_type="stack"):
        self.start_pos = start_pos
        self.size = size
        self.end_pos = start_pos + size
        self.region_type = region_type
        self.contents = []
        self.integrity = 1.0
        self.fragmentation = 0.0
        
        # 物理的特性
        self.density = 1.0 if region_type == "stack" else 0.7
        self.elasticity = 0.8
        
    def add_data(self, data_item):
        """データをバッファに追加"""
        if len(self.contents) < self.size:
            self.contents.append(data_item)
            return True
        else:
            # オーバーフロー
            self.integrity *= 0.95
            self.fragmentation += 0.05
            return False
    
    def get_physical_resonance(self):
        """バッファの物理的共鳴"""
        base_freq = 200 + (self.start_pos * 5)
        integrity_factor = self.integrity
        fragmentation_factor = 1.0 + self.fragmentation
        return base_freq * integrity_factor * fragmentation_factor

class DataParticle:
    """データ粒子を表現する物理的要素"""
    def __init__(self, value, velocity=1.0, mass=1.0):
        self.value = value
        self.velocity = velocity
        self.mass = mass
        self.position = 0.0
        self.energy = abs(value) * velocity
        self.is_overflow = False
        
        # 音響的特性
        self.freq = 220 + (abs(value) * 10)
        self.amplitude = min(1.0, self.energy * 0.1)
        
    def update_position(self, dt=0.01):
        """粒子の位置を更新"""
        self.position += self.velocity * dt
        
    def get_karplus_string(self, length=100):
        """Karplus-Strong弦でデータを表現"""
        if length <= 0:
            length = 100
        string = np.random.uniform(-self.amplitude, self.amplitude, length).astype(np.float32)
        return string

class PhysicalMemorySpace:
    """物理的メモリ空間"""
    def __init__(self, total_size=1024):
        self.total_size = total_size
        self.boundaries = []
        self.regions = []
        self.particles = []
        self.gravity = 9.8
        
        # メモリレイアウトを初期化
        self.setup_memory_layout()
        
    def setup_memory_layout(self):
        """メモリレイアウトを物理的に設定"""
        # スタック領域（高アドレスから低アドレスへ）
        stack_region = BufferRegion(self.total_size - 256, 256, "stack")
        self.regions.append(stack_region)
        
        # ヒープ領域（低アドレスから高アドレスへ）
        heap_region = BufferRegion(128, 256, "heap")
        self.regions.append(heap_region)
        
        # 境界を設定
        stack_boundary = MemoryBoundary(self.total_size - 256, strength=1.0)
        heap_boundary = MemoryBoundary(128 + 256, strength=0.8)
        
        self.boundaries.extend([stack_boundary, heap_boundary])
        
    def add_particle(self, particle):
        """粒子を空間に追加"""
        self.particles.append(particle)
        
    def update_physics(self, dt=0.01):
        """物理シミュレーションを更新"""
        for particle in self.particles:
            # 粒子の位置を更新
            particle.update_position(dt)
            
            # 境界チェック
            for boundary in self.boundaries:
                if boundary.check_collision(particle.position):
                    particle.is_overflow = True
                    # 反響を生成
                    resonance_freq = boundary.get_resonance_freq()
                    particle.freq = resonance_freq
                    
                    # エネルギー増加（オーバーフロー時）
                    particle.energy *= 1.1
                    particle.amplitude = min(1.0, particle.amplitude * 1.05)
    
    def get_collision_sounds(self):
        """衝突音を生成"""
        collision_sounds = []
        for boundary in self.boundaries:
            if boundary.violations > 0:
                # 境界の反響音
                freq = boundary.get_resonance_freq()
                duration = 0.1 * boundary.resonance
                samples = int(SAMPLE_RATE * duration)
                
                t = np.linspace(0, duration, samples)
                tone = np.sin(2 * np.pi * freq * t)
                envelope = np.exp(-t * 10)  # 減衰
                sound = tone * envelope * boundary.resonance
                
                collision_sounds.append(sound)
                
        return collision_sounds

class BufferOverflowGarden:
    """バッファオーバーフローの物理的庭園"""
    def __init__(self):
        self.memory_space = PhysicalMemorySpace()
        self.audio_buffer = np.zeros(int(SAMPLE_RATE * DURATION))
        self.time = 0.0
        
    def create_data_flow(self, num_particles):
        """データフローを生成"""
        particles = []
        
        for i in range(num_particles):
            # データ粒子の特性を設定
            value = random.uniform(-100, 100)
            velocity = random.uniform(0.5, 2.0)
            mass = random.uniform(0.5, 1.5)
            
            particle = DataParticle(value, velocity, mass)
            
            # 初期位置を設定
            if i % 2 == 0:
                # スタックから
                particle.position = self.memory_space.total_size - 50
                particle.velocity = -abs(particle.velocity)
            else:
                # ヒープから
                particle.position = 150
                particle.velocity = abs(particle.velocity)
                
            particles.append(particle)
            self.memory_space.add_particle(particle)
            
        return particles
    
    def generate_karplus_sound(self, particle, duration=0.2):
        """Karplus-Strong音で粒子を表現"""
        samples = int(SAMPLE_RATE * duration)
        
        # 基本周波数を粒子の特性から計算
        freq = particle.freq
        string_length = int(SAMPLE_RATE / freq)
        
        if string_length <= 0:
            string_length = 100
            
        # Karplus-Strongバッファ
        buffer = np.random.uniform(-particle.amplitude, particle.amplitude, string_length)
        
        # フィルタリング（オーバーフロー時は歪み）
        if particle.is_overflow:
            # 歪みフィルタ
            filter_freq = freq * (1.0 + particle.velocity * 0.1)
            b, a = signal.butter(2, filter_freq / (SAMPLE_RATE / 2), btype='low')
            buffer = signal.lfilter(b, a, buffer)
        
        # 音声生成
        audio = np.zeros(samples)
        pos = 0
        
        for i in range(samples):
            if pos < len(buffer) - 1:
                # Karplus-Strongアルゴリズム
                audio[i] = buffer[pos]
                # 減衰
                damping = 0.995 if not particle.is_overflow else 0.998
                buffer[pos] = (buffer[pos] + buffer[pos + 1]) * 0.5 * damping
                
            pos = (pos + 1) % max(1, len(buffer) - 1)
            
        return audio
    
    def generate_garden_growth(self, start_time, duration):
        """庭の成長を生成（オーバーフローの進行）"""
        start_sample = int(start_time * SAMPLE_RATE)
        end_sample = int((start_time + duration) * SAMPLE_RATE)
        
        # 成長段階に応じて粒子数を増加
        progress = (self.time - start_time) / duration
        num_particles = int(10 + progress * 40)
        
        particles = self.create_data_flow(num_particles)
        
        # 物理シミュレーション
        for _ in range(int(duration * 100)):  # 100Hzの物理更新
            self.memory_space.update_physics(0.01)
            
        # 粒子から音を生成
        for i, particle in enumerate(particles):
            particle_start = start_sample + int(i * duration * SAMPLE_RATE / len(particles))
            particle_duration = duration / len(particles)
            
            sound = self.generate_karplus_sound(particle, particle_duration)
            sound_samples = len(sound)
            
            end_pos = min(particle_start + sound_samples, end_sample)
            if end_pos > particle_start:
                self.audio_buffer[particle_start:end_pos] += sound[:end_pos - particle_start]
        
        # 衝突音を追加
        collision_sounds = self.memory_space.get_collision_sounds()
        for collision in collision_sounds:
            collision_samples = len(collision)
            collision_start = start_sample + random.randint(0, int(duration * SAMPLE_RATE) - collision_samples)
            collision_end = min(collision_start + collision_samples, end_sample)
            
            if collision_end > collision_start:
                self.audio_buffer[collision_start:collision_end] += collision[:collision_end - collision_start]
    
    def generate_section(self, section_num, start_time, duration, intensity):
        """セクションを生成"""
        print(f"Generating section {section_num}...")
        
        # セクションの特性を設定
        if section_num == 1:
            # 正常なバッファ操作
            self.generate_normal_operations(start_time, duration)
        elif section_num == 2:
            # オーバーフロー開始
            self.generate_overflow_begin(start_time, duration)
        elif section_num == 3:
            # 無秩序な庭
            self.generate_chaotic_garden(start_time, duration)
        else:
            # クラッシュ
            self.generate_crash(start_time, duration)
    
    def generate_normal_operations(self, start_time, duration):
        """正常なバッファ操作を生成"""
        # 整然としたデータフロー
        particles = self.create_data_flow(20)
        
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        for i, particle in enumerate(particles):
            particle_start = start_sample + int(i * samples / len(particles))
            particle_duration = duration / len(particles)
            
            sound = self.generate_karplus_sound(particle, particle_duration)
            sound_samples = len(sound)
            
            end_pos = min(particle_start + sound_samples, start_sample + samples)
            if end_pos > particle_start:
                self.audio_buffer[particle_start:end_pos] += sound[:end_pos - particle_start]
    
    def generate_overflow_begin(self, start_time, duration):
        """オーバーフロー開始を生成"""
        # 指数関数的に増加するオーバーフロー
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        progress_steps = 20
        for step in range(progress_steps):
            step_start = start_sample + int(step * samples / progress_steps)
            step_duration = duration / progress_steps
            
            # 進行に応じて粒子数を増加
            progress = step / progress_steps
            num_particles = int(10 + progress * 30)
            
            particles = self.create_data_flow(num_particles)
            
            # 物理シミュレーション
            for _ in range(10):
                self.memory_space.update_physics(0.01)
            
            # 音を生成
            for particle in particles:
                # オーバーフローの確率を増加
                if random.random() < progress * 0.5:
                    particle.position += random.uniform(10, 50)
                    self.memory_space.update_physics(0.01)
                
                sound = self.generate_karplus_sound(particle, step_duration / len(particles))
                sound_samples = len(sound)
                
                particle_start = step_start + random.randint(0, int(step_duration * SAMPLE_RATE) - sound_samples)
                end_pos = min(particle_start + sound_samples, start_sample + int((step + 1) * samples / progress_steps))
                
                if end_pos > particle_start:
                    self.audio_buffer[particle_start:end_pos] += sound[:end_pos - particle_start]
    
    def generate_chaotic_garden(self, start_time, duration):
        """無秩序な庭を生成"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        # 多数の粒子が同時に存在
        for burst in range(50):
            burst_start = start_sample + int(burst * samples / 50)
            burst_duration = duration / 50
            
            # 無秩序な粒子群
            particles = self.create_data_flow(random.randint(5, 15))
            
            for particle in particles:
                # 強制的にオーバーフロー
                if random.random() < 0.7:
                    particle.is_overflow = True
                    particle.position += random.uniform(20, 100)
                
                sound = self.generate_karplus_sound(particle, burst_duration)
                sound_samples = len(sound)
                
                particle_start = burst_start + random.randint(0, int(burst_duration * SAMPLE_RATE) - sound_samples)
                end_pos = min(particle_start + sound_samples, start_sample + samples)
                
                if end_pos > particle_start:
                    self.audio_buffer[particle_start:end_pos] += sound[:end_pos - particle_start] * 0.3
    
    def generate_crash(self, start_time, duration):
        """クラッシュを生成"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        # 全ての境界が崩壊
        for boundary in self.memory_space.boundaries:
            boundary.violations = 100
            boundary.resonance = 1.0
        
        # クラッシュ音
        crash_duration = duration * 0.7
        crash_samples = int(crash_duration * SAMPLE_RATE)
        
        t = np.linspace(0, crash_duration, crash_samples)
        
        # 低周波の基音
        fundamental = np.sin(2 * np.pi * 55 * t) * 0.3
        
        # 多数の高周波成分
        for i in range(10):
            freq = 440 + (i * 110)
            harmonic = np.sin(2 * np.pi * freq * t) * 0.1 / (i + 1)
            fundamental += harmonic
        
        # ノイズ成分
        noise = np.random.normal(0, 0.1, crash_samples)
        
        # エンベロープ
        envelope = np.exp(-t * 3)
        
        crash_sound = (fundamental + noise) * envelope
        
        # クラッシュ音を配置
        crash_end = min(start_sample + crash_samples, start_sample + samples)
        self.audio_buffer[start_sample:crash_end] += crash_sound[:crash_end - start_sample]
    
    def master_audio(self):
        """オーディオをマスタリング"""
        # ピーク検出
        peak = np.max(np.abs(self.audio_buffer))
        if peak > 0:
            # 正規化
            self.audio_buffer = self.audio_buffer / peak * 0.8
        
        # コンプレッション
        threshold = 0.5
        ratio = 4.0
        attack_time = 0.003
        release_time = 0.1
        
        # 簡易コンプレッサー
        envelope = np.abs(self.audio_buffer)
        gain_reduction = np.where(envelope > threshold, 
                                 threshold + (envelope - threshold) / ratio,
                                 envelope)
        gain = gain_reduction / (envelope + 1e-8)
        self.audio_buffer = self.audio_buffer * gain
        
        # 最終正規化
        peak = np.max(np.abs(self.audio_buffer))
        if peak > 0:
            self.audio_buffer = self.audio_buffer / peak * 0.9
        
        return self.audio_buffer

def generate_buffer_overflow_garden_enhanced():
    """強化版Buffer Overflow Gardenを生成"""
    print("🌱 Buffer Overflow Garden - Physical Modeling Enhancement")
    print("📍 Creating physical memory space...")
    
    garden = BufferOverflowGarden()
    
    # セクション生成
    garden.generate_section(1, 0.0, 8.0, 0.3)      # 正常操作
    garden.generate_section(2, 8.0, 8.0, 0.6)      # オーバーフロー開始
    garden.generate_section(3, 16.0, 9.0, 0.9)     # 無秩序な庭
    garden.generate_section(4, 25.0, 5.0, 1.0)      # クラッシュ
    
    # マスタリング
    print("🎚️ Mastering audio...")
    audio = garden.master_audio()
    
    # 音質分析
    rms_db = 20 * np.log10(np.sqrt(np.mean(audio**2)) + 1e-8)
    peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-8)
    dynamic_range = peak_db - rms_db
    
    print(f"📊 Audio Quality Metrics:")
    print(f"   RMS Level: {rms_db:.2f} dB")
    print(f"   Peak Level: {peak_db:.2f} dB")
    print(f"   Dynamic Range: {dynamic_range:.2f} dB")
    
    return audio

if __name__ == "__main__":
    # オーディオ生成
    audio = generate_buffer_overflow_garden_enhanced()
    
    # 保存
    output_path = "../samples/06_buffer_overflow_garden_enhanced.wav"
    wavfile.write(output_path, SAMPLE_RATE, audio.astype(np.float32))
    print(f"✅ Generated: {output_path}")
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    print(f"📊 Size: {file_size / 1024 / 1024:.2f} MB")
    print(f"⏱️ Duration: {DURATION} seconds")
    print(f"🎯 Buffer Overflow Garden Enhanced - Physical Modeling Complete")