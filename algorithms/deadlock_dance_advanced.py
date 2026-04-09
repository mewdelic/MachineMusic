#!/usr/bin/env python3
"""
Deadlock Dance Advanced - 高度な物理モデリングによるデッドロックの音響表現（簡易版）

デッドロック状態を多層的な物理モデリングで表現：
- スレッドの相互ブロッキングを弦の物理モデルで表現
- リソース競合を衝突する物体の音響で表現
- デッドロック解決までの過程を時間発展シミュレーション
"""

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import soundfile as sf
import warnings
warnings.filterwarnings('ignore')

class DeadlockDanceAdvanced:
    def __init__(self, duration=90, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.samples = int(duration * sample_rate)
        self.time = np.linspace(0, duration, self.samples)
        
        # ステレオ出力
        self.output = np.zeros((self.samples, 2), dtype=np.float64)
        
        # 物理モデリングパラメータ
        self.setup_physics_parameters()
        
    def setup_physics_parameters(self):
        """物理モデリングのパラメータを設定"""
        # 4つのスレッドの基本周波数
        self.thread_frequencies = [220, 330, 440, 550]  # A3, E4, A4, C#5
        
        # スレッドの物理的特性
        self.thread_params = [
            {'tension': 0.6, 'damping': 0.98, 'pan': -0.8},    # Thread A (左)
            {'tension': 0.7, 'damping': 0.97, 'pan': -0.3},    # Thread B (左中央)
            {'tension': 0.8, 'damping': 0.96, 'pan': 0.3},     # Thread C (右中央)
            {'tension': 0.9, 'damping': 0.95, 'pan': 0.8}      # Thread D (右)
        ]
        
        # 6つのリソース
        self.resources = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
        self.resource_frequencies = [880, 990, 1100, 1230, 1380, 1540]
        
    def generate_thread_vibration(self, thread_idx, time_idx):
        """スレッドの振動を生成（弦の物理モデル）"""
        t = self.time[time_idx]
        params = self.thread_params[thread_idx]
        base_freq = self.thread_frequencies[thread_idx]
        
        # 基本周波数を緊張度で調整
        freq = base_freq * (1.0 + params['tension'])
        
        # 振幅の時間変化（デッドロックの進行による）
        progress = t / self.duration
        
        # フェーズごとの振幅変化
        if progress < 0.2:  # 初期状態
            amplitude = 0.1 * (progress / 0.2)
        elif progress < 0.4:  # 競合発生
            amplitude = 0.1 + 0.2 * ((progress - 0.2) / 0.2)
        elif progress < 0.7:  # デッドロック状態（最大緊張）
            amplitude = 0.3 + 0.3 * np.sin(2 * np.pi * 2 * progress)
        elif progress < 0.9:  # 解決試行
            amplitude = 0.6 - 0.3 * ((progress - 0.7) / 0.2)
        else:  # タイムアウト
            amplitude = 0.3 * (1.0 - (progress - 0.9) / 0.1)
            
        # 複数の倍音を合成
        vibration = 0
        for harmonic in range(1, 4):
            harm_amp = amplitude / harmonic
            vibration += harm_amp * np.sin(2 * np.pi * freq * harmonic * t)
            
        # 減衰
        vibration *= params['damping'] ** t
        
        return vibration
        
    def generate_resource_collision(self, res1_idx, res2_idx, time_idx):
        """リソース間の衝突音を生成"""
        t = self.time[time_idx]
        
        # 衝突の周期性（2秒周期）
        cycle_pos = t % 2.0
        
        if cycle_pos < 0.1:  # 衝突発生
            # 2つのリソース周波数の平均
            freq1 = self.resource_frequencies[res1_idx]
            freq2 = self.resource_frequencies[res2_idx]
            collision_freq = (freq1 + freq2) / 2
            
            # インパクトエネルギー
            impact_energy = 0.3 * (1.0 - cycle_pos / 0.1)
            
            # インパクト波形
            impact = impact_energy * np.exp(-cycle_pos * 30) * np.sin(2 * np.pi * collision_freq * cycle_pos)
            
            # ノイズ成分
            noise = np.random.normal(0, impact_energy * 0.05)
            
            return impact + noise
        else:
            return 0
            
    def get_deadlock_detection_envelope(self, t):
        """デッドロック検出の包絡線"""
        progress = t / self.duration
        
        # 周期的な検出パターン
        cycle_time = 3.0  # 3秒周期
        cycle_progress = (t % cycle_time) / cycle_time
        
        detection_level = 0
        if progress < 0.2:
            detection_level = 0.1
        elif progress < 0.4:
            detection_level = 0.1 + 0.3 * (progress - 0.2) / 0.2
        elif progress < 0.7:
            # デッドロック状態では検出レベルが振動
            base_level = 0.4 + 0.4 * ((progress - 0.4) / 0.3)
            oscillation = 0.1 * np.sin(2 * np.pi * 5 * cycle_progress)
            detection_level = base_level + oscillation
        else:
            detection_level = 0.8 - 0.6 * ((progress - 0.7) / 0.3)
            
        return detection_level
        
    def compose(self):
        """デッドロックダンスの合成"""
        print("デッドロックダンス Advanced の生成を開始...")
        
        # 各時間ステップで音響を生成
        for i in range(0, self.samples, 10):  # 10サンプルごとに処理（高速化）
            t = self.time[i]
            
            # 左右チャンネルの初期化
            left_channel = 0
            right_channel = 0
            
            # スレッドの振動を生成
            for thread_idx in range(4):
                vibration = self.generate_thread_vibration(thread_idx, i)
                params = self.thread_params[thread_idx]
                
                # パンニング
                pan = params['pan']
                left_gain = np.sqrt((1.0 - pan) / 2.0)
                right_gain = np.sqrt((1.0 + pan) / 2.0)
                
                left_channel += vibration * left_gain
                right_channel += vibration * right_gain
                
            # リソース衝突を生成
            for res1 in range(3):
                for res2 in range(3, 6):
                    collision = self.generate_resource_collision(res1, res2, i)
                    # 衝突音は中央に配置
                    left_channel += collision * 0.5
                    right_channel += collision * 0.5
                    
            # デッドロック検出包絡線を適用
            detection_envelope = self.get_deadlock_detection_envelope(t)
            left_channel *= (1.0 + 0.5 * detection_envelope)
            right_channel *= (1.0 + 0.5 * detection_envelope)
            
            # 出力に設定（10サンプル分を同じ値で埋める）
            end_idx = min(i + 10, self.samples)
            self.output[i:end_idx, 0] = left_channel
            self.output[i:end_idx, 1] = right_channel
            
            # 進捗表示
            if i % (self.samples // 20) == 0:
                progress = (i / self.samples) * 100
                print(f"進捗: {progress:.1f}%")
                
        # リバーブ効果（簡易）
        self.apply_simple_reverb()
        
        # ノーマライズ
        max_val = np.max(np.abs(self.output))
        if max_val > 0:
            self.output = self.output / max_val * 0.8
            
        print("デッドロックダンス Advanced の生成完了！")
        
    def apply_simple_reverb(self):
        """簡易リバーブ効果"""
        reverb_decay = 0.85
        reverb_delay = 0.03  # 30ms
        delay_samples = int(reverb_delay * self.sample_rate)
        
        # ディレイを加えてミックス
        if delay_samples < self.samples:
            delayed_left = np.roll(self.output[:, 0], delay_samples)
            delayed_right = np.roll(self.output[:, 1], delay_samples)
            delayed_left[:delay_samples] = 0
            delayed_right[:delay_samples] = 0
            
            # ミックス
            wet_level = 0.2
            self.output[:, 0] = (1.0 - wet_level) * self.output[:, 0] + wet_level * delayed_left
            self.output[:, 1] = (1.0 - wet_level) * self.output[:, 1] + wet_level * delayed_right
            
    def save_audio(self, filename):
        """音声ファイルとして保存"""
        sf.write(filename, self.output, self.sample_rate)
        print(f"音声ファイルを保存しました: {filename}")
        print(f"ファイルサイズ: {len(self.output) * 2 * 2 / (1024*1024):.1f} MB")
        print(f"演奏時間: {self.duration} 秒")
        print(f"チャンネル数: 2 (ステレオ)")
        
    def create_visualization(self, filename):
        """ビジュアライゼーションを作成"""
        fig = plt.figure(figsize=(15, 12))
        gs = GridSpec(4, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. ステレオ波形
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(self.time, self.output[:, 0], 'r-', linewidth=0.5, label='Left Channel')
        ax1.plot(self.time, self.output[:, 1], 'b-', linewidth=0.5, label='Right Channel')
        ax1.set_title('Deadlock Dance Advanced - Stereo Waveform', fontsize=14)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Amplitude')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. スペクトログラム（左チャンネル）
        ax2 = fig.add_subplot(gs[1, 0])
        f, t, Sxx = scipy.signal.spectrogram(self.output[:, 0], self.sample_rate, nperseg=1024)
        im1 = ax2.pcolormesh(t, f/1000, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
        ax2.set_title('Spectrogram (Left Channel)', fontsize=12)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Frequency (kHz)')
        plt.colorbar(im1, ax=ax2, label='Power (dB)')
        
        # 3. スペクトログラム（右チャンネル）
        ax3 = fig.add_subplot(gs[1, 1])
        f, t, Sxx = scipy.signal.spectrogram(self.output[:, 1], self.sample_rate, nperseg=1024)
        im2 = ax3.pcolormesh(t, f/1000, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
        ax3.set_title('Spectrogram (Right Channel)', fontsize=12)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Frequency (kHz)')
        plt.colorbar(im2, ax=ax3, label='Power (dB)')
        
        # 4. デッドロック検出パターン
        ax4 = fig.add_subplot(gs[2, 0])
        detection_pattern = [self.get_deadlock_detection_envelope(t) for t in self.time[::100]]
        time_sparse = self.time[::100]
        ax4.plot(time_sparse, detection_pattern, 'g-', linewidth=2)
        ax4.set_title('Deadlock Detection Pattern', fontsize=12)
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Detection Level')
        ax4.grid(True, alpha=0.3)
        
        # 5. リソース競合マップ
        ax5 = fig.add_subplot(gs[2, 1])
        # リソース競合の可視化
        conflict_map = np.zeros((len(self.resources), int(self.duration)))
        for i, res_name in enumerate(self.resources):
            # 各リソースの競合時間帯を設定
            if i < 3:  # 前半のリソース
                start_time = 0.2 * self.duration
                end_time = 0.7 * self.duration
            else:  # 後半のリソース
                start_time = 0.3 * self.duration
                end_time = 0.8 * self.duration
                
            conflict_map[i, int(start_time):int(end_time)] = 1.0
            
        im5 = ax5.imshow(conflict_map, aspect='auto', cmap='Reds')
        ax5.set_title('Resource Contention Map', fontsize=12)
        ax5.set_xlabel('Time (s)')
        ax5.set_ylabel('Resources')
        ax5.set_yticks(range(len(self.resources)))
        ax5.set_yticklabels(self.resources)
        plt.colorbar(im5, ax=ax5, label='Contention Level')
        
        # 6. スペクトル重心の時間変化
        ax6 = fig.add_subplot(gs[3, :])
        # モノラルミックス
        mono_signal = np.mean(self.output, axis=1)
        
        # 短時間フーリエ変換
        frame_size = 2048
        hop_size = 1024
        spectral_centroids = []
        
        for i in range(0, len(mono_signal) - frame_size, hop_size):
            frame = mono_signal[i:i+frame_size]
            spectrum = np.abs(np.fft.fft(frame))
            freqs = np.fft.fftfreq(frame_size, 1/self.sample_rate)
            
            # 正の周波数のみ
            pos_mask = freqs > 0
            spectrum = spectrum[pos_mask]
            freqs = freqs[pos_mask]
            
            if np.sum(spectrum) > 0:
                centroid = np.sum(spectrum * freqs) / np.sum(spectrum)
                spectral_centroids.append(centroid)
                
        time_axis = np.arange(len(spectral_centroids)) * hop_size / self.sample_rate
        ax6.plot(time_axis, spectral_centroids, 'purple', linewidth=2)
        ax6.set_title('Spectral Centroid Evolution', fontsize=12)
        ax6.set_xlabel('Time (s)')
        ax6.set_ylabel('Spectral Centroid (Hz)')
        ax6.grid(True, alpha=0.3)
        
        plt.suptitle('Deadlock Dance Advanced - Physical Modeling Analysis', 
                     fontsize=16, y=0.98)
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"ビジュアライゼーションを保存しました: {filename}")
        plt.close()

def main():
    """メイン実行関数"""
    print("=" * 60)
    print("Deadlock Dance Advanced - 物理モデリングによるデッドロックの音響表現")
    print("=" * 60)
    
    # インスタンス作成
    deadlock = DeadlockDanceAdvanced(duration=90, sample_rate=44100)
    
    # 音響合成
    deadlock.compose()
    
    # 音声ファイル保存
    audio_filename = "07_deadlock_dance_advanced.wav"
    deadlock.save_audio(audio_filename)
    
    # ビジュアライゼーション作成
    viz_filename = "07_deadlock_dance_advanced_visualization.png"
    deadlock.create_visualization(viz_filename)
    
    # メタデータの表示
    print("\n" + "=" * 60)
    print("デッドロックダンス Advanced - メタデータ")
    print("=" * 60)
    print(f"トラック名: Deadlock Dance (Advanced)")
    print(f"バージョン: Advanced v1.0")
    print(f"技術: 物理モデリング、マルチスレッドシミュレーション")
    print(f"演奏時間: {deadlock.duration} 秒")
    print(f"サンプルレート: {deadlock.sample_rate} Hz")
    print(f"チャンネル数: ステレオ")
    print(f"ピーク振幅: {np.max(np.abs(deadlock.output)):.3f}")
    print(f"ファイル名: {audio_filename}")
    print(f"ビジュアライゼーション: {viz_filename}")
    
    print("\n" + "=" * 60)
    print("技術的特徴:")
    print("1. 弦の物理モデリングによるスレッド緊張状態の表現")
    print("2. 衝突音響によるリソース競合の可聴化")
    print("3. マルチスレッドデッドロックの時間発展シミュレーション")
    print("4. 空間的残響効果による没入感の向上")
    print("5. デッドロック検出パターンの音響化")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("デッドロックダンス Advanced 生成完了！")
    print("=" * 60)

if __name__ == "__main__":
    main()