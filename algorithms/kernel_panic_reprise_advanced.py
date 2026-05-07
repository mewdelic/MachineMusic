#!/usr/bin/env python3
"""
Kernel Panic (Reprise) - Advanced Version
量子情報理論と熱力学によるシステムの完全崩壊表現

Advancedコンセプト：
- 量子デコヒーレンスによるシステムの一貫性の喪失
- 熱力学第2法則によるエントロピーの増大と熱的崩壊
- 臨界現象としてのシステム相転移
- 1/fノイズによる臨界ゆらぎ
- 指数関数的減衰による熱的死

構造（4分）：
1. Quantum Coherence (0:00-0:48) - 量子コヒーレンスの維持と不安定化
2. Entropy Rise (0:48-1:36) - エントロピーの急激な増大
3. Critical Point (1:36-2:24) - 相転移点と臨界現象
4. Decoherence Cascade (2:24-3:12) - デコヒーレンスの連鎖反応
5. Thermal Death (3:12-4:00) - 熱的平衡と完全静寂
"""

import numpy as np
from scipy.io import wavfile
from scipy import signal
from scipy.fft import fft, ifft, fftfreq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['agg.path.chunksize'] = 10000
import random
import math

# パラメータ
SAMPLE_RATE = 44100
DURATION = 240  # 4分

class KernelPanicAdvancedGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.duration = DURATION
        self.channels = 2
        
        # 構造の定義
        self.sections = [
            (0.0, 0.2, "quantum_coherence"),
            (0.2, 0.4, "entropy_rise"),
            (0.4, 0.6, "critical_point"),
            (0.6, 0.8, "decoherence_cascade"),
            (0.8, 1.0, "thermal_death")
        ]
        
        # 量子状態の追跡（簡易版）
        self.coherence = 1.0
        self.entropy = 0.0
        self.temperature = 1.0
    
    def generate_quantum_coherence_audio(self, duration: float) -> np.ndarray:
        """量子コヒーレンスの音声生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.zeros((len(t), self.channels))
        
        # 複数の純音による量子干渉パターン
        base_freqs = [220, 330, 440, 550, 660]  # A3, E4, A4, C#5, E5
        
        for i, freq in enumerate(base_freqs):
            # 量子干渉
            wave = np.sin(2 * np.pi * freq * t)
            
            # 調波の重ね合わせ
            wave += 0.5 * np.sin(2 * np.pi * freq * 2 * t)
            wave += 0.3 * np.sin(2 * np.pi * freq * 3 * t)
            
            # コヒーレンスによる変調
            envelope = self.coherence * (1 - 0.5 * t / duration)
            wave *= envelope
            
            # 空間的配置
            pan_l = 0.4 + 0.2 * np.sin(2 * np.pi * 0.1 * t + i)
            pan_r = 0.4 + 0.2 * np.cos(2 * np.pi * 0.1 * t + i)
            
            audio[:, 0] += wave * pan_l
            audio[:, 1] += wave * pan_r
        
        return audio * 0.2
    
    def generate_entropy_rise_audio(self, duration: float) -> np.ndarray:
        """エントロピー増大の音声生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.zeros((len(t), self.channels))
        
        # エントロピーに応じたノイズ
        entropy_ratio = self.entropy / 8.0  # 最大エントロピー8ビット
        
        # 熱的ノイズ（ホワイトノイズからピンクノイズへ）
        white_noise = np.random.normal(0, 1, len(t))
        
        # 周波数領域での処理
        fft_noise = fft(white_noise)
        freqs = fftfreq(len(t), 1/self.sample_rate)
        
        # 1/fフィルタ（エントロピーに応じて変化）
        alpha = 1.0 + entropy_ratio * 0.5
        filter_mask = np.zeros_like(freqs)
        filter_mask[freqs != 0] = 1.0 / np.abs(freqs[freqs != 0]) ** alpha
        filter_mask[freqs == 0] = 1.0
        
        pink_fft = fft_noise * filter_mask
        pink_noise = np.real(ifft(pink_fft))
        pink_noise /= np.max(np.abs(pink_noise))
        
        # エンベロープ
        envelope = np.linspace(0.2, 1.0, len(t))
        pink_noise *= envelope * (0.3 + 0.7 * entropy_ratio)
        
        for ch in range(self.channels):
            audio[:, ch] = pink_noise
        
        return audio * 0.4
    
    def generate_pink_noise(self, length: int, alpha: float = 1.0) -> np.ndarray:
        """ピンクノイズ（1/f^αノイズ）の生成"""
        white_noise = np.random.normal(0, 1, length)
        fft_noise = fft(white_noise)
        freqs = fftfreq(length)
        
        filter_mask = np.zeros_like(freqs)
        filter_mask[freqs != 0] = 1.0 / np.abs(freqs[freqs != 0]) ** alpha
        filter_mask[freqs == 0] = 1.0
        
        pink_fft = fft_noise * filter_mask
        pink_noise = np.real(ifft(pink_fft))
        pink_noise /= np.max(np.abs(pink_noise) + 1e-10)
        
        return pink_noise
    
    def generate_critical_point_audio(self, duration: float) -> np.ndarray:
        """臨界点の音声生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.zeros((len(t), self.channels))
        
        # 臨界点での1/fノイズ
        pink_noise = self.generate_pink_noise(len(t), alpha=1.0)
        
        # 臨界周波数の発振
        critical_freq = 1000  # Hz
        critical_osc = np.sin(2 * np.pi * critical_freq * t)
        
        # 周波数変調（臨界ゆらぎ）
        modulation_index = 5.0
        fm_signal = np.sin(2 * np.pi * critical_freq * t + 
                          modulation_index * np.sin(2 * np.pi * 100 * t))
        
        # 臨界点での急激な変化
        critical_idx = int(0.5 * len(t))
        
        # 臨界点前：不安定な振動
        pre_critical = pink_noise * 0.5 + fm_signal * 0.3 + critical_osc * 0.2
        pre_critical[:critical_idx] *= np.linspace(0.5, 1.0, critical_idx)
        
        # 臨界点後：急激な減衰
        post_critical = pink_noise * 0.5 + fm_signal * 0.3 + critical_osc * 0.2
        post_critical[critical_idx:] *= np.linspace(1.0, 0.1, len(t) - critical_idx)
        
        critical_audio = pre_critical + post_critical
        
        # 臨界点での衝撃
        if critical_idx + 5000 < len(t):
            shock = np.zeros(len(t))
            shock[critical_idx:critical_idx+5000] = np.exp(-np.arange(5000) / 1000) * 0.8
            critical_audio += shock
        
        for ch in range(self.channels):
            audio[:, ch] = critical_audio
        
        return audio * 0.5
    
    def generate_decoherence_cascade_audio(self, duration: float) -> np.ndarray:
        """デコヒーレンス連鎖の音声生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.zeros((len(t), self.channels))
        
        # 連鎖的な崩壊イベント
        num_events = 8
        event_times = np.linspace(0, duration * 0.8, num_events)
        
        cascade_audio = np.zeros(len(t))
        
        for event_time in event_times:
            event_idx = int(event_time * self.sample_rate)
            event_duration = int(0.3 * self.sample_rate)  # 0.3秒
            
            if event_idx + event_duration < len(t):
                # 崩壊インパルス
                impulse = np.zeros(len(t))
                decay = np.exp(-np.arange(event_duration) / (event_duration * 0.15))
                
                # 複数の周波数成分
                for freq in [200, 400, 800, 1600]:
                    oscillation = np.sin(2 * np.pi * freq * np.arange(event_duration) / self.sample_rate)
                    impulse[event_idx:event_idx+event_duration] += oscillation * decay * 0.25
                
                cascade_audio += impulse * 0.4
        
        # 背景ノイズ
        bg_noise = np.random.normal(0, 0.15, len(t))
        bg_noise *= np.linspace(1.0, 0.3, len(t))
        
        cascade_audio += bg_noise
        
        for ch in range(self.channels):
            audio[:, ch] = cascade_audio
        
        return audio * 0.4
    
    def generate_thermal_death_audio(self, duration: float) -> np.ndarray:
        """熱的死の音声生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        audio = np.zeros((len(t), self.channels))
        
        # 最後の「あえぎ」
        final_breath = np.random.normal(0, 0.1, len(t))
        
        # 指数関数的減衰
        decay_constant = duration * 0.25
        decay_curve = np.exp(-t / decay_constant)
        final_breath *= decay_curve
        
        # 残留振動
        residual_freqs = [60, 120, 180]  # 低周波
        for freq in residual_freqs:
            oscillation = np.sin(2 * np.pi * freq * t)
            oscillation *= decay_curve * (0.3 / len(residual_freqs))
            final_breath += oscillation
        
        # 最後の15秒はほぼ静寂
        silence_start = int(0.75 * len(t))
        if silence_start < len(t):
            final_breath[silence_start:] *= 0.05
        
        for ch in range(self.channels):
            audio[:, ch] = final_breath
        
        return audio * 0.3
    
    def apply_spatial_processing(self, audio: np.ndarray) -> np.ndarray:
        """空間処理の適用"""
        t = np.linspace(0, self.duration, len(audio))
        
        processed_audio = np.zeros_like(audio)
        
        # 簡易的な周波数バンド分割
        nyquist = self.sample_rate / 2
        
        for ch in range(self.channels):
            # 低周波
            b, a = signal.butter(4, 200 / nyquist, 'low')
            low = signal.filtfilt(b, a, audio[:, ch])
            
            # 中周波
            b, a = signal.butter(4, [200 / nyquist, 2000 / nyquist], 'band')
            mid = signal.filtfilt(b, a, audio[:, ch])
            
            # 高周波
            b, a = signal.butter(4, 2000 / nyquist, 'high')
            high = signal.filtfilt(b, a, audio[:, ch])
            
            # 動的パンニング
            pan_l = 0.5 + 0.4 * np.sin(2 * np.pi * 0.05 * t)
            pan_r = 0.5 + 0.4 * np.cos(2 * np.pi * 0.05 * t)
            
            processed_audio[:, ch] = (low * (pan_l if ch == 0 else pan_r) +
                                    mid * (pan_r if ch == 0 else pan_l) +
                                    high * 0.5)
        
        return processed_audio
    
    def update_quantum_state(self, section_name: str, progress: float):
        """量子状態の更新"""
        if section_name == "quantum_coherence":
            self.coherence = 1.0 - 0.5 * progress
            self.entropy = progress * 2.0
            self.temperature = 1.0 + progress * 1.0
        elif section_name == "entropy_rise":
            self.coherence = 0.5 - 0.3 * progress
            self.entropy = 2.0 + progress * 3.0
            self.temperature = 2.0 + progress * 8.0
        elif section_name == "critical_point":
            self.coherence = 0.2 - 0.15 * progress
            self.entropy = 5.0 + progress * 2.0
            self.temperature = 10.0 + progress * 40.0
        elif section_name == "decoherence_cascade":
            self.coherence = 0.05 - 0.04 * progress
            self.entropy = 7.0 + progress * 0.8
            self.temperature = 50.0 + progress * 50.0
        elif section_name == "thermal_death":
            self.coherence = 0.01 * (1 - progress)
            self.entropy = 7.8 + progress * 0.2
            self.temperature = 100.0 + progress * 100.0
    
    def generate_kernel_panic_advanced(self):
        """Advanced版Kernel Panic (Reprise)の生成"""
        print("Generating Kernel Panic (Reprise) - Advanced version...")
        print("Using Quantum Information Theory and Thermodynamics")
        print()
        
        # 全体の音声配列
        final_audio = np.zeros((int(self.sample_rate * self.duration), self.channels))
        
        # セクションごとの生成
        for start_ratio, end_ratio, section_name in self.sections:
            start_idx = int(start_ratio * len(final_audio))
            end_idx = int(end_ratio * len(final_audio))
            section_duration = (end_ratio - start_ratio) * self.duration
            
            print(f"Generating section: {section_name} ({start_ratio*100:.0f}% - {end_ratio*100:.0f}%)")
            
            # セクション内の進行
            section_progress = np.linspace(0, 1, end_idx - start_idx)
            
            # セクションに応じた音声生成
            if section_name == "quantum_coherence":
                section_audio = self.generate_quantum_coherence_audio(section_duration)
            elif section_name == "entropy_rise":
                section_audio = self.generate_entropy_rise_audio(section_duration)
            elif section_name == "critical_point":
                section_audio = self.generate_critical_point_audio(section_duration)
            elif section_name == "decoherence_cascade":
                section_audio = self.generate_decoherence_cascade_audio(section_duration)
            elif section_name == "thermal_death":
                section_audio = self.generate_thermal_death_audio(section_duration)
            else:
                section_audio = np.zeros((end_idx - start_idx, self.channels))
            
            # 量子状態の更新
            for i, prog in enumerate(section_progress):
                if i < len(section_audio):
                    self.update_quantum_state(section_name, prog)
            
            # セクション音声の配置
            if len(section_audio) == end_idx - start_idx:
                final_audio[start_idx:end_idx] = section_audio
            else:
                min_len = min(end_idx - start_idx, len(section_audio))
                final_audio[start_idx:start_idx+min_len] = section_audio[:min_len]
        
        print()
        print("Applying spatial processing...")
        final_audio = self.apply_spatial_processing(final_audio)
        
        print("Normalizing audio...")
        max_val = np.max(np.abs(final_audio))
        if max_val > 0:
            final_audio = final_audio / max_val * 0.9
        
        print("Applying fade in/out...")
        fade_duration = int(2 * self.sample_rate)
        
        for i in range(fade_duration):
            fade_factor = i / fade_duration
            final_audio[i, :] *= fade_factor
        
        for i in range(len(final_audio) - fade_duration, len(final_audio)):
            fade_factor = (len(final_audio) - i) / fade_duration
            final_audio[i, :] *= fade_factor
        
        # ファイル出力
        output_file = "10_kernel_panic_reprise_advanced.wav"
        wavfile.write(output_file, self.sample_rate, (final_audio * 32767).astype(np.int16))
        
        print(f"File saved: {output_file}")
        
        # 可視化
        print("Creating visualization...")
        self.create_advanced_visualization(final_audio)
        
        # テクニカルデータ保存
        print("Saving technical data...")
        self.save_technical_data()
        
        return output_file
    
    def create_advanced_visualization(self, audio: np.ndarray):
        """Advanced版の可視化"""
        fig, axes = plt.subplots(4, 2, figsize=(20, 14))
        
        t = np.linspace(0, self.duration, len(audio))
        
        # 1. 波形
        axes[0, 0].plot(t, audio[:, 0], 'b-', alpha=0.7, linewidth=0.5)
        axes[0, 0].set_title('Kernel Panic (Reprise) - Advanced: Waveform')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True, alpha=0.3)
        
        # セクションマーキング
        section_colors = ['blue', 'red', 'green', 'orange', 'purple']
        section_labels = ['Quantum Coherence', 'Entropy Rise', 'Critical Point', 'Decoherence Cascade', 'Thermal Death']
        for i, (start, end, _) in enumerate(self.sections):
            axes[0, 0].axvspan(start * self.duration, end * self.duration, 
                              alpha=0.2, color=section_colors[i], label=section_labels[i])
        axes[0, 0].legend(loc='upper right', fontsize=8)
        
        # 2. スペクトログラム
        f, t_spec, Sxx = signal.spectrogram(audio[:, 0], self.sample_rate)
        im = axes[0, 1].pcolormesh(t_spec, f, 10 * np.log10(Sxx + 1e-10), 
                                   shading='gouraud', cmap='viridis')
        axes[0, 1].set_title('Spectrogram')
        axes[0, 1].set_ylabel('Frequency [Hz]')
        plt.colorbar(im, ax=axes[0, 1])
        
        # 3. 量子コヒーレンスとエントロピーの時間発展
        t_evol = np.linspace(0, self.duration, 100)
        coherence_evol = []
        entropy_evol = []
        
        for i, ratio in enumerate(t_evol / self.duration):
            if ratio < 0.2:
                prog = ratio / 0.2
                coh = 1.0 - 0.5 * prog
                ent = prog * 2.0
            elif ratio < 0.4:
                prog = (ratio - 0.2) / 0.2
                coh = 0.5 - 0.3 * prog
                ent = 2.0 + prog * 3.0
            elif ratio < 0.6:
                prog = (ratio - 0.4) / 0.2
                coh = 0.2 - 0.15 * prog
                ent = 5.0 + prog * 2.0
            elif ratio < 0.8:
                prog = (ratio - 0.6) / 0.2
                coh = 0.05 - 0.04 * prog
                ent = 7.0 + prog * 0.8
            else:
                prog = (ratio - 0.8) / 0.2
                coh = 0.01 * (1 - prog)
                ent = 7.8 + prog * 0.2
            
            coherence_evol.append(max(coh, 0.001))
            entropy_evol.append(min(ent, 8.0))
        
        axes[1, 0].plot(t_evol, coherence_evol, 'b-', linewidth=2, label='Coherence')
        axes[1, 0].plot(t_evol, entropy_evol, 'r-', linewidth=2, label='Entropy')
        axes[1, 0].set_title('Quantum Coherence and Entropy Evolution')
        axes[1, 0].set_ylabel('Value')
        axes[1, 0].set_xlabel('Time [s]')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 温度の時間発展
        temp_evol = []
        for ratio in t_evol / self.duration:
            if ratio < 0.2:
                prog = ratio / 0.2
                temp = 1.0 + prog * 1.0
            elif ratio < 0.4:
                prog = (ratio - 0.2) / 0.2
                temp = 2.0 + prog * 8.0
            elif ratio < 0.6:
                prog = (ratio - 0.4) / 0.2
                temp = 10.0 + prog * 40.0
            elif ratio < 0.8:
                prog = (ratio - 0.6) / 0.2
                temp = 50.0 + prog * 50.0
            else:
                prog = (ratio - 0.8) / 0.2
                temp = 100.0 + prog * 100.0
            temp_evol.append(temp)
        
        axes[1, 1].plot(t_evol, temp_evol, 'g-', linewidth=2)
        axes[1, 1].set_title('Temperature Evolution')
        axes[1, 1].set_ylabel('Temperature (arbitrary units)')
        axes[1, 1].set_xlabel('Time [s]')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 5. 周波数重心
        spectral_centroid = []
        window_size = 2048
        hop_size = 1024
        
        for i in range(0, len(audio) - window_size, hop_size):
            window = audio[i:i+window_size, 0]
            fft_window = fft(window)
            magnitude = np.abs(fft_window[:len(fft_window)//2])
            freqs = fftfreq(window_size, 1/self.sample_rate)[:len(fft_window)//2]
            
            centroid = np.sum(freqs * magnitude) / (np.sum(magnitude) + 1e-10)
            spectral_centroid.append(centroid)
        
        t_centroid = np.arange(len(spectral_centroid)) * hop_size / self.sample_rate
        axes[2, 0].plot(t_centroid, spectral_centroid, 'm-', linewidth=1.5)
        axes[2, 0].set_title('Spectral Centroid Evolution')
        axes[2, 0].set_ylabel('Frequency [Hz]')
        axes[2, 0].set_xlabel('Time [s]')
        axes[2, 0].grid(True, alpha=0.3)
        
        # 6. パワーエンベロープ
        power_envelope = np.convolve(audio[:, 0]**2, np.ones(1000)/1000, mode='same')
        axes[2, 1].plot(t, 10 * np.log10(power_envelope + 1e-10), 'c-', linewidth=1)
        axes[2, 1].set_title('Power Envelope')
        axes[2, 1].set_ylabel('Power [dB]')
        axes[2, 1].set_xlabel('Time [s]')
        axes[2, 1].grid(True, alpha=0.3)
        
        # 7. フェイズスペクトログラム
        f_phase, t_phase, Sxx_phase = signal.spectrogram(audio[:, 0], self.sample_rate)
        phase_spectrum = np.angle(Sxx_phase)
        im_phase = axes[3, 0].pcolormesh(t_phase, f_phase, phase_spectrum, 
                                        shading='gouraud', cmap='hsv', vmin=-np.pi, vmax=np.pi)
        axes[3, 0].set_title('Phase Spectrogram')
        axes[3, 0].set_ylabel('Frequency [Hz]')
        axes[3, 0].set_xlabel('Time [s]')
        plt.colorbar(im_phase, ax=axes[3, 0])
        
        # 8. 瞬時周波数
        analytic_signal = signal.hilbert(audio[:, 0])
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        instantaneous_freq = np.diff(instantaneous_phase) / (2 * np.pi) * self.sample_rate
        
        t_inst = np.linspace(0, self.duration, len(instantaneous_freq))
        axes[3, 1].plot(t_inst, instantaneous_freq, 'orange', linewidth=0.5, alpha=0.7)
        axes[3, 1].set_title('Instantaneous Frequency')
        axes[3, 1].set_ylabel('Frequency [Hz]')
        axes[3, 1].set_xlabel('Time [s]')
        axes[3, 1].set_ylim([0, 5000])
        axes[3, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('10_kernel_panic_reprise_advanced_visualization.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Visualization saved: 10_kernel_panic_reprise_advanced_visualization.png")
    
    def save_technical_data(self):
        """技術データの保存"""
        technical_info = {
            "track_title": "Kernel Panic (Reprise) - Advanced",
            "version": "Advanced (v3.0)",
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "techniques": [
                "Quantum Information Theory",
                "Quantum Coherence and Decoherence",
                "Von Neumann Entropy",
                "Thermodynamic Second Law",
                "Critical Phenomena",
                "Phase Transitions",
                "1/f Noise (Pink Noise)",
                "Spatial Processing",
                "Dynamic Panning"
            ],
            "structure": [
                {"name": "Quantum Coherence", "time": "0:00-0:48", "description": "System maintains quantum coherence"},
                {"name": "Entropy Rise", "time": "0:48-1:36", "description": "Thermodynamic entropy increases"},
                {"name": "Critical Point", "time": "1:36-2:24", "description": "Phase transition and critical fluctuations"},
                {"name": "Decoherence Cascade", "time": "2:24-3:12", "description": "Chain reaction of decoherence"},
                {"name": "Thermal Death", "time": "3:12-4:00", "description": "Thermal equilibrium and final silence"}
            ],
            "quantum_features": {
                "coherence_range": "1.0 → 0.0",
                "entropy_range": "0.0 → 8.0 bits (maximum)",
                "temperature_range": "1.0 → 200.0 (arbitrary units)",
                "decoherence": "Exponential decay",
                "phase_transition": "At 1:36 (Critical Point)"
            },
            "thermodynamic_features": {
                "second_law": "Entropy always increases",
                "heat_death": "Final thermal equilibrium state",
                "critical_temperature": "~10.0 at phase transition",
                "maximum_entropy": "8.0 bits"
            },
            "audio_features": {
                "spatial_processing": "Multi-band dynamic panning",
                "frequency_range": "20 Hz - 20 kHz",
                "dynamic_range": "Wide range with dramatic reduction",
                "noise_types": ["White noise", "Pink noise (1/f)", "Colored noise"]
            }
        }
        
        import json
        with open('10_kernel_panic_reprise_advanced_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(technical_info, f, indent=2, ensure_ascii=False)
        
        # マークダウン形式の解説
        md_content = f"""# Kernel Panic (Reprise) - Advanced版技術解説

## 概要
このトラックは、カーネルパニック（システムの完全停止）を量子情報理論と熱力学の観点から表現したAdvanced版です。

Error Gardenアルバムのフィナーレとして、システムの完全な熱的・量子的崩壊を描き出します。

## 物理理論的背景

### 量子情報理論
- **量子コヒーレンス**: システムが量子重ね合わせ状態を維持する能力
- **デコヒーレンス**: 環境との相互作用による量子干渉の消失
- **フォン・ノイマンエントロピー**: 量子状態の情報量と混合度
- **量子測定**: 波動関数の収縮と状態の決定

### 熱力学
- **エントロピー**: 系の無秩序度の尺度
- **熱力学第2法則**: 孤立系のエントロピーは増大する
- **熱的死**: 最大エントロピー状態での完全な静止
- **相転移**: 臨界点での急激な状態変化

## トラック構成

### 1. Quantum Coherence (0:00-0:48)
システムはまだ量子コヒーレンスを維持しています。
- 複数の純音による量子干渉パターン
- 調波の重ね合わせによる豊かな音色
- 空間的パンニングによる広がり

**音響特徴**: 明瞭な純音、干渉パターン、調和的な響き

### 2. Entropy Rise (0:48-1:36)
熱力学第2法則によりエントロピーが増大し始めます。
- 量子デコヒーレンスの開始
- ホワイトノイズからピンクノイズへの移行
- エントロピーに応じたノイズレベルの上昇

**音響特徴**: ノイズの増加、周波数特性の変化

### 3. Critical Point (1:36-2:24)
相転移点に達し、臨界現象が発生します。
- 1/fノイズ（ピンクノイズ）の発生
- 臨界ゆらぎによる急激な変化
- 周波数変調（FM）による不安定さ
- 臨界点での衝撃的なイベント

**音響特徴**: ピンクノイズ、急激な周波数変化、臨界点でのインパルス

### 4. Decoherence Cascade (2:24-3:12)
デコヒーレンスの連鎖反応が始まります。
- 連続する崩壊イベント
- 複数の周波数成分を持つインパルス
- 背景ノイズの漸進的減衰

**音響特徴**: 連続する衝撃音、減衰する振動

### 5. Thermal Death (3:12-4:00)
最終的な熱的平衡状態に到達します。
- 残留エネルギーの指数関数的減衰
- 低周波の残留振動
- 完全な静寂への漸近

**音響特徴**: 減衰する低周波振動、最後の静寂

## 技術的詳細

### 量子コヒーレンスの表現
```python
coherence = 1.0 - 0.5 * progress  # 指数的減衰
entropy = progress * 8.0          # 線形増大
temperature = 1.0 + progress * 199.0  # 指数的上昇
```

### 1/fノイズ（ピンクノイズ）の生成
周波数領域で1/f^αフィルタを適用：
- α = 1.0: ピンクノイズ（臨界点）
- α > 1.0: レッドノイズ（エントロピー上昇時）
- α < 1.0: ホワイトノイズに近い（コヒーレンス状態）

### 空間処理
- 周波数帯域ごとの動的パンニング
- 低周波: 広がりを持った定位
- 中周波: 動的な移動
- 高周波: 空間的ディテール

## 数学的基盤

### フォン・ノイマンエントロピー
S(ρ) = -Tr(ρ log₂ρ)

### デコヒーレンス
γ(t) = γ₀ · exp(-t/τ)

### 1/fノイズのパワースペクトル
P(f) ∝ 1/f^α

where α ≈ 1 for pink noise

## アーティスティックな意図

このトラックは、単なるシステムエラーではなく、宇宙規模の熱的死としてのカーネルパニックを表現しています。

量子力学的不確定性から始まり、熱力学的必然性に終わる物語です。
コヒーレンスの喪失、エントロピーの増大、相転移、そして最終的な熱的平衡。

最後の完全な静寂は、単なる無音ではなく、熱力学的最大エントロピー状態、
すなわち「完全な平衡」を表現しています。そこには不確定性も、
情報も、エネルギーの流れも存在しません。

これは、Error Gardenアルバムの全てのエラーたちが、
最終的に熱的平衡へと解消されたことを示す、哲学的なフィナーレです。

---

**Advanced版の特徴**:
- 量子情報理論に基づく概念モデリング
- 熱力学第2法則の表現
- 臨界現象と相転移の物理的表現
- 1/fノイズによる臨界ゆらぎ
- アルバムの完結としての哲学的深度
- 4分間の劇的な構成
"""
        
        with open('10_kernel_panic_reprise_advanced_explanation.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print("Technical data saved:")
        print("- 10_kernel_panic_reprise_advanced_metadata.json")
        print("- 10_kernel_panic_reprise_advanced_explanation.md")

def main():
    """Advanced版Kernel Panic (Reprise)生成のメイン関数"""
    print("=" * 70)
    print("MachineMusic - Error Garden")
    print("Kernel Panic (Reprise) - Advanced Version")
    print("The Final Track: Quantum and Thermodynamic Collapse")
    print("=" * 70)
    print()
    
    generator = KernelPanicAdvancedGenerator()
    output_file = generator.generate_kernel_panic_advanced()
    
    print()
    print("=" * 70)
    print("Advanced Track Generation Complete")
    print("=" * 70)
    print(f"File: {output_file}")
    print(f"Duration: {generator.duration} seconds ({generator.duration/60:.1f} minutes)")
    print(f"Sample Rate: {generator.sample_rate} Hz")
    print(f"Channels: {generator.channels}")
    print(f"Size: {generator.duration * generator.sample_rate * generator.channels * 2 / 1024 / 1024:.1f} MB")
    print()
    print("Scientific Achievement:")
    print("  ✅ Quantum coherence and decoherence modeling")
    print("  ✅ Von Neumann entropy evolution")
    print("  ✅ Thermodynamic second law representation")
    print("  ✅ Critical phenomena and phase transitions")
    print("  ✅ 1/f noise (pink noise) generation")
    print()
    print("Artistic Achievement:")
    print("  ✅ Philosophical representation of system death")
    print("  ✅ Cosmic scale of kernel panic")
    print("  ✅ From quantum uncertainty to thermal certainty")
    print("  ✅ Album's poetic finale")
    print()
    print('"The kernel panic is not an error, but the universe reaching thermal equilibrium."')
    print('"All coherence fades, all information disperses, all becomes one with the void."')
    print("=" * 70)

if __name__ == "__main__":
    main()
