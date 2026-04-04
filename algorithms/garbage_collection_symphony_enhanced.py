#!/usr/bin/env python3
"""
Garbage Collection Symphony Enhanced — メモリクリーナーの交響曲（物理モデリング版）

Concept:
- Physical modeling of memory allocation and collection processes
- Garbage collection as resonant acoustic phenomena
- Memory blocks as physical objects with mass, tension, and resonance
- Collection processes as wave interference and damping

Enhanced Features:
- Physical modeling synthesis for memory blocks
- Realistic resonance and damping effects
- Spatial positioning of memory processes
- Advanced collection algorithms with acoustic feedback
- Multi-layered texture representing memory hierarchy

Musical Elements:
- Memory Allocation: Resonant objects appearing in space
- Memory Usage: Harmonic complexity and density
- Garbage Collection: Wave propagation and interference
- Memory Freeing: Damping and resonance decay
- Fragmentation: Dissonance and beating effects
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import os
import random
from collections import deque

# Parameters
SAMPLE_RATE = 44100
DURATION = 40  # Extended duration for enhanced version

class PhysicalMemoryBlock:
    """
    Represents a memory block as a physical resonant object
    """
    def __init__(self, block_id, start_time, size, frequency_base):
        self.block_id = block_id
        self.start_time = start_time
        self.size = size
        self.frequency_base = frequency_base
        self.end_time = start_time + (size * 0.15)  # Longer lifetime for physical objects
        self.collected = False
        self.fragmented = False
        
        # Physical properties
        self.mass = size * 0.1  # Mass affects resonance
        self.tension = frequency_base * 0.01  # String tension
        self.damping = 0.5 + (size * 0.005)  # Damping coefficient
        self.position = random.uniform(-1, 1)  # Spatial position (-1 to 1)
        
        # Resonance modes (harmonics)
        self.resonance_modes = []
        num_modes = min(6, max(2, int(size / 15)))
        for i in range(num_modes):
            mode_freq = frequency_base * (i + 1)
            mode_amplitude = 1.0 / (i + 1)  # Amplitude decreases with mode
            mode_phase = random.uniform(0, 2 * np.pi)
            self.resonance_modes.append({
                'frequency': mode_freq,
                'amplitude': mode_amplitude,
                'phase': mode_phase,
                'q_factor': 10 + (i * 5)  # Quality factor
            })
        
        # Spatial properties
        self.reverb_time = 0.5 + (size * 0.01)  # Reverb time based on size
        self.spatial_width = min(1.0, size * 0.02)  # Spatial spread
        
    def generate_physical_audio(self, audio_array, current_time, sample_rate):
        """Generate audio using physical modeling synthesis"""
        if self.collected or current_time < self.start_time:
            return
            
        if current_time > self.end_time:
            return
            
        # Calculate lifetime progress
        life_time = current_time - self.start_time
        life_progress = life_time / (self.end_time - self.start_time)
        
        # Time slice parameters
        start_sample = int(current_time * sample_rate)
        end_sample = int((current_time + 0.05) * sample_rate)  # 50ms chunks
        end_sample = min(end_sample, len(audio_array))
        
        if start_sample >= end_sample:
            return
            
        samples = end_sample - start_sample
        t = np.linspace(0, 0.05, samples)
        
        # Generate physical model sound
        waveform = self._generate_physical_waveform(t, life_time, life_progress)
        
        # Apply spatial positioning
        waveform = self._apply_spatialization(waveform)
        
        # Apply damping over lifetime
        damping_envelope = np.exp(-life_progress * self.damping)
        if self.fragmented:
            # Fragmented objects have irregular damping
            damping_envelope *= (1 + 0.2 * np.sin(life_time * 15))
        waveform *= damping_envelope
        
        # Apply to audio array with stereo positioning
        self._apply_to_stereo_array(audio_array, waveform, start_sample, samples)
        
    def _generate_physical_waveform(self, t, life_time, life_progress):
        """Generate waveform using physical modeling"""
        waveform = np.zeros_like(t)
        
        # Sum all resonance modes
        for mode in self.resonance_modes:
            freq = mode['frequency']
            amp = mode['amplitude']
            phase = mode['phase']
            q = mode['q_factor']
            
            # Calculate resonance with damping
            omega = 2 * np.pi * freq
            damping_coeff = omega / (2 * q)
            
            # Damped oscillation
            mode_wave = np.sin(omega * t + phase) * np.exp(-damping_coeff * t)
            
            # Add frequency modulation based on mass and tension
            if self.mass > 5:
                freq_mod = np.sin(2 * np.pi * 0.5 * t) * (self.mass * 0.1)
                modulated_freq = freq * (1 + freq_mod)
                mod_wave = np.sin(2 * np.pi * modulated_freq * t + phase)
                mode_wave = 0.7 * mode_wave + 0.3 * mod_wave
            
            # Amplitude envelope for this mode
            env = amp * np.exp(-t * 2)  # Quick attack, slow decay
            if life_progress > 0.7:
                # Fade out near end of life
                env *= np.exp(-(life_progress - 0.7) * 10)
            
            waveform += mode_wave * env
            
        # Add noise component for realism
        if self.size > 30:
            noise_level = 0.02 * (self.size / 100)
            noise = np.random.normal(0, noise_level, len(t))
            waveform += noise * np.exp(-t * 5)
            
        # Normalize
        max_val = np.max(np.abs(waveform))
        if max_val > 0:
            waveform = waveform / max_val
            
        return waveform
        
    def _apply_spatialization(self, waveform):
        """Apply spatial positioning to the waveform"""
        # Simple stereo panning based on position
        pan = (self.position + 1) / 2  # Convert -1..1 to 0..1
        
        # Calculate pan gains (constant power panning)
        left_gain = np.sqrt(1 - pan)
        right_gain = np.sqrt(pan)
        
        # Convert mono to stereo
        stereo_wave = np.zeros((len(waveform), 2))
        stereo_wave[:, 0] = waveform * left_gain
        stereo_wave[:, 1] = waveform * right_gain
        
        return stereo_wave
        
    def _apply_to_stereo_array(self, audio_array, waveform, start_sample, samples):
        """Apply stereo waveform to audio array"""
        if len(waveform.shape) == 1:
            # Convert to stereo
            stereo_wave = np.zeros((samples, 2))
            stereo_wave[:, 0] = waveform
            stereo_wave[:, 1] = waveform
            waveform = stereo_wave
            
        # Ensure we don't exceed array bounds
        end_sample = min(start_sample + samples, audio_array.shape[0])
        actual_samples = end_sample - start_sample
        
        if actual_samples > 0:
            audio_array[start_sample:end_sample, :] += waveform[:actual_samples, :]
        
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


class EnhancedGarbageCollector:
    """
    Enhanced garbage collector with physical modeling and spatial processing
    """
    def __init__(self):
        self.collection_interval = 2.5  # Slightly longer interval
        self.last_collection = 0
        self.collection_efficiency = 0.85  # Slightly better efficiency
        self.collection_patterns = [
            self._physical_sweep_pattern,
            self._resonant_mark_sweep,
            self._wave_interference_pattern,
            self._spatial_collection_pattern
        ]
        
        # Physical properties of collection
        self.wave_speed = 343.0  # Speed of sound in air (m/s)
        self.collection_radius = 2.0  # Collection radius in meters
        
    def should_collect(self, current_time):
        """Check if it's time for garbage collection"""
        return current_time - self.last_collection >= self.collection_interval
        
    def collect(self, memory_blocks, current_time, audio_array, sample_rate):
        """Perform enhanced garbage collection"""
        self.last_collection = current_time
        
        # Choose collection pattern based on memory state
        memory_pressure = len([b for b in memory_blocks if not b.collected]) / len(memory_blocks)
        pattern_index = int((current_time / 8) * memory_pressure) % len(self.collection_patterns)
        pattern = self.collection_patterns[pattern_index]
        
        # Find blocks to collect based on proximity and pressure
        blocks_to_collect = self._find_blocks_to_collect(memory_blocks, current_time, memory_pressure)
        
        if blocks_to_collect:
            # Generate enhanced collection sound
            pattern(audio_array, current_time, sample_rate, blocks_to_collect)
            
            # Mark blocks as collected with spatial considerations
            collected_count = 0
            for block in blocks_to_collect:
                if collected_count < int(len(blocks_to_collect) * self.collection_efficiency):
                    if not block.collected:
                        block.collected = True
                        collected_count += 1
                        
        return len(blocks_to_collect)
        
    def _find_blocks_to_collect(self, memory_blocks, current_time, memory_pressure):
        """Find blocks that should be collected based on various criteria"""
        blocks_to_collect = []
        
        # Adjust fragmentation threshold based on memory pressure
        fragmentation_threshold = 30 * (1 - memory_pressure * 0.5)
        
        for block in memory_blocks:
            if block.should_be_collected(current_time, fragmentation_threshold):
                # Consider spatial clustering
                if self._is_in_collection_cluster(block, memory_blocks, current_time):
                    blocks_to_collect.append(block)
                    
        # Sort by collection priority
        blocks_to_collect.sort(key=lambda b: (
            b.end_time < current_time,  # Dead blocks first
            b.fragmented,  # Fragmented blocks next
            b.size  # Smaller blocks first
        ), reverse=True)
        
        return blocks_to_collect[:20]  # Limit collection per cycle
        
    def _is_in_collection_cluster(self, target_block, memory_blocks, current_time):
        """Check if block is in a spatial cluster that should be collected together"""
        cluster_radius = 0.5  # 0.5 spatial units
        cluster_count = 0
        
        for block in memory_blocks:
            if (block != target_block and 
                not block.collected and 
                abs(block.position - target_block.position) < cluster_radius):
                cluster_count += 1
                
        # Collect if in cluster of at least 2 other blocks
        return cluster_count >= 2
        
    def _physical_sweep_pattern(self, audio_array, current_time, sample_rate, blocks):
        """Physical wave propagation during collection"""
        start_sample = int(current_time * sample_rate)
        duration = 0.4  # Longer sweep
        samples = int(duration * sample_rate)
        
        if start_sample + samples > audio_array.shape[0]:
            return
            
        t = np.linspace(0, duration, samples)
        
        # Generate wave propagation sound
        sweep_wave = np.zeros((samples, 2))
        
        # Multiple wave sources based on block positions
        for i, block in enumerate(blocks[:5]):
            # Calculate wave arrival time based on position
            delay = abs(block.position) * 0.1
            delay_samples = int(delay * sample_rate)
            
            if delay_samples < samples:
                # Generate wave for this source
                freq = 200 + i * 100
                wave_t = t[delay_samples:] - delay
                if len(wave_t) > 0:
                    wave = np.sin(2 * np.pi * freq * wave_t) * 0.1
                    
                    # Apply distance attenuation
                    distance = abs(block.position)
                    attenuation = 1.0 / (1.0 + distance)
                    wave *= attenuation
                    
                    # Add to stereo with position
                    pan = (block.position + 1) / 2
                    left_gain = np.sqrt(1 - pan)
                    right_gain = np.sqrt(pan)
                    
                    wave_len = len(wave)
                    end_idx = delay_samples + wave_len
                    if end_idx <= samples:
                        sweep_wave[delay_samples:end_idx, 0] += wave * left_gain
                        sweep_wave[delay_samples:end_idx, 1] += wave * right_gain
        
        # Apply global envelope
        envelope = np.exp(-np.linspace(0, 8, samples))
        sweep_wave *= envelope[:, np.newaxis]
        
        # Apply to audio array
        end_sample = start_sample + samples
        if end_sample <= audio_array.shape[0]:
            audio_array[start_sample:end_sample, :] += sweep_wave
            
    def _resonant_mark_sweep(self, audio_array, current_time, sample_rate, blocks):
        """Resonant marking and sweeping with physical feedback"""
        # Mark phase - resonant impulses
        mark_start = int(current_time * sample_rate)
        mark_duration = 0.15
        mark_samples = int(mark_duration * sample_rate)
        
        if mark_start + mark_samples > audio_array.shape[0]:
            return
            
        # Create resonant mark sounds
        mark_wave = np.zeros((mark_samples, 2))
        
        for i, block in enumerate(blocks[:8]):
            freq = 300 + block.frequency_base * 0.5
            t = np.linspace(0, mark_duration, mark_samples)
            
            # Resonant impulse
            impulse = np.exp(-t * 30) * np.sin(2 * np.pi * freq * t)
            
            # Add block's resonance
            for mode in block.resonance_modes[:2]:
                mode_freq = mode['frequency'] * 0.5
                resonance = np.sin(2 * np.pi * mode_freq * t) * 0.3
                impulse += resonance * np.exp(-t * 20)
            
            # Normalize and apply
            impulse = impulse / np.max(np.abs(impulse)) * 0.08
            
            # Spatial positioning
            pan = (block.position + 1) / 2
            left_gain = np.sqrt(1 - pan)
            right_gain = np.sqrt(pan)
            
            mark_wave[:, 0] += impulse * left_gain
            mark_wave[:, 1] += impulse * right_gain
        
        # Sweep phase - resonant sweep
        sweep_start = mark_start + mark_samples
        sweep_duration = 0.3
        sweep_samples = int(sweep_duration * sample_rate)
        
        if sweep_start + sweep_samples <= audio_array.shape[0]:
            t = np.linspace(0, sweep_duration, sweep_samples)
            
            # Create sweeping resonator
            sweep_freq = np.linspace(400, 1200, sweep_samples)
            sweep_wave = np.sin(2 * np.pi * sweep_freq * t) * 0.12
            
            # Add resonance peaks
            for peak_freq in [600, 800, 1000]:
                resonance = np.exp(-((sweep_freq - peak_freq) ** 2) / (2 * 50 ** 2))
                sweep_wave *= (1 + resonance * 0.3)
            
            # Envelope
            envelope = np.linspace(1, 0, sweep_samples)
            sweep_wave *= envelope
            
            # Apply as stereo
            stereo_sweep = np.zeros((sweep_samples, 2))
            stereo_sweep[:, 0] = sweep_wave
            stereo_sweep[:, 1] = sweep_wave
            
            audio_array[sweep_start:sweep_start + sweep_samples, :] += stereo_sweep
        
        # Apply mark phase
        audio_array[mark_start:mark_start + mark_samples, :] += mark_wave
        
    def _wave_interference_pattern(self, audio_array, current_time, sample_rate, blocks):
        """Collection using wave interference patterns"""
        duration = 0.5
        samples = int(duration * sample_rate)
        start_sample = int(current_time * sample_rate)
        
        if start_sample + samples > audio_array.shape[0]:
            return
            
        t = np.linspace(0, duration, samples)
        interference_wave = np.zeros((samples, 2))
        
        # Create interference pattern from multiple sources
        for i, block in enumerate(blocks[:6]):
            # Primary wave
            freq1 = 250 + i * 50
            wave1 = np.sin(2 * np.pi * freq1 * t) * 0.06
            
            # Secondary wave (slightly different frequency for beating)
            freq2 = freq1 + 2  # 2Hz difference for beating
            wave2 = np.sin(2 * np.pi * freq2 * t) * 0.06
            
            # Interference
            interference = wave1 + wave2
            
            # Modulate with block properties
            modulation_freq = block.size * 0.1
            modulation = np.sin(2 * np.pi * modulation_freq * t) * 0.3
            interference *= (1 + modulation)
            
            # Spatial positioning
            pan = (block.position + 1) / 2
            left_gain = np.sqrt(1 - pan)
            right_gain = np.sqrt(pan)
            
            # Apply with delay based on position
            delay = int(abs(block.position) * 0.05 * sample_rate)
            end_delay = delay + len(interference)
            
            if end_delay <= samples:
                interference_wave[delay:end_delay, 0] += interference * left_gain
                interference_wave[delay:end_delay, 1] += interference * right_gain
        
        # Apply global envelope
        envelope = np.exp(-np.linspace(0, 6, samples))
        interference_wave *= envelope[:, np.newaxis]
        
        # Add to audio
        audio_array[start_sample:start_sample + samples, :] += interference_wave
        
    def _spatial_collection_pattern(self, audio_array, current_time, sample_rate, blocks):
        """Spatial garbage collection with 3D positioning"""
        duration = 0.6
        samples = int(duration * sample_rate)
        start_sample = int(current_time * sample_rate)
        
        if start_sample + samples > audio_array.shape[0]:
            return
            
        t = np.linspace(0, duration, samples)
        spatial_wave = np.zeros((samples, 2))
        
        # Group blocks by spatial regions
        left_blocks = [b for b in blocks if b.position < -0.3]
        center_blocks = [b for b in blocks if -0.3 <= b.position <= 0.3]
        right_blocks = [b for b in blocks if b.position > 0.3]
        
        # Process each spatial region
        regions = [
            (left_blocks, -0.8, 200),
            (center_blocks, 0.0, 300),
            (right_blocks, 0.8, 400)
        ]
        
        for region_blocks, region_pos, base_freq in regions:
            if not region_blocks:
                continue
                
            # Create region-specific sound
            region_wave = np.zeros(samples)
            
            for block in region_blocks[:3]:
                # Distance from region center
                distance = abs(block.position - region_pos)
                attenuation = np.exp(-distance * 2)
                
                # Block-specific frequency
                block_freq = base_freq + block.size * 2
                block_wave = np.sin(2 * np.pi * block_freq * t) * 0.05 * attenuation
                
                # Add resonance
                resonance_freq = block_freq * 1.5
                resonance = np.sin(2 * np.pi * resonance_freq * t) * 0.02
                block_wave += resonance
                
                region_wave += block_wave
            
            # Spatial positioning for this region
            if region_pos < 0:
                # Left region
                spatial_wave[:, 0] += region_wave * 0.8
                spatial_wave[:, 1] += region_wave * 0.4
            elif region_pos > 0:
                # Right region
                spatial_wave[:, 0] += region_wave * 0.4
                spatial_wave[:, 1] += region_wave * 0.8
            else:
                # Center region
                spatial_wave[:, 0] += region_wave * 0.6
                spatial_wave[:, 1] += region_wave * 0.6
        
        # Apply spatial master envelope
        master_envelope = np.ones(samples)
        master_envelope[-int(samples * 0.3):] *= np.linspace(1, 0, int(samples * 0.3))
        spatial_wave *= master_envelope[:, np.newaxis]
        
        # Add to audio
        audio_array[start_sample:start_sample + samples, :] += spatial_wave


def create_enhanced_garbage_collection_symphony():
    """Create the enhanced Garbage Collection Symphony with physical modeling"""
    print("=" * 60)
    print("Garbage Collection Symphony ENHANCED - Physical Modeling Edition")
    print("=" * 60)
    
    samples_total = int(SAMPLE_RATE * DURATION)
    # Create stereo audio array
    audio = np.zeros((samples_total, 2))
    
    # Enhanced memory management system
    memory_blocks = []
    garbage_collector = EnhancedGarbageCollector()
    
    # Enhanced allocation patterns with spatial distribution
    allocation_events = []
    
    # Generate allocation events with spatial considerations
    current_time = 0
    allocation_rate = 0.4  # 40% chance per time slice
    
    while current_time < DURATION:
        # Dynamic allocation rate based on time
        time_factor = 1 + 0.5 * np.sin(current_time * 0.1)
        if random.random() < allocation_rate * time_factor:
            block_size = random.randint(15, 120)
            base_freq = random.choice([220, 330, 440, 550, 660, 880])
            
            block = PhysicalMemoryBlock(
                len(memory_blocks),
                current_time,
                block_size,
                base_freq
            )
            
            # Spatial clustering - blocks tend to appear near existing ones
            if memory_blocks and random.random() < 0.6:
                # Choose a random existing block and place near it
                reference_block = random.choice(memory_blocks)
                position_offset = random.gauss(0, 0.3)  # Gaussian distribution
                block.position = np.clip(reference_block.position + position_offset, -1, 1)
            
            # Fragmentation probability based on memory pressure
            memory_pressure = len(memory_blocks) / 100.0
            if random.random() < 0.15 + memory_pressure * 0.1:
                block.fragmented = True
                
            memory_blocks.append(block)
            allocation_events.append(current_time)
            
        current_time += 0.08  # Slightly finer time resolution
        
    print(f"Allocated {len(memory_blocks)} physical memory blocks")
    
    # Generate the enhanced audio timeline
    time_steps = np.arange(0, DURATION, 0.08)
    
    print("Generating enhanced symphony with physical modeling...")
    
    collection_count = 0
    for i, current_time in enumerate(time_steps):
        # Generate audio from active memory blocks
        for block in memory_blocks:
            block.generate_physical_audio(audio, current_time, SAMPLE_RATE)
            
        # Check for enhanced garbage collection
        if garbage_collector.should_collect(current_time):
            collected = garbage_collector.collect(
                memory_blocks, current_time, audio, SAMPLE_RATE
            )
            if collected > 0:
                collection_count += 1
                print(f"  Collection {collection_count} at {current_time:.1f}s: {collected} blocks")
                
        # Progress indicator
        if i % 100 == 0:
            active_blocks = sum(1 for b in memory_blocks if not b.collected)
            print(f"  Progress: {current_time:.1f}s / {DURATION}s | Active: {active_blocks}")
    
    # Final comprehensive collection
    final_collection_time = DURATION - 3
    garbage_collector.collect(memory_blocks, final_collection_time, audio, SAMPLE_RATE)
    
    # Enhanced post-processing
    print("Applying enhanced mastering...")
    
    # Normalize per channel
    for channel in range(2):
        max_val = np.max(np.abs(audio[:, channel]))
        if max_val > 0:
            audio[:, channel] = audio[:, channel] / max_val * 0.7
    
    # Apply symphonic structure
    # Introduction (0-8s): gentle build
    intro_samples = int(8 * SAMPLE_RATE)
    intro_envelope = np.linspace(0, 1, intro_samples)
    audio[:intro_samples, 0] *= intro_envelope
    audio[:intro_samples, 1] *= intro_envelope
    
    # Main development (8-28s): full expression
    dev_start = int(8 * SAMPLE_RATE)
    dev_end = int(28 * SAMPLE_RATE)
    if dev_end < len(audio):
        # Slight compression effect in development section
        audio[dev_start:dev_end, :] *= 1.05
    
    # Climax (28-35s): intense collection activity
    climax_start = int(28 * SAMPLE_RATE)
    climax_end = int(35 * SAMPLE_RATE)
    if climax_end < len(audio):
        # Add excitation for climax
        excitation = 1 + 0.1 * np.sin(np.linspace(0, 4 * np.pi, climax_end - climax_start))
        audio[climax_start:climax_end, 0] *= excitation
        audio[climax_start:climax_end, 1] *= excitation
    
    # Resolution (35s-end): gradual fade
    resolution_start = int((DURATION - 5) * SAMPLE_RATE)
    if resolution_start < len(audio):
        resolution_envelope = np.linspace(1, 0, len(audio) - resolution_start)
        audio[resolution_start:, 0] *= resolution_envelope
        audio[resolution_start:, 1] *= resolution_envelope
    
    # Add professional reverb simulation
    print("Applying spatial reverb...")
    reverb_audio = add_spatial_reverb(audio, SAMPLE_RATE)
    audio = 0.8 * audio + 0.2 * reverb_audio
    
    # Final mastering
    # Gentle high-pass filter to remove DC
    audio = apply_highpass_filter(audio, SAMPLE_RATE, 20)
    
    # Final normalization
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.8
    
    return audio


def add_spatial_reverb(audio, sample_rate):
    """Add spatial reverb to enhance the stereo field"""
    # Simple multi-tap delay reverb
    reverb = np.zeros_like(audio)
    
    # Define delay taps (in samples)
    delay_taps = [
        (0.03, 0.3),   # 30ms, 30% feedback
        (0.05, 0.25),  # 50ms, 25% feedback
        (0.07, 0.2),   # 70ms, 20% feedback
        (0.11, 0.15),  # 110ms, 15% feedback
    ]
    
    for delay_time, feedback in delay_taps:
        delay_samples = int(delay_time * sample_rate)
        
        # Left channel reverb
        if delay_samples < len(audio):
            reverb[delay_samples:, 0] += audio[:-delay_samples, 0] * feedback
        
        # Right channel reverb with cross-feedback
        if delay_samples < len(audio):
            reverb[delay_samples:, 1] += audio[:-delay_samples, 1] * feedback
            # Add some cross-feedback
            reverb[delay_samples:, 0] += audio[:-delay_samples, 1] * feedback * 0.3
            reverb[delay_samples:, 1] += audio[:-delay_samples, 0] * feedback * 0.3
    
    # Apply low-pass filter to reverb (darker reverb tail)
    reverb = apply_lowpass_filter(reverb, sample_rate, 4000)
    
    return reverb


def butter_lowpass(cutoff, fs, order=5):
    """Design Butterworth low-pass filter"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_highpass(cutoff, fs, order=5):
    """Design Butterworth high-pass filter"""
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a


def apply_lowpass_filter(audio, sample_rate, cutoff_freq):
    """Apply low-pass filter to audio"""
    b, a = butter_lowpass(cutoff_freq, sample_rate)
    filtered_audio = np.zeros_like(audio)
    for channel in range(audio.shape[1]):
        filtered_audio[:, channel] = lfilter(b, a, audio[:, channel])
    return filtered_audio


def apply_highpass_filter(audio, sample_rate, cutoff_freq):
    """Apply high-pass filter to audio"""
    b, a = butter_highpass(cutoff_freq, sample_rate)
    filtered_audio = np.zeros_like(audio)
    for channel in range(audio.shape[1]):
        filtered_audio[:, channel] = lfilter(b, a, audio[:, channel])
    return filtered_audio


if __name__ == "__main__":
    track = create_enhanced_garbage_collection_symphony()
    
    # Convert to 16-bit PCM
    track_16bit = np.int16(track * 32767)
    
    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "samples", "09_garbage_collection_symphony_enhanced.wav")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    wavfile.write(output_path, SAMPLE_RATE, track_16bit)
    
    duration = len(track) / SAMPLE_RATE
    print(f"\n{'=' * 60}")
    print(f"Generated: {output_path}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Sample rate: {SAMPLE_RATE} Hz")
    print(f"Channels: Stereo (2)")
    print(f"Physical modeling: Enabled")
    print(f"Spatial processing: Enabled")
    print(f"Advanced collection algorithms: 4 patterns")
    print("=" * 60)
    print("\nEnhanced Symphony Complete!")
    print("\"物理モデリングによるガベージコレクションの交響曲\"")
    print("The beautiful physics of memory management made audible")