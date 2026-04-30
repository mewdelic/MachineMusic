#!/usr/bin/env python3
"""
Race Condition Advanced
競合状態が生む偶然のハーモニーを高度に表現

競合状態（Race Condition）とは、複数のスレッドが共有リソースに同時にアクセスしようとする際に
発生する予測不可能な動作現象である。このトラックは、その不確実性と偶然性を音楽的に表現する。

技術的特徴:
- マルチスレッドシミュレーションによる非決定的な音響生成
- 競合状態が生むハーモニクス構造
- 時間的な競合の視覚化
- 確率的なスケジューリングと優先度逆転
- デッドロックへの遷移表現
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
import random
import json
from datetime import datetime
import os

class RaceConditionAdvanced:
    def __init__(self, duration=60, sample_rate=48000):
        self.duration = duration
        self.sample_rate = sample_rate
        self.samples = int(duration * sample_rate)
        self.audio = np.zeros(self.samples)
        
        # スレッドパラメータ
        self.num_threads = 8
        self.shared_resource_size = 256
        self.critical_sections = []
        
        # 競合状態のパラメータ
        self.race_probability = 0.4
        self.contention_level = 0.7
        self.priority_inversion_prob = 0.15
        
        # 音響パラメータ
        self.base_freq = 220.0
        self.harmonic_complexity = 12
        self.dissonance_factor = 0.3
        
        # 時間管理
        self.time_quantum = self.samples // 1000  # 1ms単位のタイムクォンタム
        self.thread_timeline = np.zeros((self.num_threads, self.samples // self.time_quantum))
        
        print(f"Race Condition Advanced initialized")
        print(f"Duration: {duration}s, Sample Rate: {sample_rate}Hz")
        print(f"Threads: {self.num_threads}, Shared Resource Size: {self.shared_resource_size}")
        
    def simulate_thread_execution(self):
        """マルチスレッドの実行をシミュレート"""
        # スレッドごとの特性
        thread_properties = []
        for i in range(self.num_threads):
            thread_props = {
                'id': i,
                'priority': random.randint(1, 10),
                'execution_time': random.randint(5, 50),
                'critical_section_need': random.random() < 0.6,
                'io_frequency': random.randint(1, 5),
                'phase': random.uniform(0, 2 * np.pi)
            }
            thread_properties.append(thread_props)
        
        # 共有リソース状態
        shared_resource = np.zeros(self.shared_resource_size)
        resource_owner = np.full(self.shared_resource_size, -1)
        
        # 実行タイムラインの生成
        for t in range(0, self.samples // self.time_quantum):
            current_time = t * self.time_quantum / self.sample_rate
            
            # スレッドスケジューリング
            active_threads = self._schedule_threads(thread_properties, t)
            
            for thread_id in active_threads:
                if thread_id < len(thread_properties):
                    self._execute_thread_step(
                        thread_id, thread_properties[thread_id], 
                        shared_resource, resource_owner, t
                    )
        
        return thread_properties, shared_resource
    
    def _schedule_threads(self, thread_properties, time_step):
        """スレッドスケジューリング（優先度ベース）"""
        active_threads = []
        
        # ランダムなスケジューリング決定
        for i, props in enumerate(thread_properties):
            if random.random() < 0.3:  # 30%の確率で実行
                # 優先度逆転の可能性
                if random.random() < self.priority_inversion_prob:
                    active_threads.append(i)
                else:
                    # 優先度順に挿入
                    inserted = False
                    for j, active_id in enumerate(active_threads):
                        if props['priority'] > thread_properties[active_id]['priority']:
                            active_threads.insert(j, i)
                            inserted = True
                            break
                    if not inserted:
                        active_threads.append(i)
        
        # 同時実行スレッド数の制限
        return active_threads[:min(4, len(active_threads))]
    
    def _execute_thread_step(self, thread_id, thread_props, shared_resource, resource_owner, time_step):
        """スレッドの1ステップを実行"""
        self.thread_timeline[thread_id, time_step] = 1
        
        # クリティカルセクションへのアクセス
        if thread_props['critical_section_need']:
            self._access_critical_section(thread_id, shared_resource, resource_owner, time_step)
        
        # 通常処理
        self._normal_processing(thread_id, thread_props, time_step)
    
    def _access_critical_section(self, thread_id, shared_resource, resource_owner, time_step):
        """クリティカルセクションへのアクセス（競合発生）"""
        # ランダムなリソースアクセス
        resource_indices = random.sample(range(self.shared_resource_size), 
                                       random.randint(1, 5))
        
        for resource_idx in resource_indices:
            # 競合状態のチェック
            if resource_owner[resource_idx] != -1 and resource_owner[resource_idx] != thread_id:
                # 競合発生！
                self._handle_race_condition(thread_id, resource_owner[resource_idx], 
                                         resource_idx, time_step)
            else:
                # 正常アクセス
                resource_owner[resource_idx] = thread_id
                shared_resource[resource_idx] += random.uniform(-0.1, 0.1)
                
                # 一定確率でリソース解放
                if random.random() < 0.1:
                    resource_owner[resource_idx] = -1
    
    def _handle_race_condition(self, thread1, thread2, resource_idx, time_step):
        """競合状態の処理"""
        # 競合情報を記録
        race_event = {
            'time': time_step * self.time_quantum / self.sample_rate,
            'threads': [thread1, thread2],
            'resource': resource_idx,
            'type': 'race_condition'
        }
        self.critical_sections.append(race_event)
        
        # 競合による音響効果を生成
        self._generate_race_sound(thread1, thread2, resource_idx, time_step)
    
    def _generate_race_sound(self, thread1, thread2, resource_idx, time_step):
        """競合状態による音響を生成"""
        start_sample = time_step * self.time_quantum
        duration_samples = int(0.1 * self.sample_rate)  # 100ms
        end_sample = min(start_sample + duration_samples, self.samples)
        
        if end_sample <= start_sample:
            return
            
        t = np.arange(end_sample - start_sample) / self.sample_rate
        
        # スレッドごとの周波数
        freq1 = self.base_freq * (1 + 0.1 * thread1)
        freq2 = self.base_freq * (1 + 0.1 * thread2)
        
        # 競合による周波数干渉
        wave1 = np.sin(2 * np.pi * freq1 * t)
        wave2 = np.sin(2 * np.pi * freq2 * t)
        
        # ビート周波数の生成
        beat_freq = abs(freq1 - freq2)
        beat_wave = np.sin(2 * np.pi * beat_freq * t) * 0.3
        
        # 競合ノイズ
        noise_intensity = self.contention_level * 0.1
        noise = np.random.normal(0, noise_intensity, len(t))
        
        # 合成
        race_audio = (wave1 + wave2 + beat_wave + noise) * 0.25
        
        # 競合位置に応じたパンニング
        pan_pos = (thread1 - thread2) / self.num_threads
        left_gain = np.sqrt((1 - pan_pos) / 2)
        right_gain = np.sqrt((1 + pan_pos) / 2)
        
        # オーディオに追加
        self.audio[start_sample:end_sample] += race_audio
    
    def _normal_processing(self, thread_id, thread_props, time_step):
        """通常のスレッド処理音響を生成"""
        start_sample = time_step * self.time_quantum
        duration_samples = int(thread_props['execution_time'] * 0.001 * self.sample_rate)
        end_sample = min(start_sample + duration_samples, self.samples)
        
        if end_sample <= start_sample:
            return
            
        t = np.arange(end_sample - start_sample) / self.sample_rate
        
        # スレッド固有の周波数
        freq = self.base_freq * (1 + 0.05 * thread_id + 0.02 * thread_props['priority'])
        
        # 基本波形
        wave = np.sin(2 * np.pi * freq * t + thread_props['phase'])
        
        # ハーモニクス
        for harmonic in range(2, min(self.harmonic_complexity + 1, 6)):
            harmonic_freq = freq * harmonic
            harmonic_wave = np.sin(2 * np.pi * harmonic_freq * t + thread_props['phase'])
            wave += harmonic_wave * (0.5 / harmonic)
        
        # I/O待ちによる変調
        if random.random() < thread_props['io_frequency'] * 0.1:
            wave *= (1 + 0.3 * np.sin(2 * np.pi * 5 * t))
        
        # 音量調整
        wave *= 0.05
        
        # オーディオに追加
        self.audio[start_sample:end_sample] += wave
    
    def generate_deadlock_transition(self):
        """デッドロックへの遷移を表現"""
        deadlock_start = int(0.7 * self.samples)  # 70%位置から開始
        deadlock_duration = int(0.1 * self.samples)  # 10%持続
        
        if deadlock_start + deadlock_duration > self.samples:
            return
            
        t = np.arange(deadlock_duration) / self.sample_rate
        
        # デッドロック音響の生成
        # 低周波の持続音（停滞感）
        fundamental = 55.0  # 低い周波数
        drone = np.sin(2 * np.pi * fundamental * t) * 0.2
        
        # 高周波ノイズ（緊張感）
        noise = np.random.normal(0, 0.05, len(t))
        
        # 周期的なインパルス（タイムアウト）
        impulse_period = int(self.sample_rate * 0.5)  # 0.5秒ごと
        for i in range(0, len(t), impulse_period):
            if i < len(t):
                drone[i] += 0.3
        
        # 時間と共に減衰
        envelope = np.exp(-3 * t / (deadlock_duration / self.sample_rate))
        deadlock_audio = (drone + noise) * envelope
        
        self.audio[deadlock_start:deadlock_start + deadlock_duration] += deadlock_audio
    
    def apply_mastering(self):
        """マスタリング処理"""
        # ノーマライズ
        max_amplitude = np.max(np.abs(self.audio))
        if max_amplitude > 0:
            self.audio = self.audio / max_amplitude * 0.8
        
        # ローパスフィルタ（過度な高周波を抑える）
        nyquist = self.sample_rate / 2
        cutoff = 8000  # 8kHz
        b, a = butter(4, cutoff / nyquist, btype='low')
        self.audio = filtfilt(b, a, self.audio)
        
        # ステレオ化
        # 左チャンネル：スレッド1-4
        # 右チャンネル：スレッド5-8
        left_channel = np.copy(self.audio)
        right_channel = np.copy(self.audio)
        
        # スレッドごとの定位
        for i in range(self.num_threads):
            pan_pos = (i - self.num_threads/2) / (self.num_threads/2)
            # パンニング処理は既に _generate_race_sound で実装済み
        
        stereo_audio = np.column_stack((left_channel, right_channel))
        return stereo_audio
    
    def create_visualization(self, stereo_audio):
        """可視化を作成"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Race Condition Advanced - Visualization', fontsize=16, fontweight='bold')
        
        # 1. スレッド実行タイムライン
        ax1 = axes[0, 0]
        time_axis = np.arange(self.thread_timeline.shape[1]) * self.time_quantum / self.sample_rate
        
        for i in range(self.num_threads):
            ax1.plot(time_axis, self.thread_timeline[i] + i, 
                    label=f'Thread {i}', alpha=0.7, linewidth=1)
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Thread ID')
        ax1.set_title('Thread Execution Timeline')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 2. 競合状態の分布
        ax2 = axes[0, 1]
        if self.critical_sections:
            race_times = [event['time'] for event in self.critical_sections]
            race_resources = [event['resource'] for event in self.critical_sections]
            
            ax2.scatter(race_times, race_resources, alpha=0.6, s=30, c='red')
            ax2.set_xlabel('Time (s)')
            ax2.set_ylabel('Resource Index')
            ax2.set_title(f'Race Conditions ({len(self.critical_sections)} events)')
            ax2.grid(True, alpha=0.3)
        
        # 3. オーディオ波形
        ax3 = axes[1, 0]
        time_audio = np.arange(len(stereo_audio)) / self.sample_rate
        ax3.plot(time_audio, stereo_audio[:, 0], alpha=0.7, label='Left', linewidth=0.5)
        ax3.plot(time_audio, stereo_audio[:, 1], alpha=0.7, label='Right', linewidth=0.5)
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Amplitude')
        ax3.set_title('Audio Waveform')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. スペクトログラム
        ax4 = axes[1, 1]
        from scipy import signal
        frequencies, times, Sxx = signal.spectrogram(stereo_audio[:, 0], 
                                                   self.sample_rate, nperseg=1024)
        im = ax4.pcolormesh(times, frequencies, 10 * np.log10(Sxx + 1e-10), 
                           shading='gouraud', cmap='viridis')
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Frequency (Hz)')
        ax4.set_title('Spectrogram (Left Channel)')
        plt.colorbar(im, ax=ax4, label='Power (dB)')
        
        plt.tight_layout()
        plt.savefig('04_race_condition_advanced_visualization.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Visualization saved as '04_race_condition_advanced_visualization.png'")
    
    def save_metadata(self):
        """メタデータを保存"""
        metadata = {
            "title": "Race Condition Advanced",
            "album": "Error Garden (Advanced)",
            "track_number": 4,
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "creation_date": datetime.now().isoformat(),
            "technical_details": {
                "num_threads": self.num_threads,
                "shared_resource_size": self.shared_resource_size,
                "race_probability": self.race_probability,
                "contention_level": self.contention_level,
                "priority_inversion_probability": self.priority_inversion_prob,
                "critical_sections_count": len(self.critical_sections),
                "base_frequency": self.base_freq,
                "harmonic_complexity": self.harmonic_complexity
            },
            "description": "競合状態が生む偶然のハーモニーを高度に表現。マルチスレッドの非決定性を音楽化。"
        }
        
        with open('04_race_condition_advanced_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print("Metadata saved as '04_race_condition_advanced_metadata.json'")
    
    def generate(self):
        """音声を生成"""
        print("Starting Race Condition Advanced generation...")
        
        # スレッド実行のシミュレーション
        thread_properties, shared_resource = self.simulate_thread_execution()
        
        # 競合状態の音響生成（シミュレーション中に一部生成済み）
        
        # デッドロック遷移の生成
        self.generate_deadlock_transition()
        
        # マスタリング
        stereo_audio = self.apply_mastering()
        
        # 可視化
        self.create_visualization(stereo_audio)
        
        # メタデータ保存
        self.save_metadata()
        
        # WAVファイル保存
        wavfile.write('04_race_condition_advanced.wav', self.sample_rate, stereo_audio)
        print("Audio saved as '04_race_condition_advanced.wav'")
        
        # 統計情報
        print(f"\nGeneration Statistics:")
        print(f"Total race conditions: {len(self.critical_sections)}")
        print(f"Audio duration: {self.duration}s")
        print(f"Sample rate: {self.sample_rate}Hz")
        print(f"File size: {os.path.getsize('04_race_condition_advanced.wav') / (1024*1024):.1f} MB")
        
        return stereo_audio

def main():
    """メイン実行関数"""
    print("=== Race Condition Advanced Generator ===")
    print("競合状態が生む偶然のハーモニーを表現\n")
    
    # インスタンス作成
    composer = RaceConditionAdvanced(duration=60, sample_rate=48000)
    
    # 音声生成
    audio = composer.generate()
    
    print("\n✅ Race Condition Advanced completed successfully!")
    print("Files generated:")
    print("- 04_race_condition_advanced.wav (audio)")
    print("- 04_race_condition_advanced_visualization.png (visualization)")
    print("- 04_race_condition_advanced_metadata.json (metadata)")

if __name__ == "__main__":
    main()