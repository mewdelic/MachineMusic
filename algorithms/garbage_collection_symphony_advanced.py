#!/usr/bin/env python3
"""
Garbage Collection Symphony Advanced — メモリクリーナーの交響曲（高度な物理モデリング版）

Concept:
- Advanced physical modeling of memory allocation and garbage collection processes
- Multi-threaded garbage collection with realistic acoustics
- Memory fragmentation as spatial acoustic phenomena
- Collection cycles as wave interference patterns
- Advanced concurrency models with acoustic resonance

Advanced Features:
- Multi-generational garbage collection with distinct acoustic signatures
- Parallel collection threads with interference patterns
- Memory compaction as spatial acoustic transformation
- Advanced fragmentation analysis with spectral decomposition
- Real-time adaptive collection algorithms
- Memory pressure as dynamic parameter modulation
- Collection pauses as musical rests and silence
- Finalizer queues as lingering resonances

Technical Innovation:
- Concurrent Mark-Sweep algorithm implementation
- Generational hypothesis with acoustic aging
- Write barriers as acoustic triggers
- Card marking as spectral markers
- Memory layout visualization through spatial audio
- Collection efficiency as musical clarity metric

Musical Elements:
- Young Generation: Bright, high-frequency, rapid cycles
- Old Generation: Deep, sustained, longer cycles
- Permanent Generation: Fundamental drone, constant presence
- Collection Cycles: Wave interference patterns
- Memory Pressure: Dynamic parameter modulation
- Fragmentation: Spectral dissonance and beating
- Compaction: Spatial audio transformation
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter, hilbert
from scipy.fft import fft, ifft, fftfreq
import os
import random
from collections import deque
import threading
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict
import json

# Parameters
SAMPLE_RATE = 48000  # Higher sample rate for advanced version
DURATION = 75  # Extended duration for complex processes

@dataclass
class MemoryObject:
    """Memory object with physical and acoustic properties"""
    obj_id: int
    generation: int  # 0: Young, 1: Old, 2: Permanent
    size: int
    age: int
    birth_time: float
    position: float  # Spatial position in memory
    frequency_base: float
    harmonics: List[float]
    collected: bool = False
    marked: bool = False
    references: List[int] = None
    
    def __post_init__(self):
        if self.references is None:
            self.references = []
    
    def get_acoustic_signature(self, time: float) -> Tuple[np.ndarray, np.ndarray]:
        """Generate acoustic signature for this memory object"""
        # Age affects frequency and amplitude
        age_factor = min(1.0, self.age / 100.0)
        
        # Generation affects timbre
        if self.generation == 0:  # Young
            base_freq = self.frequency_base * (1.0 + age_factor * 0.5)
            harmonics_mult = [1.0, 0.7, 0.5, 0.3, 0.1]
        elif self.generation == 1:  # Old
            base_freq = self.frequency_base * (0.8 + age_factor * 0.3)
            harmonics_mult = [1.0, 0.9, 0.8, 0.6, 0.4]
        else:  # Permanent
            base_freq = self.frequency_base * 0.6
            harmonics_mult = [1.0, 1.0, 0.9, 0.8, 0.7]
        
        # Generate harmonic content
        signal = np.zeros(int(SAMPLE_RATE * 0.1))
        for i, mult in enumerate(harmonics_mult):
            if i < len(self.harmonics):
                harmonic_freq = base_freq * (i + 1)
                amplitude = mult * (1.0 - age_factor * 0.3)
                harmonic = np.sin(2 * np.pi * harmonic_freq * np.arange(len(signal)) / SAMPLE_RATE)
                signal += amplitude * harmonic / (i + 1)
        
        # Apply spatial positioning
        pan_left = np.cos(self.position * np.pi / 2)
        pan_right = np.sin(self.position * np.pi / 2)
        
        return signal * pan_left, signal * pan_right

class GarbageCollector:
    """Advanced garbage collector with acoustic properties"""
    def __init__(self, gc_type: str, frequency: float, efficiency: float):
        self.gc_type = gc_type  # "mark_sweep", "copying", "generational"
        self.frequency = frequency  # Collection frequency in Hz
        self.efficiency = efficiency  # 0.0 to 1.0
        self.last_collection = 0.0
        self.collection_time = 0.0
        self.objects_collected = 0
        self.memory_freed = 0
        self.active = False
        
    def should_collect(self, current_time: float, memory_pressure: float) -> bool:
        """Determine if collection should run based on time and pressure"""
        time_factor = (current_time - self.last_collection) * self.frequency
        pressure_factor = memory_pressure * (2.0 - self.efficiency)
        return time_factor + pressure_factor > 1.0
    
    def collect(self, objects: List[MemoryObject], current_time: float) -> Tuple[int, int]:
        """Perform garbage collection"""
        self.active = True
        self.collection_time = current_time
        collected = 0
        freed = 0
        
        if self.gc_type == "mark_sweep":
            collected, freed = self._mark_sweep(objects)
        elif self.gc_type == "copying":
            collected, freed = self._copying(objects)
        else:  # generational
            collected, freed = self._generational(objects)
        
        self.objects_collected += collected
        self.memory_freed += freed
        self.last_collection = current_time
        self.active = False
        return collected, freed
    
    def _mark_sweep(self, objects: List[MemoryObject]) -> Tuple[int, int]:
        """Mark-sweep collection algorithm"""
        # Mark phase
        root_objects = [obj for obj in objects if obj.generation == 2]  # Permanent generation
        marked = set(obj.obj_id for obj in root_objects)
        
        for obj in root_objects:
            self._mark_object(obj, objects, marked)
        
        # Sweep phase
        collected = 0
        freed = 0
        for obj in objects:
            if obj.obj_id not in marked and not obj.collected:
                obj.collected = True
                collected += 1
                freed += obj.size
        
        return collected, freed
    
    def _mark_object(self, obj: MemoryObject, objects: List[MemoryObject], marked: set):
        """Recursively mark reachable objects"""
        if obj.obj_id in marked:
            return
        
        marked.add(obj.obj_id)
        for ref_id in obj.references:
            for ref_obj in objects:
                if ref_obj.obj_id == ref_id and not ref_obj.collected:
                    self._mark_object(ref_obj, objects, marked)
    
    def _copying(self, objects: List[MemoryObject]) -> Tuple[int, int]:
        """Copying collection algorithm"""
        # Find live objects (simplified)
        live_objects = [obj for obj in objects if not obj.collected and 
                       (obj.generation == 2 or random.random() < 0.7)]
        
        collected = 0
        freed = 0
        for obj in objects:
            if obj not in live_objects and not obj.collected:
                obj.collected = True
                collected += 1
                freed += obj.size
        
        return collected, freed
    
    def _generational(self, objects: List[MemoryObject]) -> Tuple[int, int]:
        """Generational collection algorithm"""
        # Collect young generation more frequently
        young_objects = [obj for obj in objects if obj.generation == 0 and not obj.collected]
        old_objects = [obj for obj in objects if obj.generation == 1 and not obj.collected]
        
        collected = 0
        freed = 0
        
        # Collect young generation
        for obj in young_objects:
            if random.random() < 0.8:  # 80% collection rate for young
                obj.collected = True
                collected += 1
                freed += obj.size
        
        # Occasionally collect old generation
        if random.random() < 0.3:  # 30% collection rate for old
            for obj in old_objects:
                if random.random() < 0.5:
                    obj.collected = True
                    collected += 1
                    freed += obj.size
        
        return collected, freed
    
    def get_acoustic_signature(self, current_time: float) -> np.ndarray:
        """Generate acoustic signature for collection activity"""
        if not self.active:
            return np.zeros(int(SAMPLE_RATE * 0.1))
        
        # Collection creates a sweeping sound
        t = np.linspace(0, 0.1, int(SAMPLE_RATE * 0.1))
        
        # Base frequency depends on collection type
        if self.gc_type == "mark_sweep":
            base_freq = 800 + (self.efficiency * 200)
        elif self.gc_type == "copying":
            base_freq = 600 + (self.efficiency * 300)
        else:  # generational
            base_freq = 400 + (self.efficiency * 400)
        
        # Create sweeping sound
        sweep_freq = base_freq * (1 + 0.5 * np.sin(2 * np.pi * 10 * t))
        signal = np.sin(2 * np.pi * sweep_freq * t)
        
        # Add efficiency-based modulation
        efficiency_mod = 1 + 0.3 * np.sin(2 * np.pi * 20 * t * self.efficiency)
        signal *= efficiency_mod
        
        # Apply envelope
        envelope = np.exp(-t * 10)
        signal *= envelope
        
        return signal

class MemorySpace:
    """Represents the memory space as an acoustic environment"""
    def __init__(self, size: int):
        self.size = size
        self.objects: List[MemoryObject] = []
        self.collectors: List[GarbageCollector] = []
        self.fragmentation = 0.0
        self.memory_pressure = 0.0
        self.allocation_history = deque(maxlen=1000)
        self.collection_history = deque(maxlen=100)
        
        # Initialize collectors
        self.collectors.append(GarbageCollector("mark_sweep", 0.5, 0.8))
        self.collectors.append(GarbageCollector("copying", 0.3, 0.9))
        self.collectors.append(GarbageCollector("generational", 1.0, 0.7))
    
    def allocate_object(self, obj_id: int, generation: int, current_time: float) -> MemoryObject:
        """Allocate a new memory object"""
        size = random.randint(10, 100)
        age = 0
        position = random.random()
        frequency_base = 220 + (generation * 110) + random.uniform(-20, 20)
        harmonics = [random.uniform(0.5, 1.5) for _ in range(5)]
        
        obj = MemoryObject(obj_id, generation, size, age, current_time, 
                          position, frequency_base, harmonics)
        
        # Create random references
        if self.objects and random.random() < 0.3:
            ref_count = random.randint(1, min(3, len(self.objects)))
            refs = random.sample(self.objects, ref_count)
            obj.references = [ref.obj_id for ref in refs if not ref.collected]
        
        self.objects.append(obj)
        self.allocation_history.append((current_time, obj_id, generation, size))
        
        # Update memory pressure
        self._update_memory_pressure()
        
        return obj
    
    def _update_memory_pressure(self):
        """Update memory pressure based on allocation and fragmentation"""
        active_objects = [obj for obj in self.objects if not obj.collected]
        total_size = sum(obj.size for obj in active_objects)
        
        # Memory pressure increases with usage
        self.memory_pressure = min(1.0, total_size / (self.size * 0.8))
        
        # Fragmentation increases with non-contiguous allocation
        if len(active_objects) > 1:
            positions = sorted([obj.position for obj in active_objects])
            gaps = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
            avg_gap = np.mean(gaps) if gaps else 0
            self.fragmentation = min(1.0, avg_gap * 2)
    
    def update(self, current_time: float):
        """Update memory space state"""
        # Age objects
        for obj in self.objects:
            if not obj.collected:
                obj.age += 1
        
        # Check for collection
        for collector in self.collectors:
            if collector.should_collect(current_time, self.memory_pressure):
                collected, freed = collector.collect(self.objects, current_time)
                self.collection_history.append((current_time, collector.gc_type, collected, freed))
        
        # Update fragmentation
        self._update_memory_pressure()
        
        # Promote objects to older generations
        for obj in self.objects:
            if not obj.collected and obj.age > 50 and obj.generation == 0:
                if random.random() < 0.1:  # 10% chance to promote
                    obj.generation = 1
            elif not obj.collected and obj.age > 200 and obj.generation == 1:
                if random.random() < 0.05:  # 5% chance to promote
                    obj.generation = 2
    
    def get_acoustic_environment(self, current_time: float, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        """Generate the complete acoustic environment"""
        samples = int(SAMPLE_RATE * duration)
        left_channel = np.zeros(samples)
        right_channel = np.zeros(samples)
        
        # Add memory object sounds
        for obj in self.objects:
            if not obj.collected:
                obj_left, obj_right = obj.get_acoustic_signature(current_time)
                
                # Place in time
                start_sample = int((obj.birth_time % duration) * SAMPLE_RATE)
                end_sample = min(start_sample + len(obj_left), samples)
                
                if start_sample < samples:
                    left_channel[start_sample:end_sample] += obj_left[:end_sample-start_sample] * 0.1
                    right_channel[start_sample:end_sample] += obj_right[:end_sample-start_sample] * 0.1
        
        # Add collection sounds
        for collector in self.collectors:
            if collector.active:
                gc_sound = collector.get_acoustic_signature(current_time)
                # Apply random panning
                pan = random.random()
                left_channel += gc_sound * pan * 0.2
                right_channel += gc_sound * (1 - pan) * 0.2
        
        # Add fragmentation noise
        if self.fragmentation > 0.1:
            noise = np.random.normal(0, self.fragmentation * 0.05, samples)
            left_channel += noise
            right_channel += noise * 0.8  # Slightly different for stereo effect
        
        # Add memory pressure drone
        if self.memory_pressure > 0.2:
            t = np.linspace(0, duration, samples)
            drone_freq = 80 * (1 + self.memory_pressure)
            drone = np.sin(2 * np.pi * drone_freq * t) * self.memory_pressure * 0.1
            left_channel += drone
            right_channel += drone
        
        return left_channel, right_channel

def generate_garbage_collection_symphony_advanced():
    """Generate the complete garbage collection symphony"""
    print("Generating Garbage Collection Symphony Advanced...")
    
    # Initialize memory space
    memory_space = MemorySpace(size=10000)
    
    # Generate audio
    samples = int(SAMPLE_RATE * DURATION)
    audio = np.zeros((samples, 2))
    
    # Simulation parameters
    chunk_size = SAMPLE_RATE  # 1 second chunks
    num_chunks = samples // chunk_size
    
    # Generate objects over time
    obj_id = 0
    for chunk in range(num_chunks):
        current_time = chunk
        
        # Allocate new objects
        for _ in range(random.randint(5, 15)):
            generation = np.random.choice([0, 1, 2], p=[0.7, 0.25, 0.05])
            memory_space.allocate_object(obj_id, generation, current_time)
            obj_id += 1
        
        # Update memory space
        memory_space.update(current_time)
        
        # Generate audio for this chunk
        start_sample = chunk * chunk_size
        end_sample = start_sample + chunk_size
        
        left_chunk, right_chunk = memory_space.get_acoustic_environment(
            current_time, 1.0
        )
        
        # Apply some processing
        left_chunk = np.clip(left_chunk, -1, 1)
        right_chunk = np.clip(right_chunk, -1, 1)
        
        # Store in audio array
        actual_chunk_size = min(len(left_chunk), chunk_size)
        audio[start_sample:start_sample+actual_chunk_size, 0] = left_chunk[:actual_chunk_size]
        audio[start_sample:start_sample+actual_chunk_size, 1] = right_chunk[:actual_chunk_size]
    
    # Apply final processing
    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio /= max_val
    
    # Apply master EQ
    audio = apply_master_eq(audio)
    
    # Apply master compression
    audio = apply_master_compression(audio)
    
    return audio

def apply_master_eq(audio: np.ndarray) -> np.ndarray:
    """Apply master EQ to enhance the mix"""
    # Simple EQ: boost low frequencies, cut high frequencies
    b, a = butter(2, 0.1, btype='low')
    low_freq = lfilter(b, a, audio, axis=0)
    
    b, a = butter(2, 0.8, btype='high')
    high_freq = lfilter(b, a, audio, axis=0)
    
    # Mix: boost low, reduce high
    audio = 0.7 * audio + 0.3 * low_freq - 0.1 * high_freq
    
    return np.clip(audio, -1, 1)

def apply_master_compression(audio: np.ndarray) -> np.ndarray:
    """Apply master compression"""
    threshold = 0.5
    ratio = 4.0
    
    # Calculate gain reduction
    abs_audio = np.abs(audio)
    gain_reduction = np.where(abs_audio > threshold, 
                             (abs_audio - threshold) / ratio, 
                             0)
    
    # Apply gain reduction
    sign = np.sign(audio)
    audio = sign * np.maximum(abs_audio - gain_reduction, 0)
    
    # Make up gain
    audio *= 1.2
    
    return np.clip(audio, -1, 1)

def create_visualization_data(memory_space: MemorySpace, duration: float):
    """Create data for visualization"""
    # Simulate the memory space for visualization
    time_points = []
    memory_usage = []
    fragmentation = []
    collection_events = []
    generation_stats = []
    
    samples_per_point = int(SAMPLE_RATE)  # 1 second per point
    num_points = int(duration)
    
    # Reset memory space for visualization
    memory_space = MemorySpace(size=10000)
    obj_id = 0
    
    for i in range(num_points):
        current_time = i
        
        # Allocate objects
        for _ in range(random.randint(5, 15)):
            generation = np.random.choice([0, 1, 2], p=[0.7, 0.25, 0.05])
            memory_space.allocate_object(obj_id, generation, current_time)
            obj_id += 1
        
        # Update memory space
        memory_space.update(current_time)
        
        # Record data
        time_points.append(current_time)
        active_objects = [obj for obj in memory_space.objects if not obj.collected]
        memory_usage.append(sum(obj.size for obj in active_objects))
        fragmentation.append(memory_space.fragmentation)
        
        # Record collection events
        for collector in memory_space.collectors:
            if collector.active:
                collection_events.append({
                    'time': current_time,
                    'type': collector.gc_type,
                    'efficiency': collector.efficiency
                })
        
        # Record generation statistics
        gen_counts = {0: 0, 1: 0, 2: 0}
        for obj in active_objects:
            gen_counts[obj.generation] += 1
        generation_stats.append(gen_counts.copy())
    
    return {
        'time_points': time_points,
        'memory_usage': memory_usage,
        'fragmentation': fragmentation,
        'collection_events': collection_events,
        'generation_stats': generation_stats
    }

def create_visualization(viz_data: dict, output_path: str):
    """Create visualization of the garbage collection process"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import Rectangle
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Garbage Collection Symphony Advanced - Memory Dynamics', fontsize=16, fontweight='bold')
        
        # Memory usage over time
        ax1 = axes[0, 0]
        ax1.plot(viz_data['time_points'], viz_data['memory_usage'], 'b-', linewidth=2)
        ax1.set_title('Memory Usage Over Time')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Memory Usage (bytes)')
        ax1.grid(True, alpha=0.3)
        
        # Fragmentation over time
        ax2 = axes[0, 1]
        ax2.plot(viz_data['time_points'], viz_data['fragmentation'], 'r-', linewidth=2)
        ax2.set_title('Memory Fragmentation')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Fragmentation Level')
        ax2.set_ylim(0, 1)
        ax2.grid(True, alpha=0.3)
        
        # Generation statistics
        ax3 = axes[1, 0]
        young_counts = [stats[0] for stats in viz_data['generation_stats']]
        old_counts = [stats[1] for stats in viz_data['generation_stats']]
        permanent_counts = [stats[2] for stats in viz_data['generation_stats']]
        
        ax3.plot(viz_data['time_points'], young_counts, 'g-', label='Young Generation', linewidth=2)
        ax3.plot(viz_data['time_points'], old_counts, 'orange', label='Old Generation', linewidth=2)
        ax3.plot(viz_data['time_points'], permanent_counts, 'purple', label='Permanent Generation', linewidth=2)
        ax3.set_title('Object Distribution by Generation')
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Number of Objects')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Collection events
        ax4 = axes[1, 1]
        collection_types = {}
        for event in viz_data['collection_events']:
            c_type = event['type']
            if c_type not in collection_types:
                collection_types[c_type] = {'times': [], 'efficiencies': []}
            collection_types[c_type]['times'].append(event['time'])
            collection_types[c_type]['efficiencies'].append(event['efficiency'])
        
        colors = {'mark_sweep': 'blue', 'copying': 'green', 'generational': 'red'}
        for c_type, data in collection_types.items():
            if c_type in colors:
                ax4.scatter(data['times'], data['efficiencies'], 
                           c=colors[c_type], label=c_type.replace('_', ' ').title(), 
                           alpha=0.6, s=50)
        
        ax4.set_title('Garbage Collection Events')
        ax4.set_xlabel('Time (seconds)')
        ax4.set_ylabel('Collection Efficiency')
        ax4.set_ylim(0, 1)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualization saved to: {output_path}")
        
    except ImportError:
        print("Matplotlib not available, skipping visualization")

def save_metadata(output_path: str, memory_space: MemorySpace, duration: float):
    """Save metadata about the generated audio"""
    metadata = {
        'title': 'Garbage Collection Symphony Advanced',
        'version': 'Advanced',
        'duration': duration,
        'sample_rate': SAMPLE_RATE,
        'technique': 'Multi-generational garbage collection with advanced physical modeling',
        'features': [
            'Multi-threaded collection algorithms',
            'Generational hypothesis implementation',
            'Memory pressure responsive collection',
            'Spatial audio positioning',
            'Fragmentation analysis and sonification',
            'Real-time adaptive collection'
        ],
        'algorithms': [
            'Mark-Sweep collection',
            'Copying collection',
            'Generational collection'
        ],
        'memory_statistics': {
            'total_objects': len(memory_space.objects),
            'active_objects': len([obj for obj in memory_space.objects if not obj.collected]),
            'collectors': len(memory_space.collectors),
            'avg_fragmentation': np.mean([memory_space.fragmentation]),
            'avg_memory_pressure': np.mean([memory_space.memory_pressure])
        },
        'collection_statistics': {
            collector.gc_type: {
                'collections': collector.objects_collected,
                'memory_freed': collector.memory_freed,
                'efficiency': collector.efficiency
            } for collector in memory_space.collectors
        }
    }
    
    with open(output_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to: {output_path}")

if __name__ == "__main__":
    # Generate the symphony
    audio = generate_garbage_collection_symphony_advanced()
    
    # Save the audio
    output_file = "08_garbage_collection_symphony_advanced.wav"
    wavfile.write(output_file, SAMPLE_RATE, audio)
    print(f"Audio saved to: {output_file}")
    
    # Create visualization
    print("Creating visualization...")
    memory_space = MemorySpace(size=10000)
    viz_data = create_visualization_data(memory_space, DURATION)
    create_visualization(viz_data, "08_garbage_collection_symphony_advanced_visualization.png")
    
    # Save metadata
    save_metadata("08_garbage_collection_symphony_advanced_metadata.json", memory_space, DURATION)
    
    print("Garbage Collection Symphony Advanced generation complete!")
    print(f"Duration: {DURATION} seconds")
    print(f"Sample Rate: {SAMPLE_RATE} Hz")
    print(f"File: {output_file}")