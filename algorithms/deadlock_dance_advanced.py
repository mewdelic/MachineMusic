#!/usr/bin/env python3
"""
Deadlock Dance Advanced - 高度な物理モデリングによるデッドロックの音響表現

デッドロックの状態を高度な物理モデリングで表現。
複数のプロセスが互いにリソースを待機し、全く進行できない状態を音楽化。
"""

import numpy as np
import scipy.signal
import soundfile as sf
from pathlib import Path
import matplotlib.pyplot as plt

class DeadlockDanceAdvanced:
    def __init__(self, duration=180, sample_rate=44100):
        self.duration = duration
        self.sample_rate = sample_rate
        self.num_samples = int(duration * sample_rate)
        
        # プロセス数（デッドロックの当事者）
        self.num_processes = 4
        
        # 各プロセスの基本周波数
        self.base_freqs = [110.0, 165.0, 220.0, 330.0]  # A2, E3, A3, E4
        
        # 物理モデリングパラメータ
        self.damping = 0.998
        self.nonlinear_factor = 0.3
        self.coupling_strength = 0.15
        
        # 空間化パラメータ
        self.room_size = 0.8
        self.reverb_time = 2.5
        
        # マルチバンド処理
        self.bands = 6
        self.band_freqs = [100, 300, 800, 2000, 5000, 12000]
        
        # 出力先
        self.output_dir = Path("samples")
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"DeadlockDanceAdvanced initialized: duration={duration}s, sample_rate={sample_rate}")
        
    def create_deadlock_pattern(self, time_array):
        """
        デッドロックの競合パターンを生成
        複数のプロセスが互いにブロックし合う状態を表現
        """
        deadlock_pattern = np.zeros((self.num_processes, len(time_array)))
        
        for i in range(self.num_processes):
            # 各プロセスの競合サイクル
            cycle_period = 2.0 + i * 0.5  # 各プロセスの周期は少しずつ異なる
            
            # リソース要求パターン（矩形波に近い）
            resource_request = scipy.signal.square(
                2 * np.pi * time_array / cycle_period,
                duty=0.3
            )
            
            # 競合状態の強度（時間経過とともに悪化）
            intensity = 1.0 + 0.5 * (time_array / self.duration) ** 2
            
            # 他のプロセスからの干渉
            interference = np.zeros_like(time_array)
            for j in range(self.num_processes):
                if i != j:
                    interference += 0.1 * scipy.signal.square(
                        2 * np.pi * time_array / (2.0 + j * 0.5),
                        duty=0.3
                    )
            
            deadlock_pattern[i] = resource_request * intensity * (1 + interference)
            
        return deadlock_pattern
    
    def physical_model_oscillator(self, freq, phase, damping, excitation):
        """
        物理モデリングオシレーター
        減衰振動子と非線形結合をモデル化
        """
        # 連続時間から離散時間への変換
        omega = 2 * np.pi * freq / self.sample_rate
        
        # 減衰係数
        alpha = damping
        
        # 非線形項
        nonlinear = self.nonlinear_factor * np.sin(3 * phase)
        
        # 位相の更新（非線形振動子）
        phase_update = omega + nonlinear * excitation
        
        # 振幅の更新（減衰と励起）
        amplitude = alpha * (1 + 0.1 * excitation)
        
        return phase_update, amplitude
    
    def coupled_oscillators(self, deadlock_pattern, time_array):
        """
        結合振動子システムによるデッドロックの表現
        """
        # 各プロセスの信号
        signals = np.zeros((self.num_processes, self.num_samples))
        
        # 位相と振幅の状態
        phases = np.zeros(self.num_processes)
        amplitudes = np.ones(self.num_processes)
        
        # カップリングマトリックス（どのプロセスがどのプロセスをブロックするか）
        coupling_matrix = np.array([
            [0.0, 0.3, 0.0, 0.2],    # プロセス0 → 1, 3をブロック
            [0.2, 0.0, 0.3, 0.0],    # プロセス1 → 0, 2をブロック
            [0.0, 0.2, 0.0, 0.3],    # プロセス2 → 1, 3をブロック
            [0.3, 0.0, 0.2, 0.0]     # プロセス3 → 0, 2をブロック
        ])
        
        for t in range(self.num_samples):
            # 各プロセスの状態を更新
            for i in range(self.num_processes):
                # 基本周波数（時間変動）
                freq_variation = self.base_freqs[i] * (1 + 0.1 * deadlock_pattern[i, t])
                
                # 他のプロセスからのカップリング影響
                coupling_effect = 0
                for j in range(self.num_processes):
                    coupling_effect += coupling_matrix[i, j] * signals[j, max(0, t-1)]
                
                # 物理モデリングによるオシレーター更新
                phase_update, amplitude_update = self.physical_model_oscillator(
                    freq_variation, phases[i], self.damping, deadlock_pattern[i, t]
                )
                
                phases[i] += phase_update
                amplitudes[i] = amplitude_update * (1 - 0.001 * coupling_effect)
                
                # 信号生成
                signal = amplitudes[i] * np.sin(phases[i])
                
                # カップリング効果の適用
                signal += self.coupling_strength * coupling_effect
                
                # バンドパスフィルタリング（各プロセスの周波数帯域）
                low_freq = self.base_freqs[i] * 0.8
                high_freq = self.base_freqs[i] * 1.5
                
                # 簡易的なバンドパス（本実装では後処理で適用）
                signals[i, t] = signal
                
        return signals
    
    def multiband_processing(self, mixed_signal):
        """
        マルチバンド処理による音質向上
        """
        # マルチバンド分解
        bands = []
        
        # 低域カット
        bands.append(scipy.signal.butter(2, self.band_freqs[0], 'high', 
                                         fs=self.sample_rate, output='sos'))
        
        # バンドパスフィルタ
        for i in range(len(self.band_freqs) - 1):
            low = self.band_freqs[i]
            high = self.band_freqs[i + 1]
            band = scipy.signal.butter(2, [low, high], 'bandpass',
                                       fs=self.sample_rate, output='sos')
            bands.append(band)
        
        # 高域カット
        bands.append(scipy.signal.butter(2, self.band_freqs[-1], 'low',
                                         fs=self.sample_rate, output='sos'))
        
        # 各バンドの処理
        processed_bands = []
        for i, sos in enumerate(bands):
            # フィルタリング
            filtered = scipy.signal.sosfilt(sos, mixed_signal)
            
            # バンドごとのエンベロープ処理
            envelope = np.abs(filtered)
            envelope = scipy.signal.savgol_filter(envelope, 101, 3)
            
            # バンドごとのダイナミクス処理
            if i < 3:  # 低域は緩やかな変化
                filtered = filtered * (1 + 0.2 * envelope / np.max(envelope + 1e-10))
            else:  # 高域は鋭い変化
                filtered = filtered * (1 + 0.5 * envelope / np.max(envelope + 1e-10))
            
            processed_bands.append(filtered)
        
        # バンドの合成
        output = np.sum(processed_bands, axis=0)
        
        # 正規化
        output = output / np.max(np.abs(output) + 1e-10)
        
        return output
    
    def spatial_processing(self, signal):
        """
        空間化処理による立体感の付与
        """
        # ステレオ信号の生成
        stereo_signal = np.zeros((2, len(signal)))
        
        # 周波数帯域ごとの空間化
        for i in range(len(self.band_freqs) - 1):
            low = self.band_freqs[i]
            high = self.band_freqs[i + 1]
            
            # バンド抽出
            sos = scipy.signal.butter(2, [low, high], 'bandpass',
                                      fs=self.sample_rate, output='sos')
            band_signal = scipy.signal.sosfilt(sos, signal)
            
            # パンニング（周波数帯域ごとに異なる定位）
            pan_angle = (i / (len(self.band_freqs) - 1)) * np.pi
            left_gain = np.cos(pan_angle) ** 2
            right_gain = np.sin(pan_angle) ** 2
            
            # クロスフィード（わずかな逆位相信号の追加）
            left_signal = band_signal * left_gain + 0.1 * band_signal * right_gain
            right_signal = band_signal * right_gain + 0.1 * band_signal * left_gain
            
            stereo_signal[0] += left_signal
            stereo_signal[1] += right_signal
        
        # リバーブの適用
        reverb_length = int(self.reverb_time * self.sample_rate)
        reverb_decay = np.exp(-3 * np.arange(reverb_length) / reverb_length)
        
        # コンボリューションリバーブ（簡易版）
        for channel in range(2):
            impulse_response = np.random.randn(reverb_length) * reverb_decay
            impulse_response[0] = 1.0  # ダイレクト音
            
            # 畳み込み
            wet_signal = np.convolve(stereo_signal[channel], impulse_response, mode='same')
            
            # ドライ/ウェットミックス
            stereo_signal[channel] = 0.7 * stereo_signal[channel] + 0.3 * wet_signal
        
        # 正規化
        stereo_signal = stereo_signal / np.max(np.abs(stereo_signal) + 1e-10)
        
        return stereo_signal
    
    def generate_composition(self):
        """
        Deadlock Dance Advancedの全体構成を生成
        """
        print("Generating Deadlock Dance Advanced...")
        
        # 時間軸の生成
        time_array = np.linspace(0, self.duration, self.num_samples)
        
        print("Creating deadlock patterns...")
        # デッドロックパターンの生成
        deadlock_pattern = self.create_deadlock_pattern(time_array)
        
        print("Generating coupled oscillators...")
        # 結合振動子システムの生成
        coupled_signals = self.coupled_oscillators(deadlock_pattern, time_array)
        
        print("Mixing signals...")
        # 信号のミックス（デッドロックの緊張感を表現）
        mixed_signal = np.sum(coupled_signals, axis=0)
        
        print("Applying envelope...")
        # 時間変化によるエンベロープ
        envelope = np.ones_like(time_array)
        
        # 構造的なエンベロープ（時間に応じて調整）
        # 導入部 - 緊張感の構築 (全体の20%)
        intro_samples = int(0.2 * self.num_samples)
        envelope[:intro_samples] = np.linspace(0, 1, intro_samples)
        
        # 発展部 - 競合の激化 (20%-60%)
        dev_start = int(0.2 * self.num_samples)
        dev_end = int(0.6 * self.num_samples)
        dev_samples = dev_end - dev_start
        envelope[dev_start:dev_end] *= (1 + 0.3 * np.sin(np.linspace(0, 4*np.pi, dev_samples)))
        
        # クライマックス - 完全なデッドロック (60%-80%)
        climax_start = int(0.6 * self.num_samples)
        climax_end = int(0.8 * self.num_samples)
        climax_samples = climax_end - climax_start
        envelope[climax_start:climax_end] *= (1.5 + 0.5 * np.sin(np.linspace(0, 8*np.pi, climax_samples)))
        
        # 終結部 - 静寂へ (80%-100%)
        outro_start = int(0.8 * self.num_samples)
        outro_samples = self.num_samples - outro_start
        envelope[outro_start:] *= np.linspace(1, 0, outro_samples)
        
        # エンベロープの適用
        mixed_signal *= envelope
        
        print("Applying multiband processing...")
        # マルチバンド処理
        mixed_signal = self.multiband_processing(mixed_signal)
        
        print("Applying spatial processing...")
        # 空間化処理
        stereo_signal = self.spatial_processing(mixed_signal)
        
        print("Applying final dynamics...")
        # 最終的なダイナミクス処理
        # コンプレッサー効果（簡易版）
        threshold = 0.5
        ratio = 4.0
        
        # RMSレベルの計算（より効率的な方法）
        window_size = 1024
        hop_size = 512
        
        # スライディングウィンドウでのRMS計算
        rms_level = np.zeros(len(stereo_signal[0]))
        for i in range(0, len(stereo_signal[0]) - window_size, hop_size):
            window = stereo_signal[0, i:i+window_size]
            rms = np.sqrt(np.mean(window**2))
            rms_level[i:i+hop_size] = rms
        
        # 最後の部分を処理
        if len(rms_level) < len(stereo_signal[0]):
            rms_level[-1] = rms_level[-2]
        
        # スムージング
        try:
            rms_level = scipy.signal.savgol_filter(rms_level, 101, 3)
        except:
            # エラーが発生した場合はそのまま使用
            pass
        
        # コンプレッション
        gain_reduction = np.ones_like(rms_level)
        compression_mask = rms_level > threshold
        gain_reduction[compression_mask] = 1 - (1 - 1/ratio) * (rms_level[compression_mask] - threshold)
        
        # ゲインの適用
        for channel in range(2):
            stereo_signal[channel] *= gain_reduction
        
        # 正規化
        max_val = np.max(np.abs(stereo_signal))
        if max_val > 0:
            stereo_signal = stereo_signal / max_val
        
        print("Composition generation complete!")
        return stereo_signal, time_array, deadlock_pattern
    
    def create_visualization(self, time_array, deadlock_pattern, stereo_signal):
        """
        デッドロックの可視化
        """
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # デッドロックパターンの可視化
        ax1 = axes[0]
        for i in range(self.num_processes):
            ax1.plot(time_array[:1000], deadlock_pattern[i, :1000], 
                    label=f'Process {i}', alpha=0.7)
        ax1.set_ylabel('Deadlock Intensity')
        ax1.set_title('Deadlock Dance Advanced - Process Competition Patterns')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # スペクトログラム
        ax2 = axes[1]
        from scipy import signal
        f, t, Sxx = signal.spectrogram(stereo_signal[0], self.sample_rate, 
                                      nperseg=2048, noverlap=512)
        im = ax2.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
        ax2.set_ylabel('Frequency [Hz]')
        ax2.set_title('Spectrogram - Deadlock Frequency Clashes')
        plt.colorbar(im, ax=ax2, label='Power [dB]')
        
        # 波形とエンベロープ
        ax3 = axes[2]
        ax3.plot(time_array[:5000], stereo_signal[0, :5000], 'b-', 
                alpha=0.7, label='Left Channel')
        ax3.plot(time_array[:5000], stereo_signal[1, :5000], 'r-', 
                alpha=0.7, label='Right Channel')
        ax3.set_xlabel('Time [s]')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Deadlock Dance Advanced - Waveform Output')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def save_composition(self):
        """
        楽曲の保存とエクスポート
        """
        # 楽曲の生成
        stereo_signal, time_array, deadlock_pattern = self.generate_composition()
        
        # 可視化の作成
        fig = self.create_visualization(time_array, deadlock_pattern, stereo_signal)
        
        # 音声ファイルの保存
        output_path = self.output_dir / "07_deadlock_dance_advanced.wav"
        sf.write(output_path, stereo_signal.T, self.sample_rate)
        print(f"Audio saved to: {output_path}")
        
        # 可視化の保存
        viz_path = self.output_dir / "07_deadlock_dance_advanced_visualization.png"
        fig.savefig(viz_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to: {viz_path}")
        
        # 可視化の表示
        plt.show()
        
        return str(output_path), str(viz_path)

def main():
    """
    Deadlock Dance Advancedのメイン実行関数
    """
    # 作曲の実行
    composer = DeadlockDanceAdvanced(duration=180)  # 3分
    audio_path, viz_path = composer.save_composition()
    
    print("\n" + "="*60)
    print("Deadlock Dance Advanced - Generation Complete")
    print("="*60)
    print(f"Audio File: {audio_path}")
    print(f"Visualization: {viz_path}")
    print("\nTrack Details:")
    print("- Title: Deadlock Dance Advanced")
    print("- Duration: 3:00")
    print("- Concept: Advanced physical modeling of system deadlock")
    print("- Techniques: Coupled oscillators, multiband processing, spatialization")
    print("- Status: Enhanced album expansion (Advanced version)")
    print("="*60)

if __name__ == "__main__":
    main()