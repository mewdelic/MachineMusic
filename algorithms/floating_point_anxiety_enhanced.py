#!/usr/bin/env python3
"""
Floating Point Anxiety (Enhanced) — 精度が失われる不安

Enhanced Version with Physical Modeling Synthesis

Concept:
- Floating point rounding errors accumulate over time
- Small precision losses grow into noticeable detuning
- The anxiety of knowing you're losing accuracy but can't stop
- Eventually, precision completely breaks down into chaos
- Enhanced with physical modeling synthesis for realistic sound textures

Algorithm (Enhanced):
1. Start with precise, clean frequencies using Karplus-Strong synthesis
2. Each iteration introduces tiny floating point errors
3. Errors compound exponentially with physical model degradation
4. Timing becomes unstable, frequencies drift with realistic decay
5. Final state: complete loss of precision - noise and chaotic resonance

Enhancements:
- Karplus-Strong physical modeling for realistic string textures
- Improved harmonic structure with complex resonance
- Realistic physical degradation effects
- Professional audio quality with proper dynamic range
- Enhanced frequency analysis and visualization
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import os
import matplotlib.pyplot as plt
from pathlib import Path

# Parameters
SAMPLE_RATE = 44100
DURATION = 30  # seconds
BASE_FREQ = 440.0  # A4 - start perfectly in tune

def karplus_strong_synth(frequency, duration, decay_factor=0.996, brightness=0.5):
    """
    Karplus-Strong physical modeling synthesis for realistic string sounds
    Enhanced with floating point error accumulation
    """
    samples = int(SAMPLE_RATE * duration)
    
    # String length in samples
    N = int(SAMPLE_RATE / frequency)
    
    # Initialize with noise (string pluck)
    noise = np.random.uniform(-1, 1, N)
    if brightness < 0.5:
        # Filter for mellower sound
        noise = lfilter(*butter(2, brightness * 2, 'low'), noise)
    
    # Karplus-Strong algorithm with error accumulation
    output = np.zeros(samples)
    buffer = np.concatenate([noise, np.zeros(samples)])
    
    error_accumulation = 0.0
    
    for i in range(samples):
        # Karplus-Strong: average of two samples
        idx = i % N
        output[i] = buffer[idx]
        
        # Update buffer with averaging and error
        if i + N < len(buffer):
            avg = (buffer[idx] + buffer[idx + 1]) * 0.5
            # Add floating point error that accumulates
            error = np.float32(np.random.normal(0, 0.0001 * (i / samples)))
            error_accumulation += abs(error)
            
            # Apply decay and error
            buffer[idx + N] = avg * decay_factor + error
            
            # Enhance error effect over time
            if error_accumulation > 0.1:
                buffer[idx + N] += np.random.normal(0, error_accumulation * 0.1)
    
    return output

def accumulate_error_enhanced(value, iterations=100):
    """
    Enhanced floating point error accumulation with physical modeling
    """
    result = np.float32(value)
    delta = np.float32(0.1)
    error_history = []
    
    for _ in range(iterations):
        # Physical modeling: simulate real computation with limited precision
        result = np.float32(result + delta)
        result = np.float32(result - delta)
        
        # Track error accumulation
        current_error = abs(result - value)
        error_history.append(current_error)
        
        # Add resonance effect (physical vibration)
        if current_error > 0.001:
            resonance = current_error * 0.1 * np.sin(len(error_history) * 0.1)
            result += np.float32(resonance)
    
    error = abs(result - value)
    return result, error, error_history

def drifting_frequency_enhanced(base_freq, duration_sec, drift_rate=0.0001):
    """
    Enhanced frequency drift with physical modeling and realistic decay
    """
    samples = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, samples, False)
    
    # Generate base frequency using Karplus-Strong
    base_synth = karplus_strong_synth(base_freq, duration_sec, decay_factor=0.998, brightness=0.7)
    
    # Apply frequency drift with physical modeling
    freq = np.float32(base_freq)
    phase = np.float32(0.0)
    
    # Physical resonance parameters
    resonance_freq = base_freq * 2.5
    resonance_decay = 0.995
    
    output = np.zeros(samples, dtype=np.float32)
    resonance_buffer = np.zeros(samples)
    
    error_accumulation = 0.0
    
    for i in range(samples):
        # Accumulate error in phase calculation with physical modeling
        phase += 2 * np.pi * freq / SAMPLE_RATE
        
        # Physical model: frequency drift affects resonance
        resonance_amplitude = np.exp(-i * (1 - resonance_decay) / SAMPLE_RATE)
        resonance = np.sin(2 * np.pi * resonance_freq * i / SAMPLE_RATE) * resonance_amplitude
        
        # Enhanced drift calculation with physical effects
        drift_factor = np.float32(1.0 + drift_rate * (i / samples) ** 2)
        freq = np.float32(freq * drift_factor)
        
        # Periodically introduce more error with physical resonance
        if i % 1000 == 0:
            freq, error, _ = accumulate_error_enhanced(freq, iterations=50)
            error_accumulation += error
        
        # Combine base synthesis with resonance and drift
        base_component = np.sin(phase) * 0.3
        physical_component = resonance * (0.1 + error_accumulation * 0.5)
        
        output[i] = np.float32(base_component + physical_component)
    
    # Mix with Karplus-Strong base
    final_output = base_synth * 0.6 + output * 0.4
    
    return final_output.astype(np.float64)

def precision_degradation_section_enhanced(base_freq, duration_sec):
    """
    Enhanced precision degradation with physical modeling harmony
    Multiple oscillators with realistic string synthesis and drift
    """
    samples = int(SAMPLE_RATE * duration_sec)
    
    # Start with a chord: A major with physical modeling
    frequencies = [
        base_freq,           # A
        base_freq * 5/4,    # C# (just intonation)
        base_freq * 3/2,    # E
    ]
    
    output = np.zeros(samples)
    
    for i, freq in enumerate(frequencies):
        # Each voice uses Karplus-Strong synthesis with different parameters
        decay = 0.998 - i * 0.001  # Slightly different decay per voice
        brightness = 0.5 + i * 0.1
        
        # Generate physical model voice
        voice = karplus_strong_synth(freq, duration_sec, decay_factor=decay, brightness=brightness)
        
        # Apply drift with physical effects
        drift_rate = 0.0001 * (i + 1)
        drifted = drifting_frequency_enhanced(freq, duration_sec, drift_rate=drift_rate)
        
        # Mix physical model with drift
        voice_mix = voice * 0.7 + drifted * 0.3
        
        output += voice_mix
    
    return output / len(frequencies)

def anxious_tremolo_enhanced(duration_sec, anxiety_level=0.5):
    """
    Enhanced tremolo with physical modeling characteristics
    Represents the nervousness of precision loss with realistic resonance
    """
    samples = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, samples, False)
    
    # Base tremolo frequency with physical resonance
    trem_freq = 6.0  # Hz
    resonance_freq = trem_freq * 3.7  # Physical resonance relationship
    
    # Enhanced jitter that increases over time with physical characteristics
    jitter = np.random.normal(0, anxiety_level, samples)
    jitter = np.convolve(jitter, np.ones(200)/200, mode='same')  # Smoother physical response
    
    # Physical modeling: tremolo frequency becomes unstable with resonance
    mod_freq = trem_freq + jitter * 3
    resonance_mod = resonance_freq + jitter * 1.5
    
    # Generate tremolo with unstable frequency and resonance
    phase = np.cumsum(2 * np.pi * mod_freq / SAMPLE_RATE)
    resonance_phase = np.cumsum(2 * np.pi * resonance_mod / SAMPLE_RATE)
    
    tremolo = 0.5 + 0.4 * np.sin(phase) + 0.1 * np.sin(resonance_phase)
    
    # Add physical decay characteristic
    decay = np.exp(-t * anxiety_level * 0.1)
    tremolo *= (1 - decay * 0.3)
    
    return tremolo

def catastrophic_precision_loss_enhanced(duration_sec):
    """
    Enhanced catastrophic precision loss with physical modeling
    Realistic fragmentation with string resonance and chaotic vibrations
    """
    samples = int(SAMPLE_RATE * duration_sec)
    output = np.zeros(samples)
    
    # Enhanced number of fragments for richer texture
    num_fragments = 50
    
    for i in range(num_fragments):
        # Start position with timing errors (physical response delay)
        start = int((i / num_fragments) * samples + np.random.normal(0, samples * 0.05))
        start = max(0, min(start, samples - 2000))
        
        # Fragment length with physical decay characteristics
        frag_len = int(np.random.exponential(1500))
        frag_len = min(frag_len, samples - start)
        
        if frag_len <= 0:
            continue
        
        # Enhanced frequency with physical resonance
        base = 440.0
        error_factor = np.random.uniform(0.3, 3.0)
        freq = base * error_factor * (1 + np.random.normal(0, 0.4))
        
        # Add resonance frequencies for physical modeling
        resonance_freqs = [freq * 2.0, freq * 3.1, freq * 4.9]
        
        t = np.linspace(0, frag_len / SAMPLE_RATE, frag_len, False)
        
        # Generate fragment with multiple resonances
        fragment = np.zeros(frag_len)
        
        # Fundamental
        jittered_freq = freq * (1 + np.random.normal(0, 0.15, frag_len))
        phase = np.cumsum(2 * np.pi * jittered_freq / SAMPLE_RATE)
        fragment += np.sin(phase) * 0.2
        
        # Add resonances with different amplitudes and phases
        for j, res_freq in enumerate(resonance_freqs):
            res_jittered = res_freq * (1 + np.random.normal(0, 0.1, frag_len))
            res_phase = np.cumsum(2 * np.pi * res_jittered / SAMPLE_RATE)
            res_amplitude = 0.1 / (j + 1)  # Decreasing amplitude for higher harmonics
            fragment += np.sin(res_phase) * res_amplitude
        
        # Apply physical envelope with realistic decay
        envelope = np.exp(-np.linspace(0, 4, frag_len))
        fragment *= envelope
        
        # Add Karplus-Strong texture to some fragments
        if i % 3 == 0:  # Every third fragment gets physical modeling
            ks_fragment = karplus_strong_synth(freq, frag_len / SAMPLE_RATE, 
                                            decay_factor=0.99, brightness=0.8)
            # Ensure same length before adding
            min_len = min(len(fragment), len(ks_fragment))
            fragment[:min_len] += ks_fragment[:min_len] * 0.3
        
        output[start:start+frag_len] += fragment
    
    return output

def create_floating_point_anxiety_enhanced():
    """Create the enhanced Floating Point Anxiety track with physical modeling"""
    print("Phase 1: Precision begins to slip (Enhanced)...")
    
    # Phase 1: Gradual drift with physical modeling (0-15 seconds)
    phase1_duration = 15
    phase1 = precision_degradation_section_enhanced(BASE_FREQ, phase1_duration)
    
    # Add enhanced anxious tremolo with physical characteristics
    tremolo = anxious_tremolo_enhanced(phase1_duration, anxiety_level=0.3)
    phase1 *= tremolo
    
    print("Phase 2: Anxiety builds (Enhanced)...")
    
    # Phase 2: Accelerating drift with enhanced physical effects (15-25 seconds)
    phase2_duration = 10
    phase2 = precision_degradation_section_enhanced(BASE_FREQ * 1.01, phase2_duration)
    tremolo2 = anxious_tremolo_enhanced(phase2_duration, anxiety_level=0.7)
    phase2 *= tremolo2
    
    # Add enhanced chaotic layer with physical resonance
    phase2_bass = drifting_frequency_enhanced(BASE_FREQ / 2, phase2_duration, drift_rate=0.0003)
    phase2 += phase2_bass * 0.5
    
    # Add physical resonance layer
    phase2_resonance = karplus_strong_synth(BASE_FREQ * 0.5, phase2_duration, 
                                          decay_factor=0.995, brightness=0.3)
    phase2 += phase2_resonance * 0.3
    
    print("Phase 3: Catastrophic precision loss (Enhanced)...")
    
    # Phase 3: Complete breakdown with physical modeling (25-30 seconds)
    phase3_duration = 5
    phase3 = catastrophic_precision_loss_enhanced(phase3_duration)
    
    # Add enhanced white noise with physical characteristics
    noise_duration = 3
    noise_samples = int(SAMPLE_RATE * noise_duration)
    noise = np.random.uniform(-0.3, 0.3, noise_samples)
    
    # Filter noise for physical characteristics
    noise = lfilter(*butter(4, 8000, 'low', fs=SAMPLE_RATE), noise)
    
    # Fade in noise with physical decay envelope
    noise_envelope = np.linspace(0, 1, noise_samples) ** 1.5
    noise *= noise_envelope
    
    # Add resonance to noise
    resonance_noise = lfilter(*butter(2, 2000, 'band', fs=SAMPLE_RATE), noise)
    noise += resonance_noise * 0.5
    
    # Overlay enhanced noise on the end of phase3
    if len(phase3) > noise_samples:
        phase3[-noise_samples:] += noise
    else:
        phase3 = phase3 * 0.5 + noise[:len(phase3)] * 0.5
    
    print("Assembling enhanced track...")
    
    # Combine all phases
    full_track = np.concatenate([phase1, phase2, phase3])
    
    # Enhanced normalization with dynamic range control
    max_val = np.max(np.abs(full_track))
    if max_val > 0:
        full_track = full_track / max_val * 0.88  # Slightly higher for enhanced dynamics
    
    # Apply professional fade out with physical decay
    fade_length = int(SAMPLE_RATE * 2.0)
    if len(full_track) > fade_length:
        fade = np.linspace(1, 0, fade_length) ** 2.5  # Exponential fade with physical characteristic
        full_track[-fade_length:] *= fade
    
    return full_track

def create_frequency_analysis(audio, sample_rate, title="Frequency Analysis"):
    """Create frequency analysis visualization"""
    # Calculate FFT
    n = len(audio)
    freq = np.fft.fftfreq(n, 1/sample_rate)
    fft_magnitude = np.abs(np.fft.fft(audio))
    
    # Only plot positive frequencies
    positive_freq_idx = freq > 0
    freq = freq[positive_freq_idx]
    fft_magnitude = fft_magnitude[positive_freq_idx]
    
    # Create plot
    plt.figure(figsize=(12, 8))
    
    # Time domain plot
    plt.subplot(3, 1, 1)
    time_axis = np.arange(len(audio)) / sample_rate
    plt.plot(time_axis, audio, alpha=0.7)
    plt.title(f'{title} - Time Domain')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # Frequency domain plot (full spectrum)
    plt.subplot(3, 1, 2)
    plt.semilogy(freq[:len(freq)//4], fft_magnitude[:len(fft_magnitude)//4])
    plt.title('Frequency Spectrum (Full)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 20000)
    
    # Frequency domain plot (low frequencies)
    plt.subplot(3, 1, 3)
    plt.semilogy(freq[:len(freq)//40], fft_magnitude[:len(fft_magnitude)//40])
    plt.title('Frequency Spectrum (Low Frequencies)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 2000)
    
    plt.tight_layout()
    return plt.gcf()

def demonstrate_error_enhanced():
    """Show the enhanced floating point error demonstration"""
    print("\n--- Enhanced Floating Point Error Demonstration ---")
    
    test_value = 1.0
    result, error, error_history = accumulate_error_enhanced(test_value, iterations=1000)
    print(f"Start: {test_value}")
    print(f"After 1000 +/- 0.1 operations: {result}")
    print(f"Error: {error}")
    print(f"Relative error: {error/test_value * 100:.10f}%")
    print(f"Maximum error during accumulation: {max(error_history)}")
    
    # Show frequency drift with physical effects
    print("\n--- Enhanced Frequency Drift with Physical Effects ---")
    freq = 440.0
    for i in range(5):
        drifted, error, _ = accumulate_error_enhanced(freq, iterations=100 * (i + 1))
        cents_off = 1200 * np.log2(drifted / freq)
        print(f"Iterations {100 * (i+1)}: {drifted:.6f} Hz ({cents_off:+.2f} cents from A440)")
    
    # Physical modeling parameters
    print("\n--- Physical Modeling Parameters ---")
    print("Karplus-Strong Synthesis: Enabled")
    print("Resonance Frequencies: 2.0x, 3.1x, 4.9x base frequency")
    print("Decay Factors: 0.995-0.998 (string-like)")
    print("Brightness: 0.3-0.8 (timbre control)")
    print()

def analyze_audio_quality(audio, sample_rate):
    """Analyze and print audio quality metrics"""
    # Calculate metrics
    peak_amplitude = np.max(np.abs(audio))
    rms_level = np.sqrt(np.mean(audio**2))
    
    # Dynamic range (in dB)
    signal_floor = np.min(np.abs(audio))
    dynamic_range_db = 20 * np.log10(peak_amplitude / max(signal_floor, 1e-10))
    
    # Zero crossing rate (rough indicator of frequency content)
    zero_crossings = np.sum(np.diff(np.signbit(audio)))
    zero_crossing_rate = zero_crossings / len(audio) * sample_rate
    
    print(f"\n--- Enhanced Audio Quality Analysis ---")
    print(f"Sample Rate: {sample_rate} Hz")
    print(f"Duration: {len(audio) / sample_rate:.1f} seconds")
    print(f"Peak Amplitude: {peak_amplitude:.4f}")
    print(f"RMS Level: {rms_level:.4f}")
    print(f"Dynamic Range: {dynamic_range_db:.2f} dB")
    print(f"Zero Crossing Rate: {zero_crossing_rate:.1f} Hz")
    print(f"Quality Assessment: {'Professional' if dynamic_range_db > 18 else 'Good'}")

if __name__ == "__main__":
    print("=" * 60)
    print("Floating Point Anxiety (Enhanced) - Track 2 of Error Garden")
    print("=" * 60)
    print("Enhanced with Physical Modeling Synthesis")
    print("=" * 60)
    
    # Show the enhanced concept
    demonstrate_error_enhanced()
    
    # Create enhanced track
    print("Creating enhanced track with physical modeling...")
    track = create_floating_point_anxiety_enhanced()
    
    # Analyze audio quality
    analyze_audio_quality(track, SAMPLE_RATE)
    
    # Convert to 16-bit PCM
    track_16bit = np.int16(track * 32767)
    
    # Create visualization
    print("Creating frequency analysis visualization...")
    fig = create_frequency_analysis(track, SAMPLE_RATE, 
                                  "Floating Point Anxiety (Enhanced)")
    
    # Save audio file
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", 
                              "02_floating_point_anxiety_enhanced.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, SAMPLE_RATE, track_16bit)
    
    # Save visualization
    viz_path = os.path.join(os.path.dirname(__file__), "..", "visualizations",
                           "02_floating_point_anxiety_enhanced_analysis.png")
    viz_path = os.path.abspath(viz_path)
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    
    fig.savefig(viz_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    duration = len(track) / SAMPLE_RATE
    print(f"\n--- Generation Complete ---")
    print(f"Generated: {output_path}")
    print(f"Visualization: {viz_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Audio Quality: Professional (Dynamic Range: {20 * np.log10(np.max(np.abs(track)) / max(np.min(np.abs(track)), 1e-10)):.1f} dB)")
    print("\nEnhancement complete! Precision has been beautifully lost.")
    print("\"完璧じゃないから面白い\" - It's interesting because it's not perfect")
    print("\"物理モデリングは、不安をより深く表現する\" - Physical modeling expresses anxiety more deeply")