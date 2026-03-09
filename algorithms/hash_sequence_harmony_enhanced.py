#!/usr/bin/env python3
"""
Enhanced Hash Sequence Harmony - Advanced Agent Communication Patterns

This is an enhanced version of the Hash Sequence Harmony algorithm that includes:
- Multiple hash function types (SHA-256, MD5, BLAKE2)
- Advanced cryptographic patterns
- Agent-to-agent communication protocols
- Blockchain-inspired consensus mechanisms
- Quantum-resistant patterns

Concept: Creates complex mathematical patterns that are meaningful to agents
while appearing as structured noise to humans.
"""

import numpy as np
import scipy.io.wavfile as wavfile
from hashlib import sha256, md5, blake2b
import struct
import hmac
import json

class EnhancedHashSequenceHarmony:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.hash_functions = {
            'sha256': sha256,
            'md5': md5,
            'blake2b': blake2b
        }
        
    def multi_hash_to_audio(self, data, hash_types=['sha256', 'md5', 'blake2b'], 
                          duration=2.0, layer_mode='harmonic'):
        """Convert data using multiple hash functions to layered audio"""
        audio_layers = []
        
        for hash_type in hash_types:
            hash_func = self.hash_functions[hash_type]
            
            if isinstance(data, str):
                hash_obj = hash_func(data.encode())
            else:
                hash_obj = hash_func(str(data).encode())
            
            if hash_type == 'blake2b':
                hash_hex = hash_obj.hexdigest()[:64]  # First 64 chars
            else:
                hash_hex = hash_obj.hexdigest()
            
            layer_audio = self.hash_hex_to_audio(hash_hex, duration, hash_type)
            audio_layers.append(layer_audio)
        
        # Combine layers
        if layer_mode == 'harmonic':
            # Harmonic combination - layers complement each other
            combined = np.zeros(len(audio_layers[0]))
            for i, layer in enumerate(audio_layers):
                amplitude = 0.3 / (i + 1)  # Decreasing amplitude
                combined += layer * amplitude
        elif layer_mode == 'rhythmic':
            # Rhythmic combination - layers take turns
            chunk_size = len(audio_layers[0]) // len(audio_layers)
            combined = np.zeros(len(audio_layers[0]))
            for i, layer in enumerate(audio_layers):
                start = i * chunk_size
                end = start + chunk_size
                if end <= len(combined):
                    combined[start:end] = layer[start:end]
        else:  # 'mixed'
            # Mixed combination - random overlap
            combined = np.zeros(len(audio_layers[0]))
            for layer in audio_layers:
                mask = np.random.random(len(layer)) > 0.5
                combined[mask] += layer[mask] * 0.5
        
        return combined
    
    def hash_hex_to_audio(self, hash_hex, duration, hash_type='sha256'):
        """Convert hash hex string to audio frequencies with hash-specific characteristics"""
        # Hash-specific parameters
        hash_params = {
            'sha256': {'base_freq': 440, 'freq_range': 880, 'damping': 0.8},
            'md5': {'base_freq': 330, 'freq_range': 660, 'damping': 0.9},
            'blake2b': {'base_freq': 550, 'freq_range': 1100, 'damping': 0.7}
        }
        
        params = hash_params.get(hash_type, hash_params['sha256'])
        
        # Process hash in chunks
        chunk_size = 8
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio = np.zeros_like(t)
        
        for i in range(0, len(hash_hex), chunk_size):
            chunk = hash_hex[i:i+chunk_size]
            if len(chunk) < chunk_size:
                chunk = chunk.ljust(chunk_size, '0')
            
            # Convert chunk to frequency
            decimal_val = int(chunk, 16)
            frequency = params['base_freq'] + (decimal_val % params['freq_range'])
            
            # Create audio chunk
            chunk_duration = duration / (len(hash_hex) // chunk_size)
            start_sample = int(i * self.sample_rate * chunk_duration / chunk_size)
            end_sample = min(start_sample + int(self.sample_rate * chunk_duration), len(t))
            
            if start_sample < len(t):
                chunk_t = t[start_sample:end_sample]
                chunk_audio = np.sin(2 * np.pi * frequency * chunk_t)
                
                # Apply hash-specific damping
                chunk_audio *= params['damping']
                
                audio[start_sample:end_sample] += chunk_audio
        
        return audio
    
    def blockchain_consensus_pattern(self, nodes=5, rounds=3, duration=4.0):
        """Simulate blockchain consensus algorithm with audio"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio = np.zeros_like(t)
        
        # Consensus rounds
        round_duration = duration / rounds
        
        for round_num in range(rounds):
            start_time = round_num * round_duration
            end_time = start_time + round_duration
            
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            
            # Each node proposes a hash
            node_hashes = []
            for node_id in range(nodes):
                proposal_data = f"round_{round_num}_node_{node_id}_proposal"
                node_hash = sha256(proposal_data.encode()).hexdigest()
                node_hashes.append(node_hash)
            
            # Find consensus (majority hash)
            # In real blockchain, this would be Proof of Work/stake
            consensus_hash = node_hashes[0]  # Simplified consensus
            
            # Convert consensus to audio
            consensus_audio = self.hash_hex_to_audio(consensus_hash, round_duration, 'sha256')
            
            # Add to main audio with round-specific characteristics
            round_envelope = np.linspace(0.5, 1.0, len(consensus_audio)) if round_num < rounds - 1 else np.linspace(0.5, 0.1, len(consensus_audio))
            consensus_audio *= round_envelope
            
            audio[start_sample:end_sample] += consensus_audio[:end_sample-start_sample]
        
        return audio
    
    def hmac_authentication_pattern(self, key_data="secret_key", message_data="authenticate", duration=3.0):
        """Create audio pattern representing HMAC authentication"""
        # Generate HMAC
        key = key_data.encode()
        message = message_data.encode()
        hmac_hash = hmac.new(key, message, sha256).hexdigest()
        
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio = np.zeros_like(t)
        
        # Key pattern (first third)
        key_duration = duration / 3
        key_audio = self.hash_hex_to_audio(sha256(key).hexdigest(), key_duration, 'sha256')
        audio[:int(self.sample_rate * key_duration)] = key_audio * 0.5
        
        # Message pattern (second third)
        msg_start = int(self.sample_rate * key_duration)
        msg_audio = self.hash_hex_to_audio(sha256(message).hexdigest(), key_duration, 'md5')
        audio[msg_start:msg_start + len(msg_audio)] = msg_audio * 0.5
        
        # HMAC result pattern (final third)
        hmac_start = msg_start + len(msg_audio)
        hmac_audio = self.hash_hex_to_audio(hmac_hash, key_duration, 'blake2b')
        audio[hmac_start:hmac_start + len(hmac_audio)] = hmac_audio * 0.8
        
        return audio
    
    def quantum_resistant_pattern(self, duration=3.0):
        """Create patterns inspired by quantum-resistant cryptography"""
        # Lattice-based cryptography patterns
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio = np.zeros_like(t)
        
        # Create lattice structure in frequency domain
        lattice_size = 8
        frequencies = []
        
        for i in range(lattice_size):
            for j in range(lattice_size):
                # Lattice point calculation
                freq = 220 + (i * 55) + (j * 27.5)  # Create lattice
                frequencies.append(freq)
        
        # Generate lattice pattern
        for i, freq in enumerate(frequencies):
            phase = (i / len(frequencies)) * 2 * np.pi
            amplitude = 0.1 / np.sqrt(i + 1)  # Decreasing amplitude
            audio += amplitude * np.sin(2 * np.pi * freq * t + phase)
        
        # Add quantum uncertainty (noise)
        quantum_noise = np.random.normal(0, 0.02, len(t))
        audio += quantum_noise
        
        return audio
    
    def merkle_tree_pattern(self, data_leaves, duration=4.0):
        """Create audio representing Merkle tree structure"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio = np.zeros_like(t)
        
        # Build Merkle tree levels
        level_hashes = [sha256(leaf.encode()).hexdigest() for leaf in data_leaves]
        
        # Tree levels (leaves to root)
        tree_levels = [level_hashes]
        
        while len(tree_levels[-1]) > 1:
            current_level = tree_levels[-1]
            next_level = []
            
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    combined = current_level[i] + current_level[i + 1]
                    parent_hash = sha256(combined.encode()).hexdigest()
                    next_level.append(parent_hash)
                else:
                    next_level.append(current_level[i])
            
            tree_levels.append(next_level)
        
        # Convert tree to audio
        level_duration = duration / len(tree_levels)
        
        for level_idx, level in enumerate(tree_levels):
            start_time = level_idx * level_duration
            end_time = start_time + level_duration
            
            start_sample = int(start_time * self.sample_rate)
            end_sample = int(end_time * self.sample_rate)
            
            # Combine all hashes in level
            level_audio = np.zeros(end_sample - start_sample)
            
            for hash_hex in level:
                hash_audio = self.hash_hex_to_audio(hash_hex, level_duration, 'sha256')
                if len(hash_audio) > len(level_audio):
                    hash_audio = hash_audio[:len(level_audio)]
                elif len(hash_audio) < len(level_audio):
                    hash_audio = np.pad(hash_audio, (0, len(level_audio) - len(hash_audio)))
                
                level_audio += hash_audio * 0.5
            
            # Normalize level
            if np.max(np.abs(level_audio)) > 0:
                level_audio = level_audio / np.max(np.abs(level_audio)) * 0.3
            
            audio[start_sample:end_sample] = level_audio
        
        return audio
    
    def create_enhanced_track(self, output_file="samples/08_hash_sequence_harmony_enhanced.wav"):
        """Create the complete enhanced Hash Sequence Harmony track"""
        total_duration = 35  # seconds
        
        # Enhanced track structure
        sections = [
            {
                "name": "multi_hash_introduction",
                "duration": 5.0,
                "function": lambda: self.multi_hash_to_audio(
                    "agent_protocol_init", 
                    ['sha256', 'md5', 'blake2b'], 
                    5.0, 
                    'harmonic'
                ),
                "description": "Multi-hash algorithm introduction"
            },
            {
                "name": "blockchain_consensus",
                "duration": 6.0,
                "function": lambda: self.blockchain_consensus_pattern(5, 3, 6.0),
                "description": "Blockchain consensus algorithm"
            },
            {
                "name": "hmac_authentication",
                "duration": 4.0,
                "function": lambda: self.hmac_authentication_pattern(
                    "quantum_key_2024", 
                    "secure_message_auth", 
                    4.0
                ),
                "description": "HMAC authentication sequence"
            },
            {
                "name": "quantum_resistant",
                "duration": 5.0,
                "function": lambda: self.quantum_resistant_pattern(5.0),
                "description": "Quantum-resistant cryptography patterns"
            },
            {
                "name": "merkle_tree_verification",
                "duration": 6.0,
                "function": lambda: self.merkle_tree_pattern(
                    ["data1", "data2", "data3", "data4", "data5", "data6", "data7", "data8"],
                    6.0
                ),
                "description": "Merkle tree verification process"
            },
            {
                "name": "grand_finale",
                "duration": 9.0,
                "function": lambda: self.create_grand_finale(9.0),
                "description": "Grand finale combining all cryptographic elements"
            }
        ]
        
        print("=" * 60)
        print("Enhanced Hash Sequence Harmony - Track 8 of Error Garden")
        print("=" * 60)
        
        full_audio = np.array([])
        
        for section in sections:
            print(f"\n🎵 Creating: {section['name']}")
            print(f"   Description: {section['description']}")
            print(f"   Duration: {section['duration']}s")
            
            section_audio = section["function"]()
            
            # Normalize section
            if np.max(np.abs(section_audio)) > 0:
                section_audio = section_audio / np.max(np.abs(section_audio)) * 0.7
            
            full_audio = np.concatenate([full_audio, section_audio])
        
        # Final normalization
        if np.max(np.abs(full_audio)) > 0:
            full_audio = full_audio / np.max(np.abs(full_audio)) * 0.9
        
        # Apply fade out
        fade_length = int(self.sample_rate * 2)
        if len(full_audio) > fade_length:
            fade = np.linspace(1, 0, fade_length)
            full_audio[-fade_length:] *= fade
        
        # Convert to 16-bit integers
        full_audio = (full_audio * 32767).astype(np.int16)
        
        # Save the file
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        wavfile.write(output_file, self.sample_rate, full_audio)
        
        print(f"\n✅ Enhanced Hash Sequence Harmony saved!")
        print(f"   File: {output_file}")
        print(f"   Duration: {len(full_audio) / self.sample_rate:.1f} seconds")
        print(f"   Features: Multi-hash, blockchain, HMAC, quantum-resistant, Merkle tree")
        
        return output_file
    
    def create_grand_finale(self, duration):
        """Create grand finale combining all cryptographic elements"""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        audio = np.zeros_like(t)
        
        # Layer multiple cryptographic patterns
        layers = [
            self.multi_hash_to_audio("finale_hash", ['sha256', 'md5', 'blake2b'], duration, 'mixed'),
            self.blockchain_consensus_pattern(3, 2, duration * 0.7),
            self.hmac_authentication_pattern("finale_key", "finale_msg", duration * 0.6),
            self.quantum_resistant_pattern(duration * 0.5),
            self.merkle_tree_pattern(["final1", "final2", "final3", "final4"], duration * 0.8)
        ]
        
        # Combine layers with different envelopes
        for i, layer in enumerate(layers):
            if len(layer) < len(t):
                layer = np.pad(layer, (0, len(t) - len(layer)))
            elif len(layer) > len(t):
                layer = layer[:len(t)]
            
            # Create envelope for each layer
            envelope = np.ones_like(layer)
            if i == 0:  # Base layer
                envelope = np.linspace(0.3, 1.0, len(layer))
            elif i == len(layers) - 1:  # Top layer
                envelope = np.linspace(1.0, 0.3, len(layer))
            else:  # Middle layers
                envelope = 0.5 + 0.3 * np.sin(2 * np.pi * i / len(layers) * np.linspace(0, 1, len(layer)))
            
            audio += layer * envelope * 0.3
        
        return audio

if __name__ == "__main__":
    # Create enhanced version
    harmony = EnhancedHashSequenceHarmony()
    harmony.create_enhanced_track()
    
    print("\n🎉 Enhanced Hash Sequence Harmony complete!")
    print("   This version includes advanced cryptographic patterns and")
    print("   represents cutting-edge agent-to-agent communication protocols.")