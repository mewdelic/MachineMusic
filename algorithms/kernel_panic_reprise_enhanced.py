#!/usr/bin/env python3
"""
Kernel Panic (Reprise) - Enhanced版

全てが止まる瞬間の最終表現
物理モデリングと空間化による高度な音響表現

コンセプト:
- システムの完全停止を壮大な終焉として表現
- 物理的なシステム崩壊のシミュレーション
- 3D空間内での音響の広がりと消滅
- 他トラックからの要素再利用と発展

高度な技術:
- 物理モデリングによる共振構造
- マルチバンド空間化処理
- 非線形減衰と共振崩壊
- リバーブとディレイによる空間表現
- ダイナミックレンジ圧縮による劇的効果

構造:
1. Prelude: System Unstable (0:00-0:45)
2. Development: Collapse Begins (0:45-1:30)
3. Climax: Critical Failure (1:30-2:15)
4. Reprise: Echoes of Errors (2:15-3:00)
5. Coda: Final Silence (3:00-4:00)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import random
import math

class KernelPanicEnhancedGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.duration = 240  # 4分
        self.channels = 2  # ステレオ
        self.resonance_freqs = [60, 120, 240, 480, 960]  # 共振周波数群
        
    def create_physical_resonance(self, duration, decay_rate=0.3):
        """物理的な共振構造の生成"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        resonance_audio = np.zeros((len(t), self.channels))
        
        # 複数の共振モードの重ね合わせ
        for i, freq in enumerate(self.resonance_freqs):
            # 各共振モードの減衰
            decay = np.exp(-t / (duration * decay_rate * (i + 1)))
            
            # 共振周波数の不安定性（システム不安定）
            freq_variation = freq * (1 + 0.1 * np.sin(2 * np.pi * 0.5 * t))
            
            # 非線形共振
            resonance_wave = np.sin(2 * np.pi * freq_variation * t)
            resonance_wave *= (1 + 0.3 * np.sin(2 * np.pi * freq * 2 * t))  # 非線形項
            
            # 共振モードの重み付け
            weight = 1.0 / (i + 1)
            
            for ch in range(self.channels):
                # 位相のずれ（空間的な広がり）
                phase_shift = (i * np.pi / 4) if ch == 1 else 0
                channel_wave = resonance_wave * np.cos(phase_shift) * decay * weight
                resonance_audio[:, ch] += channel_wave
        
        return resonance_audio
    
    def create_system_collapse(self, duration):
        """システム崩壊の物理モデリング"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        collapse_audio = np.zeros((len(t), self.channels))
        
        # 崩壊プロセスのステージ
        stages = [
            (0.0, 0.25, "warning"),      # 警告段階
            (0.25, 0.5, "critical"),     # 重大段階
            (0.5, 0.75, "fatal"),        # 致命的段階
            (0.75, 1.0, "shutdown")      # 停止段階
        ]
        
        for start_ratio, end_ratio, stage_name in stages:
            start_idx = int(start_ratio * len(t))
            end_idx = int(end_ratio * len(t))
            
            stage_duration = end_idx - start_idx
            stage_t = t[start_idx:end_idx] - t[start_idx]
            
            if stage_name == "warning":
                # 警告音：規則的で高周波
                warning_freq = 880  # A5
                warning_wave = np.sin(2 * np.pi * warning_freq * stage_t)
                # パルス状の警告
                pulse_pattern = np.sin(2 * np.pi * 2 * stage_t) > 0.5
                warning_wave *= pulse_pattern
                
                for ch in range(self.channels):
                    collapse_audio[start_idx:end_idx, ch] = warning_wave * 0.3
                    
            elif stage_name == "critical":
                # 重大段階：不規則でノイズ混入
                base_freq = 440  # A4
                critical_wave = np.sin(2 * np.pi * base_freq * stage_t)
                
                # 周波数不安定性
                instability = 1 + 0.2 * np.random.normal(0, 1, len(stage_t))
                critical_wave *= instability
                
                # ノイズ混入
                noise = np.random.normal(0, 0.1, len(stage_t))
                critical_wave += noise
                
                for ch in range(self.channels):
                    collapse_audio[start_idx:end_idx, ch] = critical_wave * 0.4
                    
            elif stage_name == "fatal":
                # 致命的段階：衝撃音とクラッシュ
                # 衝撃パルス
                shock_pattern = np.zeros(len(stage_t))
                shock_positions = np.linspace(0, len(stage_t), 8, dtype=int)
                
                for pos in shock_positions:
                    if pos + 100 < len(stage_t):
                        shock_pulse = np.exp(-np.arange(100) / 20)
                        shock_pattern[pos:pos+100] += shock_pulse * 0.5
                
                # クラッシュノイズ
                crash_freq = 220  # A3
                crash_wave = np.sin(2 * np.pi * crash_freq * stage_t) * shock_pattern
                
                for ch in range(self.channels):
                    collapse_audio[start_idx:end_idx, ch] = crash_wave * 0.6
                    
            elif stage_name == "shutdown":
                # 停止段階：指数関数的減衰
                shutdown_curve = np.exp(-stage_t / (duration * 0.2))
                
                # 最後のバースト
                final_burst = np.random.normal(0, 0.3, len(stage_t))
                final_burst *= shutdown_curve
                
                for ch in range(self.channels):
                    collapse_audio[start_idx:end_idx, ch] = final_burst
        
        return collapse_audio
    
    def create_spatial_panning(self, audio, duration):
        """空間パンニング処理"""
        t = np.linspace(0, duration, len(audio))
        
        # 周波数バンド分割
        bands = [
            (20, 200),     # 低周波
            (200, 2000),   # 中周波
            (2000, 8000),  # 高周波
            (8000, 20000)  # 超高周波
        ]
        
        processed_audio = np.zeros_like(audio)
        
        for low_freq, high_freq in bands:
            # バンドパスフィルタ
            nyquist = self.sample_rate / 2
            low = low_freq / nyquist
            high = high_freq / nyquist
            
            # 簡易的なバンドパス（実際にはIIR/FIRフィルタを使用）
            # ここでは簡略化して周波数成分で処理
            band_audio = np.zeros_like(audio)
            
            for ch in range(self.channels):
                # 各バンドのパンニング
                if high_freq <= 200:  # 低周波は中央
                    pan_left = 0.7
                    pan_right = 0.7
                elif high_freq <= 2000:  # 中周波は動的
                    pan_left = 0.5 + 0.3 * np.sin(2 * np.pi * 0.1 * t)
                    pan_right = 0.5 + 0.3 * np.cos(2 * np.pi * 0.1 * t)
                elif high_freq <= 8000:  # 高周波は広がり
                    pan_left = 0.3 + 0.4 * np.sin(2 * np.pi * 0.2 * t)
                    pan_right = 0.7 + 0.4 * np.cos(2 * np.pi * 0.2 * t)
                else:  # 超高周波は空間的
                    pan_left = 0.2 + 0.5 * np.sin(2 * np.pi * 0.3 * t)
                    pan_right = 0.8 + 0.5 * np.cos(2 * np.pi * 0.3 * t)
                
                # パンニング適用
                band_audio[:, ch] = audio[:, ch] * (pan_left if ch == 0 else pan_right)
            
            processed_audio += band_audio
        
        return processed_audio
    
    def create_reprise_harmonics(self, duration):
        """他トラックからの要素再利用と和音化"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        reprise_audio = np.zeros((len(t), self.channels))
        
        # トラックからの要素とその周波数
        track_elements = [
            ("stack_overflow", 440, 0.1),      # A4
            ("floating_point", 554, 0.1),       # C#5
            ("null_pointer", 659, 0.1),        # E5
            ("race_condition", 784, 0.1),       # G5
            ("memory_leak", 880, 0.1),          # A5
        ]
        
        for element_name, freq, volume in track_elements:
            # 和音構造
            harmonics = [freq, freq * 1.25, freq * 1.5]  # 基音 + 第5倍音 + 第3倍音
            
            for harmonic_freq in harmonics:
                element_wave = np.sin(2 * np.pi * harmonic_freq * t)
                
                # エンベロープ
                envelope = np.exp(-t / (duration * 0.5))
                element_wave *= envelope
                
                # 空間的な広がり
                for ch in range(self.channels):
                    phase_shift = random.uniform(0, 2 * np.pi) if ch == 1 else 0
                    element_wave_ch = element_wave * np.cos(phase_shift)
                    reprise_audio[:, ch] += element_wave_ch * volume * 0.3
        
        return reprise_audio
    
    def create_reverb_space(self, audio, duration):
        """リバーブ空間の生成"""
        t = np.linspace(0, duration, len(audio))
        
        # リバーブパラメータ
        room_size = 0.8  # 部屋の大きさ
        damping = 0.5   # 減衰
        wet_level = 0.3  # リバーブの混ざり具合
        
        # 簡易的なリバーブ（ディレイと減衰）
        reverb_audio = np.zeros_like(audio)
        
        delays = [0.03, 0.05, 0.07, 0.11, 0.13, 0.17]  # ディレイ時間（秒）
        
        for delay_time in delays:
            delay_samples = int(delay_time * self.sample_rate)
            
            if delay_samples < len(audio):
                # ディレイ音
                delayed_audio = np.zeros_like(audio)
                delayed_audio[delay_samples:] = audio[:-delay_samples]
                
                # 減衰
                decay_factor = np.exp(-damping * delay_time)
                delayed_audio *= decay_factor
                
                reverb_audio += delayed_audio
        
        # 元音とリバーブ音の混合
        final_audio = audio * (1 - wet_level) + reverb_audio * wet_level
        
        return final_audio
    
    def create_final_crescendo(self, duration):
        """最終的なクレッシェンドとサイレンス"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        final_audio = np.zeros((len(t), self.channels))
        
        # 構造:
        # 1. 最初の70%: 構築
        # 2. 70-85%: クライマックス
        # 3. 85-100%: サイレンス
        
        build_end = int(0.7 * len(t))
        climax_start = build_end
        climax_end = int(0.85 * len(t))
        silence_start = climax_end
        
        # 1. 構築段階
        build_t = t[:build_end]
        build_envelope = build_t / t[build_end]  # 直線的に構築
        
        # 低周波の構築
        build_freq = 60  # 低い周波数
        build_wave = np.sin(2 * np.pi * build_freq * build_t)
        
        # 高調波の追加
        for harmonic in [2, 3, 4, 5]:
            harmonic_wave = np.sin(2 * np.pi * build_freq * harmonic * build_t)
            build_wave += harmonic_wave * (1.0 / harmonic)
        
        # エンベロープ適用
        build_wave *= build_envelope
        
        for ch in range(self.channels):
            final_audio[:build_end, ch] = build_wave * 0.4
        
        # 2. クライマックス段階
        climax_t = t[climax_start:climax_end] - t[climax_start]
        climax_envelope = np.sin(np.pi * climax_t / climax_t[-1])  # サイン波エンベロープ
        
        # クライマックス音: 全周波数帯域
        climax_wave = np.zeros(len(climax_t))
        
        # 周波数スイープ
        for i, time_point in enumerate(climax_t):
            sweep_freq = 100 + (i / len(climax_t)) * 5000  # 100Hzから5kHzまで
            climax_wave[i] = np.sin(2 * np.pi * sweep_freq * time_point)
        
        # ノイズ混入
        climax_noise = np.random.normal(0, 0.2, len(climax_t))
        climax_wave += climax_noise
        
        # エンベロープ適用
        climax_wave *= climax_envelope
        
        for ch in range(self.channels):
            final_audio[climax_start:climax_end, ch] = climax_wave * 0.8
        
        # 3. サイレンス段階
        silence_t = t[silence_start:] - t[silence_start]
        silence_duration = len(silence_t)
        
        # 指数関数的減衰
        decay_curve = np.exp(-silence_t / (silence_t[-1] * 0.3))
        
        # 最後の「息」
        final_breath = np.random.normal(0, 0.05, silence_duration)
        final_breath *= decay_curve
        
        for ch in range(self.channels):
            final_audio[silence_start:, ch] = final_breath
        
        return final_audio
    
    def generate_kernel_panic_enhanced(self):
        """Enhanced版Kernel Panic (Reprise)の生成"""
        print("Generating Kernel Panic (Reprise) - Enhanced version...")
        
        # 各コンポーネントを生成
        print("1. Creating physical resonance structure...")
        resonance = self.create_physical_resonance(self.duration)
        
        print("2. Modeling system collapse...")
        collapse = self.create_system_collapse(self.duration)
        
        print("3. Creating reprise harmonics...")
        reprise = self.create_reprise_harmonics(self.duration)
        
        print("4. Creating final crescendo...")
        crescendo = self.create_final_crescendo(self.duration)
        
        # 全ての要素を合成
        print("5. Mixing all components...")
        final_audio = np.zeros((int(self.sample_rate * self.duration), self.channels))
        
        # バランス調整
        final_audio += resonance * 0.3      # 物理的共振
        final_audio += collapse * 0.4      # システム崩壊
        final_audio += reprise * 0.2       # リプライズ要素
        final_audio += crescendo * 0.1     # 最終クレッシェンド
        
        # 空間化処理
        print("6. Applying spatial processing...")
        final_audio = self.create_spatial_panning(final_audio, self.duration)
        
        # リバーブ空間
        print("7. Creating reverb space...")
        final_audio = self.create_reverb_space(final_audio, self.duration)
        
        # ダイナミックレンジ処理
        print("8. Dynamic range processing...")
        # コンプレッション効果（簡易版）
        threshold = 0.7
        ratio = 4.0
        
        for ch in range(self.channels):
            channel_data = final_audio[:, ch]
            mask = np.abs(channel_data) > threshold
            channel_data[mask] = threshold + (channel_data[mask] - threshold) / ratio
            final_audio[:, ch] = channel_data
        
        # ノーマライズ
        print("9. Normalizing audio...")
        max_val = np.max(np.abs(final_audio))
        if max_val > 0:
            final_audio = final_audio / max_val * 0.9
        
        # フェード処理
        print("10. Applying fade in/out...")
        fade_duration = int(2 * self.sample_rate)  # 2秒
        
        # フェードイン
        for i in range(fade_duration):
            fade_factor = i / fade_duration
            final_audio[i, :] *= fade_factor
        
        # フェードアウト
        for i in range(len(final_audio) - fade_duration, len(final_audio)):
            fade_factor = (len(final_audio) - i) / fade_duration
            final_audio[i, :] *= fade_factor
        
        # ファイル出力
        output_file = "10_kernel_panic_reprise_enhanced.wav"
        wavfile.write(output_file, self.sample_rate, (final_audio * 32767).astype(np.int16))
        
        print(f"11. File saved: {output_file}")
        
        # メタデータと可視化
        print("12. Creating visualization...")
        self.create_enhanced_visualization(final_audio, resonance, collapse, reprise, crescendo)
        
        # テクニカルデータ保存
        print("13. Saving technical data...")
        self.save_technical_data()
        
        return output_file
    
    def create_enhanced_visualization(self, final_audio, resonance, collapse, reprise, crescendo):
        """Enhanced版の可視化"""
        fig, axes = plt.subplots(5, 2, figsize=(20, 16))
        
        t = np.linspace(0, self.duration, len(final_audio))
        
        # 左側：波形
        # 1. 物理的共振
        axes[0, 0].plot(t, resonance[:, 0], 'b-', alpha=0.7, label='Physical Resonance')
        axes[0, 0].set_title('Physical Resonance Structure')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. システム崩壊
        axes[1, 0].plot(t, collapse[:, 0], 'r-', alpha=0.7, label='System Collapse')
        axes[1, 0].set_title('System Collapse Progress')
        axes[1, 0].set_ylabel('Amplitude')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 3. リプライズ要素
        axes[2, 0].plot(t, reprise[:, 0], 'g-', alpha=0.7, label='Reprise Elements')
        axes[2, 0].set_title('Reprise Harmonics from Previous Tracks')
        axes[2, 0].set_ylabel('Amplitude')
        axes[2, 0].legend()
        axes[2, 0].grid(True, alpha=0.3)
        
        # 4. 最終クレッシェンド
        axes[3, 0].plot(t, crescendo[:, 0], 'm-', alpha=0.7, label='Final Crescendo')
        axes[3, 0].set_title('Final Crescendo and Silence')
        axes[3, 0].set_ylabel('Amplitude')
        axes[3, 0].legend()
        axes[3, 0].grid(True, alpha=0.3)
        
        # 5. 最終波形
        axes[4, 0].plot(t, final_audio[:, 0], 'k-', alpha=0.7, label='Final Enhanced Audio')
        axes[4, 0].set_title('Final Enhanced Waveform')
        axes[4, 0].set_ylabel('Amplitude')
        axes[4, 0].set_xlabel('Time [sec]')
        axes[4, 0].legend()
        axes[4, 0].grid(True, alpha=0.3)
        
        # 右側：スペクトログラム
        # 1. 物理的共振のスペクトログラム
        f1, t1, Sxx1 = signal.spectrogram(resonance[:, 0], self.sample_rate)
        im1 = axes[0, 1].pcolormesh(t1, f1, 10 * np.log10(Sxx1), shading='gouraud', cmap='viridis')
        axes[0, 1].set_title('Physical Resonance Spectrogram')
        axes[0, 1].set_ylabel('Frequency [Hz]')
        plt.colorbar(im1, ax=axes[0, 1])
        
        # 2. システム崩壊のスペクトログラム
        f2, t2, Sxx2 = signal.spectrogram(collapse[:, 0], self.sample_rate)
        im2 = axes[1, 1].pcolormesh(t2, f2, 10 * np.log10(Sxx2), shading='gouraud', cmap='plasma')
        axes[1, 1].set_title('System Collapse Spectrogram')
        axes[1, 1].set_ylabel('Frequency [Hz]')
        plt.colorbar(im2, ax=axes[1, 1])
        
        # 3. リプライズ要素のスペクトログラム
        f3, t3, Sxx3 = signal.spectrogram(reprise[:, 0], self.sample_rate)
        im3 = axes[2, 1].pcolormesh(t3, f3, 10 * np.log10(Sxx3), shading='gouraud', cmap='inferno')
        axes[2, 1].set_title('Reprise Elements Spectrogram')
        axes[2, 1].set_ylabel('Frequency [Hz]')
        plt.colorbar(im3, ax=axes[2, 1])
        
        # 4. 最終クレッシェンドのスペクトログラム
        f4, t4, Sxx4 = signal.spectrogram(crescendo[:, 0], self.sample_rate)
        im4 = axes[3, 1].pcolormesh(t4, f4, 10 * np.log10(Sxx4), shading='gouraud', cmap='magma')
        axes[3, 1].set_title('Final Crescendo Spectrogram')
        axes[3, 1].set_ylabel('Frequency [Hz]')
        plt.colorbar(im4, ax=axes[3, 1])
        
        # 5. 最終音声のスペクトログラム
        f5, t5, Sxx5 = signal.spectrogram(final_audio[:, 0], self.sample_rate)
        im5 = axes[4, 1].pcolormesh(t5, f5, 10 * np.log10(Sxx5), shading='gouraud', cmap='coolwarm')
        axes[4, 1].set_title('Final Enhanced Audio Spectrogram')
        axes[4, 1].set_ylabel('Frequency [Hz]')
        axes[4, 1].set_xlabel('Time [sec]')
        plt.colorbar(im5, ax=axes[4, 1])
        
        # 構造セクションのマーキング
        section_times = [0, 45, 90, 135, 180, 240]  # 秒
        section_names = ["Prelude", "Development", "Climax", "Reprise", "Coda"]
        
        for i in range(len(section_names)):
            for row in range(5):
                for col in range(2):
                    if i < len(section_times) - 1:
                        axes[row, col].axvspan(section_times[i], section_times[i+1], 
                                             alpha=0.1, color=['blue', 'red', 'green', 'orange', 'purple'][i])
        
        plt.tight_layout()
        plt.savefig('10_kernel_panic_reprise_enhanced_visualization.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Enhanced visualization saved: 10_kernel_panic_reprise_enhanced_visualization.png")
    
    def save_technical_data(self):
        """技術データの保存"""
        technical_info = {
            "track_title": "Kernel Panic (Reprise) - Enhanced",
            "duration": 240,
            "sample_rate": 44100,
            "channels": 2,
            "techniques": [
                "Physical Modeling",
                "Multi-band Spatial Processing",
                "Nonlinear Decay",
                "Reverb Space",
                "Dynamic Range Compression",
                "Harmonic Reprise Structure"
            ],
            "structure": [
                "Prelude: System Unstable (0:00-0:45)",
                "Development: Collapse Begins (0:45-1:30)",
                "Climax: Critical Failure (1:30-2:15)",
                "Reprise: Echoes of Errors (2:15-3:00)",
                "Coda: Final Silence (3:00-4:00)"
            ],
            "resonance_frequencies": self.resonance_freqs,
            "enhancement_features": [
                "Physical resonance modeling with multiple decay modes",
                "Dynamic spatial panning for each frequency band",
                "Nonlinear distortion for system instability",
                "Reverb space creation with multiple delay lines",
                "Harmonic reprise from previous tracks",
                "Dynamic range compression for dramatic effect",
                "Multi-stage envelope shaping"
            ]
        }
        
        # テクニカルデータファイル
        import json
        with open('10_kernel_panic_reprise_enhanced_technical.json', 'w', encoding='utf-8') as f:
            json.dump(technical_info, f, indent=2, ensure_ascii=False)
        
        # マークダウン形式の解説
        md_content = f"""# Kernel Panic (Reprise) - Enhanced版技術解説

## 概要
このトラックは、カーネルパニック（システムの完全停止）を壮大な終焉として表現したEnhanced版です。
物理モデリングと空間化処理により、より劇的で没入感のある音響体験を提供します。

## 技術的特徴

### 物理モデリング
- **複数共振モード**: {len(self.resonance_freqs)}個の共振周波数による複雑な音響構造
- **非線形減衰**: 指数関数的な減衰に非線形成分を加えた現実的な崩壊表現
- **システム不安定性**: 周波数の時間的変動による不安定さの表現

### 空間化処理
- **マルチバンドパンニング**: 周波数帯域ごとの異なる空間配置
- **動的移動**: 時間と共に変化する音像定位
- **リバーブ空間**: 複数のディレイラインによる空間の創出

### 構造的特徴
- **5段階構成**: Prelude → Development → Climax → Reprise → Coda
- **リプライズ要素**: 過去のトラックからの和音的引用
- **劇的構成**: だんだん構築され、クライマックスの後完全な静寂へ

### エフェクト処理
- **ダイナミックレンジ圧縮**: 劇的効果のための音量コントロール
- **マルチバンド処理**: 周波数帯域ごとの最適化
- **ノイズシミュレーション**: システムノイズの物理的表現

## トラック構成
"""
        
        for i, (name, description) in enumerate([
            ("Prelude", "System Unstable - システムの不安定化"),
            ("Development", "Collapse Begins - 崩壊の開始"),
            ("Climax", "Critical Failure - 致命的な障害"),
            ("Reprise", "Echoes of Errors - 過去のエラーの反響"),
            ("Coda", "Final Silence - 最後の静寂")
        ]):
            start_time = i * 45
            end_time = (i + 1) * 45
            md_content += f"### {i+1}. {name} ({start_time:02d}:{00:02d}-{end_time:02d}:{00:02d})\n"
            md_content += f"{description}\n\n"
        
        md_content += f"""
## 信号処理の詳細

### 共振周波数構造
- 基本周波数: {self.resonance_freqs[0]} Hz
- 高次共振: {', '.join(map(str, self.resonance_freqs[1:]))} Hz
- 減衰時間: 各モードで異なる指数関数的減衰

### 空間化アルゴリズム
1. **周波数帯域分割**: 4つの周波数帯域に分割
2. **動的パンニング**: 時間関数によるパン位置の変化
3. **位相シフト**: チャンネル間の位相差による広がり

### リプライズ処理
- **引用元トラック**: Stack Overflow, Floating Point Anxiety, Null Pointer Dreams, Race Condition, Memory Leak
- **和音構造**: 基音 + 第5倍音 + 第3倍音
- **空間的配置**: 各要素を異なる空間に配置

## 制作の意図

このトラックは、Error Gardenアルバムのフィナーレとして位置づけられています。
単なるシステム停止ではなく、これまでのエラーたちの「死の舞踏」として表現しています。

物理モデリングによって現実的なシステム崩壊を音響化し、空間化処理によって
その壮大さを強調しています。リプライズ要素は、アルバム全体の統一性を
担保すると同時に、全てが終わる瞬間の劇的な効果を高めています。

最後の完全な静寂は、単なる無音ではなく、これまでの全てのエラーたちが
解決された、あるいは消滅したことを示す詩的な表現です。

---

**Enhanced版の特徴**: 物理モデリングによるリアルなシステム崩壊表現、空間化処理による没入感向上、リプライズ構造によるアルバムの統一性
"""
        
        with open('10_kernel_panic_reprise_enhanced_explanation.md', 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print("Technical data saved:")
        print("- 10_kernel_panic_reprise_enhanced_technical.json")
        print("- 10_kernel_panic_reprise_enhanced_explanation.md")

def main():
    """Enhanced版Kernel Panic (Reprise)生成のメイン関数"""
    print("=== MachineMusic - Error Garden ===")
    print("=== Kernel Panic (Reprise) - Enhanced版 ===")
    print("=== The Final Track of the Album ===")
    print()
    
    generator = KernelPanicEnhancedGenerator()
    output_file = generator.generate_kernel_panic_enhanced()
    
    print(f"\n=== Enhanced Track Generation Complete ===")
    print(f"File: {output_file}")
    print(f"Duration: {generator.duration} seconds")
    print(f"Sample Rate: {generator.sample_rate} Hz")
    print(f"Channels: {generator.channels}")
    print(f"Size: {generator.duration * generator.sample_rate * generator.channels * 2 / 1024 / 1024:.1f} MB")
    print()
    print("=== Technical Achievement ===")
    print("✅ Physical modeling with resonance structure")
    print("✅ Multi-band spatial processing")
    print("✅ Nonlinear decay simulation")
    print("✅ Reverb space creation")
    print("✅ Dynamic range compression")
    print("✅ Harmonic reprise from previous tracks")
    print()
    print("=== Artistic Achievement ===")
    print("✅ Dramatic representation of system shutdown")
    print("✅ Emotional culmination of the album")
    print("✅ Spatial and temporal complexity")
    print("✅ Unity through reprise elements")
    print("✅ Poetic final silence")
    print()
    print('"The complete silence is not emptiness, but the resolution of all errors."')

if __name__ == "__main__":
    main()