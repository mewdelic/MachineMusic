#!/usr/bin/env python3
"""
Memory Leak Lullaby Advanced - 複雑系理論による高度な物理モデリング

メモリリークを「記憶の徐々なる消失」として捉え、
複雑系理論（自己組織性、相転移、カオス的記憶構造）を用いて表現する。

Advanced版の特徴：
- 量子記憶干渉によるメモリ状態の重ね合わせ
- スピングラス的記憶構造の緩和現象
- 相転移によるクリーンアップと再形成
- カオス的記憶トラッキングのアトラクタ構造
- 複雑系フラクタル記憶空間の進化
- 自己組織的記憶ゴミ集積現象

技術的特徴：
- 6つの異なる物理セクション
- ステレオ音声と高度なマスタリング
- 複雑系パラメータのリアルタイム評価
"""

import numpy as np
import scipy.signal
import scipy.fft
from scipy.io import wavfile
import matplotlib.pyplot as plt
import soundfile as sf

class MemoryLeakLullabyAdvanced:
    def __init__(self, duration=60, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.total_samples = int(duration * sample_rate)
        
        # 複雑系パラメータ
        self.memory_capacity = 1000
        self.quantum_memory_states = 20
        self.spin_glass_size = 16
        self.fractal_memory_dimension = 1.8
        self.chaos_memory_strength = 0.3
        
        # 音響パラメータ
        self.base_frequency = 220.0  # A3音
        self.memory_decay_rate = 0.995
        self.noise_floor = -60.0  # dB
        
        # 出力配列
        self.left_channel = np.zeros(self.total_samples)
        self.right_channel = np.zeros(self.total_samples)
        
    def generate_quantum_memory_interference(self, start_time, end_time):
        """
        セクション1: 量子記憶干渉 (0-10秒)
        量子メモリ状態の重ね合わせと干渉によるメモリ状態の揺らぎ
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # 量子メモリ状態の生成
        memory_states = []
        for i in range(self.quantum_memory_states):
            # 各メモリ状態は複素数で表現（振幅と位相）
            amplitude = np.random.uniform(0.1, 1.0)
            phase = np.random.uniform(0, 2 * np.pi)
            frequency = self.base_frequency * (1 + 0.1 * i)
            
            # 量子状態の時間発展
            decay = np.exp(-0.1 * t)
            state = amplitude * decay * np.exp(1j * (2 * np.pi * frequency * t + phase))
            memory_states.append(state)
        
        # 量子状態の干渉
        interference = np.sum(memory_states, axis=0)
        
        # 実部を音声信号として抽出
        quantum_signal = np.real(interference)
        
        # メモリリークによる干渉の不安定化
        leak_factor = 1 - (t / (end_time - start_time)) ** 2
        quantum_signal *= leak_factor
        
        # 周波数フィルタリング（低域通過）
        filtered_signal = self._lowpass_filter(quantum_signal, 1000)
        
        return filtered_signal
    
    def generate_spin_glass_memory_relaxation(self, start_time, end_time):
        """
        セクション2: スピングラス的記憶構造の緩和 (10-20秒)
        スピングラスモデルによるメモリの緩和現象とフラストレーション
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        # 16x16 スピングラスの初期化
        spins = np.random.choice([-1, 1], (self.spin_glass_size, self.spin_glass_size))
        
        # ランダム相互作用（フラストレーションを含む）
        J_h = np.random.uniform(-1, 1, (self.spin_glass_size, self.spin_glass_size))
        J_v = np.random.uniform(-1, 1, (self.spin_glass_size, self.spin_glass_size))
        
        # メモリ状態の追跡
        memory_decay = np.zeros(samples)
        signal = np.zeros(samples)
        
        for i in range(samples):
            # 温度の時間減少（緩和過程）
            temperature = 2.0 * np.exp(-i / (samples * 0.3))
            
            if temperature > 0.1:
                # メトロポリス法によるスピン更新
                for _ in range(self.spin_glass_size):
                    x, y = np.random.randint(0, self.spin_glass_size, 2)
                    
                    # エネルギー差の計算
                    energy_diff = 2 * spins[x, y] * (
                        J_h[x, (y+1) % self.spin_glass_size] * spins[x, (y+1) % self.spin_glass_size] +
                        J_h[x, (y-1) % self.spin_glass_size] * spins[x, (y-1) % self.spin_glass_size] +
                        J_v[(x+1) % self.spin_glass_size, y] * spins[(x+1) % self.spin_glass_size, y] +
                        J_v[(x-1) % self.spin_glass_size, y] * spins[(x-1) % self.spin_glass_size, y]
                    )
                    
                    # メトロポリス基準
                    if energy_diff < 0 or np.random.random() < np.exp(-energy_diff / temperature):
                        spins[x, y] *= -1
            
            # 磁化の計算（記憶状態）
            magnetization = np.sum(spins) / (self.spin_glass_size ** 2)
            memory_decay[i] = abs(magnetization)
            
            # 磁化を音声周波数にマッピング
            frequency = self.base_frequency * (1 + 0.5 * magnetization)
            signal[i] = 0.1 * np.sin(2 * np.pi * frequency * i / self.sample_rate)
        
        # メモリリークによる減衰
        leak_envelope = np.exp(-0.5 * np.linspace(0, 1, samples))
        signal *= leak_envelope
        
        return signal
    
    def generate_phase_transition_cleanup(self, start_time, end_time):
        """
        セクション3: 相転移によるクリーンアップ (20-30秒)
        高温相から低温相への相転移によるメモリクリーンアップ
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # 温度スケジューリング（高温→低温）
        critical_temperature = 2.27  # 2Dイジング模型の臨界温度
        temperatures = np.linspace(critical_temperature * 2, critical_temperature * 0.5, samples)
        
        # 相転移パラメータ
        order_parameter = np.zeros(samples)
        signal = np.zeros(samples)
        
        for i, temp in enumerate(temperatures):
            # 秩序パラメータの計算
            if temp > critical_temperature:
                # 高温相：無秩序
                order_parameter[i] = 0
            else:
                # 低温相：秩序
                order_parameter[i] = 1 - (temp / critical_temperature) ** 2
            
            # 秩序パラメータを音声特性にマッピング
            # 高温相：ノイジー、低温相：調和的
            if temp > critical_temperature:
                # 高温相：広帯域ノイズ
                noise = np.random.normal(0, 0.1)
                signal[i] = noise * (temp / (critical_temperature * 2))
            else:
                # 低温相：調和音
                clean_freq = self.base_frequency * (1 + order_parameter[i])
                signal[i] = 0.2 * np.sin(2 * np.pi * clean_freq * t[i]) * order_parameter[i]
        
        # 相転移臨界点での共鳴現象
        critical_region = np.abs(temperatures - critical_temperature) < 0.1
        signal[critical_region] *= 2.0  # 臨界現象の増幅
        
        return signal
    
    def generate_chaotic_memory_tracking(self, start_time, end_time):
        """
        セクション4: カオス的記憶トラッキング (30-40秒)
        カオスアトラクタによるメモリアドレスの軌道追跡
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        # ヘノンアトラクタパラメータ（記憶アドレスのカオス的振る舞い）
        a = 1.4
        b = 0.3
        
        # 初期条件（メモリアドレス）
        x, y = 0.1, 0.1
        
        # 軌道の記録
        trajectory_x = np.zeros(samples)
        trajectory_y = np.zeros(samples)
        
        for i in range(samples):
            # ヘノン写像
            x_new = 1 - a * x**2 + y
            y_new = b * x
            
            trajectory_x[i] = x_new
            trajectory_y[i] = y_new
            
            x, y = x_new, y_new
        
        # 軌道を音声周波数にマッピング
        signal = np.zeros(samples)
        
        for i in range(samples):
            # x座標を周波数、y座標を振幅にマッピング
            freq = self.base_frequency * (1 + 0.5 * trajectory_x[i])
            amplitude = 0.1 * (1 + trajectory_y[i])
            
            signal[i] = amplitude * np.sin(2 * np.pi * freq * i / self.sample_rate)
        
        # カオス的メモリリーク：軌道の安定性の喪失
        chaos_factor = 1 - np.exp(-0.1 * np.arange(samples) / self.sample_rate)
        signal *= (1 - chaos_factor * self.chaos_memory_strength)
        
        return signal
    
    def generate_fractal_memory_space(self, start_time, end_time):
        """
        セクション5: 複雑系フラクタル記憶空間 (40-50秒)
        フラクタル構造を持つ記憶空間の進化
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # フラクタルブラウンノイズの生成
        # 1/fノイズ（ピンクノイズ）でフラクタル次元を制御
        white_noise = np.random.normal(0, 1, samples)
        
        # FFTによる1/fノイズ生成
        fft_freq = np.fft.fftfreq(samples, 1/self.sample_rate)
        fft_freq[0] = 1  # DC成分を避ける
        
        # 1/f特性のフィルタ
        filter_power = 0.5 * (2 - self.fractal_memory_dimension)
        fft_filter = np.abs(fft_freq) ** (-filter_power)
        fft_filter[0] = 1  # DC成分
        
        # フィルタリング
        fft_noise = np.fft.fft(white_noise)
        fractal_noise = np.fft.ifft(fft_noise * fft_filter).real
        
        # 正規化
        fractal_noise = fractal_noise / np.max(np.abs(fractal_noise)) * 0.1
        
        # フラクタル構造の時間発展（メモリ空間の拡大）
        growth_factor = 1 + 0.5 * t / (end_time - start_time)
        fractal_signal = fractal_noise * growth_factor
        
        # メモリ断片の重畳（フラクタル的自己相似性）
        for scale in [0.5, 0.25, 0.125]:
            scaled_signal = self._scale_signal(fractal_signal, scale)
            fractal_signal += 0.3 * scaled_signal
        
        return fractal_signal
    
    def generate_self_organized_memory_garbage(self, start_time, end_time):
        """
        セクション6: 自己組織的記憶ゴミ集積 (50-60秒)
        自己組織性によるメモリゴミの集積現象
        """
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        samples = end_sample - start_sample
        
        t = np.linspace(0, end_time - start_time, samples)
        
        # メモリセルの自己組織化モデル
        num_cells = 50
        cell_positions = np.random.uniform(0, 1, num_cells)
        cell_memory = np.random.uniform(0, 1, num_cells)
        
        # 自己組織化パラメータ
        interaction_range = 0.1
        organization_strength = 0.1
        
        signal = np.zeros(samples)
        
        for i in range(samples):
            # 時間発展
            cell_positions += np.random.normal(0, 0.01, num_cells)
            cell_memory *= self.memory_decay_rate  # メモリの減衰
            
            # 相互作用による自己組織化
            forces = np.zeros(num_cells)
            for j in range(num_cells):
                for k in range(j+1, num_cells):
                    distance = abs(cell_positions[j] - cell_positions[k])
                    if distance < interaction_range:
                        # 引力（類似したメモリは集まる）
                        force = organization_strength * (1 - distance / interaction_range)
                        if cell_memory[j] > 0.5 and cell_memory[k] > 0.5:
                            forces[j] += force * np.sign(cell_positions[k] - cell_positions[j])
                            forces[k] += force * np.sign(cell_positions[j] - cell_positions[k])
            
            # 位置の更新
            cell_positions += forces * 0.01
            
            # 集積現象の音声化
            cluster_density = self._calculate_cluster_density(cell_positions, cell_memory)
            frequency = self.base_frequency * (1 + cluster_density)
            
            signal[i] = 0.05 * np.sin(2 * np.pi * frequency * t[i]) * cluster_density
        
        # ゴミ集積の断続的爆発現象
        garbage_bursts = np.random.random(samples) < 0.001  # 稀なバースト
        signal[garbage_bursts] *= 5.0
        
        return signal
    
    def _lowpass_filter(self, signal, cutoff_freq):
        """低域通過フィルタ"""
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_freq / nyquist
        b, a = scipy.signal.butter(4, normalized_cutoff, btype='low')
        return scipy.signal.filtfilt(b, a, signal)
    
    def _scale_signal(self, signal, scale_factor):
        """信号のスケーリング"""
        scaled_length = int(len(signal) * scale_factor)
        if scaled_length == 0:
            return np.zeros_like(signal)
        
        # 線形補間によるスケーリング
        indices = np.linspace(0, len(signal) - 1, scaled_length)
        scaled_signal = np.interp(indices, np.arange(len(signal)), signal)
        
        # 元の長さに再スケーリング
        return np.interp(np.arange(len(signal)), indices, scaled_signal)
    
    def _calculate_cluster_density(self, positions, memory_values):
        """クラスタ密度の計算"""
        # メモリ値が高いセルのみを考慮
        active_positions = positions[memory_values > 0.5]
        
        if len(active_positions) < 2:
            return 0
        
        # 平均最近傍距離
        distances = []
        for i, pos in enumerate(active_positions):
            other_positions = np.delete(active_positions, i)
            min_distance = np.min(np.abs(other_positions - pos))
            distances.append(min_distance)
        
        # 距離が小さいほど密度が高い
        mean_distance = np.mean(distances)
        density = 1 / (1 + mean_distance * 10)
        
        return density
    
    def generate_stereo_signal(self):
        """ステレオ信号の生成"""
        # 各セクションの生成
        sections = [
            (0, 10, self.generate_quantum_memory_interference),
            (10, 20, self.generate_spin_glass_memory_relaxation),
            (20, 30, self.generate_phase_transition_cleanup),
            (30, 40, self.generate_chaotic_memory_tracking),
            (40, 50, self.generate_fractal_memory_space),
            (50, 60, self.generate_self_organized_memory_garbage)
        ]
        
        for start_time, end_time, generator in sections:
            # モノラル信号生成
            mono_signal = generator(start_time, end_time)
            
            # ステレオ配置
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            
            # 左右チャンネルに別の効果を適用
            # 左チャンネル：空間的広がり
            left_signal = mono_signal * np.linspace(0.7, 1.0, len(mono_signal))
            
            # 右チャンネル：時間的遅延による深み
            delay_samples = int(0.01 * self.sample_rate)  # 10ms遅延
            right_signal = np.zeros_like(mono_signal)
            if delay_samples < len(mono_signal):
                right_signal[delay_samples:] = mono_signal[:-delay_samples] * np.linspace(1.0, 0.7, len(mono_signal) - delay_samples)
            
            # メイン信号に混合
            self.left_channel[start_sample:end_sample] += left_signal
            self.right_channel[start_sample:end_sample] += right_signal
    
    def apply_mastering(self):
        """マスタリング処理"""
        # 1. ノーマライズ
        max_left = np.max(np.abs(self.left_channel))
        max_right = np.max(np.abs(self.right_channel))
        max_level = max(max_left, max_right)
        
        if max_level > 0:
            self.left_channel /= max_level
            self.right_channel /= max_level
        
        # 2. コンプレッション（マルチバンド）
        # 低域、中域、高域に分割
        low_cutoff = 200
        high_cutoff = 2000
        
        # フィルタ設計
        b_low, a_low = scipy.signal.butter(4, low_cutoff / (self.sample_rate/2), btype='low')
        b_mid, a_mid = scipy.signal.butter(4, [low_cutoff / (self.sample_rate/2), high_cutoff / (self.sample_rate/2)], btype='band')
        b_high, a_high = scipy.signal.butter(4, high_cutoff / (self.sample_rate/2), btype='high')
        
        # 各バンドに分離
        left_low = scipy.signal.filtfilt(b_low, a_low, self.left_channel)
        left_mid = scipy.signal.filtfilt(b_mid, a_mid, self.left_channel)
        left_high = scipy.signal.filtfilt(b_high, a_high, self.left_channel)
        
        right_low = scipy.signal.filtfilt(b_low, a_low, self.right_channel)
        right_mid = scipy.signal.filtfilt(b_mid, a_mid, self.right_channel)
        right_high = scipy.signal.filtfilt(b_high, a_high, self.right_channel)
        
        # コンプレッション（簡易的なソフトクリップ）
        def soft_clip(signal, threshold=0.8):
            return np.tanh(signal / threshold) * threshold
        
        left_low = soft_clip(left_low * 0.8)
        left_mid = soft_clip(left_mid * 0.9)
        left_high = soft_clip(left_high * 0.7)
        
        right_low = soft_clip(right_low * 0.8)
        right_mid = soft_clip(right_mid * 0.9)
        right_high = soft_clip(right_high * 0.7)
        
        # 再結合
        self.left_channel = left_low + left_mid + left_high
        self.right_channel = right_low + right_mid + right_high
        
        # 3. ステレオイメージ拡張
        mid = (self.left_channel + self.right_channel) / 2
        side = (self.left_channel - self.right_channel) / 2
        
        # サイド信号の拡張
        side_enhancement = 1.2
        side *= side_enhancement
        
        # 再結合
        self.left_channel = mid + side
        self.right_channel = mid - side
        
        # 4. 最終リミッティング
        final_limit = 0.95
        self.left_channel = np.clip(self.left_channel, -final_limit, final_limit)
        self.right_channel = np.clip(self.right_channel, -final_limit, final_limit)
        
        # 5. ノイズフロアの追加
        noise_floor = np.random.normal(0, 0.0001, len(self.left_channel))
        self.left_channel += noise_floor
        self.right_channel += np.random.normal(0, 0.0001, len(self.right_channel))
    
    def save_audio(self, filename):
        """オーディオファイルの保存"""
        # 16bit整数に変換
        audio_data = np.column_stack((self.left_channel, self.right_channel))
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # WAVファイルとして保存
        wavfile.write(filename, self.sample_rate, audio_data)
        print(f"Audio saved to: {filename}")
    
    def analyze_complexity(self):
        """複雑系パラメータの分析"""
        # 左右チャンネルの平均を解析
        mono_signal = (self.left_channel + self.right_channel) / 2
        
        # フラクタル次元の推定（ボックスカウンティング法の簡易版）
        def estimate_fractal_dimension(signal):
            # 信号を2値化
            binary_signal = signal > np.mean(signal)
            
            # 異なるスケールでのカウント
            scales = [1, 2, 4, 8, 16, 32, 64]
            counts = []
            
            for scale in scales:
                # スケールダウン
                scaled_length = len(signal) // scale
                if scaled_length == 0:
                    continue
                    
                scaled_signal = binary_signal[:scaled_length * scale].reshape(-1, scale)
                box_count = np.any(scaled_signal, axis=1).sum()
                counts.append(box_count)
            
            if len(counts) < 2:
                return 1.0
            
            # 対数プロットでの傾き
            log_scales = np.log(scales[:len(counts)])
            log_counts = np.log(counts)
            
            # 線形回帰
            slope = np.polyfit(log_scales, log_counts, 1)[0]
            dimension = 2 - slope
            
            return max(1.0, min(2.0, dimension))
        
        # リアプノフ指数の推定（簡易版）
        def estimate_lyapunov_exponent(signal):
            # 近隣軌道の発散の平均
            window_size = 1000
            if len(signal) < window_size * 2:
                return 0.0
            
            divergences = []
            for i in range(0, len(signal) - window_size, window_size // 2):
                segment1 = signal[i:i+window_size]
                segment2 = signal[i+window_size//2:i+window_size//2+window_size]
                
                # 発散の計算
                divergence = np.mean((segment1 - segment2) ** 2)
                divergences.append(divergence)
            
            if not divergences:
                return 0.0
            
            # 発散の対数の平均
            avg_divergence = np.mean(divergences)
            if avg_divergence > 0:
                return np.log(avg_divergence)
            else:
                return 0.0
        
        # 複雑性メトリックの計算
        fractal_dim = estimate_fractal_dimension(mono_signal)
        lyapunov_exp = estimate_lyapunov_exponent(mono_signal)
        
        # スペクトルエントロピー
        fft_spectrum = np.abs(np.fft.fft(mono_signal))
        spectrum_normalized = fft_spectrum / np.sum(fft_spectrum)
        spectral_entropy = -np.sum(spectrum_normalized * np.log(spectrum_normalized + 1e-10))
        
        return {
            'fractal_dimension': fractal_dim,
            'lyapunov_exponent': lyapunov_exp,
            'spectral_entropy': spectral_entropy,
            'signal_energy': np.sum(mono_signal ** 2) / len(mono_signal),
            'dynamic_range': 20 * np.log10((np.max(np.abs(mono_signal)) + 1e-10) / (np.std(mono_signal) + 1e-10))
        }

def main():
    """メイン処理"""
    print("Memory Leak Lullaby Advanced - 複雑系理論による高度な物理モデリング")
    print("=" * 60)
    
    # インスタンス生成
    mll_advanced = MemoryLeakLullabyAdvanced(duration=60)
    
    print("1. ステレオ信号生成中...")
    mll_advanced.generate_stereo_signal()
    
    print("2. マスタリング処理中...")
    mll_advanced.apply_mastering()
    
    print("3. 複雑性分析中...")
    complexity_metrics = mll_advanced.analyze_complexity()
    
    print("4. オーディオファイル保存中...")
    output_filename = "05_memory_leak_lullaby_advanced.wav"
    mll_advanced.save_audio(output_filename)
    
    print("\n" + "=" * 60)
    print("🎵 Memory Leak Lullaby Advanced 生成完了！")
    print("=" * 60)
    print(f"ファイル名: {output_filename}")
    print(f"収録時間: {mll_advanced.duration}秒")
    print(f"サンプルレート: {mll_advanced.sample_rate}Hz")
    print(f"音声形式: ステレオWAV")
    print()
    print("🔬 複雑系パラメータ:")
    print(f"  • フラクタル次元: {complexity_metrics['fractal_dimension']:.4f}")
    print(f"  • リアプノフ指数: {complexity_metrics['lyapunov_exponent']:.4f}")
    print(f"  • スペクトルエントロピー: {complexity_metrics['spectral_entropy']:.4f}")
    print(f"  • 信号エネルギー: {complexity_metrics['signal_energy']:.6f}")
    print(f"  • ダイナミックレンジ: {complexity_metrics['dynamic_range']:.2f}dB")
    print()
    print("🎼 構成セクション:")
    print("  1. 量子記憶干渉 (0-10秒)")
    print("     - 量子メモリ状態の重ね合わせと干渉")
    print("     - メモリリークによる不安定化")
    print()
    print("  2. スピングラス的記憶構造の緩和 (10-20秒)")
    print("     - フラストレーションを持つメモリ緩和")
    print("     - メトロポリス法によるスピンダイナミクス")
    print()
    print("  3. 相転移によるクリーンアップ (20-30秒)")
    print("     - 高温相→低温相の相転移")
    print("     - 臨界現象による共鳴")
    print()
    print("  4. カオス的記憶トラッキング (30-40秒)")
    print("     - ヘノンアトラクタによるメモリ軌道")
    print("     - カオス的メモリリーク")
    print()
    print("  5. 複雑系フラクタル記憶空間 (40-50秒)")
    print("     - フラクタル構造の記憶空間")
    print("     - 自己相似的なメモリ断片")
    print()
    print("  6. 自己組織的記憶ゴミ集積 (50-60秒)")
    print("     - メモリゴミの自己組織的集積")
    print("     - 断続的バースト現象")
    print()
    print("🎨 芸術的コンセプト:")
    print("「Memory Leak Lullaby Advanced」は、メモリリークを単なる")
    print("技術的な問題としてではなく、複雑系が示す美しい現象と")
    print("して表現しました。量子からスケールまで、異なるレベルの")
    print("記憶現象が音楽を通じて統合され、聴き手に新たな科学的")
    print("洞察と芸術的感動を提供します。")
    print()
    print("✨ Advanced版の特徴:")
    print("- 複雑系理論の統合的な音楽的応用")
    print("- 6つの異なる物理モデルによる多層的表現")
    print("- 学術的概念の直感的音響化")
    print("- 高度なマスタリングとステレオ音響")

if __name__ == "__main__":
    main()