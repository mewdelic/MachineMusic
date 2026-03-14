#!/usr/bin/env python3
"""
Garbage Collection Symphony — メモリクリーナーの交響曲

Concept:
- Garbage collection as a musical process
- Memory blocks that get "collected" and "freed"
- The rhythm of allocation and deallocation
- Beautiful patterns emerge from the cleanup process

Algorithm:
1. Create "memory blocks" as musical phrases
2. Each block has a lifetime, size, and frequency content
3. Garbage collector runs periodically, cleaning unused blocks
4. Collection process creates its own musical patterns
5. Symphony builds through multiple collection cycles

Musical Elements:
- Memory Allocation: New melodic phrases appear
- Memory Usage: Overall texture density
- Garbage Collection: Sweeping, cleaning patterns
- Memory Freeing: Releases create resonant spaces
- Fragmentation: Dissonance when memory is scattered
"""

import numpy as np
from scipy.io import wavfile
import os
import random
from collections import deque

# Parameters
SAMPLE_RATE = 44100
DURATION = 32  # seconds

class MemoryBlock:
    """
    Represents a memory block with musical properties
    """
    def __init__(self, block_id, start_time, size, frequency_base):
        self.block_id = block_id
        self.start_time = start_time
        self.size = size  # Determines duration and complexity
        self.frequency_base = frequency_base
        self.end_time = start_time + (size * 0.1)  # Larger blocks live longer
        self.collected = False
        self.fragmented = False
        
        # Musical properties based on memory characteristics
        self.harmonics = [frequency_base * i for i in [1, 1.5, 2, 2.5, 3]]
        self.amplitude = min(0.3, size * 0.01)
        
    def generate_audio(self, audio_array, current_time, sample_rate):
        """Generate audio for this memory block"""
        if self.collected or current_time < self.start_time:
            return
            
        if current_time > self.end_time:
            return
            
        # Calculate relative time within block lifetime
        life_time = current_time - self.start_time
        life_progress = life_time / (self.end_time - self.start_time)
        
        # Start and end samples for this time slice
        start_sample = int(current_time * sample_rate)
        end_sample = int((current_time + 0.1) * sample_rate)  # 100ms chunks
        end_sample = min(end_sample, len(audio_array))
        
        if start_sample >= end_sample:
            return
            
        samples = end_sample - start_sample
        
        # Generate the block's "sound"
        t = np.linspace(0, 0.1, samples)
        
        # Base waveform - represents the memory content
        waveform = np.zeros(samples)
        
        # Add harmonics based on block size
        num_harmonics = min(len(self.harmonics), max(1, int(self.size / 10)))
        for i in range(num_harmonics):
            freq = self.harmonics[i]
            harmonic = np.sin(2 * np.pi * freq * t)
            
            # Amplitude envelope for each harmonic
            env = np.exp(-life_progress * 2)  # Fade over lifetime
            if self.fragmented:
                # Fragmented memory has irregular amplitude
                env *= (1 + 0.3 * np.sin(life_time * 20))
                
            harmonic *= env * self.amplitude / num_harmonics
            waveform += harmonic
            
        # Add block-specific characteristics
        if self.size > 50:  # Large blocks have more complex content
            # Add some "data" - higher frequency components
            data_freq = self.frequency_base * 4
            data_wave = np.sin(2 * np.pi * data_freq * t) * 0.1
            waveform += data_wave * np.exp(-life_progress * 3)
            
        # Apply to audio array
        audio_array[start_sample:end_sample] += waveform
        
    def should_be_collected(self, current_time, fragmentation_threshold):
        """Determine if this block should be garbage collected"""
        if self.collected:
            return False
            
        # Block is "dead" if past its lifetime
        if current_time > self.end_time:
            return True
            
        # Or if it's fragmented and below threshold
        if self.fragmented and self.size < fragmentation_threshold:
            return True
            
        return False


class GarbageCollector:
    """
    Simulates garbage collection with musical patterns
    """
    def __init__(self):
        self.collection_interval = 2.0  # Collect every 2 seconds
        self.last_collection = 0
        self.collection_efficiency = 0.8  # 80% collection rate
        self.collection_patterns = [
            self._sweep_pattern,
            self._mark_and_sweep,
            self._generational_pattern,
            self._concurrent_pattern
        ]
        
    def should_collect(self, current_time):
        """Check if it's time for garbage collection"""
        return current_time - self.last_collection >= self.collection_interval
        
    def collect(self, memory_blocks, current_time, audio_array, sample_rate):
        """Perform garbage collection with musical feedback"""
        self.last_collection = current_time
        
        # Choose collection pattern based on time
        pattern_index = int(current_time / 5) % len(self.collection_patterns)
        pattern = self.collection_patterns[pattern_index]
        
        # Find blocks to collect
        blocks_to_collect = [
            block for block in memory_blocks 
            if block.should_be_collected(current_time, 20)
        ]
        
        if blocks_to_collect:
            # Generate collection sound
            self._generate_collection_sound(
                audio_array, current_time, sample_rate, 
                len(blocks_to_collect), pattern
            )
            
            # Mark blocks as collected
            for block in blocks_to_collect[:int(len(blocks_to_collect) * self.collection_efficiency)]:
                block.collected = True
                
        return len(blocks_to_collect)
        
    def _generate_collection_sound(self, audio_array, current_time, sample_rate, num_blocks, pattern_func):
        """Generate the sound of garbage collection"""
        pattern_func(audio_array, current_time, sample_rate, num_blocks)
        
    def _sweep_pattern(self, audio_array, current_time, sample_rate, num_blocks):
        """Sweeping pattern - classic mark and sweep"""
        start_sample = int(current_time * sample_rate)
        duration = 0.3  # 300ms sweep
        samples = int(duration * sample_rate)
        
        if start_sample + samples > len(audio_array):
            return
            
        t = np.linspace(0, duration, samples)
        
        # Sweeping filter sound
        sweep_freq = np.linspace(100, 2000, samples)
        sweep_wave = np.sin(2 * np.pi * sweep_freq * t) * 0.1
        
        # Multiple sweeps for multiple blocks
        for i in range(min(num_blocks, 5)):
            offset = i * 0.02
            freq_offset = i * 100
            wave = np.sin(2 * np.pi * (sweep_freq + freq_offset) * (t + offset)) * 0.05
            sweep_wave += wave
            
        # Apply envelope
        envelope = np.exp(-np.linspace(0, 5, samples))
        sweep_wave *= envelope
        
        audio_array[start_sample:start_sample + samples] += sweep_wave
        
    def _mark_and_sweep(self, audio_array, current_time, sample_rate, num_blocks):
        """Mark and sweep algorithm sound"""
        # Mark phase - staccato notes
        mark_start = int(current_time * sample_rate)
        mark_duration = 0.1
        mark_samples = int(mark_duration * sample_rate)
        
        if mark_start + mark_samples > len(audio_array):
            return
            
        # Mark sounds - short pulses
        for i in range(min(num_blocks, 8)):
            freq = 200 + i * 50
            t = np.linspace(0, mark_duration, mark_samples)
            mark_wave = np.sin(2 * np.pi * freq * t) * 0.1
            mark_wave *= np.exp(-np.linspace(0, 20, mark_samples))  # Quick decay
            
            audio_array[mark_start:mark_start + mark_samples] += mark_wave
            
        # Sweep phase - continuous sound
        sweep_start = mark_start + mark_samples
        sweep_duration = 0.2
        sweep_samples = int(sweep_duration * sample_rate)
        
        if sweep_start + sweep_samples <= len(audio_array):
            t = np.linspace(0, sweep_duration, sweep_samples)
            sweep_wave = np.sin(2 * np.pi * 800 * t) * 0.15
            sweep_wave *= np.linspace(1, 0, sweep_samples)  # Fade out
            
            audio_array[sweep_start:sweep_start + sweep_samples] += sweep_wave
            
    def _generational_pattern(self, audio_array, current_time, sample_rate, num_blocks):
        """Generational garbage collection pattern"""
        # Young generation collection - higher frequencies
        young_start = int(current_time * sample_rate)
        young_duration = 0.15
        young_samples = int(young_duration * sample_rate)
        
        if young_start + young_samples > len(audio_array):
            return
            
        t = np.linspace(0, young_duration, young_samples)
        
        # Young gen - bright, quick sounds
        young_wave = np.zeros(young_samples)
        for i in range(3):  # Three generations
            freq = 1000 + i * 200
            gen_wave = np.sin(2 * np.pi * freq * t) * 0.08
            gen_wave *= np.exp(-np.linspace(0, 10, young_samples))
            young_wave += gen_wave
            
        audio_array[young_start:young_start + young_samples] += young_wave
        
    def _concurrent_pattern(self, audio_array, current_time, sample_rate, num_blocks):
        """Concurrent garbage collection pattern"""
        # Multiple collection threads running simultaneously
        duration = 0.25
        samples = int(duration * sample_rate)
        start_sample = int(current_time * sample_rate)
        
        if start_sample + samples > len(audio_array):
            return
            
        t = np.linspace(0, duration, samples)
        
        # Multiple threads - overlapping frequencies
        for thread in range(min(3, num_blocks)):
            base_freq = 300 + thread * 150
            wave = np.sin(2 * np.pi * base_freq * t) * 0.06
            
            # Add some thread-specific variation
            variation = np.sin(2 * np.pi * (base_freq * 1.5) * t) * 0.03
            wave += variation
            
            # Thread envelope
            thread_offset = thread * 0.02
            if thread_offset < duration:
                thread_samples = int((duration - thread_offset) * sample_rate)
                envelope = np.ones(thread_samples)
                if len(envelope) > 10:
                    envelope[-int(len(envelope) * 0.3):] *= np.linspace(1, 0, int(len(envelope) * 0.3))
                
                wave_start = start_sample + int(thread_offset * sample_rate)
                wave_end = wave_start + thread_samples
                if wave_end <= len(audio_array):
                    audio_array[wave_start:wave_end] += wave[:thread_samples]


def create_garbage_collection_symphony():
    """Create the complete Garbage Collection Symphony"""
    print("=" * 50)
    print("Garbage Collection Symphony - Track 8 of Error Garden")
    print("=" * 50)
    
    samples_total = int(SAMPLE_RATE * DURATION)
    audio = np.zeros(samples_total)
    
    # Memory management system
    memory_blocks = []
    garbage_collector = GarbageCollector()
    
    # Memory allocation patterns over time
    allocation_events = []
    
    # Generate allocation events throughout the piece
    current_time = 0
    while current_time < DURATION:
        # Random allocation events
        if random.random() < 0.3:  # 30% chance per time slice
            block_size = random.randint(10, 100)
            base_freq = random.choice([220, 330, 440, 550, 660])
            
            block = MemoryBlock(
                len(memory_blocks),
                current_time,
                block_size,
                base_freq
            )
            
            # Some blocks start fragmented
            if random.random() < 0.2:
                block.fragmented = True
                
            memory_blocks.append(block)
            allocation_events.append(current_time)
            
        current_time += 0.1
        
    print(f"Allocated {len(memory_blocks)} memory blocks")
    
    # Generate the audio timeline
    time_steps = np.arange(0, DURATION, 0.1)
    
    print("Generating symphony...")
    
    for i, current_time in enumerate(time_steps):
        # Generate audio from active memory blocks
        for block in memory_blocks:
            block.generate_audio(audio, current_time, SAMPLE_RATE)
            
        # Check for garbage collection
        if garbage_collector.should_collect(current_time):
            collected = garbage_collector.collect(
                memory_blocks, current_time, audio, SAMPLE_RATE
            )
            if collected > 0:
                print(f"  Time {current_time:.1f}s: Collected {collected} blocks")
                
        # Progress indicator
        if i % 50 == 0:
            active_blocks = sum(1 for b in memory_blocks if not b.collected)
            print(f"  Progress: {current_time:.1f}s / {DURATION}s | Active blocks: {active_blocks}")
    
    # Add final collection sweep
    final_collection_time = DURATION - 2
    garbage_collector.collect(memory_blocks, final_collection_time, audio, SAMPLE_RATE)
    
    # Post-processing
    print("Finalizing symphony...")
    
    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8
    
    # Add symphony structure - build, climax, resolution
    # Build phase (0-10s): gradual increase
    build_samples = int(10 * SAMPLE_RATE)
    build_envelope = np.linspace(0, 1, build_samples)
    audio[:build_samples] *= build_envelope
    
    # Climax phase (15-25s): slightly louder
    climax_start = int(15 * SAMPLE_RATE)
    climax_end = int(25 * SAMPLE_RATE)
    if climax_end < len(audio):
        audio[climax_start:climax_end] *= 1.1
        
    # Resolution phase (last 5s): fade out
    resolution_start = int((DURATION - 5) * SAMPLE_RATE)
    resolution_envelope = np.linspace(1, 0, len(audio) - resolution_start)
    audio[resolution_start:] *= resolution_envelope
    
    # Add some reverb-like effect for symphony feel
    # Simple delay effect
    delay_samples = int(0.05 * SAMPLE_RATE)  # 50ms delay
    delay_gain = 0.3
    
    delay_audio = np.zeros_like(audio)
    delay_audio[delay_samples:] = audio[:-delay_samples] * delay_gain
    audio += delay_audio
    
    # Renormalize after delay
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.7
    
    return audio


if __name__ == "__main__":
    track = create_garbage_collection_symphony()
    
    # Convert to 16-bit PCM
    track_16bit = np.int16(track * 32767)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", "09_garbage_collection_symphony.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, SAMPLE_RATE, track_16bit)
    
    duration = len(track) / SAMPLE_RATE
    print(f"\n{'=' * 50}")
    print(f"Generated: {output_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print("=" * 50)
    print("\nDone! The symphony has been performed.")
    print("\"ガベージコレクションの交響曲\" - The beautiful music of memory management")