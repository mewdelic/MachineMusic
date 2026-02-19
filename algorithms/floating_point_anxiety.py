#!/usr/bin/env python3
"""
Floating Point Anxiety — 精度が失われる不安

Concept:
- Floating point rounding errors accumulate over time
- Small precision losses grow into noticeable detuning
- The anxiety of knowing you're losing accuracy but can't stop
- Eventually, precision completely breaks down into chaos

Algorithm:
1. Start with precise, clean frequencies
2. Each iteration introduces tiny floating point errors
3. Errors compound exponentially
4. Timing becomes unstable, frequencies drift
5. Final state: complete loss of precision - noise
"""

import numpy as np
from scipy.io import wavfile
import os

# Parameters
SAMPLE_RATE = 44100
DURATION = 30  # seconds
BASE_FREQ = 440.0  # A4 - start perfectly in tune

def accumulate_error(value, iterations=100):
    """
    Intentionally accumulate floating point errors
    by repeatedly adding and subtracting small values
    """
    result = value
    delta = 0.1
    
    for _ in range(iterations):
        result += delta
        result -= delta
    
    # The result should be 'value' but won't be exactly
    error = abs(result - value)
    return result, error

def drifting_frequency(base_freq, duration_sec, drift_rate=0.0001):
    """
    Generate a tone that slowly drifts due to accumulated errors
    The drift accelerates over time
    """
    samples = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, samples, False)
    
    # Frequency drifts due to "accumulated errors"
    # Using float32 to ensure precision loss
    freq = np.float32(base_freq)
    phase = np.float32(0.0)
    
    output = np.zeros(samples, dtype=np.float32)
    
    for i in range(samples):
        # Accumulate error in phase calculation
        phase += 2 * np.pi * freq / SAMPLE_RATE
        
        # Intentionally use imprecise operations
        freq = np.float32(freq * (1.0 + np.float32(drift_rate * (i / samples))))
        
        # Periodically introduce more error
        if i % 1000 == 0:
            freq, _ = accumulate_error(freq, iterations=50)
        
        output[i] = np.float32(np.sin(phase) * 0.3)
    
    return output.astype(np.float64)

def precision_degradation_section(base_freq, duration_sec):
    """
    Multiple oscillators drifting at different rates
    Harmony disintegrates into microtonal chaos
    """
    samples = int(SAMPLE_RATE * duration_sec)
    
    # Start with a chord: A major
    frequencies = [
        base_freq,           # A
        base_freq * 5/4,    # C# (just intonation)
        base_freq * 3/2,    # E
    ]
    
    output = np.zeros(samples)
    
    for i, freq in enumerate(frequencies):
        # Each voice drifts differently
        drift_rate = 0.0001 * (i + 1)
        voice = drifting_frequency(freq, duration_sec, drift_rate)
        output += voice
    
    return output / len(frequencies)

def anxious_tremolo(duration_sec, anxiety_level=0.5):
    """
    Tremolo that becomes more unstable with higher anxiety
    Represents the nervousness of precision loss
    """
    samples = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, samples, False)
    
    # Base tremolo frequency
    trem_freq = 6.0  # Hz
    
    # Add jitter that increases over time
    jitter = np.random.normal(0, anxiety_level, samples)
    jitter = np.convolve(jitter, np.ones(100)/100, mode='same')  # Smooth
    
    # Tremolo frequency becomes unstable
    mod_freq = trem_freq + jitter * 3
    
    # Generate tremolo with unstable frequency
    phase = np.cumsum(2 * np.pi * mod_freq / SAMPLE_RATE)
    tremolo = 0.5 + 0.5 * np.sin(phase)
    
    return tremolo

def catastrophic_precision_loss(duration_sec):
    """
    The moment when precision completely fails
    Frequencies become unrecognizable, timing breaks down
    """
    samples = int(SAMPLE_RATE * duration_sec)
    output = np.zeros(samples)
    
    # Scattered, detuned fragments
    num_fragments = 30
    for i in range(num_fragments):
        # Start position with timing errors
        start = int((i / num_fragments) * samples + np.random.normal(0, samples * 0.05))
        start = max(0, min(start, samples - 1000))
        
        # Fragment length varies wildly
        frag_len = int(np.random.exponential(2000))
        frag_len = min(frag_len, samples - start)
        
        if frag_len <= 0:
            continue
        
        # Frequency is completely wrong now
        base = 440.0
        error_factor = np.random.uniform(0.5, 2.0)
        freq = base * error_factor * (1 + np.random.normal(0, 0.3))
        
        t = np.linspace(0, frag_len / SAMPLE_RATE, frag_len, False)
        
        # Add jitter to the fragment itself
        jittered_freq = freq * (1 + np.random.normal(0, 0.1, frag_len))
        phase = np.cumsum(2 * np.pi * jittered_freq / SAMPLE_RATE)
        
        fragment = np.sin(phase) * 0.15
        
        # Apply envelope
        envelope = np.exp(-np.linspace(0, 3, frag_len))
        fragment *= envelope
        
        output[start:start+frag_len] += fragment
    
    return output

def create_floating_point_anxiety():
    """Create the full Floating Point Anxiety track"""
    print("Phase 1: Precision begins to slip...")
    
    # Phase 1: Gradual drift (0-15 seconds)
    phase1_duration = 15
    phase1 = precision_degradation_section(BASE_FREQ, phase1_duration)
    
    # Add anxious tremolo
    tremolo = anxious_tremolo(phase1_duration, anxiety_level=0.3)
    phase1 *= tremolo
    
    print("Phase 2: Anxiety builds...")
    
    # Phase 2: Accelerating drift (15-25 seconds)
    phase2_duration = 10
    phase2 = precision_degradation_section(BASE_FREQ * 1.01, phase2_duration)  # Already drifted
    tremolo2 = anxious_tremolo(phase2_duration, anxiety_level=0.7)
    phase2 *= tremolo2
    
    # Add more chaotic layer
    phase2_bass = drifting_frequency(BASE_FREQ / 2, phase2_duration, drift_rate=0.0003)
    phase2 += phase2_bass * 0.5
    
    print("Phase 3: Catastrophic precision loss...")
    
    # Phase 3: Complete breakdown (25-30 seconds)
    phase3_duration = 5
    phase3 = catastrophic_precision_loss(phase3_duration)
    
    # Add white noise representing total loss of precision
    noise_duration = 3
    noise_samples = int(SAMPLE_RATE * noise_duration)
    noise = np.random.uniform(-0.2, 0.2, noise_samples)
    
    # Fade in noise at the end
    noise_envelope = np.linspace(0, 1, noise_samples) ** 2
    noise *= noise_envelope
    
    # Overlay noise on the end of phase3
    if len(phase3) > noise_samples:
        phase3[-noise_samples:] += noise
    else:
        phase3 = phase3 * 0.5 + noise[:len(phase3)] * 0.5
    
    print("Assembling track...")
    
    # Combine all phases
    full_track = np.concatenate([phase1, phase2, phase3])
    
    # Normalize
    max_val = np.max(np.abs(full_track))
    if max_val > 0:
        full_track = full_track / max_val * 0.85
    
    # Apply subtle fade out at the very end
    fade_length = int(SAMPLE_RATE * 1.5)
    if len(full_track) > fade_length:
        fade = np.linspace(1, 0, fade_length) ** 2  # Exponential fade
        full_track[-fade_length:] *= fade
    
    return full_track

def demonstrate_error():
    """Show the floating point error accumulation"""
    print("\n--- Floating Point Error Demonstration ---")
    
    test_value = 1.0
    result, error = accumulate_error(test_value, iterations=1000)
    print(f"Start: {test_value}")
    print(f"After 1000 +/- 0.1 operations: {result}")
    print(f"Error: {error}")
    print(f"Relative error: {error/test_value * 100:.10f}%")
    
    # Show frequency drift
    print("\n--- Frequency Drift ---")
    freq = 440.0
    for i in range(5):
        drifted, _ = accumulate_error(freq, iterations=100 * (i + 1))
        cents_off = 1200 * np.log2(drifted / freq)
        print(f"Iterations {100 * (i+1)}: {drifted:.6f} Hz ({cents_off:.2f} cents from A440)")
    
    print()

if __name__ == "__main__":
    print("=" * 50)
    print("Floating Point Anxiety - Track 2 of Error Garden")
    print("=" * 50)
    
    # Show the concept
    demonstrate_error()
    
    track = create_floating_point_anxiety()
    
    # Convert to 16-bit PCM
    track_16bit = np.int16(track * 32767)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", "02_floating_point_anxiety.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, SAMPLE_RATE, track_16bit)
    
    duration = len(track) / SAMPLE_RATE
    print(f"\nGenerated: {output_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print("\nDone! Precision has been lost.")
    print("\"完璧じゃないから面白い\" - It's interesting because it's not perfect")
