#!/usr/bin/env python3
"""
Track 6: Buffer Overflow Garden - Advanced Version with Complex Systems
コンセプト：はみ出したデータが咲く花の複雑系物理庭園

Advancedコンセプト：
- 複雑系理論によるバッファオーバーフローの創発的表現
- カオス的フラクタル構造としてのメモリレイアウト
- 量子力学的干渉としてのデータ衝突
- 非平衡熱力学としてのエントロピー増加
- ネットワークトポロジーとしての境界相互作用

高度な物理モデリング技術：
- リアプノフ指数による安定性解析
- フラクタル次元によるオーバーフロー構造
- トポロジカル欠陥としてのバグ
- スピングラス状態としてのメモリ配置
- 相転移現象としてのクラッシュ
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.spatial import distance
from scipy.fft import fft, ifft
import random
import math
from dataclasses import dataclass
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

# パラメータ
SAMPLE_RATE = 44100
DURATION = 45  # Advanced版は長めに
NUM_DIMENSIONS = 3  # 3次元空間

@dataclass
class QuantumState:
    """量子状態を表現するデータクラス"""
    amplitude: complex
    phase: float
    energy: float
    
    def __post_init__(self):
        # 波動関数の正規化
        norm = abs(self.amplitude)
        if norm > 0:
            self.amplitude = self.amplitude / norm

class LyapunovAnalyzer:
    """リアプノフ指数によるシステム安定性解析"""
    def __init__(self, dimension=3):
        self.dimension = dimension
        self.lyapunov_spectrum = np.zeros(dimension)
        self.stability_history = []
        
    def calculate_spectrum(self, trajectory, dt=0.01):
        """リアプノフスペクトルを計算"""
        # ヤコビ行列の近似計算
        n_points = len(trajectory)
        if n_points < 10:
            return self.lyapunov_spectrum
            
        # 簡略化：隣接点間の距離の拡大率を計算
        try:
            trajectory = np.array(trajectory)
            if trajectory.ndim == 3:  # 時系列×次元
                trajectory = trajectory.reshape(trajectory.shape[0], -1)
            
            # 隣接点間の距離
            distances = []
            for i in range(1, min(50, len(trajectory))):
                dist = np.linalg.norm(trajectory[i] - trajectory[i-1])
                distances.append(dist)
            
            if len(distances) > 5:
                log_distances = np.log(np.array(distances) + 1e-10)
                time_steps = np.arange(len(log_distances)) * dt
                
                if len(time_steps) > 1:
                    coeffs = np.polyfit(time_steps, log_distances, 1)
                    self.lyapunov_spectrum[0] = max(0, coeffs[0])  # 正の値のみ
        except:
            # エラー時はデフォルト値
            self.lyapunov_spectrum[0] = 0.1
                
        return self.lyapunov_spectrum

class FractalMemory:
    """フラクタル構造を持つメモリ空間"""
    def __init__(self, depth=4, size=1024):
        self.depth = depth
        self.size = size
        self.fractal_dimension = 1.58  # 典型的なフラクタル次元
        self.memory_tree = self.build_fractal_tree()
        
    def build_fractal_tree(self):
        """フラクタルツリーを構築"""
        tree = {}
        
        def _build_node(level, start, end):
            if level >= self.depth:
                return {'type': 'leaf', 'start': start, 'end': end, 'data': []}
                
            mid = (start + end) // 2
            node = {
                'type': 'branch',
                'level': level,
                'start': start,
                'end': end,
                'left': _build_node(level + 1, start, mid),
                'right': _build_node(level + 1, mid, end)
            }
            return node
            
        return _build_node(0, 0, self.size)
    
    def calculate_fractal_dimension(self):
        """フラクタル次元を計算"""
        # ボックスカウンティング法
        scales = [2**i for i in range(1, 8)]
        counts = []
        
        for scale in scales:
            count = 0
            boxes = self.size // scale
            for i in range(boxes):
                for j in range(boxes):
                    # ボックス内のデータをカウント
                    # 簡略化のためランダムな密度分布
                    density = np.random.random()
                    if density > 0.7:
                        count += 1
            counts.append(count)
        
        # 次元計算
        if len(counts) > 1:
            log_scales = np.log(scales[:len(counts)])
            log_counts = np.log(counts)
            coeffs = np.polyfit(log_scales, -log_counts, 1)
            self.fractal_dimension = coeffs[0]
            
        return self.fractal_dimension

class TopologicalDefect:
    """トポロジカル欠陥としてのバグ"""
    def __init__(self, position, charge=1):
        self.position = position
        self.charge = charge  # 欠陥の電荷
        self.strength = abs(charge)
        self.interaction_range = 10.0
        
    def get_field_strength(self, position):
        """位置における場の強さ"""
        distance = np.linalg.norm(np.array(position) - np.array(self.position))
        if distance < 1e-10:
            distance = 1e-10
        return self.strength * self.charge / (distance ** 2)

class SpinGlassMemory:
    """スピングラス状態としてのメモリ配置"""
    def __init__(self, size=64):
        self.size = size
        self.spins = np.random.choice([-1, 1], (size, size))
        self.coupling = np.random.randn(size, size) * 0.5
        self.temperature = 2.0  # スピングラスの転移温度
        
    def calculate_energy(self):
        """エネルギーを計算"""
        energy = 0
        for i in range(self.size):
            for j in range(self.size):
                # 近傍相互作用
                neighbors = [
                    ((i+1) % self.size, j),
                    (i, (j+1) % self.size)
                ]
                for ni, nj in neighbors:
                    energy -= self.coupling[i, j] * self.spins[i, j] * self.spins[ni, nj]
        return energy / 2  # 二重カウントを回避
    
    def metropolis_step(self):
        """メトロポリス法によるスピン更新"""
        # ランダムにスピンを選択
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        
        # エネルギー変化を計算
        current_energy = self.calculate_energy()
        self.spins[i, j] *= -1
        new_energy = self.calculate_energy()
        
        delta_E = new_energy - current_energy
        
        # メトロポリス基準
        if delta_E > 0 and random.random() > math.exp(-delta_E / self.temperature):
            # 拒否
            self.spins[i, j] *= -1
            
    def update_dynamics(self, steps=100):
        """スピンダイナミクスを更新"""
        for _ in range(steps):
            self.metropolis_step()

class QuantumMemoryCell:
    """量子メモリセル"""
    def __init__(self, position):
        self.position = np.array(position)
        self.quantum_state = QuantumState(
            amplitude=complex(1.0, 0.0),
            phase=0.0,
            energy=1.0
        )
        self.classical_bit = 0
        self.coherence = 1.0
        
    def apply_quantum_gate(self, gate_type):
        """量子ゲートを適用"""
        if gate_type == "hadamard":
            # アダマールゲート
            self.quantum_state.amplitude = complex(
                self.quantum_state.amplitude.real + self.quantum_state.amplitude.imag,
                self.quantum_state.amplitude.real - self.quantum_state.amplitude.imag
            ) / math.sqrt(2)
        elif gate_type == "phase":
            # 位相ゲート
            self.quantum_state.phase += math.pi / 4
            self.quantum_state.amplitude *= complex(math.cos(self.quantum_state.phase), 
                                                   math.sin(self.quantum_state.phase))
    
    def measure(self):
        """測定による状態の収束"""
        probability = abs(self.quantum_state.amplitude) ** 2
        if random.random() < probability:
            self.classical_bit = 1
        else:
            self.classical_bit = 0
        self.coherence *= 0.9  # デコヒーレンス

class BufferOverflowGardenAdvanced:
    """高度なバッファオーバーフローの物理庭園"""
    def __init__(self):
        self.fractal_memory = FractalMemory(depth=5)
        self.lyapunov_analyzer = LyapunovAnalyzer(dimension=3)
        self.spin_glass = SpinGlassMemory(size=32)
        self.defects = []
        self.quantum_cells = []
        
        self.audio_buffer = np.zeros(int(SAMPLE_RATE * DURATION))
        self.trajectory_history = []
        self.time = 0.0
        
        self.setup_complex_system()
        
    def setup_complex_system(self):
        """複雑系を初期化"""
        # トポロジカル欠陥の配置
        for _ in range(5):
            position = np.random.rand(3) * 100
            charge = random.choice([-1, 1])
            defect = TopologicalDefect(position, charge)
            self.defects.append(defect)
        
        # 量子メモリセルの配置
        for i in range(20):
            position = np.random.rand(3) * 100
            cell = QuantumMemoryCell(position)
            # 量子状態の重ね合わせ
            cell.quantum_state.amplitude = complex(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
            self.quantum_cells.append(cell)
    
    def calculate_chaos_metric(self):
        """カオス度を計算"""
        if len(self.trajectory_history) < 10:
            return 0.0
            
        trajectory = np.array(self.trajectory_history[-100:])  # 最新100点
        lyapunov_spectrum = self.lyapunov_analyzer.calculate_spectrum(trajectory)
        
        # 最大リアプノフ指数
        max_lyapunov = np.max(lyapunov_spectrum)
        
        # フラクタル次元
        fractal_dim = self.fractal_memory.calculate_fractal_dimension()
        
        # スピングラスのエネルギー
        spin_energy = self.spin_glass.calculate_energy()
        
        # 総合カオス度
        chaos_metric = abs(max_lyapunov) * (fractal_dim - 1.0) * abs(spin_energy) / 1000
        
        return chaos_metric
    
    def generate_quantum_interference(self, start_time, duration):
        """量子干渉を音響化"""
        start_sample = int(start_time * SAMPLE_RATE)
        end_sample = int((start_time + duration) * SAMPLE_RATE)
        samples = end_sample - start_sample
        
        # 量子状態の干渉
        interference_pattern = np.zeros(samples)
        
        for i, cell in enumerate(self.quantum_cells):
            # 量子ゲートの適用
            if random.random() < 0.1:  # 10%の確率でゲート適用
                cell.apply_quantum_gate(random.choice(["hadamard", "phase"]))
            
            # 測定
            cell.measure()
            
            # 干渉パターンの生成
            freq = 220 + (cell.position[0] * 5) + (cell.classical_bit * 100)
            t = np.linspace(0, duration, samples)
            
            # 量子コヒーレンスによる位相
            phase = cell.quantum_state.phase * cell.coherence
            wave = np.sin(2 * np.pi * freq * t + phase)
            
            # エネルギーによる振幅
            amplitude = cell.quantum_state.energy * cell.coherence * 0.1
            interference_pattern += wave * amplitude
        
        # バッファに追加
        self.audio_buffer[start_sample:end_sample] += interference_pattern * 0.3
    
    def generate_fractal_structure(self, start_time, duration):
        """フラクタル構造を音響化"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        # フラクタルノイズの生成
        fractal_noise = np.zeros(samples)
        
        # オクターブバンドによるフラクタル
        num_octaves = 6
        base_freq = 55  # A1
        
        for octave in range(num_octaves):
            freq = base_freq * (2 ** octave)
            amplitude = 1.0 / (2 ** octave)
            
            t = np.linspace(0, duration, samples)
            wave = np.sin(2 * np.pi * freq * t)
            
            # フラクタル次元による変調
            fractal_dim = self.fractal_memory.fractal_dimension
            if fractal_dim > 0:
                wave *= amplitude ** fractal_dim
            
            fractal_noise += wave
        
        # 正規化
        if np.max(np.abs(fractal_noise)) > 0:
            fractal_noise = fractal_noise / np.max(np.abs(fractal_noise)) * 0.2
        
        # バッファに追加
        self.audio_buffer[start_sample:start_sample + samples] += fractal_noise
    
    def generate_topological_defects(self, start_time, duration):
        """トポロジカル欠陥を音響化"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        defect_sound = np.zeros(samples)
        
        for defect in self.defects:
            # 欠陥の場の周波数
            base_freq = 110 + (defect.charge * 50) + (defect.strength * 20)
            
            t = np.linspace(0, duration, samples)
            
            # 場の強さによる振幅変調
            for i in range(0, samples, 10):
                pos = [i / samples * 100, random.random() * 100, random.random() * 100]
                field_strength = defect.get_field_strength(pos)
                
                # 周波数変調
                freq_mod = base_freq * (1 + field_strength * 0.1)
                wave = np.sin(2 * np.pi * freq_mod * t[i:i+10])
                amplitude = min(0.1, field_strength * 0.01)
                
                defect_sound[i:i+10] += wave * amplitude
        
        # バッファに追加
        self.audio_buffer[start_sample:start_sample + samples] += defect_sound
    
    def generate_spin_glass_dynamics(self, start_time, duration):
        """スピングラスダイナミクスを音響化"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        # スピンダイナミクスの更新
        self.spin_glass.update_dynamics(steps=50)
        
        # エネルギーに基づく音響生成
        energy = self.spin_glass.calculate_energy()
        
        t = np.linspace(0, duration, samples)
        
        # エネルギーに基づく基本周波数
        base_freq = 220 + abs(energy) * 10
        
        # スピン配置による音響
        spin_sound = np.zeros(samples)
        
        for i in range(0, self.spin_glass.size, 2):
            for j in range(0, self.spin_glass.size, 2):
                # スピンの相互作用
                spin_product = self.spin_glass.spins[i, j] * self.spin_glass.spins[(i+1) % self.spin_glass.size, j]
                
                # 局所的な周波数
                local_freq = base_freq * (1 + spin_product * 0.1)
                
                wave = np.sin(2 * np.pi * local_freq * t)
                amplitude = 0.01  # 小さな振幅
                
                spin_sound += wave * amplitude
        
        # 正規化
        if np.max(np.abs(spin_sound)) > 0:
            spin_sound = spin_sound / np.max(np.abs(spin_sound)) * 0.15
        
        # バッファに追加
        self.audio_buffer[start_sample:start_sample + samples] += spin_sound
    
    def generate_phase_transition(self, start_time, duration):
        """相転移現象を音響化"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        # 温度変化による相転移
        initial_temp = 5.0
        final_temp = 0.5
        
        t = np.linspace(0, duration, samples)
        temperature = initial_temp + (final_temp - initial_temp) * (t / duration)
        
        # 相転移音
        transition_sound = np.zeros(samples)
        
        for i, temp in enumerate(temperature):
            # 温度に応じた周波数
            if temp > 2.5:  # 高温相
                freq = 440
                amplitude = 0.1
            elif temp > 1.5:  # 転移領域
                freq = 220 + random.uniform(-50, 50)  # ゆらぎ
                amplitude = 0.2
            else:  # 低温相
                freq = 110
                amplitude = 0.05
            
            # トランジェント生成
            if i < samples - 1:
                wave = np.sin(2 * np.pi * freq * t[i:i+1]) * amplitude
                transition_sound[i:i+1] += wave
        
        # バッファに追加
        self.audio_buffer[start_sample:start_sample + samples] += transition_sound
    
    def generate_chaotic_overflow(self, start_time, duration):
        """カオス的オーバーフローを生成"""
        start_sample = int(start_time * SAMPLE_RATE)
        samples = int(duration * SAMPLE_RATE)
        
        # カオス度の計算
        chaos_metric = self.calculate_chaos_metric()
        
        # ローレンツアトラクタによるカオス生成
        def lorenz_system(x, y, z, sigma=10, rho=28, beta=8/3):
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            return dx, dy, dz
        
        # カオス軌道の生成
        trajectory = []
        x, y, z = 1.0, 1.0, 1.0
        dt = 0.01
        
        for _ in range(samples // 10):
            dx, dy, dz = lorenz_system(x, y, z)
            x += dx * dt
            y += dy * dt
            z += dz * dt
            
            trajectory.append([x, y, z])
            
            # 軌道履歴の保存
            self.trajectory_history.append([x, y, z])
        
        # 軌道を音響化
        chaotic_sound = np.zeros(samples)
        
        for i, point in enumerate(trajectory):
            # 各座標を周波数にマッピング
            freq_x = 220 + (point[0] * 10)
            freq_y = 330 + (point[1] * 10)
            freq_z = 440 + (point[2] * 10)
            
            # 音響生成
            t_sub = np.linspace(0, duration / len(trajectory), 10)
            
            wave_x = np.sin(2 * np.pi * freq_x * t_sub) * 0.1
            wave_y = np.sin(2 * np.pi * freq_y * t_sub) * 0.1
            wave_z = np.sin(2 * np.pi * freq_z * t_sub) * 0.1
            
            combined = wave_x + wave_y + wave_z
            
            # 配置
            pos = i * 10
            if pos + len(combined) < samples:
                chaotic_sound[pos:pos + len(combined)] += combined
        
        # カオス度による変調
        if np.max(np.abs(chaotic_sound)) > 0:
            chaotic_sound = chaotic_sound / np.max(np.abs(chaotic_sound)) * (0.1 + chaos_metric)
        
        # バッファに追加
        self.audio_buffer[start_sample:start_sample + samples] += chaotic_sound
    
    def generate_advanced_sections(self):
        """高度なセクションを生成"""
        print("🌱 Generating Advanced Buffer Overflow Garden...")
        
        # セクション1: 量子干渉 (0-10秒)
        print("🔬 Section 1: Quantum Interference...")
        self.generate_quantum_interference(0.0, 10.0)
        
        # セクション2: フラクタル構造 (10-20秒)
        print("🌀 Section 2: Fractal Structure...")
        self.generate_fractal_structure(10.0, 10.0)
        
        # セクション3: トポロジカル欠陥 (20-27秒)
        print("🕸️ Section 3: Topological Defects...")
        self.generate_topological_defects(20.0, 7.0)
        
        # セクション4: スピングラスダイナミクス (27-35秒)
        print("🧲 Section 4: Spin Glass Dynamics...")
        self.generate_spin_glass_dynamics(27.0, 8.0)
        
        # セクション5: 相転移現象 (35-40秒)
        print("🔄 Section 5: Phase Transition...")
        self.generate_phase_transition(35.0, 5.0)
        
        # セクション6: カオス的オーバーフロー (40-45秒)
        print("🌪️ Section 6: Chaotic Overflow...")
        self.generate_chaotic_overflow(40.0, 5.0)
    
    def master_audio_advanced(self):
        """高度なオーディオマスタリング"""
        # マルチバンド処理
        from scipy.signal import butter, filtfilt
        
        def butter_bandpass(lowcut, highcut, fs, order=5):
            nyq = 0.5 * fs
            low = lowcut / nyq
            high = highcut / nyq
            b, a = butter(order, [low, high], btype='band')
            return b, a
        
        # 低域（60-250Hz）
        b_low, a_low = butter_bandpass(60, 250, SAMPLE_RATE, order=4)
        low_band = filtfilt(b_low, a_low, self.audio_buffer)
        
        # 中域（250-4000Hz）
        b_mid, a_mid = butter_bandpass(250, 4000, SAMPLE_RATE, order=4)
        mid_band = filtfilt(b_mid, a_mid, self.audio_buffer)
        
        # 高域（4000-16000Hz）
        b_high, a_high = butter_bandpass(4000, 16000, SAMPLE_RATE, order=4)
        high_band = filtfilt(b_high, a_high, self.audio_buffer)
        
        # バンドごとの処理
        # 低域：コンプレッション
        low_compressed = self.apply_compression(low_band, threshold=-20, ratio=4)
        
        # 中域：イコライゼーション
        mid_equalized = mid_band * 1.2  # 中域をブースト
        
        # 高域：Exciter
        high_excited = self.apply_exciter(high_band)
        
        # 再合成
        processed_audio = low_compressed + mid_equalized + high_excited
        
        # ステレオ拡張
        stereo_audio = self.create_stereo_image(processed_audio)
        
        # 最終マスタリング
        final_audio = self.final_mastering(stereo_audio)
        
        return final_audio
    
    def apply_compression(self, audio, threshold=-20, ratio=4):
        """コンプレッションを適用"""
        threshold_linear = 10 ** (threshold / 20)
        gain_reduction = np.where(np.abs(audio) > threshold_linear,
                                 threshold_linear + (np.abs(audio) - threshold_linear) / ratio,
                                 np.abs(audio))
        gain = gain_reduction / (np.abs(audio) + 1e-8)
        return audio * gain
    
    def apply_exciter(self, audio):
        """ハーモニックエキサイターを適用"""
        # 高調波生成
        harmonics = np.abs(audio) ** 1.5 * np.sign(audio)
        # 原音との混合
        excited = audio + 0.3 * harmonics
        return excited
    
    def create_stereo_image(self, mono_audio):
        """ステレオイメージを作成"""
        # 左右にわずかな遅延と位相シフト
        left_channel = mono_audio
        right_channel = np.roll(mono_audio, 10)  # サンプル遅延
        
        # 位相シフト
        right_channel = right_channel * 0.9
        
        # ステレオミックス
        stereo_audio = np.zeros((len(mono_audio), 2))
        stereo_audio[:, 0] = left_channel
        stereo_audio[:, 1] = right_channel
        
        return stereo_audio
    
    def final_mastering(self, stereo_audio):
        """最終マスタリング"""
        # リミッター
        limit_threshold = -0.3
        limit_linear = 10 ** (limit_threshold / 20)
        
        # ピーククリップ
        stereo_audio = np.clip(stereo_audio, -limit_linear, limit_linear)
        
        # 最終正規化
        peak = np.max(np.abs(stereo_audio))
        if peak > 0:
            stereo_audio = stereo_audio / peak * 0.95
        
        return stereo_audio

def generate_buffer_overflow_garden_advanced():
    """高度なBuffer Overflow Gardenを生成"""
    print("🌱 Buffer Overflow Garden - Advanced Complex Systems Version")
    print("📍 Creating complex physical memory space...")
    
    garden = BufferOverflowGardenAdvanced()
    
    # 高度なセクション生成
    garden.generate_advanced_sections()
    
    # 高度なマスタリング
    print("🎚️ Advanced mastering...")
    audio = garden.master_audio_advanced()
    
    # 音質分析
    if len(audio.shape) == 1:
        # モノラルの場合
        rms_db = 20 * np.log10(np.sqrt(np.mean(audio**2)) + 1e-8)
        peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-8)
    else:
        # ステレオの場合
        rms_db = 20 * np.log10(np.sqrt(np.mean(audio**2)) + 1e-8)
        peak_db = 20 * np.log10(np.max(np.abs(audio)) + 1e-8)
    
    dynamic_range = peak_db - rms_db
    
    print(f"📊 Advanced Audio Quality Metrics:")
    print(f"   RMS Level: {rms_db:.2f} dB")
    print(f"   Peak Level: {peak_db:.2f} dB")
    print(f"   Dynamic Range: {dynamic_range:.2f} dB")
    
    # カオス度の最終計算
    chaos_metric = garden.calculate_chaos_metric()
    print(f"🌀 Chaos Metric: {chaos_metric:.4f}")
    
    # フラクタル次元
    fractal_dim = garden.fractal_memory.calculate_fractal_dimension()
    print(f"📐 Fractal Dimension: {fractal_dim:.4f}")
    
    return audio

if __name__ == "__main__":
    # オーディオ生成
    audio = generate_buffer_overflow_garden_advanced()
    
    # 保存
    output_path = "06_buffer_overflow_garden_advanced.wav"
    wavfile.write(output_path, SAMPLE_RATE, audio.astype(np.float32))
    print(f"✅ Generated: {output_path}")
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    print(f"📊 Size: {file_size / 1024 / 1024:.2f} MB")
    print(f"⏱️ Duration: {DURATION} seconds")
    print(f"🎯 Buffer Overflow Garden Advanced - Complex Systems Complete")