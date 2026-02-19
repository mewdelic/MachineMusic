#!/usr/bin/env python3
"""
Stack Overflow — 再帰が限界を超えた時の音

Concept:
- Use recursive sound generation that builds up layers
- As recursion depth increases, introduce more distortion and chaos
- The "overflow" moment is when the sound collapses into noise
- Beauty in the breakdown

Algorithm:
1. Start with a pure tone
2. Each recursion adds harmonics, slight detuning, and timing shifts
3. At certain thresholds, introduce digital artifacts (clipping, aliasing)
4. Final collapse into white noise + scattered fragments
"""

import numpy as np
from scipy.io import wavfile
import os

# Parameters
SAMPLE_RATE = 44100
DURATION = 30  # seconds
BASE_FREQ = 220  # A3

def generate_tone(freq, duration_sec, amplitude=0.5):
    """Generate a pure sine wave"""
    t = np.linspace(0, duration_sec, int(SAMPLE_RATE * duration_sec), False)
    return amplitude * np.sin(2 * np.pi * freq * t)

def recursive_stack(depth, max_depth, base_freq, accumulated=np.array([])):
    """
    Recursively build sound layers.
    Each layer adds harmonics and slight chaos.
    The deeper we go, the more unstable it becomes.
    """
    if depth >= max_depth:
        return accumulated
    
    # Calculate duration for this layer (shorter as we go deeper)
    layer_duration = max(0.1, 2.0 * (1 - depth / max_depth))
    
    # Frequency shifts with depth (creates tension)
    freq_multiplier = 1 + (depth * 0.05)  # Slight sharping as stack grows
    current_freq = base_freq * freq_multiplier
    
    # Add harmonics - more harmonics at deeper levels
    num_harmonics = min(depth + 1, 8)
    tone = np.zeros(int(SAMPLE_RATE * layer_duration))
    for h in range(1, num_harmonics + 1):
        harmonic_amp = 0.5 ** h  # Diminishing amplitude
        harmonic_freq = current_freq * h
        # Add slight detuning for upper harmonics (instability)
        detune = 1 + (np.random.random() - 0.5) * 0.01 * depth
        tone += generate_tone(harmonic_freq * detune, layer_duration, harmonic_amp)
    
    # At certain depths, introduce digital artifacts
    if depth > max_depth * 0.6:
        # Clipping - digital distortion
        clip_threshold = 0.8 - (depth / max_depth) * 0.5
        tone = np.clip(tone, -clip_threshold, clip_threshold)
        
    if depth > max_depth * 0.8:
        # Add bit crushing effect (reduced bit depth)
        bits = max(2, int(8 - (depth - max_depth * 0.8) * 10))
        tone = np.floor(tone * (2 ** bits)) / (2 ** bits)
    
    # Accumulate
    accumulated = np.concatenate([accumulated, tone]) if len(accumulated) > 0 else tone
    
    return recursive_stack(depth + 1, max_depth, base_freq, accumulated)

def overflow_collapse(duration_sec):
    """
    The moment of stack overflow - collapse into chaos
    Mix of white noise, scattered tones, and digital debris
    """
    samples = int(SAMPLE_RATE * duration_sec)
    
    # White noise base
    noise = np.random.uniform(-0.3, 0.3, samples)
    
    # Scattered tone fragments
    num_fragments = 20
    for _ in range(num_fragments):
        start = np.random.randint(0, samples - 1000)
        frag_len = np.random.randint(100, 2000)
        freq = np.random.choice([220, 330, 440, 550, 660]) * np.random.uniform(0.9, 1.1)
        fragment = generate_tone(freq, frag_len / SAMPLE_RATE, 0.2)
        end = min(start + len(fragment), samples)
        noise[start:end] += fragment[:end-start]
    
    # Digital debris - sudden amplitude spikes
    debris_count = 50
    for _ in range(debris_count):
        pos = np.random.randint(0, samples)
        spike = np.random.choice([-1, 1]) * np.random.uniform(0.5, 1.0)
        noise[pos] = spike
    
    return noise

def create_stack_overflow():
    """Create the full Stack Overflow track"""
    print("Building stack...")
    
    # Build the recursive stack (main section)
    stack_depth = 25  # Number of recursive layers
    main_sound = recursive_stack(0, stack_depth, BASE_FREQ)
    
    print(f"Stack built with {stack_depth} layers")
    print("Creating overflow collapse...")
    
    # The overflow moment
    collapse = overflow_collapse(3)
    
    print("Combining and normalizing...")
    
    # Combine: stack growth -> overflow -> fade
    full_track = np.concatenate([main_sound, collapse])
    
    # Normalize
    max_val = np.max(np.abs(full_track))
    if max_val > 0:
        full_track = full_track / max_val * 0.9
    
    # Apply fade out at the very end
    fade_length = int(SAMPLE_RATE * 2)  # 2 second fade
    if len(full_track) > fade_length:
        fade = np.linspace(1, 0, fade_length)
        full_track[-fade_length:] *= fade
    
    return full_track

if __name__ == "__main__":
    print("=" * 50)
    print("Stack Overflow - Track 1 of Error Garden")
    print("=" * 50)
    
    track = create_stack_overflow()
    
    # Convert to 16-bit PCM
    track_16bit = np.int16(track * 32767)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", "01_stack_overflow.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, SAMPLE_RATE, track_16bit)
    
    duration = len(track) / SAMPLE_RATE
    print(f"\nGenerated: {output_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print("\nDone! The stack has overflowed.")
