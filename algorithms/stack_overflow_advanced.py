"""
Stack Overflow Advanced - 高度な物理モデリングによるスタックオーバーフローの音響化

複数の物理モデルを組み合わせ、スタックオーバーフローをより芸術的に表現。
非線形効果と空間化を取り入れ、カオス的で複雑な音響構造を生成。
"""

import numpy as np
import scipy.signal
from scipy.io import wavfile
import soundfile as sf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class StackOverflowAdvanced:
    def __init__(self, sample_rate=44100, duration=180):
        self.sample_rate = sample_rate
        self.duration = duration
        self.time = np.linspace(0, duration, int(sample_rate * duration))
        
        # 物理パラメータ
        self.gravity = 9.81
        self.stack_height = 100  # スタックの初期高さ
        self.max_pressure = 1000.0  # 最大圧力
        
        # 音響パラメータ
        self.base_freq = 80  # 基本周波数
        self.freq_mod_depth = 50  # 周波数変調の深さ
        
    def generate_physical_stack_model(self):
        """物理的なスタックモデルの生成"""
        # スタックの各層を時間とともに変化
        stack_layers = []
        
        for i in range(20):  # 20層のスタック
            # 各層の固有振動数（圧力依存）
            pressure_factor = np.linspace(1.0, 0.1, len(self.time))
            natural_freq = self.base_freq * (i + 1) * pressure_factor
            
            # 各層の振動
            layer_vibration = np.sin(2 * np.pi * natural_freq * self.time)
            
            # 減衰（高さに依存）
            damping = np.exp(-0.1 * (i + 1) * self.time / self.duration)
            layer_vibration *= damping
            
            stack_layers.append(layer_vibration)
        
        return np.array(stack_layers)
    
    def generate_nonlinear_effects(self, base_signal):
        """非線形効果の生成"""
        # 圧縮効果（ソフトクリッピング）
        threshold = 0.8
        compressed = np.tanh(base_signal / threshold) * threshold
        
        # 歪み効果
        distortion = 0.1 * np.sign(base_signal) * np.power(np.abs(base_signal), 0.5)
        
        # 相互変調
        modulation_freq = self.base_freq * 0.1
        modulation = 1 + 0.3 * np.sin(2 * np.pi * modulation_freq * self.time)
        
        return compressed * modulation + distortion
    
    def generate_spatial_effects(self, signal):
        """空間化効果の生成"""
        # 3D空間でのスタックの位置
        positions = np.random.randn(len(signal), 3)
        
        # 距離による減衰
        distances = np.linalg.norm(positions, axis=1)
        attenuation = 1 / (1 + distances * 0.1)
        
        # 空間的フィルタリング
        filtered_signal = np.zeros_like(signal)
        for i, pos in enumerate(positions[:10]):  # 最初の10層のみ
            delay_samples = int(pos[2] * 100)  # Z軸を遅延として使用
            delayed_signal = np.roll(signal, delay_samples)
            filtered_signal += delayed_signal * attenuation[i] * 0.1
        
        return filtered_signal
    
    def generate_chaos_feedback(self, signal):
        """カオス的フィードバックの生成"""
        # ロジスティックマップによるフィードバック
        r = 3.9  # カオス領域のパラメータ
        feedback_gain = np.zeros_like(signal)
        
        for i in range(1, len(signal)):
            feedback_gain[i] = r * feedback_gain[i-1] * (1 - feedback_gain[i-1])
            if i == 1:
                feedback_gain[i] = 0.5  # 初期値
        
        feedback_signal = signal * (1 + 0.5 * feedback_gain)
        
        # フィードバック遅延
        delayed_feedback = np.roll(feedback_signal, int(self.sample_rate * 0.1))
        
        return signal + 0.3 * delayed_feedback
    
    def compose_overflow_event(self):
        """スタックオーバーフローイベントの作曲"""
        print("生成中: 物理スタックモデル...")
        stack_model = self.generate_physical_stack_model()
        
        # 全層の合成
        combined_signal = np.sum(stack_model, axis=0)
        
        print("生成中: 非線形効果...")
        nonlinear_signal = self.generate_nonlinear_effects(combined_signal)
        
        print("生成中: 空間化効果...")
        spatial_signal = self.generate_spatial_effects(nonlinear_signal)
        
        print("生成中: カオスフィードバック...")
        final_signal = self.generate_chaos_feedback(spatial_signal)
        
        # 正規化
        final_signal = final_signal / np.max(np.abs(final_signal)) * 0.8
        
        return final_signal
    
    def generate_3d_visualization(self, signal):
        """3D可視化の生成"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 時系列を3D空間に配置
        t_sample = self.time[::100]  # サンプリング
        s_sample = signal[::100]
        
        # スタックのような3D構造を生成
        x = np.cos(t_sample * 0.1) * np.abs(s_sample)
        y = np.sin(t_sample * 0.1) * np.abs(s_sample)
        z = t_sample * 10  # 時間を高さとして
        
        # 色の設定
        colors = plt.cm.viridis(np.abs(s_sample) / np.max(np.abs(s_sample)))
        
        ax.scatter(x, y, z, c=colors, s=50, alpha=0.6)
        
        ax.set_xlabel('X (Stack Width)')
        ax.set_ylabel('Y (Stack Depth)')
        ax.set_zlabel('Z (Time/Height)')
        ax.set_title('Stack Overflow Advanced - 3D Visualization')
        
        plt.tight_layout()
        plt.savefig('stack_overflow_advanced_visualization.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("3D可視化を保存: stack_overflow_advanced_visualization.png")
    
    def save_audio(self, signal, filename):
        """音声ファイルの保存"""
        # 音声の正規化
        signal = signal / np.max(np.abs(signal)) * 0.8
        
        # 16bit PCMに変換
        audio_int16 = (signal * 32767).astype(np.int16)
        
        # WAVファイルとして保存
        wavfile.write(filename, self.sample_rate, audio_int16)
        print(f"音声ファイルを保存: {filename}")
        
        # メタデータ付きで保存（soundfile使用）
        sf.write(filename.replace('.wav', '_sf.wav'), signal, self.sample_rate)
        
    def run(self):
        """全体の実行"""
        print("=== Stack Overflow Advanced 生成開始 ===")
        
        # 音声の生成
        print("音声を生成中...")
        audio_signal = self.compose_overflow_event()
        
        # 音声ファイルの保存
        output_filename = "01_stack_overflow_advanced.wav"
        self.save_audio(audio_signal, output_filename)
        
        # 可視化の生成
        print("可視化を生成中...")
        self.generate_3d_visualization(audio_signal)
        
        print("=== Stack Overflow Advanced 生成完了 ===")
        print(f"出力ファイル:")
        print(f"  - 音声: {output_filename}")
        print(f"  - 可視化: stack_overflow_advanced_visualization.png")

if __name__ == "__main__":
    # Stack Overflow Advancedの生成
    generator = StackOverflowAdvanced()
    generator.run()