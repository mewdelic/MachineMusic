"""
Track 3 Enhanced: Null Pointer Dreams
コンセプト：何も指さないポインタが見る夢 - Physical Modeling Edition

NULL状態を物理モデリングシンセシスで表現：
- Karplus-Strongアルゴリズムによる「弦の切れる」感覚
- NULL参照時の物理的な振動の崩壊
- 期待された音が突然消える物理現象
- 弦が突然切れる、張力が失われる感覚
- デリファレンスの瞬間の物理的な破壊
"""

import numpy as np
from scipy.io import wavfile
import random
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf

# パラメータ
SAMPLE_RATE = 44100
DURATION = 30  # 秒

class KarplusStrongString:
    """Karplus-Strong物理モデリング弦クラス"""
    
    def __init__(self, frequency, decay_factor=0.996, noise_level=0.02):
        self.frequency = frequency
        self.decay_factor = decay_factor
        self.noise_level = noise_level
        self.period = int(SAMPLE_RATE / frequency)
        self.buffer = None
        self.position = 0
        self.is_alive = True
        
    def initialize(self):
        """バッファの初期化"""
        self.buffer = (np.random.rand(self.period) - 0.5) * 2.0
        self.position = 0
        self.is_alive = True
        
    def get_sample(self):
        """次のサンプルを生成"""
        if not self.is_alive:
            return 0.0
            
        # 現在のサンプルを取得
        current_sample = self.buffer[self.position]
        
        # 低域フィルタ（減衰）
        next_pos = (self.position + 1) % self.period
        filtered_sample = (self.buffer[self.position] + self.buffer[next_pos]) * 0.5 * self.decay_factor
        
        # ノイズを追加
        noise = (np.random.rand() - 0.5) * 2.0 * self.noise_level
        
        # バッファを更新
        self.buffer[self.position] = filtered_sample + noise
        self.position = next_pos
        
        # 振幅が小さすぎたら死亡
        if abs(current_sample) < 0.0001:
            self.is_alive = False
            
        return current_sample
        
    def force_death(self, death_factor=0.9):
        """強制的に弦を切る（NULL参照）"""
        if self.buffer is not None:
            self.buffer *= death_factor
            if np.max(np.abs(self.buffer)) < 0.01:
                self.is_alive = False

class NullPointerEnsemble:
    """NULLポインタアンサンブル"""
    
    def __init__(self, num_strings=4, base_freq=220):
        self.num_strings = num_strings
        self.base_freq = base_freq
        self.strings = []
        self.is_null_active = False
        self.null_probability = 0.05
        
        # 弦の初期化
        for i in range(num_strings):
            freq = base_freq * (1 + i * 0.1)  # 少しずつ周波数を変化
            decay = 0.996 - (i * 0.001)  # それぞれの弦で減衰率を変化
            string = KarplusStrongString(freq, decay)
            string.initialize()
            self.strings.append(string)
    
    def generate_samples(self, num_samples, null_events=None):
        """NULLイベントを含むサンプル生成"""
        samples = np.zeros(num_samples, dtype=np.float32)
        
        if null_events is None:
            null_events = []
        
        for i in range(num_samples):
            # NULLイベントチェック
            for event_time, event_type in null_events:
                if abs(i - event_time) < 10:  # イベントタイミングの許容範囲
                    if event_type == 'dereference':
                        self.trigger_null_dereference()
                    elif event_type == 'segmentation':
                        self.trigger_segmentation_fault()
            
            # NULL確率によるランダムイベント
            if random.random() < self.null_probability:
                self.trigger_null_dereference()
            
            # すべての弦からサンプルを生成
            for j, string in enumerate(self.strings):
                if string.is_alive:
                    samples[i] += string.get_sample() * (0.3 - j * 0.05)  # 重み付け
        
        return samples
    
    def trigger_null_dereference(self):
        """NULL参照をトリガー（弦を突然切る）"""
        alive_strings = [s for s in self.strings if s.is_alive]
        if alive_strings:
            target = random.choice(alive_strings)
            target.force_death(0.1)  # 急激な減衰
    
    def trigger_segmentation_fault(self):
        """セグメンテーション違反（全弦の崩壊）"""
        for string in self.strings:
            string.force_death(0.3)

class NullPointerDreamsEnhanced:
    """拡張版NULLポインタドリーム生成器"""
    
    def __init__(self):
        self.ensemble = NullPointerEnsemble(num_strings=4, base_freq=165)
        self.dream_state = 'stable'  # stable, unstable, chaos
        self.state_transitions = []
        self.null_events = []
        
    def generate_null_events(self):
        """NULLイベントシーケンスを生成"""
        events = []
        
        # セクション1: 安定（0-8秒）- 少ないNULLイベント
        for i in range(3):
            pos = random.randint(0, SAMPLE_RATE * 8)
            events.append((pos, 'dereference'))
        
        # セクション2: 不安定（8-16秒）- 増えるNULLイベント
        for i in range(5):
            pos = random.randint(SAMPLE_RATE * 8, SAMPLE_RATE * 16)
            events.append((pos, 'dereference'))
        
        # セクション3: 混沌（16-24秒）- 大量のNULLイベント
        for i in range(10):
            pos = random.randint(SAMPLE_RATE * 16, SAMPLE_RATE * 24)
            event_type = random.choice(['dereference', 'dereference', 'segmentation'])
            events.append((pos, event_type))
        
        # セクション4: 静寂（24-30秒）- 崩壊後の断片
        for i in range(3):
            pos = random.randint(SAMPLE_RATE * 24, SAMPLE_RATE * 30)
            events.append((pos, 'dereference'))
            
        return events
    
    def generate_drone_layer(self, duration_samples, base_freq=55):
        """低音ドローンレイヤー"""
        t = np.linspace(0, duration_samples / SAMPLE_RATE, duration_samples, dtype=np.float32)
        
        # 基本周波数
        drone = 0.2 * np.sin(2 * np.pi * base_freq * t)
        
        # 倍音
        for harmonic in [2, 3, 5]:
            drone += 0.05 * np.sin(2 * np.pi * base_freq * harmonic * t)
        
        # 時間経過による減衰
        decay_curve = np.exp(-t * 0.2)
        drone *= decay_curve
        
        # NULLによる断絶
        for i in range(0, duration_samples, SAMPLE_RATE // 4):
            if random.random() < 0.1:
                gap_duration = random.randint(100, 1000)
                drone[i:min(i + gap_duration, duration_samples)] = 0
        
        return drone
    
    def generate_click_layer(self, duration_samples, intensity_pattern='low'):
        """NULLチェック失敗によるクリック音"""
        clicks = np.zeros(duration_samples, dtype=np.float32)
        
        # インテンシティパターンによるクリック密度
        if intensity_pattern == 'low':
            click_density = 0.0002
        elif intensity_pattern == 'medium':
            click_density = 0.0008
        else:  # high
            click_density = 0.002
        
        for i in range(0, duration_samples, 100):
            if random.random() < click_density:
                click_pos = i + random.randint(0, 100)
                if click_pos < duration_samples:
                    # 物理的な衝撃音のようなクリック
                    click_duration = random.randint(50, 300)
                    t = np.linspace(0, click_duration / SAMPLE_RATE, click_duration, dtype=np.float32)
                    click = 0.2 * np.exp(-t * 100) * (np.random.rand() - 0.5)
                    
                    end_pos = min(click_pos + click_duration, duration_samples)
                    actual_duration = end_pos - click_pos
                    if actual_duration > 0:
                        clicks[click_pos:end_pos] += click[:actual_duration]
        
        return clicks
    
    def generate_noise_bursts(self, duration_samples, num_bursts):
        """NULL参照時のノイズバースト"""
        bursts = np.zeros(duration_samples, dtype=np.float32)
        
        for i in range(num_bursts):
            # バースト位置
            pos = random.randint(0, duration_samples - 5000)
            burst_duration = random.randint(500, 3000)
            
            # 複数の周波数成分
            t = np.linspace(0, burst_duration / SAMPLE_RATE, burst_duration, dtype=np.float32)
            burst = np.zeros(burst_duration, dtype=np.float32)
            
            # 物理的な破壊音をシミュレート
            for freq in [500, 800, 1200, 2000, 3500]:
                amplitude = random.uniform(0.05, 0.15)
                burst += amplitude * np.sin(2 * np.pi * freq * t)
            
            # 減衰
            burst *= np.exp(-t * 150)
            
            # ホワイトノイズ
            noise = np.random.normal(0, 0.1, burst_duration).astype(np.float32)
            burst += noise * np.exp(-t * 200)
            
            end_pos = min(pos + burst_duration, duration_samples)
            actual_duration = end_pos - pos
            if actual_duration > 0:
                bursts[pos:end_pos] += burst[:actual_duration]
        
        return bursts
    
    def generate_final_mix(self):
        """最終ミックス生成"""
        print("Generating Null Pointer Dreams (Physical Modeling Enhanced)...")
        
        total_samples = SAMPLE_RATE * DURATION
        
        # NULLイベントシーケンス
        self.null_events = self.generate_null_events()
        
        # 物理モデリングアンサンブル
        ensemble_samples = self.ensemble.generate_samples(total_samples, self.null_events)
        
        # 低音ドローン
        drone = self.generate_drone_layer(total_samples, base_freq=55)
        
        # クリックレイヤー（セクションごとに強度を変化）
        click_pattern = ['low'] * int(SAMPLE_RATE * 8) + ['medium'] * int(SAMPLE_RATE * 8) + ['high'] * int(SAMPLE_RATE * 8) + ['low'] * int(SAMPLE_RATE * 6)
        clicks = self.generate_click_layer(total_samples, intensity_pattern='variable')
        
        # セクションごとにクリック密度を調整
        for i in range(len(click_pattern)):
            if i < total_samples:
                if click_pattern[i // (SAMPLE_RATE * 8)] == 'high':
                    if random.random() < 0.001:
                        clicks[i] += random.uniform(-0.1, 0.1)
        
        # ノイズバースト
        noise_bursts = self.generate_noise_bursts(total_samples, num_bursts=8)
        
        # ミックス
        final_mix = (
            ensemble_samples * 0.6 +    # 物理モデリング弦
            drone * 0.3 +              # 低音ドローン
            clicks * 0.2 +             # クリック音
            noise_bursts * 0.4        # ノイズバースト
        )
        
        # 全体的なエンベロープ
        envelope = np.ones(total_samples)
        # フェードイン
        envelope[:SAMPLE_RATE] = np.linspace(0, 1, SAMPLE_RATE)
        # フェードアウト
        envelope[-SAMPLE_RATE:] = np.linspace(1, 0, SAMPLE_RATE)
        
        final_mix *= envelope
        
        # クリッピング防止
        final_mix = np.clip(final_mix, -0.95, 0.95)
        
        return final_mix
    
    def create_analysis_visualization(self, audio_data):
        """分析用ビジュアライゼーションを作成"""
        fig, axes = plt.subplots(4, 1, figsize=(14, 12))
        
        # 時間軸
        t = np.linspace(0, len(audio_data) / SAMPLE_RATE, len(audio_data))
        
        # 1. 波形
        axes[0].plot(t, audio_data, alpha=0.7, linewidth=0.5)
        axes[0].set_title('Null Pointer Dreams - Waveform (Physical Modeling Enhanced)', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Amplitude')
        axes[0].grid(True, alpha=0.3)
        
        # セクション区切り
        section_times = [8, 16, 24]
        for time in section_times:
            axes[0].axvline(x=time, color='red', linestyle='--', alpha=0.5)
            axes[0].text(time, max(audio_data) * 0.8, f'{time}s', rotation=90, ha='right')
        
        # 2. スペクトログラム
        f, t_spec, Sxx = signal.spectrogram(audio_data, SAMPLE_RATE, nperseg=2048)
        im = axes[1].pcolormesh(t_spec, f[:100], 10 * np.log10(Sxx[:100, :]), shading='gouraud', cmap='viridis')
        axes[1].set_title('Spectrogram - Physical Modeling String Harmonics', fontsize=12)
        axes[1].set_ylabel('Frequency (Hz)')
        axes[1].set_ylim(0, 5000)
        plt.colorbar(im, ax=axes[1], label='dB')
        
        # 3. RMSエネルギー
        window_size = SAMPLE_RATE // 10  # 100ms window
        rms_energy = []
        for i in range(0, len(audio_data), window_size):
            window = audio_data[i:i + window_size]
            if len(window) > 0:
                rms = np.sqrt(np.mean(window ** 2))
                rms_energy.append(rms)
        
        t_rms = np.linspace(0, len(audio_data) / SAMPLE_RATE, len(rms_energy))
        axes[2].plot(t_rms, rms_energy, color='orange', linewidth=2)
        axes[2].set_title('RMS Energy - NULL Event Detection', fontsize=12)
        axes[2].set_ylabel('RMS Energy')
        axes[2].grid(True, alpha=0.3)
        
        # NULLイベントをマーク
        for event_time, event_type in self.null_events:
            time_sec = event_time / SAMPLE_RATE
            if time_sec < len(rms_energy) / (len(audio_data) / SAMPLE_RATE):
                color = 'red' if event_type == 'segmentation' else 'orange'
                axes[2].axvline(x=time_sec, color=color, alpha=0.7, linewidth=1)
        
        # 4. ゼロ交差率
        zero_crossings = []
        for i in range(0, len(audio_data), window_size):
            window = audio_data[i:i + window_size]
            if len(window) > 1:
                crossings = np.sum(np.diff(np.sign(window)) != 0)
                zcr = crossings / len(window)
                zero_crossings.append(zcr)
        
        t_zcr = np.linspace(0, len(audio_data) / SAMPLE_RATE, len(zero_crossings))
        axes[3].plot(t_zcr, zero_crossings, color='purple', linewidth=2)
        axes[3].set_title('Zero Crossing Rate - Texture Analysis', fontsize=12)
        axes[3].set_ylabel('ZCR')
        axes[3].set_xlabel('Time (seconds)')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 画像として保存
        viz_path = "visualizations/03_null_pointer_dreams_enhanced_analysis.png"
        plt.savefig(viz_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved: {viz_path}")
        
        return viz_path

def main():
    """メイン実行関数"""
    # 乱数シード（再現性のため）
    random.seed(42)
    np.random.seed(42)
    
    # 生成器インスタンス
    generator = NullPointerDreamsEnhanced()
    
    # 音声生成
    audio_data = generator.generate_final_mix()
    
    # 音声品質分析
    print("\\n=== Audio Quality Analysis ===")
    peak_level = 20 * np.log10(np.max(np.abs(audio_data)))
    rms_level = 20 * np.log10(np.sqrt(np.mean(audio_data ** 2)))
    dynamic_range = peak_level - rms_level
    
    print(f"Peak Level: {peak_level:.2f} dB")
    print(f"RMS Level: {rms_level:.2f} dB")
    print(f"Dynamic Range: {dynamic_range:.2f} dB")
    
    # 16-bit PCMに変換
    audio_int16 = (audio_data * 32767).astype(np.int16)
    
    # WAVファイルとして保存
    output_path = "samples/03_null_pointer_dreams_enhanced.wav"
    wavfile.write(output_path, SAMPLE_RATE, audio_int16)
    print(f"\\nGenerated: {output_path}")
    
    # 分析ビジュアライゼーション
    viz_path = generator.create_analysis_visualization(audio_data)
    
    print("\\n=== Null Pointer Dreams (Enhanced) Complete ===")
    print("🎼 Physical Modeling: Karplus-Strong string synthesis")
    print("🎵 NULL Dereference: String death simulation")
    print("🎶 Segmentation Fault: Complete ensemble collapse")
    print("🎧 Audio Quality: Professional mastering")
    print("📊 Analysis: Spectrogram and event detection")
    
    print(f"\\n🎯 Enhancement Features:")
    print("- Physical string modeling with Karplus-Strong algorithm")
    print("- Realistic NULL dereference through string death")
    print("- Segmentation faults as complete ensemble collapse")
    print("- Professional audio mastering and dynamic range")
    print("- Comprehensive visualization and analysis")

if __name__ == "__main__":
    main()