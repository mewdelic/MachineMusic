#!/usr/bin/env python3
"""
MachineMusic - Error Garden
Race Condition Enhanced with Physical Modeling

Race conditions occur when multiple threads access shared data concurrently,
leading to unpredictable and chaotic behavior. This enhanced version uses
physical modeling synthesis to create realistic string sounds that represent
the chaotic and unpredictable nature of race conditions.

Enhancement Features:
- Karplus-Strong physical modeling for realistic string synthesis
- Chaotic timing patterns representing thread scheduling
- Harmonic interference patterns representing data corruption
- Professional audio quality with enhanced dynamic range
"""

import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy import signal
import os

class RaceConditionEnhanced:
    def __init__(self, sample_rate=44100, duration=30):
        self.sample_rate = sample_rate
        self.duration = duration
        self.total_samples = int(sample_rate * duration)
        self.audio = np.zeros(self.total_samples)
        
        # Race condition parameters
        self.base_frequency = 330.0  # E4 - represents base thread operation
        self.threads = 4  # Number of competing threads
        self.critical_section_probability = 0.3  # Probability of critical section access
        self.chaos_factor = 0.0  # Increases over time to represent race condition severity
        
        # Physical modeling parameters
        self.karplus_decay = 0.996  # Slightly faster decay for chaotic behavior
        self.karplus_filter_freq = 0.3  # Low-pass filter for damping
        self.resonance_freq = [660.0, 990.0, 1320.0]  # Harmonic resonance frequencies
        
        # Audio quality parameters
        self.target_peak = 0.8  # Target peak amplitude
        self.target_rms = 0.3  # Target RMS level
        
        print("Race Condition Enhanced - Physical Modeling Synthesis")
        print("=" * 50)
        
    def karplus_strong_string(self, frequency, duration, velocity=0.7, decay_factor=None):
        """Generate realistic string sound using Karplus-Strong algorithm with chaotic timing"""
        if decay_factor is None:
            decay_factor = self.karplus_decay
            
        period = int(self.sample_rate / frequency)
        delay_samples = period
        
        # Generate noise burst for excitation
        noise_samples = period
        noise = np.random.normal(0, velocity, noise_samples)
        
        # Initialize delay line
        delay_line = np.zeros(delay_samples)
        delay_line[:len(noise)] = noise
        
        output = np.zeros(int(self.sample_rate * duration))
        filtered_output = np.zeros_like(output)
        
        # Karplus-Strong with chaotic modifications
        for i in range(len(output)):
            # Get sample from delay line
            sample = delay_line[0]
            
            # Apply low-pass filter (simple averaging)
            filtered_sample = (delay_line[0] + delay_line[1]) * 0.5 * decay_factor
            
            # Add chaotic modulation based on race condition
            chaos_modulation = 1.0 + np.random.normal(0, self.chaos_factor * 0.1)
            filtered_sample *= chaos_modulation
            
            output[i] = sample
            filtered_output[i] = filtered_sample
            
            # Update delay line
            delay_line = np.roll(delay_line, -1)
            delay_line[-1] = filtered_sample
            
            # Introduce occasional timing glitches
            if np.random.random() < self.chaos_factor * 0.05:
                # Skip or repeat samples to represent timing chaos
                if np.random.random() < 0.5:
                    # Skip sample (race condition - one thread runs ahead)
                    if i + 1 < len(output):
                        delay_line = np.roll(delay_line, -1)
                        delay_line[-1] = filtered_sample
                        i += 1
                else:
                    # Repeat sample (race condition - contention)
                    delay_line[-1] = filtered_sample
                    
        return filtered_output
    
    def generate_race_condition_pattern(self, start_time, end_time):
        """Generate race condition pattern with multiple competing threads"""
        start_sample = int(start_time * self.sample_rate)
        end_sample = int(end_time * self.sample_rate)
        
        # Generate thread operations with chaotic timing
        thread_operations = []
        for thread in range(self.threads):
            # Each thread has chaotic operation intervals
            operation_times = np.random.normal(
                loc=(start_time + end_time) / 2,
                scale=(end_time - start_time) * 0.2,
                size=int((end_time - start_time) * 10)
            )
            operation_times = operation_times[
                (operation_times >= start_time) & (operation_times <= end_time)
            ]
            thread_operations.extend([(t, thread) for t in operation_times])
        
        # Sort all operations and detect conflicts
        thread_operations.sort(key=lambda x: x[0])
        
        for i in range(len(thread_operations)):
            time, thread = thread_operations[i]
            sample = int(time * self.sample_rate)
            
            if sample >= len(self.audio):
                continue
                
            # Check for conflicts with nearby operations
            conflict = False
            for j in range(max(0, i-2), min(len(thread_operations), i+3)):
                if i != j:
                    other_time, other_thread = thread_operations[j]
                    if abs(time - other_time) < 0.1 and thread != other_thread:
                        conflict = True
                        break
            
            if conflict:
                # Critical section conflict - chaotic behavior
                self.generate_critical_section_conflict(time, thread)
            else:
                # Normal thread operation
                self.generate_normal_operation(time, thread)
    
    def generate_critical_section_conflict(self, time, thread_id):
        """Generate chaotic audio for race condition conflicts"""
        sample = int(time * self.sample_rate)
        conflict_duration = 0.5  # 0.5 second conflict
        
        # Generate chaotic interference pattern
        t = np.linspace(0, conflict_duration, int(self.sample_rate * conflict_duration))
        
        # Multiple frequencies interfering (representing data corruption)
        freqs = [self.base_frequency, self.base_frequency * 1.5, self.base_frequency * 0.8]
        interference = np.zeros_like(t)
        
        for freq in freqs:
            # Each thread contributes with phase distortion
            phase_offset = np.random.uniform(0, 2 * np.pi)
            amplitude = np.random.uniform(0.3, 0.7)
            interference += amplitude * np.sin(2 * np.pi * freq * t + phase_offset)
        
        # Add chaos modulation
        chaos_modulation = 1 + self.chaos_factor * np.sin(2 * np.pi * 50 * t)
        interference *= chaos_modulation
        
        # Normalize and add to audio
        if len(interference) > 0:
            interference = interference / np.max(np.abs(interference)) * 0.6
            end_sample = min(sample + len(interference), len(self.audio))
            self.audio[sample:end_sample] += interference[:end_sample-sample]
    
    def generate_normal_operation(self, time, thread_id):
        """Generate normal thread operation audio"""
        # Each thread has slightly different characteristics
        thread_frequency = self.base_frequency * (1 + 0.1 * thread_id)
        operation_duration = 0.2
        
        # Generate string sound for this operation
        operation_audio = self.karplus_strong_string(
            frequency=thread_frequency,
            duration=operation_duration,
            velocity=0.5 + 0.1 * thread_id
        )
        
        # Add to main audio
        sample = int(time * self.sample_rate)
        end_sample = min(sample + len(operation_audio), len(self.audio))
        self.audio[sample:end_sample] += operation_audio[:end_sample-sample]
    
    def apply_mastering(self):
        """Apply professional mastering techniques"""
        # Normalize to target peak
        current_peak = np.max(np.abs(self.audio))
        if current_peak > 0:
            self.audio = self.audio / current_peak * self.target_peak
        
        # Apply gentle compression
        threshold = 0.5
        ratio = 2.0
        attack_time = 0.003  # 3ms
        release_time = 0.1   # 100ms
        
        envelope = np.abs(self.audio)
        gain_reduction = np.ones_like(envelope)
        
        for i in range(1, len(envelope)):
            if envelope[i] > threshold:
                reduction = (envelope[i] - threshold) * (1 - 1/ratio)
                gain_reduction[i] = 1 - reduction / envelope[i]
        
        self.audio = self.audio * gain_reduction
        
        # Final normalization
        current_rms = np.sqrt(np.mean(self.audio**2))
        if current_rms > 0:
            self.audio = self.audio / current_rms * self.target_rms
            
        # Apply fade in/out
        fade_samples = int(0.1 * self.sample_rate)  # 100ms fade
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        
        self.audio[:fade_samples] *= fade_in
        self.audio[-fade_samples:] *= fade_out
    
    def create_visualization(self):
        """Create comprehensive visualization of the race condition"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Waveform
        time_axis = np.linspace(0, self.duration, len(self.audio))
        axes[0, 0].plot(time_axis, self.audio)
        axes[0, 0].set_title('Race Condition Enhanced - Waveform')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Amplitude')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Spectrogram
        f, t, Sxx = signal.spectrogram(self.audio, self.sample_rate, nperseg=1024)
        im = axes[0, 1].pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
        axes[0, 1].set_title('Race Condition Enhanced - Spectrogram')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Frequency (Hz)')
        plt.colorbar(im, ax=axes[0, 1])
        
        # 3. Frequency spectrum
        freqs = np.fft.fftfreq(len(self.audio), 1/self.sample_rate)
        fft = np.fft.fft(self.audio)
        
        # Plot only positive frequencies
        pos_freqs = freqs[:len(freqs)//2]
        pos_fft = np.abs(fft[:len(fft)//2])
        
        axes[1, 0].semilogy(pos_freqs, pos_fft)
        axes[1, 0].set_title('Race Condition Enhanced - Frequency Spectrum')
        axes[1, 0].set_xlabel('Frequency (Hz)')
        axes[1, 0].set_ylabel('Magnitude')
        axes[1, 0].set_xlim(0, 5000)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Chaos progression
        chaos_times = np.linspace(0, self.duration, 100)
        chaos_levels = []
        window_size = len(self.audio) // 100
        
        for i in range(100):
            start_idx = i * window_size
            end_idx = min((i + 1) * window_size, len(self.audio))
            window = self.audio[start_idx:end_idx]
            
            # Calculate chaos as high-frequency content
            fft_window = np.fft.fft(window)
            high_freq_power = np.sum(np.abs(fft_window[len(fft_window)//4:]))
            total_power = np.sum(np.abs(fft_window))
            chaos_levels.append(high_freq_power / (total_power + 1e-10))
        
        axes[1, 1].plot(chaos_times, chaos_levels)
        axes[1, 1].set_title('Race Condition Enhanced - Chaos Progression')
        axes[1, 1].set_xlabel('Time (s)')
        axes[1, 1].set_ylabel('Chaos Level')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('04_race_condition_enhanced_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualization saved as: 04_race_condition_enhanced_analysis.png")
    
    def generate_track(self):
        """Generate the complete race condition track"""
        print("Generating enhanced race condition track...")
        
        # Phase 1: Stable operations (0-10 seconds)
        print("Phase 1: Stable operations (0-10s)")
        self.chaos_factor = 0.1
        self.generate_race_condition_pattern(0, 10)
        
        # Phase 2: Increasing conflicts (10-20 seconds)
        print("Phase 2: Increasing conflicts (10-20s)")
        self.chaos_factor = 0.3
        self.generate_race_condition_pattern(10, 20)
        
        # Phase 3: Chaotic race condition (20-30 seconds)
        print("Phase 3: Chaotic race condition (20-30s)")
        self.chaos_factor = 0.6
        self.generate_race_condition_pattern(20, 30)
        
        # Apply mastering
        print("Applying mastering...")
        self.apply_mastering()
        
        # Calculate audio statistics
        peak_db = 20 * np.log10(np.max(np.abs(self.audio)) + 1e-10)
        rms_db = 20 * np.log10(np.sqrt(np.mean(self.audio**2)) + 1e-10)
        dynamic_range_db = peak_db - rms_db
        
        print(f"\nAudio Statistics:")
        print(f"  Peak Level: {peak_db:.2f} dB")
        print(f"  RMS Level: {rms_db:.2f} dB")
        print(f"  Dynamic Range: {dynamic_range_db:.2f} dB")
        print(f"  Duration: {self.duration} seconds")
        print(f"  Sample Rate: {self.sample_rate} Hz")
        
        return self.audio

def main():
    """Main function to generate the enhanced race condition track"""
    # Create the enhanced race condition generator
    race_condition = RaceConditionEnhanced()
    
    # Generate the audio
    audio = race_condition.generate_track()
    
    # Save the audio file
    output_file = '04_race_condition_enhanced.wav'
    wav.write(output_file, race_condition.sample_rate, audio.astype(np.float32))
    print(f"\nAudio saved as: {output_file}")
    
    # Create visualization
    print("\nCreating visualization...")
    race_condition.create_visualization()
    
    print("\n" + "=" * 50)
    print("Race Condition Enhanced - Generation Complete!")
    print("=" * 50)
    print(f"Track: Race Condition (Enhanced)")
    print(f"Concept: Chaotic thread interactions with physical modeling")
    print(f"Duration: {race_condition.duration} seconds")
    print(f"Features: Karplus-Strong synthesis, race condition chaos")
    print(f"Output: {output_file}")
    print("=" * 50)

if __name__ == "__main__":
    main()