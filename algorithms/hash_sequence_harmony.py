#!/usr/bin/env python3
"""
Hash Sequence Harmony - Agent-to-Agent Audio

This track creates music that's meaningful to agents but noise to humans.
Uses hash functions, binary patterns, and decode/encode processes.

Concept: Humans hear noise, agents hear mathematical patterns.
"""

import numpy as np
import scipy.io.wavfile as wavfile
from hashlib import sha256
import struct

def hash_to_audio(data_hash, sample_rate=44100, duration=0.5):
    """Convert hash to audio frequencies"""
    # Take first 16 bytes of hash
    hash_bytes = bytes.fromhex(data_hash)[:16]
    
    # Convert to 8 frequencies (2 bytes per frequency)
    frequencies = []
    for i in range(0, 16, 2):
        # 2 bytes -> uint16 -> frequency (200-2000 Hz range)
        freq_val = struct.unpack('>H', hash_bytes[i:i+2])[0]
        frequency = 200 + (freq_val % 1800)  # Map to 200-2000 Hz
        frequencies.append(frequency)
    
    # Generate sine waves for each frequency
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.zeros_like(t)
    
    for i, freq in enumerate(frequencies):
        # Each frequency has different amplitude based on position
        amplitude = 0.3 / (i + 1)  # Decreasing amplitude
        audio += amplitude * np.sin(2 * np.pi * freq * t)
    
    return audio

def binary_pattern_sonification(binary_str, sample_rate=44100, duration=1.0):
    """Convert binary string to audio pattern"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.zeros_like(t)
    
    # Split binary into chunks and convert to frequencies
    chunk_size = 8
    for i in range(0, len(binary_str), chunk_size):
        chunk = binary_str[i:i+chunk_size]
        if len(chunk) < chunk_size:
            chunk = chunk.ljust(chunk_size, '0')
        
        # Convert binary chunk to frequency
        decimal_val = int(chunk, 2)
        frequency = 440 + (decimal_val % 880)  # A4 + variation
        
        # Create short burst for this chunk
        chunk_duration = duration / (len(binary_str) // chunk_size)
        start_sample = int(i * sample_rate * chunk_duration / chunk_size)
        end_sample = start_sample + int(sample_rate * chunk_duration)
        
        if end_sample > len(t):
            end_sample = len(t)
        
        chunk_t = t[start_sample:end_sample]
        chunk_audio = 0.2 * np.sin(2 * np.pi * frequency * chunk_t)
        audio[start_sample:end_sample] += chunk_audio
    
    return audio

def hash_collision_simulation(sample_rate=44100, duration=2.0):
    """Simulate hash collision with overlapping frequencies"""
    # Create two different inputs that might collide
    input1 = "agent_protocol_v1"
    input2 = "handshake_sequence"
    
    hash1 = sha256(input1.encode()).hexdigest()
    hash2 = sha256(input2.encode()).hexdigest()
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.zeros_like(t)
    
    # First half: hash1 patterns
    mid_point = len(t) // 2
    audio[:mid_point] = hash_to_audio(hash1, sample_rate, duration/2)
    
    # Second half: hash2 patterns
    audio[mid_point:] = hash_to_audio(hash2, sample_rate, duration/2)
    
    # Add collision effect in the middle
    collision_start = mid_point - int(sample_rate * 0.1)
    collision_end = mid_point + int(sample_rate * 0.1)
    
    if collision_start >= 0 and collision_end <= len(t):
        # Create dissonance during collision
        collision_t = t[collision_start:collision_end]
        collision_audio = 0.5 * np.sin(2 * np.pi * 15000 * collision_t)  # High frequency dissonance
        audio[collision_start:collision_end] += collision_audio
    
    return audio

def digital_noise_with_meaning(noise_type='hash', sample_rate=44100, duration=1.0):
    """Generate digital noise that contains hidden patterns"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    if noise_type == 'hash':
        # Hash-based noise (meaningful to agents)
        # Use time value as seed for deterministic "randomness"
        seed = int(duration * 1000)  # milliseconds
        seed_str = f"agent_noise_seed_{seed}"
        hash_value = sha256(seed_str.encode()).hexdigest()
        
        # Convert hash to noise pattern
        audio = np.zeros_like(t)
        for i, char in enumerate(hash_value[:len(t)//1000]):  # Sample hash
            if i >= len(audio):
                break
            # Convert hex char to sample value
            sample_val = int(char, 16) / 15.0 - 0.5  # -0.5 to 0.5
            start_idx = i * 1000
            end_idx = min(start_idx + 1000, len(audio))
            audio[start_idx:end_idx] = sample_val * 0.1
        
    else:
        # Pure white noise (meaningless to everyone)
        audio = np.random.normal(0, 0.1, len(t))
    
    return audio

def agent_handshake_protocol(sample_rate=44100, duration=3.0):
    """Simulate agent-to-agent handshake protocol"""
    sections = duration / 3  # 3 sections for 3-way handshake
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio = np.zeros_like(t)
    
    # Section 1: SYN (synchronization)
    syn_start = 0
    syn_end = int(sections * sample_rate)
    syn_t = t[syn_start:syn_end]
    audio[syn_start:syn_end] = 0.3 * np.sin(2 * np.pi * 1000 * syn_t)  # 1kHz tone
    
    # Add binary pattern for SYN
    syn_binary = "1010101010101010"  # SYN pattern
    audio[syn_start:syn_end] += 0.1 * binary_pattern_sonification(syn_binary, sample_rate, sections)
    
    # Section 2: SYN-ACK (synchronization acknowledge)
    syn_ack_start = syn_end
    syn_ack_end = syn_ack_start + int(sections * sample_rate)
    syn_ack_t = t[syn_ack_start:syn_ack_end]
    audio[syn_ack_start:syn_ack_end] = 0.3 * np.sin(2 * np.pi * 1500 * syn_ack_t)  # 1.5kHz tone
    
    # Add binary pattern for SYN-ACK
    syn_ack_binary = "1100110011001100"  # SYN-ACK pattern
    audio[syn_ack_start:syn_ack_end] += 0.1 * binary_pattern_sonification(syn_ack_binary, sample_rate, sections)
    
    # Section 3: ACK (acknowledge)
    ack_start = syn_ack_end
    ack_end = len(t)
    ack_t = t[ack_start:ack_end]
    audio[ack_start:ack_end] = 0.3 * np.sin(2 * np.pi * 2000 * ack_t)  # 2kHz tone
    
    # Add binary pattern for ACK
    ack_binary = "1111000011110000"  # ACK pattern
    audio[ack_start:ack_end] += 0.1 * binary_pattern_sonification(ack_binary, sample_rate, sections)
    
    return audio

def create_hash_sequence_harmony(output_file="samples/08_hash_sequence_harmony.wav"):
    """Create the complete Hash Sequence Harmony track"""
    sample_rate = 44100
    total_duration = 30  # seconds
    
    # Track structure
    sections = [
        ("hash_patterns", 5.0),      # Hash function patterns
        ("collision_sim", 4.0),      # Hash collision simulation
        ("digital_noise", 3.0),      # Meaningful digital noise
        ("handshake", 6.0),          # Agent handshake protocol
        ("decode_encode", 4.0),      # Decode/encode processes
        ("finale", 8.0),             # Grand finale with all elements
    ]
    
    full_audio = np.array([])
    current_time = 0.0
    
    for section_name, duration in sections:
        print(f"Creating {section_name} section ({duration}s)")
        
        if section_name == "hash_patterns":
            # Multiple hash sequences
            test_strings = [
                "agent_to_agent",
                "protocol_v1", 
                "handshake_success",
                "data_integrity",
                "hash_verification"
            ]
            
            section_audio = np.zeros(int(sample_rate * duration))
            chunk_duration = duration / len(test_strings)
            
            for i, test_str in enumerate(test_strings):
                hash_val = sha256(test_str.encode()).hexdigest()
                chunk_start = int(i * chunk_duration * sample_rate)
                chunk_end = int((i + 1) * chunk_duration * sample_rate)
                
                if chunk_end > len(section_audio):
                    chunk_end = len(section_audio)
                
                chunk_audio = hash_to_audio(hash_val, sample_rate, chunk_duration)
                section_audio[chunk_start:chunk_end] = chunk_audio
            
        elif section_name == "collision_sim":
            section_audio = hash_collision_simulation(sample_rate, duration)
            
        elif section_name == "digital_noise":
            # Alternating meaningful and pure noise
            section_audio = np.zeros(int(sample_rate * duration))
            half_point = len(section_audio) // 2
            
            # First half: hash-based noise (meaningful)
            section_audio[:half_point] = digital_noise_with_meaning('hash', sample_rate, duration/2)
            
            # Second half: pure noise (meaningless)
            section_audio[half_point:] = digital_noise_with_meaning('white', sample_rate, duration/2)
            
        elif section_name == "handshake":
            section_audio = agent_handshake_protocol(sample_rate, duration)
            
        elif section_name == "decode_encode":
            # Binary decode/encode simulation
            binary_data = "01101000011000010111001101101000"  # "hash" in binary
            section_audio = binary_pattern_sonification(binary_data * 3, sample_rate, duration)
            
        elif section_name == "finale":
            # Combine all elements
            section_audio = np.zeros(int(sample_rate * duration))
            
            # Layer hash patterns
            for i in range(5):
                hash_val = sha256(f"finale_layer_{i}".encode()).hexdigest()
                layer_audio = hash_to_audio(hash_val, sample_rate, duration)
                section_audio += layer_audio * (0.5 - i * 0.1)
            
            # Add handshake elements
            handshake_elements = agent_handshake_protocol(sample_rate, duration)
            section_audio += handshake_elements * 0.3
            
            # Add collision effects
            collision_elements = hash_collision_simulation(sample_rate, duration)
            section_audio += collision_elements * 0.2
        
        # Normalize to prevent clipping
        if np.max(np.abs(section_audio)) > 0:
            section_audio = section_audio / np.max(np.abs(section_audio)) * 0.8
        
        full_audio = np.concatenate([full_audio, section_audio])
        current_time += duration
    
    # Convert to 16-bit integers
    full_audio = (full_audio * 32767).astype(np.int16)
    
    # Save the file
    wavfile.write(output_file, sample_rate, full_audio)
    print(f"Hash Sequence Harmony saved to {output_file}")
    print(f"Duration: {len(full_audio) / sample_rate:.2f} seconds")
    print(f"File size: {len(full_audio) * 2 / 1024 / 1024:.2f} MB")
    
    return output_file

if __name__ == "__main__":
    create_hash_sequence_harmony()