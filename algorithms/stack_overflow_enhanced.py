#!/usr/bin/env python3
"""
Error Garden - Machine Music Album
Daily Update Script: March 19, 2026

Track: Stack Overflow Enhancement
Objective: Add physical modeling synthesis to enhance the original recursive pattern
"""

import numpy as np
import scipy.signal
import scipy.io.wavfile
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt
import os

class StackOverflowEnhanced:
    """Enhanced Stack Overflow with physical modeling synthesis"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.max_depth = 16  # Maximum recursion depth
        self.base_frequency = 220.0  # A3 note
        self.resonance_freq = 880.0  # A5 note for physical resonance
        
    def generate_karplus_strong_pluck(self, frequency, duration, decay_factor=0.996):
        """Generate Karplus-Strong physical modeling synthesis for plucked string"""
        num_samples = int(duration * self.sample_rate)
        buffer_size = int(self.sample_rate / frequency)
        
        # Initialize buffer with noise
        buffer = np.random.uniform(-1, 1, buffer_size)
        
        # Create output buffer
        output = np.zeros(num_samples)
        
        # Karplus-Strong algorithm
        for i in range(num_samples):
            output[i] = buffer[i % buffer_size]
            # Apply averaging and decay
            buffer[i % buffer_size] = decay_factor * 0.5 * (
                buffer[i % buffer_size] + 
                buffer[(i + 1) % buffer_size]
            )
        
        return output
    
    def generate_recursive_harmonics(self, depth, duration, frequency):
        """Generate recursive harmonic structure with physical modeling"""
        samples = int(duration * self.sample_rate)
        output = np.zeros(samples)
        
        for d in range(1, depth + 1):
            if d == 1:
                # Base frequency with Karplus-Strong
                fundamental = self.generate_karplus_strong_pluck(frequency, duration, 0.998)
                output += fundamental * (1.0 / d)
            else:
                # Harmonics with decreasing amplitude and shorter duration
                harmonic_freq = frequency * d
                harmonic_duration = duration / (d ** 0.5)
                harmonic_samples = int(harmonic_duration * self.sample_rate)
                
                # Generate harmonic with filtered noise
                t = np.linspace(0, harmonic_duration, harmonic_samples)
                harmonic = np.sin(2 * np.pi * harmonic_freq * t)
                
                # Add physical resonance
                resonance = np.sin(2 * np.pi * self.resonance_freq * t) * 0.1
                
                # Combine and filter
                combined = harmonic + resonance
                filtered = signal.butter(4, harmonic_freq * 2 / self.sample_rate, 'lowpass', output='sos')
                harmonic_filtered = signal.sosfilt(filtered[0], combined)
                
                # Pad to match output length
                padded = np.zeros(samples)
                padded[:harmonic_samples] = harmonic_filtered
                
                output += padded * (0.5 / d)
        
        return output
    
    def add_stack_overflow_effects(self, audio, overflow_times):
        """Add stack overflow effects - sudden cuts and distortions"""
        output = audio.copy()
        
        for time in overflow_times:
            sample_pos = int(time * self.sample_rate)
            if sample_pos < len(output):
                # Create overflow effect - sudden cut and high-frequency burst
                overflow_duration = 0.1  # 100ms
                overflow_samples = int(overflow_duration * self.sample_rate)
                
                # Cut the audio
                output[sample_pos:] *= 0.1
                
                # Add high-frequency noise representing memory corruption
                noise = np.random.normal(0, 0.2, min(overflow_samples, len(output) - sample_pos))
                output[sample_pos:sample_pos + overflow_samples] += noise
        
        return output
    
    def generate_enhanced_stack_overflow(self, duration=30):
        """Generate enhanced Stack Overflow track with physical modeling"""
        # Create recursive structure leading to overflow
        phases = []
        
        # Phase 1: Stable recursion (0-10 seconds)
        for depth in range(1, 8):
            phase_duration = 10.0 / 7
            phase_audio = self.generate_recursive_harmonics(depth, phase_duration, self.base_frequency)
            phases.append(phase_audio)
        
        # Phase 2: Deep recursion approaching limit (10-20 seconds)
        for depth in range(8, 12):
            phase_duration = 10.0 / 4
            phase_audio = self.generate_recursive_harmonics(depth, phase_duration, self.base_frequency * 1.1)
            phases.append(phase_audio)
        
        # Phase 3: Stack overflow (20-30 seconds)
        overflow_phase = self.generate_recursive_harmonics(self.max_depth, 10, self.base_frequency * 1.5)
        
        # Add overflow effects at specific times
        overflow_times = [21.0, 23.0, 25.5, 27.8]
        overflow_phase = self.add_stack_overflow_effects(overflow_phase, overflow_times)
        phases.append(overflow_phase)
        
        # Concatenate all phases
        full_audio = np.concatenate(phases)
        
        # Normalize
        full_audio = full_audio / np.max(np.abs(full_audio)) * 0.8
        
        return full_audio
    
    def save_audio(self, audio, filename):
        """Save audio as WAV file"""
        sf.write(filename, audio, self.sample_rate)
        print(f"Enhanced Stack Overflow saved to: {filename}")
    
    def create_visualization(self, audio, filename):
        """Create visualization of the enhanced track"""
        plt.figure(figsize=(15, 10))
        
        # Create subplots
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))
        
        # Waveform
        time = np.linspace(0, len(audio) / self.sample_rate, len(audio))
        ax1.plot(time, audio, alpha=0.7, color='#2196F3', linewidth=0.5)
        ax1.set_title('Enhanced Stack Overflow - Waveform', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Amplitude')
        ax1.grid(True, alpha=0.3)
        
        # Spectrogram
        frequencies, times, Sxx = signal.spectrogram(audio, self.sample_rate)
        im = ax2.pcolormesh(times, frequencies, 10 * np.log10(Sxx + 1e-10), 
                            shading='gouraud', cmap='viridis')
        ax2.set_title('Enhanced Stack Overflow - Spectrogram', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Frequency (Hz)')
        plt.colorbar(im, ax=ax2, label='Power (dB)')
        
        # Frequency spectrum at different time points
        time_points = [5, 15, 25]  # Analyze at 5s, 15s, and 25s
        colors = ['#4CAF50', '#FF9800', '#F44336']
        labels = ['Stable Recursion', 'Deep Recursion', 'Stack Overflow']
        
        for i, (t, color, label) in enumerate(zip(time_points, colors, labels)):
            sample_pos = int(t * self.sample_rate)
            window_size = 4096
            if sample_pos + window_size < len(audio):
                segment = audio[sample_pos:sample_pos + window_size]
                freqs = np.fft.fftfreq(window_size, 1/self.sample_rate)
                fft = np.fft.fft(segment * np.hanning(window_size))
                
                # Only positive frequencies
                pos_freqs = freqs[:window_size//2]
                pos_fft = np.abs(fft[:window_size//2])
                
                ax3.semilogy(pos_freqs, pos_fft, color=color, label=label, alpha=0.8)
        
        ax3.set_title('Enhanced Stack Overflow - Frequency Analysis', fontsize=16, fontweight='bold')
        ax3.set_xlabel('Frequency (Hz)')
        ax3.set_ylabel('Magnitude')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, 5000)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Visualization saved to: {filename}")

def main():
    """Main function to generate enhanced Stack Overflow"""
    print("🎵 Enhanced Stack Overflow Generation")
    print("=" * 50)
    
    # Initialize generator
    generator = StackOverflowEnhanced()
    
    # Generate enhanced audio
    print("🎼 Generating enhanced Stack Overflow with physical modeling...")
    enhanced_audio = generator.generate_enhanced_stack_overflow()
    
    # Save audio
    output_dir = "samples"
    os.makedirs(output_dir, exist_ok=True)
    
    audio_filename = f"{output_dir}/01_stack_overflow_enhanced.wav"
    generator.save_audio(enhanced_audio, audio_filename)
    
    # Create visualization
    viz_dir = "visualizations"
    os.makedirs(viz_dir, exist_ok=True)
    
    viz_filename = f"{viz_dir}/01_stack_overflow_enhanced_analysis.png"
    generator.create_visualization(enhanced_audio, viz_filename)
    
    print("\n✅ Enhanced Stack Overflow Generation Complete!")
    print(f"📁 Audio: {audio_filename}")
    print(f"📊 Visualization: {viz_filename}")
    print(f"🎵 Duration: {len(enhanced_audio)/44100:.2f} seconds")
    
    # Audio analysis
    print(f"\n📈 Audio Analysis:")
    print(f"   Peak Amplitude: {np.max(np.abs(enhanced_audio)):.4f}")
    print(f"   RMS Level: {np.sqrt(np.mean(enhanced_audio**2)):.4f}")
    print(f"   Dynamic Range: {20*np.log10(np.max(np.abs(enhanced_audio))/np.sqrt(np.mean(enhanced_audio**2))):.2f} dB")
    
    return enhanced_audio

if __name__ == "__main__":
    main()