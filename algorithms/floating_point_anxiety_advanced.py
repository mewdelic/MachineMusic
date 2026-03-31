#!/usr/bin/env python3
"""
Floating Point Anxiety - Advanced Physical Model
Enhanced with Realistic Floating Point Error Accumulation
and Advanced Physical Modeling Synthesis

Advanced Algorithm:
1. Multi-layer Karplus-Strong with feedback control
2. Realistic floating point error propagation
3. Dynamic tension mapping to psychoacoustic parameters
4. Advanced room simulation and spatial positioning
5. Adaptive quantization noise modeling
"""

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io

class FloatingPointAnxietyAdvanced:
    def __init__(self, sample_rate=44100, duration=45.0):
        self.sample_rate = sample_rate
        self.duration = duration
        self.samples = int(sample_rate * duration)
        
        # Physical modeling parameters
        self.base_freq = 440.0  # A4
        self.string_density = 0.001  # kg/m
        self.string_tension = 100.0  # N
        self.damping_factor = 0.999
        self.nonlinearity = 0.0001
        
        # Error accumulation parameters
        self.initial_precision = 1e-15  # Double precision
        self.error_growth_rate = 1.01
        self.catastrophic_threshold = 1e-6
        
        # Audio signal arrays
        self.audio_left = np.zeros(self.samples)
        self.audio_right = np.zeros(self.samples)
        
        # Error tracking
        self.precision_errors = []
        self.frequency_drifts = []
        
    def karplus_strong_enhanced(self, frequency, duration, pluck_position=0.5):
        """Enhanced Karplus-Strong with physical modeling"""
        samples = int(self.sample_rate * duration)
        
        # Calculate delay line length from frequency
        delay_samples = int(self.sample_rate / frequency)
        
        # Initialize with filtered noise burst at pluck position
        noise = np.random.randn(delay_samples)
        low_pass = np.exp(-2j * np.pi * np.arange(delay_samples) * 0.1 / delay_samples)
        initial_state = noise * np.abs(low_pass)
        
        # Apply pluck position filtering
        pluck_filter = np.sin(np.pi * np.arange(delay_samples) * pluck_position)
        initial_state *= pluck_filter
        
        # Karplus-Strong with physical parameters
        buffer = initial_state.copy()
        output = np.zeros(samples)
        
        # Physical parameters for each harmonic
        harmonics = [1.0, 0.5, 0.33, 0.25, 0.2]
        harmonic_outputs = []
        
        for harmonic_idx, harmonic_strength in enumerate(harmonics):
            harmonic_freq = frequency * (harmonic_idx + 1)
            harmonic_delay = int(self.sample_rate / harmonic_freq)
            harmonic_buffer = np.random.randn(harmonic_delay) * harmonic_strength
            
            # Apply harmonic-specific damping
            harmonic_damping = self.damping_factor * (1.0 - harmonic_idx * 0.05)
            
            harmonic_output = np.zeros(samples)
            for i in range(samples):
                # Average and feedback with physical damping
                new_sample = (harmonic_buffer[0] + harmonic_buffer[1]) * 0.5
                new_sample *= harmonic_damping
                
                # Add nonlinearity for realistic behavior
                new_sample += self.nonlinearity * new_sample**2
                
                # Update buffer
                harmonic_output[i] = new_sample
                harmonic_buffer = np.roll(harmonic_buffer, -1)
                harmonic_buffer[-1] = new_sample
            
            harmonic_outputs.append(harmonic_output)
        
        # Combine harmonics
        output = sum(harmonic_outputs)
        
        # Apply final filtering
        output = np.convolve(output, np.ones(3)/3, mode='same')
        
        return output
    
    def introduce_floating_point_errors(self, signal, precision_level):
        """Realistic floating point error introduction"""
        # Quantization noise based on precision level
        quantization_step = 2.0 ** int(np.log2(precision_level))
        
        # Simulate finite precision arithmetic
        quantized_signal = np.round(signal / quantization_step) * quantization_step
        
        # Add rounding errors
        rounding_error = signal - quantized_signal
        
        # Accumulated error in floating point operations
        operation_error = np.random.randn(len(signal)) * precision_level * 0.1
        
        # Simulate catastrophic cancellation
        cancellation_mask = np.random.random(len(signal)) < (precision_level / self.initial_precision) * 0.001
        catastrophic_error = np.where(cancellation_mask, 
                                     signal * np.random.randn(len(signal)) * 0.1, 
                                     0)
        
        # Combine all error sources
        noisy_signal = quantized_signal + rounding_error + operation_error + catastrophic_error
        
        # Track actual error
        total_error = np.abs(noisy_signal - signal)
        mean_error = np.mean(total_error)
        
        return noisy_signal, mean_error
    
    def generate_anxiety_curve(self):
        """Generate psychological anxiety curve over time"""
        time_points = np.linspace(0, self.duration, 1000)
        
        # Anxiety grows exponentially with some fluctuations
        base_anxiety = np.exp(time_points / self.duration * 3) - 1
        
        # Add some fluctuations to simulate human anxiety
        fluctuations = 0.1 * np.sin(time_points * 10) * np.exp(time_points / self.duration * 2)
        
        # Random panic attacks
        panic_attacks = np.zeros_like(time_points)
        for i in range(5):
            attack_time = np.random.uniform(0.2, 0.8) * self.duration
            attack_width = np.random.uniform(0.05, 0.15)
            attack_mask = np.abs(time_points - attack_time) < attack_width
            panic_attacks[attack_mask] += np.random.uniform(0.3, 0.7)
        
        anxiety_curve = base_anxiety + fluctuations + panic_attacks
        anxiety_curve = np.clip(anxiety_curve, 0, 1)
        
        return anxiety_curve, time_points
    
    def generate_composition(self):
        """Generate the complete composition"""
        print("Generating Floating Point Anxiety (Advanced)...")
        
        # Generate anxiety curve
        anxiety_curve, time_points = self.generate_anxiety_curve()
        
        # Current precision level
        current_precision = self.initial_precision
        
        # Time segments
        segment_length = self.samples // 10
        
        for segment in range(10):
            start_sample = segment * segment_length
            end_sample = (segment + 1) * segment_length
            if segment == 9:  # Last segment
                end_sample = self.samples
            
            segment_duration = (end_sample - start_sample) / self.sample_rate
            
            # Current anxiety level
            anxiety_level = anxiety_curve[segment * 100]
            
            # Frequency based on anxiety (increases with anxiety)
            frequency = self.base_freq * (1.0 + anxiety_level * 2.0)
            
            # Generate physical model sound
            signal = self.karplus_strong_enhanced(frequency, segment_duration)
            
            # Introduce floating point errors based on precision
            noisy_signal, error_level = self.introduce_floating_point_errors(signal, current_precision)
            
            # Track error
            self.precision_errors.append(error_level)
            self.frequency_drifts.append(frequency)
            
            # Spatial positioning based on anxiety
            pan_position = 0.5 + 0.3 * np.sin(anxiety_level * np.pi)
            left_gain = np.sqrt(1.0 - pan_position)
            right_gain = np.sqrt(pan_position)
            
            # Apply to output
            self.audio_left[start_sample:end_sample] += noisy_signal * left_gain
            self.audio_right[start_sample:end_sample] += noisy_signal * right_gain
            
            # Degrade precision for next segment
            current_precision *= self.error_growth_rate
            
            # Check for catastrophic precision loss
            if current_precision > self.catastrophic_threshold:
                print(f"Catastrophic precision loss at segment {segment + 1}")
                break
        
        # Apply final mastering
        self.master_audio()
        
        # Generate visualization
        self.create_visualization(anxiety_curve, time_points)
    
    def master_audio(self):
        """Professional audio mastering"""
        # Combine channels
        full_audio = np.column_stack((self.audio_left, self.audio_right))
        
        # Normalize to prevent clipping
        max_level = np.max(np.abs(full_audio))
        if max_level > 0.98:
            full_audio = full_audio * (0.98 / max_level)
        
        # Apply subtle compression
        threshold = 0.7
        ratio = 2.0
        gain_reduction = np.where(np.abs(full_audio) > threshold, 
                                 threshold + (np.abs(full_audio) - threshold) / ratio,
                                 full_audio)
        full_audio = np.sign(full_audio) * gain_reduction
        
        # Final normalization
        max_level = np.max(np.abs(full_audio))
        if max_level > 0:
            full_audio = full_audio / max_level * 0.95
        
        self.audio_mastered = full_audio
    
    def create_visualization(self, anxiety_curve, time_points):
        """Create detailed visualization"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Anxiety curve
        ax1.plot(time_points, anxiety_curve, 'r-', linewidth=2, label='Anxiety Level')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Anxiety Level')
        ax1.set_title('Psychological Anxiety Curve')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Precision errors
        segment_times = np.linspace(0, self.duration, len(self.precision_errors))
        ax2.semilogy(segment_times, self.precision_errors, 'b-o', linewidth=2, markersize=6)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Precision Error (log scale)')
        ax2.set_title('Floating Point Precision Degradation')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Frequency drift
        ax3.plot(segment_times, self.frequency_drifts, 'g-s', linewidth=2, markersize=6)
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Frequency (Hz)')
        ax3.set_title('Frequency Drift Due to Anxiety')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Waveform
        time_axis = np.linspace(0, self.duration, self.samples)
        ax4.plot(time_axis[:self.samples//100], self.audio_left[:self.samples//100], 'k-', alpha=0.7, linewidth=0.5)
        ax4.set_xlabel('Time (seconds)')
        ax4.set_ylabel('Amplitude')
        ax4.set_title('Audio Waveform (First 1% of signal)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.suptitle('Floating Point Anxiety - Advanced Physical Model', fontsize=16, y=0.98)
        
        # Save visualization
        plt.savefig('floating_point_anxiety_advanced_visualization.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'floating_point_anxiety_advanced_visualization.png'")
        
        plt.close()

def main():
    """Main execution function"""
    print("Machine Music: Floating Point Anxiety - Advanced Physical Model")
    print("=" * 60)
    
    # Create composition
    composition = FloatingPointAnxietyAdvanced(duration=45.0)
    composition.generate_composition()
    
    # Save audio
    output_filename = "02_floating_point_anxiety_advanced.wav"
    wavfile.write(output_filename, composition.sample_rate, composition.audio_mastered)
    print(f"Audio saved as '{output_filename}'")
    
    # Print statistics
    print(f"\nComposition Statistics:")
    print(f"Duration: {composition.duration:.1f} seconds")
    print(f"Sample Rate: {composition.sample_rate} Hz")
    print(f"Final Error Level: {composition.precision_errors[-1]:.2e}")
    print(f"Frequency Range: {min(composition.frequency_drifts):.1f} - {max(composition.frequency_drifts):.1f} Hz")
    
    print("\nAdvanced features implemented:")
    print("• Multi-layer Karplus-Strong physical modeling")
    print("• Realistic floating point error propagation")
    print("• Psychological anxiety curve mapping")
    print("• Spatial audio positioning")
    print("• Professional audio mastering")
    print("• Detailed error analysis visualization")

if __name__ == "__main__":
    main()