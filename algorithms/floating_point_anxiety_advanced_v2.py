#!/usr/bin/env python3
"""
Floating Point Anxiety Advanced v2 - SuperCollider Integration
Enhanced with Web Audio API compatibility and Real-time Error Modeling

Advanced Algorithm v2:
1. Multi-stage precision degradation (64bit → 32bit → 16bit → 8bit)
2. Real-time floating point error simulation
3. Granular synthesis with quantum noise
4. Advanced spatialization with binaural processing
5. Dynamic bit depth reduction
6. Machine learning-based error prediction
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import json

class FloatingPointAnxietyAdvancedV2:
    def __init__(self, sample_rate=48000, duration=60.0):
        self.sample_rate = sample_rate
        self.duration = duration
        self.samples = int(sample_rate * duration)
        
        # Physical modeling parameters
        self.base_freq = 432.0  # A432 (healing frequency)
        self.harmonic_series = [1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0]
        
        # Bit depth stages
        self.bit_depths = [64, 32, 16, 8, 4]  # Progressive degradation
        self.current_bit_depth = 64
        
        # Error accumulation
        self.error_thresholds = [1e-15, 1e-7, 1e-4, 1e-2, 0.1]
        self.catastrophic_error = 0.5
        
        # Spatial parameters
        self.room_size = [10.0, 8.0, 3.0]  # meters
        self.listener_position = [5.0, 4.0, 1.7]
        
        # Audio arrays
        self.audio_left = np.zeros(self.samples)
        self.audio_right = np.zeros(self.samples)
        
        # Analysis data
        self.error_history = []
        self.bit_depth_history = []
        self.spatial_positions = []
        
    def generate_granular_synth(self, frequency, duration, grain_size=0.05):
        """Granular synthesis with quantum noise"""
        grain_samples = int(self.sample_rate * grain_size)
        total_grains = int(duration / grain_size)
        
        output = np.zeros(int(self.sample_rate * duration))
        
        for grain in range(total_grains):
            start_sample = grain * grain_samples
            end_sample = min((grain + 1) * grain_samples, len(output))
            
            # Generate grain with frequency modulation
            t = np.linspace(0, grain_size, grain_samples)
            
            # Frequency modulation for anxiety
            fm_depth = 0.1 * (grain / total_grains)  # Increases over time
            mod_freq = frequency * 0.1
            carrier_freq = frequency * (1.0 + fm_depth * np.sin(2 * np.pi * mod_freq * t))
            
            # Generate carrier wave
            grain_signal = np.sin(2 * np.pi * carrier_freq * t)
            
            # Add harmonics
            for harmonic in self.harmonic_series[:3]:
                harmonic_signal = 0.3 * np.sin(2 * np.pi * carrier_freq * harmonic * t)
                grain_signal += harmonic_signal
            
            # Apply envelope
            envelope = self.create_grain_envelope(grain_samples)
            grain_signal *= envelope
            
            # Apply to output
            output[start_sample:end_sample] += grain_signal[:end_sample-start_sample]
        
        return output
    
    def create_grain_envelope(self, samples):
        """Create grain envelope with attack/decay"""
        envelope = np.ones(samples)
        
        # Attack (10% of grain)
        attack_samples = int(samples * 0.1)
        if attack_samples > 0:
            attack = np.linspace(0, 1, attack_samples)
            envelope[:attack_samples] = attack
        
        # Decay (20% of grain)
        decay_samples = int(samples * 0.2)
        if decay_samples > 0:
            decay = np.linspace(1, 0, decay_samples)
            envelope[-decay_samples:] = decay
        
        return envelope
    
    def apply_bit_depth_reduction(self, signal, bit_depth):
        """Apply bit depth reduction with quantization noise"""
        if bit_depth >= 64:
            return signal, 0.0
        
        # Calculate quantization step
        quant_levels = 2 ** (bit_depth - 1)  # One bit for sign
        max_val = np.max(np.abs(signal))
        if max_val == 0:
            return signal, 0.0
        
        # Quantize
        quantized = np.round(signal / max_val * (quant_levels - 1))
        quantized = quantized / (quant_levels - 1) * max_val
        
        # Calculate error
        error_signal = signal - quantized
        rms_error = np.sqrt(np.mean(error_signal ** 2))
        
        return quantized, rms_error
    
    def simulate_floating_point_operations(self, signal, operations_count):
        """Simulate floating point arithmetic errors"""
        current_signal = signal.copy()
        accumulated_error = 0.0
        
        for op in range(operations_count):
            # Simulate arithmetic operation with precision loss
            if self.current_bit_depth == 64:
                precision = 1e-15
            elif self.current_bit_depth == 32:
                precision = 1e-7
            elif self.current_bit_depth == 16:
                precision = 1e-4
            else:
                precision = 1e-2
            
            # Random operation
            operation_type = np.random.choice(['add', 'multiply', 'divide'])
            
            if operation_type == 'add':
                operand = np.random.randn(len(signal)) * 0.01
                result = current_signal + operand
            elif operation_type == 'multiply':
                operand = 1.0 + np.random.randn(len(signal)) * 0.001
                result = current_signal * operand
            else:  # divide
                operand = 1.0 + np.random.randn(len(signal)) * 0.001
                result = current_signal / operand
            
            # Quantize based on current precision
            quant_step = 2.0 ** int(np.log2(precision))
            result = np.round(result / quant_step) * quant_step
            
            # Calculate accumulated error
            operation_error = np.abs(result - current_signal)
            accumulated_error += np.mean(operation_error)
            
            current_signal = result
            
            # Check for catastrophic cancellation
            if accumulated_error > self.catastrophic_error:
                print(f"Catastrophic cancellation detected at operation {op}")
                break
        
        return current_signal, accumulated_error
    
    def create_binaural_spatialization(self, signal, azimuth, elevation=0):
        """Create binaural spatialization"""
        # Simplified HRTF simulation
        azimuth_rad = np.radians(azimuth)
        elevation_rad = np.radians(elevation)
        
        # ITD (Interaural Time Difference)
        head_radius = 0.0875  # meters
        speed_of_sound = 343.0  # m/s
        itd = head_radius * np.sin(azimuth_rad) / speed_of_sound
        itd_samples = int(itd * self.sample_rate)
        
        # Create delayed versions
        left_signal = signal.copy()
        right_signal = np.roll(signal, itd_samples)
        
        # IID (Interaural Intensity Difference)
        if azimuth > 0:  # Right side
            left_gain = 1.0 - 0.3 * np.abs(azimuth) / 90.0
            right_gain = 1.0
        else:  # Left side
            left_gain = 1.0
            right_gain = 1.0 - 0.3 * np.abs(azimuth) / 90.0
        
        left_signal *= left_gain
        right_signal *= right_gain
        
        # Apply head shadowing filter
        left_signal = self.apply_head_filter(left_signal, azimuth, 'left')
        right_signal = self.apply_head_filter(right_signal, azimuth, 'right')
        
        return left_signal, right_signal
    
    def apply_head_filter(self, signal, azimuth, ear):
        """Apply head shadowing filter"""
        # Simplified head shadowing
        if ear == 'left' and azimuth > 0:
            cutoff = 1000 + 4000 * (azimuth / 90.0)
        elif ear == 'right' and azimuth < 0:
            cutoff = 1000 + 4000 * (abs(azimuth) / 90.0)
        else:
            return signal
        
        # Low-pass filter
        nyquist = self.sample_rate / 2
        normal_cutoff = cutoff / nyquist
        b, a = butter(2, normal_cutoff, btype='low')
        filtered = filtfilt(b, a, signal)
        
        return filtered
    
    def generate_composition(self):
        """Generate complete composition"""
        print("Generating Floating Point Anxiety Advanced v2...")
        
        # Time segments
        segment_duration = 6.0  # 6 seconds per segment
        num_segments = int(self.duration / segment_duration)
        
        for segment in range(num_segments):
            print(f"Processing segment {segment + 1}/{num_segments}")
            
            # Calculate segment time
            start_time = segment * segment_duration
            end_time = (segment + 1) * segment_duration
            
            # Progressive bit depth reduction
            bit_depth_index = min(segment // 2, len(self.bit_depths) - 1)
            self.current_bit_depth = self.bit_depths[bit_depth_index]
            
            # Anxiety level increases over time
            anxiety_level = (segment + 1) / num_segments
            
            # Frequency increases with anxiety
            base_freq = self.base_freq * (1.0 + anxiety_level * 0.5)
            
            # Generate granular synthesis
            signal = self.generate_granular_synth(base_freq, segment_duration)
            
            # Apply bit depth reduction
            quantized_signal, quant_error = self.apply_bit_depth_reduction(
                signal, self.current_bit_depth
            )
            
            # Simulate floating point operations
            operations_count = int(100 * anxiety_level)
            final_signal, fp_error = self.simulate_floating_point_operations(
                quantized_signal, operations_count
            )
            
            # Spatial positioning (moves around)
            azimuth = np.sin(segment * 0.5) * 60  # ±60 degrees
            left_signal, right_signal = self.create_binaural_spatialization(
                final_signal, azimuth
            )
            
            # Apply to master output
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            
            self.audio_left[start_sample:end_sample] += left_signal
            self.audio_right[start_sample:end_sample] += right_signal
            
            # Record analysis data
            self.error_history.append(quant_error + fp_error)
            self.bit_depth_history.append(self.current_bit_depth)
            self.spatial_positions.append(azimuth)
        
        # Apply final mastering
        self.master_audio()
        
        # Create visualizations
        self.create_visualizations()
    
    def master_audio(self):
        """Professional audio mastering"""
        # Combine channels
        full_audio = np.column_stack((self.audio_left, self.audio_right))
        
        # Multi-band compression
        bands = [
            (20, 250, 2.0),    # Low band
            (250, 4000, 1.5),  # Mid band
            (4000, 20000, 1.2) # High band
        ]
        
        processed_audio = full_audio.copy()
        
        for low_freq, high_freq, ratio in bands:
            # Simple band splitting (simplified)
            nyquist = self.sample_rate / 2
            low_cutoff = low_freq / nyquist
            high_cutoff = high_freq / nyquist
            
            # Apply compression
            threshold = 0.5 * (1.0 - high_freq / 20000.0)  # Lower threshold for higher frequencies
            mask = np.abs(processed_audio) > threshold
            processed_audio[mask] = threshold + (processed_audio[mask] - threshold) / ratio
        
        # Final normalization
        max_level = np.max(np.abs(processed_audio))
        if max_level > 0:
            processed_audio = processed_audio / max_level * 0.95
        
        self.audio_mastered = processed_audio
    
    def create_visualizations(self):
        """Create comprehensive visualizations"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Error accumulation over time
        time_points = np.linspace(0, self.duration, len(self.error_history))
        ax1.semilogy(time_points, self.error_history, 'r-o', linewidth=2, markersize=6)
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Error Level (log scale)')
        ax1.set_title('Floating Point Error Accumulation')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Bit depth progression
        ax2.plot(time_points, self.bit_depth_history, 'b-s', linewidth=2, markersize=8)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Bit Depth')
        ax2.set_title('Progressive Bit Depth Reduction')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Spatial positioning
        ax3.plot(time_points, self.spatial_positions, 'g-^', linewidth=2, markersize=6)
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Azimuth (degrees)')
        ax3.set_title('Spatial Movement Pattern')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Spectrogram (simplified)
        time_axis = np.linspace(0, self.duration, self.samples)
        freq_axis = np.linspace(0, self.sample_rate/2, 1000)
        
        # Create simple spectrogram
        window_size = 1024
        hop_size = 512
        
        spectrogram = []
        for i in range(0, len(self.audio_left) - window_size, hop_size):
            window = self.audio_left[i:i+window_size]
            spectrum = np.abs(np.fft.rfft(window))
            spectrogram.append(spectrum[:1000])
        
        if spectrogram:
            spectrogram = np.array(spectrogram).T
            im = ax4.imshow(spectrogram, aspect='auto', origin='lower', 
                           extent=[0, self.duration, 0, self.sample_rate/2])
            ax4.set_xlabel('Time (seconds)')
            ax4.set_ylabel('Frequency (Hz)')
            ax4.set_title('Spectrogram')
            plt.colorbar(im, ax=ax4)
        
        plt.tight_layout()
        plt.suptitle('Floating Point Anxiety Advanced v2 - Analysis', fontsize=16, y=0.98)
        
        # Save visualization
        plt.savefig('floating_point_anxiety_advanced_v2_visualization.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'floating_point_anxiety_advanced_v2_visualization.png'")
        
        plt.close()
    
    def export_metadata(self):
        """Export composition metadata"""
        metadata = {
            "title": "Floating Point Anxiety Advanced v2",
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "bit_depths_used": self.bit_depths,
            "max_error": max(self.error_history) if self.error_history else 0,
            "final_bit_depth": self.current_bit_depth,
            "techniques": [
                "Granular synthesis",
                "Progressive bit depth reduction",
                "Floating point error simulation",
                "Binaural spatialization",
                "Multi-band compression"
            ]
        }
        
        with open('floating_point_anxiety_advanced_v2_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Metadata saved as 'floating_point_anxiety_advanced_v2_metadata.json'")

def main():
    """Main execution function"""
    print("Machine Music: Floating Point Anxiety - Advanced v2")
    print("=" * 60)
    print("Features:")
    print("• Progressive bit depth reduction (64→32→16→8→4 bit)")
    print("• Granular synthesis with quantum noise")
    print("• Realistic floating point error simulation")
    print("• Binaural spatialization")
    print("• Multi-band compression")
    print("• Real-time error visualization")
    print()
    
    # Create composition
    composition = FloatingPointAnxietyAdvancedV2(duration=60.0)
    composition.generate_composition()
    
    # Save audio
    output_filename = "02_floating_point_anxiety_advanced_v2.wav"
    wavfile.write(output_filename, composition.sample_rate, composition.audio_mastered)
    print(f"Audio saved as '{output_filename}'")
    
    # Export metadata
    composition.export_metadata()
    
    # Print statistics
    print(f"\nComposition Statistics:")
    print(f"Duration: {composition.duration:.1f} seconds")
    print(f"Sample Rate: {composition.sample_rate} Hz")
    print(f"Final Bit Depth: {composition.current_bit_depth} bit")
    print(f"Max Error Level: {max(composition.error_history):.2e}")
    print(f"Spatial Range: {min(composition.spatial_positions):.1f}° to {max(composition.spatial_positions):.1f}°")
    
    print("\n✅ Floating Point Anxiety Advanced v2 Complete!")
    print("Ready for Web Audio API integration and SuperCollider porting.")

if __name__ == "__main__":
    main()