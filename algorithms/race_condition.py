#!/usr/bin/env python3
"""
Race Condition — 競合が生む偶然のハーモニー

Concept:
- Multiple independent "threads" of sound running concurrently
- They compete for shared resources (amplitude, frequency bands, timing)
- When multiple threads access the same resource, unpredictable artifacts occur
- The beauty is in the collision - harmonies that shouldn't exist but do

Algorithm:
1. Spawn multiple sound threads with different patterns
2. Each thread has its own timing, but they drift
3. When threads collide in frequency/amplitude space, create interference
4. Critical sections produce sudden changes
5. Deadlock moments create sustained tension
"""

import numpy as np
from scipy.io import wavfile
import os
from threading import Lock
import time

# Parameters
SAMPLE_RATE = 44100
DURATION = 35  # seconds

class SoundThread:
    """
    Represents a concurrent sound-generating thread
    Each has its own frequency, pattern, and timing
    """
    def __init__(self, thread_id, base_freq, pattern_type):
        self.thread_id = thread_id
        self.base_freq = base_freq
        self.pattern_type = pattern_type
        self.phase = 0.0
        self.amplitude = 0.3
        self.timing_drift = np.random.uniform(-0.1, 0.1)
        self.active = True
        
    def generate_chunk(self, samples, global_time, shared_state):
        """Generate a chunk of sound, competing for shared resources"""
        output = np.zeros(samples)
        
        if not self.active:
            return output
            
        # Timing instability - threads drift
        local_time = global_time + self.timing_drift * np.sin(global_time * 0.5)
        
        for i in range(samples):
            t = local_time + i / SAMPLE_RATE
            
            # Check if we're in a "critical section" (collision zone)
            in_critical = False
            
            # Pattern-specific generation
            if self.pattern_type == "pulse":
                freq = self.base_freq
                # Pulse pattern with jitter
                period = SAMPLE_RATE * 0.25
                if int(t * SAMPLE_RATE) % int(period) < int(period * 0.3):
                    val = np.sin(self.phase) * self.amplitude
                else:
                    val = 0
                    
            elif self.pattern_type == "wave":
                freq = self.base_freq * (1 + 0.02 * np.sin(t * 2))
                val = np.sin(self.phase) * self.amplitude * 0.7
                
            elif self.pattern_type == "drift":
                freq = self.base_freq * (1 + self.timing_drift * t * 0.01)
                val = np.sin(self.phase) * self.amplitude * 0.5
                
            else:  # random
                freq = self.base_freq * np.random.uniform(0.98, 1.02)
                val = np.sin(self.phase) * self.amplitude * 0.6
            
            # Update phase
            self.phase += 2 * np.pi * freq / SAMPLE_RATE
            
            # Check for collision with shared state
            freq_band = int(freq / 100)  # Which frequency band
            if freq_band in shared_state['occupied_bands']:
                # COLLISION! Race condition effect
                in_critical = True
                shared_state['collision_count'] += 1
                
                # Random interference - the sound of two threads colliding
                interference = shared_state['interference_factor']
                val *= (1 + interference * np.random.uniform(-0.5, 0.5))
                
                # Sometimes create harmonics from collision
                if np.random.random() < 0.1:
                    val += np.sin(self.phase * 2) * self.amplitude * 0.3
            else:
                # Occupy this band
                shared_state['occupied_bands'][freq_band] = self.thread_id
            
            # Amplitude competition - threads fight for headroom
            total_amplitude = shared_state['current_amplitude']
            if total_amplitude + abs(val) > shared_state['max_amplitude']:
                # Resource contention - reduce amplitude
                val *= shared_state['max_amplitude'] / (total_amplitude + 0.001)
                shared_state['contention_events'] += 1
            
            shared_state['current_amplitude'] = total_amplitude + abs(val)
            
            output[i] = val
            
        # Clean up occupied bands periodically
        if np.random.random() < 0.1:
            shared_state['occupied_bands'].clear()
            
        return output


def create_race_condition():
    """Create the full Race Condition track"""
    print("Initializing threads...")
    
    # Create multiple competing threads
    threads = [
        SoundThread(0, 220.0, "pulse"),     # A3 - steady pulse
        SoundThread(1, 330.0, "wave"),      # E4 - wave pattern
        SoundThread(2, 440.0, "drift"),     # A4 - drifting
        SoundThread(3, 550.0, "random"),    # C#5 - random
        SoundThread(4, 165.0, "pulse"),     # E3 - bass pulse
        SoundThread(5, 660.0, "wave"),      # E5 - high wave
    ]
    
    # Shared state that threads compete for
    shared_state = {
        'occupied_bands': {},
        'current_amplitude': 0.0,
        'max_amplitude': 0.8,
        'collision_count': 0,
        'contention_events': 0,
        'interference_factor': 0.0
    }
    
    samples_total = int(SAMPLE_RATE * DURATION)
    output = np.zeros(samples_total)
    
    # Generate in chunks to simulate concurrent execution
    chunk_size = 4410  # 0.1 second chunks
    
    print("Running race conditions...")
    
    for chunk_start in range(0, samples_total, chunk_size):
        chunk_end = min(chunk_start + chunk_size, samples_total)
        actual_chunk_size = chunk_end - chunk_start
        global_time = chunk_start / SAMPLE_RATE
        
        # Increase interference over time
        shared_state['interference_factor'] = min(1.0, global_time / 20)
        
        # Reset amplitude tracking for this chunk
        shared_state['current_amplitude'] = 0.0
        
        # Generate from each thread (simulated concurrency)
        chunk_mix = np.zeros(actual_chunk_size)
        
        for thread in threads:
            thread_chunk = thread.generate_chunk(actual_chunk_size, global_time, shared_state)
            chunk_mix += thread_chunk
        
        # Mix into output
        output[chunk_start:chunk_end] = chunk_mix
        
        # Progress indicator
        if chunk_start % (SAMPLE_RATE * 5) < chunk_size:
            print(f"  Progress: {global_time:.1f}s / {DURATION}s | Collisions: {shared_state['collision_count']}")
    
    print(f"\nTotal collisions: {shared_state['collision_count']}")
    print(f"Contention events: {shared_state['contention_events']}")
    
    return output, shared_state


def add_deadlock_section(track, start_time, duration):
    """
    Add a 'deadlock' moment - sustained tension where everything freezes
    This represents threads waiting on each other forever
    """
    start_sample = int(start_time * SAMPLE_RATE)
    samples = int(duration * SAMPLE_RATE)
    
    # Sustained dissonant chord - frozen state
    frequencies = [220, 277, 330, 415, 494]  # Cluster chord
    sustained = np.zeros(samples)
    
    for freq in frequencies:
        t = np.linspace(0, duration, samples, False)
        # Slight beating between frequencies
        beat = np.sin(2 * np.pi * (freq + np.random.uniform(-1, 1)) * t)
        sustained += beat * 0.15
    
    # Add tension through slow amplitude modulation
    mod = np.sin(np.linspace(0, np.pi * 2, samples)) * 0.3 + 0.7
    sustained *= mod
    
    # Blend into track
    end_sample = min(start_sample + samples, len(track))
    actual_samples = end_sample - start_sample
    track[start_sample:end_sample] += sustained[:actual_samples]
    
    return track


def add_mutex_release(track, time, duration=0.5):
    """
    The moment of 'mutex release' - sudden burst of activity
    All waiting threads rush in at once
    """
    start_sample = int(time * SAMPLE_RATE)
    samples = int(duration * SAMPLE_RATE)
    
    burst = np.zeros(samples)
    
    # Multiple frequencies burst in
    for _ in range(8):
        freq = np.random.choice([220, 330, 440, 550, 660]) * np.random.uniform(0.9, 1.1)
        t = np.linspace(0, duration, samples, False)
        tone = np.sin(2 * np.pi * freq * t) * np.random.uniform(0.1, 0.2)
        
        # Sharp attack, quick decay
        envelope = np.exp(-np.linspace(0, 8, samples))
        tone *= envelope
        
        burst += tone
    
    end_sample = min(start_sample + samples, len(track))
    actual_samples = end_sample - start_sample
    track[start_sample:end_sample] += burst[:actual_samples]
    
    return track


def create_race_condition_full():
    """Create complete track with all sections"""
    print("=" * 50)
    print("Race Condition - Track 4 of Error Garden")
    print("=" * 50)
    
    # Generate base race condition
    track, state = create_race_condition()
    
    print("\nAdding deadlock moments...")
    
    # Add deadlock section around 15 seconds
    track = add_deadlock_section(track, 15, 2)
    
    # Add mutex release after deadlock
    track = add_mutex_release(track, 17, 0.3)
    
    # Another deadlock near the end
    track = add_deadlock_section(track, 28, 3)
    
    print("Finalizing track...")
    
    # Normalize
    max_val = np.max(np.abs(track))
    if max_val > 0:
        track = track / max_val * 0.85
    
    # Fade in (first 2 seconds)
    fade_in = int(SAMPLE_RATE * 2)
    track[:fade_in] *= np.linspace(0, 1, fade_in)
    
    # Fade out (last 3 seconds)
    fade_out = int(SAMPLE_RATE * 3)
    track[-fade_out:] *= np.linspace(1, 0, fade_out)
    
    return track


if __name__ == "__main__":
    track = create_race_condition_full()
    
    # Convert to 16-bit PCM
    track_16bit = np.int16(track * 32767)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", "04_race_condition.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, SAMPLE_RATE, track_16bit)
    
    duration = len(track) / SAMPLE_RATE
    print(f"\n{'=' * 50}")
    print(f"Generated: {output_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print("=" * 50)
    print("\nDone! The threads have raced.")
    print("\"競合が生む偶然のハーモニー\" - The accidental harmonies of competition")
