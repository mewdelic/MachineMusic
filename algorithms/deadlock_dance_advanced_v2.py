#!/usr/bin/env python3
"""
Deadlock Dance Advanced - 高度な物理モデリングによるデッドロックの音響化

複数のプロセスが互いに待機するデッドロック状態を、
複雑な相互作用とカオス的振る舞いとして表現。
"""

import numpy as np
import scipy.signal
from scipy.io import wavfile
import soundfile as sf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

class DeadlockDanceAdvanced:
    def __init__(self, sample_rate=44100, duration=240):
        self.sample_rate = sample_rate
        self.duration = duration
        self.time = np.linspace(0, duration, int(sample_rate * duration))
        
        # デッドロックのプロセス数
        self.num_processes = 4
        
        # 物理パラメータ
        self.coupling_strength = 0.8  # プロセス間の結合強度
        self.friction = 0.1  # 摩擦係数
        self.chaos_threshold = 0.95  # カオス発生閾値
        
        # 音響パラメータ
        self.base_freqs = [60, 90, 120, 150]  # 各プロセスの基本周波数
        self.resonance_freqs = [200, 300, 400, 500]  # 共振周波数
        
    def generate_process_dynamics(self):
        """プロセスの動的挙動生成"""
        # 各プロセスの状態（位置と速度）
        positions = np.zeros((self.num_processes, len(self.time)))
        velocities = np.zeros((self.num_processes, len(self.time)))
        
        # 初期条件
        for i in range(self.num_processes):
            positions[i, 0] = np.random.uniform(-1, 1)
            velocities[i, 0] = np.random.uniform(-0.1, 0.1)
        
        # 時間発展の計算
        dt = 1.0 / self.sample_rate
        for t in range(1, len(self.time)):
            for i in range(self.num_processes):
                # 他のプロセスからの影響（デッドロックの結合）
                coupling_force = 0
                for j in range(self.num_processes):
                    if i != j:
                        # 相互拘束力
                        distance = positions[i, t-1] - positions[j, t-1]
                        coupling_force += -self.coupling_strength * np.tanh(distance)
                
                # 摩擦力
                friction_force = -self.friction * velocities[i, t-1]
                
                # 外部駆動力（周期的な刺激）
                driving_force = 0.1 * np.sin(2 * np.pi * self.base_freqs[i] * self.time[t])
                
                # 合力の計算
                total_force = coupling_force + friction_force + driving_force
                
                # 速度と位置の更新
                velocities[i, t] = velocities[i, t-1] + total_force * dt
                positions[i, t] = positions[i, t-1] + velocities[i, t] * dt
                
                # デッドロック状態の検出と応答
                if np.abs(positions[i, t]) > self.chaos_threshold:
                    # カオス的振る舞いの発現
                    velocities[i, t] += np.random.normal(0, 0.01)
        
        return positions, velocities
    
    def generate_resonance_structure(self, positions):
        """共鳴構造の生成"""
        resonance_signal = np.zeros(len(self.time))
        
        for i in range(self.num_processes):
            # 位置による周波数変調
            freq_mod = self.resonance_freqs[i] * (1 + 0.3 * positions[i])
            
            # 共鳴信号の生成
            resonance = np.sin(2 * np.pi * freq_mod * self.time)
            
            # 振幅変調（位置の大きさに依存）
            amp_mod = 1 / (1 + np.abs(positions[i]))
            resonance *= amp_mod
            
            resonance_signal += resonance
        
        return resonance_signal / self.num_processes
    
    def generate_beat_patterns(self, velocities):
        """ビートパターンの生成（デッドロックの周期的な衝突）"""
        beat_signal = np.zeros(len(self.time))
        
        # 速度の大きさが閾値を超えたときにビートを生成
        velocity_magnitudes = np.sum(np.abs(velocities), axis=0)
        
        # ビートの検出
        beat_threshold = np.percentile(velocity_magnitudes, 90)
        beat_indices = np.where(velocity_magnitudes > beat_threshold)[0]
        
        # 各ビートに音を付加
        for idx in beat_indices:
            if idx < len(self.time) - 1000:  # 範囲チェック
                # 短いパルス音を生成
                pulse = np.exp(-np.arange(1000) / 100.0)
                pulse *= np.sin(2 * np.pi * 1000 * np.arange(1000) / self.sample_rate)
                
                # ビート信号に追加
                end_idx = min(idx + len(pulse), len(beat_signal))
                actual_length = end_idx - idx
                beat_signal[idx:end_idx] += pulse[:actual_length] * 0.3
        
        return beat_signal
    
    def generate_spatial_deadlock(self, signal):
        """空間的なデッドロック効果"""
        # 4つのプロセスを空間的に配置
        spatial_positions = [
            [-1, -1, 0],  # 左下奥
            [1, -1, 0],   # 右下奥
            [-1, 1, 0],   # 左上手前
            [1, 1, 0]     # 右上手前
        ]
        
        left_channel = np.zeros(len(signal))
        right_channel = np.zeros(len(signal))
        
        for i, pos in enumerate(spatial_positions):
            # 距離による減衰
            distance = np.sqrt(pos[0]**2 + pos[1]**2)
            attenuation = 1 / (1 + distance * 0.5)
            
            # パンニング
            pan = (pos[0] + 1) / 2  # -1 to 1 -> 0 to 1
            left_gain = np.sqrt(1 - pan)
            right_gain = np.sqrt(pan)
            
            # プロセス固有の周波数成分
            process_signal = signal * np.sin(2 * np.pi * self.base_freqs[i] * self.time * 0.01)
            
            left_channel += process_signal * attenuation * left_gain / self.num_processes
            right_channel += process_signal * attenuation * right_gain / self.num_processes
        
        return np.column_stack([left_channel, right_channel])
    
    def generate_chaos_emergence(self, base_signal):
        """カオスの創発"""
        # リアプノフ指数によるカオスの評価
        lyapunov_sum = np.zeros(len(self.time))
        
        for i in range(1, len(self.time)):
            # 近傍点との距離の発散
            if i > 10:
                diff = np.abs(base_signal[i] - base_signal[i-10])
                lyapunov_sum[i] = lyapunov_sum[i-1] + np.log(diff + 1e-10)
        
        # カオスの強度
        chaos_intensity = np.abs(lyapunov_sum) / np.max(np.abs(lyapunov_sum) + 1e-10)
        
        # カオスによる音響変調
        chaos_modulation = 1 + 0.5 * chaos_intensity
        
        return base_signal * chaos_modulation
    
    def compose_deadlock_dance(self):
        """デッドロックダンスの作曲"""
        print("生成中: プロセス動力学...")
        positions, velocities = self.generate_process_dynamics()
        
        print("生成中: 共鳴構造...")
        resonance = self.generate_resonance_structure(positions)
        
        print("生成中: ビートパターン...")
        beats = self.generate_beat_patterns(velocities)
        
        print("生成中: 基本信号合成...")
        base_signal = resonance + beats
        
        print("生成中: カオス創発...")
        chaos_signal = self.generate_chaos_emergence(base_signal)
        
        print("生成中: 空間化...")
        spatial_signal = self.generate_spatial_deadlock(chaos_signal)
        
        # ステレオ信号のモノラル変換（処理のため）
        mono_signal = np.mean(spatial_signal, axis=1)
        
        # 最終処理
        print("生成中: 最終処理...")
        final_signal = self.apply_final_effects(mono_signal)
        
        # 再度ステレオ化
        final_stereo = self.generate_spatial_deadlock(final_signal)
        
        # 正規化
        max_val = np.max(np.abs(final_stereo))
        if max_val > 0:
            final_stereo = final_stereo / max_val * 0.8
        
        return final_stereo, positions, velocities
    
    def apply_final_effects(self, signal):
        """最終的なエフェクト処理"""
        # 低域フィルタ（デッドロックの重さを表現）
        low_freq = 100
        high_freq = 800
        b, a = scipy.signal.butter(4, [low_freq, high_freq], 'bandpass', fs=self.sample_rate)
        filtered = scipy.signal.filtfilt(b, a, signal)
        
        # コンプレッション
        threshold = 0.7
        ratio = 4
        compressed = np.where(np.abs(filtered) > threshold, 
                             np.sign(filtered) * (threshold + (np.abs(filtered) - threshold) / ratio),
                             filtered)
        
        # リバーブ（空間的な閉塞感）
        reverb_decay = 0.5
        reverb_mix = 0.3
        reverb_signal = self.generate_simple_reverb(compressed, reverb_decay)
        
        return compressed * (1 - reverb_mix) + reverb_signal * reverb_mix
    
    def generate_simple_reverb(self, signal, decay_time):
        """簡単なリバーブ生成"""
        reverb_length = int(self.sample_rate * decay_time)
        reverb_signal = np.zeros_like(signal)
        
        # 多数の遅延線
        delays = [0.03, 0.05, 0.07, 0.11, 0.13, 0.17]  # 秒
        gains = [0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
        
        for delay, gain in zip(delays, gains):
            delay_samples = int(delay * self.sample_rate)
            delayed = np.roll(signal, delay_samples)
            delayed[:delay_samples] = 0  # 先頭をゼロで埋める
            reverb_signal += delayed * gain
        
        return reverb_signal / len(delays)
    
    def generate_phase_space_visualization(self, positions, velocities):
        """位相空間の可視化"""
        fig = plt.figure(figsize=(15, 10))
        
        # 4つのプロセスの位相空間プロット
        for i in range(self.num_processes):
            ax = fig.add_subplot(2, 2, i+1)
            
            # 位置と速度の関係
            pos_sample = positions[i, ::100]  # サンプリング
            vel_sample = velocities[i, ::100]
            time_sample = self.time[::100]
            
            # 色の時間変化
            colors = plt.cm.plasma(time_sample / self.duration)
            
            scatter = ax.scatter(pos_sample, vel_sample, c=time_sample, 
                               cmap='plasma', s=1, alpha=0.6)
            
            ax.set_xlabel(f'Process {i+1} Position')
            ax.set_ylabel(f'Process {i+1} Velocity')
            ax.set_title(f'Deadlock Phase Space - Process {i+1}')
            ax.grid(True, alpha=0.3)
            
            # カラーバー
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Time (s)')
        
        plt.tight_layout()
        plt.savefig('deadlock_dance_advanced_phase_space.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("位相空間可視化を保存: deadlock_dance_advanced_phase_space.png")
    
    def generate_3d_trajectory(self, positions):
        """3D軌道の可視化"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # プロセス1と2の関係を3Dで表現
        t_sample = self.time[::200]
        p1_sample = positions[0, ::200]
        p2_sample = positions[1, ::200]
        p3_sample = positions[2, ::200]
        
        # 色の時間変化
        colors = plt.cm.viridis(t_sample / self.duration)
        
        # 3D軌道
        for i in range(len(t_sample)-1):
            ax.plot([p1_sample[i], p1_sample[i+1]], 
                   [p2_sample[i], p2_sample[i+1]], 
                   [p3_sample[i], p3_sample[i+1]], 
                   color=colors[i], alpha=0.6)
        
        ax.scatter(p1_sample[0], p2_sample[0], p3_sample[0], 
                  color='red', s=100, label='Start')
        ax.scatter(p1_sample[-1], p2_sample[-1], p3_sample[-1], 
                  color='blue', s=100, label='End')
        
        ax.set_xlabel('Process 1 Position')
        ax.set_ylabel('Process 2 Position')
        ax.set_zlabel('Process 3 Position')
        ax.set_title('Deadlock Dance Advanced - 3D Trajectory')
        ax.legend()
        
        plt.tight_layout()
        plt.savefig('deadlock_dance_advanced_3d_trajectory.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("3D軌道可視化を保存: deadlock_dance_advanced_3d_trajectory.png")
    
    def save_audio(self, signal, filename):
        """音声ファイルの保存"""
        # ステレオ信号の保存
        sf.write(filename, signal, self.sample_rate)
        print(f"音声ファイルを保存: {filename}")
        
        # メタ情報の追加
        print(f"  - チャンネル数: {signal.shape[1] if len(signal.shape) > 1 else 1}")
        print(f"  - サンプルレート: {self.sample_rate} Hz")
        print(f"  - 時間: {len(signal) / self.sample_rate:.1f} 秒")
    
    def run(self):
        """全体の実行"""
        print("=== Deadlock Dance Advanced 生成開始 ===")
        
        # 音声の生成
        print("音声を生成中...")
        audio_signal, positions, velocities = self.compose_deadlock_dance()
        
        # 音声ファイルの保存
        output_filename = "07_deadlock_dance_advanced.wav"
        self.save_audio(audio_signal, output_filename)
        
        # 可視化の生成
        print("可視化を生成中...")
        self.generate_phase_space_visualization(positions, velocities)
        self.generate_3d_trajectory(positions)
        
        print("=== Deadlock Dance Advanced 生成完了 ===")
        print(f"出力ファイル:")
        print(f"  - 音声: {output_filename}")
        print(f"  - 位相空間可視化: deadlock_dance_advanced_phase_space.png")
        print(f"  - 3D軌道可視化: deadlock_dance_advanced_3d_trajectory.png")

if __name__ == "__main__":
    # Deadlock Dance Advancedの生成
    generator = DeadlockDanceAdvanced()
    generator.run()