#!/usr/bin/env python3
"""
Segmentation Fault Enhanced - Enhanced algorithmic composition
Memory segmentation violation as musical expression with physical modeling

「領域違反の破裂」- 不正なメモリアクセスが生む衝撃的な音響表現

Enhanced features:
- Physical modeling of memory access violations
- Dynamic segmentation fault simulation
- Multi-layered crash soundscape
- Real-time spatialization effects
"""

import numpy as np
import scipy.signal
import soundfile as sf
import matplotlib.pyplot as plt
from pathlib import Path
import json

class SegmentationFaultEnhanced:
    def __init__(self, sample_rate=44100, duration=40.0):
        self.sample_rate = sample_rate
        self.duration = duration
        self.samples = int(sample_rate * duration)
        
        # Memory segmentation parameters
        self.memory_segments = 8  # Number of memory segments
        self.segment_size = self.samples // self.memory_segments
        self.access_patterns = ['sequential', 'random', 'overflow', 'illegal']
        
        # Physical modeling parameters
        self.resonance_freq = 2000  # Hz - resonance of the crash
        self.decay_rate = 0.8  # Decay rate for crash sounds
        self.noise_threshold = 0.1  # Threshold for noise floor
        
        # Audio processing parameters
        self.master_channel = np.zeros(self.samples)
        self.channels = {}
        
    def generate_memory_access_pattern(self, pattern_type, segment_idx):
        """Generate different types of memory access patterns"""
        segment_start = segment_idx * self.segment_size
        segment_end = segment_start + self.segment_size
        
        pattern = np.zeros(self.segment_size)
        
        if pattern_type == 'sequential':
            # Sequential access - smooth transitions
            pattern = np.linspace(0, 1, self.segment_size)
            
        elif pattern_type == 'random':
            # Random access - noise-like behavior
            pattern = np.random.random(self.segment_size)
            
        elif pattern_type == 'overflow':
            # Buffer overflow - exponential growth beyond bounds
            overflow_point = int(self.segment_size * 0.7)
            pattern[:overflow_point] = np.linspace(0, 1, overflow_point)
            pattern[overflow_point:] = np.exp(np.linspace(0, -5, self.segment_size - overflow_point))
            
        elif pattern_type == 'illegal':
            # Illegal access - sudden spikes and violations
            pattern = np.random.random(self.segment_size) * 0.3
            # Add sudden illegal access spikes
            spike_positions = np.random.choice(self.segment_size, size=5, replace=False)
            pattern[spike_positions] = np.random.random(5) * 0.8 + 0.2
            
        return pattern
    
    def create_crash_sound(self, crash_time, crash_intensity):
        """Create physical modeling of segmentation fault crash sound"""
        crash_samples = int(self.sample_rate * 0.5)  # 0.5 second crash
        crash_start = int(crash_time * self.sample_rate)
        crash_end = min(crash_start + crash_samples, self.samples)
        
        if crash_end > self.samples:
            crash_samples = self.samples - crash_start
            crash_end = self.samples
            
        # Create crash waveform using physical modeling
        t = np.linspace(0, crash_samples / self.sample_rate, crash_samples)
        
        # Resonant crash sound
        fundamental = self.resonance_freq * (1 + 0.5 * np.sin(t * 10))
        crash_wave = np.sin(2 * np.pi * fundamental * t)
        
        # Add harmonics
        for harmonic in range(2, 6):
            harmonic_wave = np.sin(2 * np.pi * fundamental * harmonic * t)
            crash_wave += harmonic_wave / (harmonic ** 1.5)
        
        # Apply amplitude envelope
        envelope = np.exp(-t * self.decay_rate * 10)
        crash_wave *= envelope * crash_intensity
        
        # Add noise component
        noise_floor = np.random.random(crash_samples) * self.noise_threshold * 0.1
        crash_wave += noise_floor
        
        # Apply distortion
        crash_wave = np.tanh(crash_wave * 2) / 2
        
        return crash_wave, crash_start, crash_end
    
    def generate_segmentation_violation(self):
        """Generate main segmentation violation soundscape"""
        print("Generating segmentation violation soundscape...")
        
        # Create multiple memory access scenarios
        violations = []
        
        for segment_idx in range(self.memory_segments):
            pattern_type = np.random.choice(self.access_patterns)
            access_pattern = self.generate_memory_access_pattern(pattern_type, segment_idx)
            
            # Check for violations
            violations_mask = access_pattern > 0.8
            if np.any(violations_mask):
                # Create violation at peak access
                violation_time = (segment_idx * self.segment_size + 
                                np.argmax(access_pattern)) / self.sample_rate
                violation_intensity = np.max(access_pattern)
                
                violation_sound, start, end = self.create_crash_sound(
                    violation_time, violation_intensity)
                
                violations.append((violation_sound, start, end))
        
        return violations
    
    def apply_spatial_effects(self, audio):
        """Apply spatialization effects to enhance the crash feeling"""
        print("Applying spatial effects...")
        
        # Create stereo image
        stereo_audio = np.zeros((len(audio), 2))
        
        # Pan different frequency bands
        from scipy import signal
        
        # Low frequencies - centered
        low_freq = signal.butter(4, 500, btype='low', fs=self.sample_rate, output='sos')
        low = signal.sosfilt(low_freq, audio)
        stereo_audio[:, 0] += low * 0.5
        stereo_audio[:, 1] += low * 0.5
        
        # Mid frequencies - slightly panned
        mid_freq = signal.butter(4, [500, 4000], btype='band', fs=self.sample_rate, output='sos')
        mid = signal.sosfilt(mid_freq, audio)
        stereo_audio[:, 0] += mid * 0.7
        stereo_audio[:, 1] += mid * 0.3
        
        # High frequencies - widely panned
        high_freq = signal.butter(4, 4000, btype='high', fs=self.sample_rate, output='sos')
        high = signal.sosfilt(high_freq, audio)
        stereo_audio[:, 0] += high * 0.9
        stereo_audio[:, 1] += high * 0.1
        
        return stereo_audio
    
    def generate_memory_corruption_noise(self):
        """Generate noise representing memory corruption"""
        print("Generating memory corruption noise...")
        
        # Create multiple layers of noise
        noise_layers = []
        
        # White noise - random corruption
        white_noise = np.random.random(self.samples) * 0.1
        noise_layers.append(white_noise)
        
        # Impulse noise - bit flips
        impulse_positions = np.random.choice(self.samples, 
                                          size=int(self.samples * 0.001), 
                                          replace=False)
        impulse_noise = np.zeros(self.samples)
        impulse_noise[impulse_positions] = np.random.random(len(impulse_positions)) * 0.5
        noise_layers.append(impulse_noise)
        
        # Burst noise - consecutive corruption
        burst_starts = np.random.choice(self.samples - 1000, size=20, replace=False)
        burst_noise = np.zeros(self.samples)
        for start in burst_starts:
            end = min(start + 100, self.samples)
            burst_intensity = np.random.random()
            burst_noise[start:end] = np.random.random(end - start) * burst_intensity * 0.3
        noise_layers.append(burst_noise)
        
        # Combine noise layers
        combined_noise = np.sum(noise_layers, axis=0)
        
        # Apply filter to shape the noise
        from scipy import signal
        filter_freq = 2000  # Hz
        b, a = signal.butter(4, filter_freq / (self.sample_rate / 2), btype='low')
        shaped_noise = signal.lfilter(b, a, combined_noise)
        
        return shaped_noise
    
    def compose_segmentation_fault(self):
        """Compose the complete segmentation fault piece"""
        print("Composing segmentation fault...")
        
        # Start with memory corruption noise
        noise_floor = self.generate_memory_corruption_noise()
        self.master_channel += noise_floor * 0.3
        
        # Add segmentation violations
        violations = self.generate_segmentation_violation()
        
        for violation_sound, start, end in violations:
            if end <= self.samples:
                self.master_channel[start:end] += violation_sound
        
        # Create dynamic tension building
        tension_sections = 4
        section_length = self.samples // tension_sections
        
        for i in range(tension_sections):
            section_start = i * section_length
            section_end = section_start + section_length
            
            # Build tension gradually
            if i < tension_sections - 1:
                tension_factor = (i + 1) / tension_sections
                section_audio = np.random.random(section_length) * tension_factor * 0.1
                
                # Add resonant elements
                t = np.linspace(0, section_length / self.sample_rate, section_length)
                resonant_freq = 1000 * (1 + i * 0.5)
                resonance = np.sin(2 * np.pi * resonant_freq * t) * tension_factor * 0.05
                
                self.master_channel[section_start:section_end] += section_audio + resonance
            else:
                # Final section - major segmentation fault
                crash_start = section_start + section_length // 3
                crash_intensity = 1.0
                crash_sound, crash_snd_start, crash_snd_end = self.create_crash_sound(
                    crash_start / self.sample_rate, crash_intensity)
                
                if crash_snd_end <= self.samples:
                    self.master_channel[crash_snd_start:crash_snd_end] += crash_sound
        
        # Apply final processing
        self.master_channel = self.normalize_audio(self.master_channel)
        
        # Apply spatial effects
        stereo_audio = self.apply_spatial_effects(self.master_channel)
        
        return stereo_audio
    
    def normalize_audio(self, audio):
        """Normalize audio to prevent clipping"""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val * 0.8  # Leave some headroom
        return audio
    
    def create_visualization(self, audio):
        """Create visualization of the segmentation fault"""
        print("Creating visualization...")
        
        # Create time domain plot
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        
        # Plot left channel
        axes[0].plot(audio[:, 0])
        axes[0].set_title('Segmentation Fault - Left Channel')
        axes[0].set_ylabel('Amplitude')
        axes[0].grid(True, alpha=0.3)
        
        # Plot right channel
        axes[1].plot(audio[:, 1])
        axes[1].set_title('Segmentation Fault - Right Channel')
        axes[1].set_ylabel('Amplitude')
        axes[1].grid(True, alpha=0.3)
        
        # Plot spectrogram
        axes[2].specgram(audio[:, 0], Fs=self.sample_rate, cmap='viridis')
        axes[2].set_title('Segmentation Fault - Spectrogram')
        axes[2].set_ylabel('Frequency (Hz)')
        axes[2].set_xlabel('Time (s)')
        
        plt.tight_layout()
        plt.savefig('/root/.openclaw/workspace/MachineMusic/visualizations/09_segmentation_fault_enhanced.png', 
                    dpi=150, bbox_inches='tight')
        plt.close()
        
        print("Visualization saved: 09_segmentation_fault_enhanced.png")
    
    def save_audio(self, audio, filename):
        """Save audio to file"""
        # Create samples directory if it doesn't exist
        samples_dir = Path('/root/.openclaw/workspace/MachineMusic/samples')
        samples_dir.mkdir(exist_ok=True)
        
        filepath = samples_dir / filename
        sf.write(str(filepath), audio, self.sample_rate)
        print(f"Audio saved: {filename}")
    
    def generate_metadata(self):
        """Generate metadata for the track"""
        metadata = {
            "title": "Segmentation Fault Enhanced",
            "track_number": 9,
            "album": "Error Garden",
            "artist": "MachineMusic",
            "genre": "Experimental/Algorithmic",
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "techniques": [
                "Physical Modeling",
                "Data Sonification", 
                "Algorithmic Composition",
                "Spatial Audio",
                "Memory Access Simulation"
            ],
            "description": "Enhanced version of segmentation fault with physical modeling of memory violations and spatial effects",
            "inspiration": "Memory segmentation violations represented through resonant crash sounds and spatial disorientation",
            "software": ["Python", "numpy", "scipy", "soundfile"],
            "date_created": "2026-04-08",
            "version": "Enhanced v1.0"
        }
        
        return metadata
    
    def run(self):
        """Run the complete composition process"""
        print("Starting Segmentation Fault Enhanced composition...")
        print(f"Duration: {self.duration} seconds")
        print(f"Sample rate: {self.sample_rate} Hz")
        print("=" * 50)
        
        # Compose the piece
        audio = self.compose_segmentation_fault()
        
        # Create visualization
        self.create_visualization(audio)
        
        # Save audio
        filename = "09_segmentation_fault_enhanced.wav"
        self.save_audio(audio, filename)
        
        # Save metadata
        metadata = self.generate_metadata()
        metadata_path = Path('/root/.openclaw/workspace/MachineMusic/docs/metadata')
        metadata_path.mkdir(exist_ok=True)
        
        with open(metadata_path / "09_segmentation_fault_enhanced.json", 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("=" * 50)
        print("Segmentation Fault Enhanced composition completed!")
        print(f"Total duration: {self.duration:.1f} seconds")
        print(f"Channels: {audio.shape[1]}")
        print(f"Peak amplitude: {np.max(np.abs(audio)):.3f}")
        
        return audio

if __name__ == "__main__":
    # Create and run the enhanced segmentation fault composition
    composer = SegmentationFaultEnhanced(
        sample_rate=44100,
        duration=40.0
    )
    
    audio = composer.run()
    
    print("\nEnhanced Segmentation Fault features:")
    print("- Physical modeling of memory access violations")
    print("- Multi-layered crash soundscape")
    print("- Real-time spatialization effects")
    print("- Dynamic memory corruption simulation")
    print("- Enhanced audio quality and complexity")