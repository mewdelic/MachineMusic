#!/usr/bin/env python3
"""
Enhanced Visualization Generator for MachineMusic - Error Garden
Adds sophisticated visualizations that match the error themes
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle
import json
import os
from datetime import datetime

class ErrorVisualizer:
    """Creates error-specific visualizations for MachineMusic tracks"""
    
    def __init__(self, output_dir="visualizations"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Color schemes for different error types
        self.color_schemes = {
            'stack_overflow': ['#ff4444', '#ff6666', '#ff8888', '#ffaaaa'],
            'floating_point_anxiety': ['#4444ff', '#6666ff', '#8888ff', '#aaaaff'],
            'null_pointer_dreams': ['#44ff44', '#66ff66', '#88ff88', '#aaffaa'],
            'race_condition': ['#ff44ff', '#ff66ff', '#ff88ff', '#ffaaff'],
            'memory_leak': ['#ffff44', '#ffff66', '#ffff88', '#ffffaa'],
            'buffer_overflow': ['#44ffff', '#66ffff', '#88ffff', '#aaffff'],
            'deadlock': ['#ff8844', '#ffaa66', '#ffcc88', '#ffeeaa'],
            'hash_sequence': ['#8844ff', '#aa66ff', '#cc88ff', '#eeaaff'],
            'segmentation_fault': ['#ff0044', '#ff0066', '#ff0088', '#ff00aa'],
            'kernel_panic': ['#000000', '#333333', '#666666', '#999999']
        }
    
    def create_stack_overflow_viz(self, duration=10, fps=30):
        """Create visualization for Stack Overflow - recursive layers reaching limits"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['stack_overflow']
        layers = []
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Calculate how many layers based on frame (simulating stack growth)
            max_layers = min(20, frame // 5 + 1)
            
            for i in range(max_layers):
                layer_size = 8 - (i * 0.3)  # Each layer gets smaller
                alpha = max(0.1, 1.0 - (i * 0.05))  # Fade out as we go deeper
                
                color = colors[i % len(colors)]
                
                # Create recursive rectangles
                rect = Rectangle((1 + i * 0.1, 1 + i * 0.1), 
                               layer_size, layer_size,
                               fill=False, edgecolor=color, alpha=alpha, linewidth=2)
                ax.add_patch(rect)
                
                # Add some "stack data" text
                if i < 5:  # Only show text for first few layers
                    ax.text(5, 9 - i * 1.5, f'stack_depth_{i}', 
                           color=color, alpha=alpha, fontsize=10, ha='center')
            
            # Show "overflow" effect
            if max_layers >= 15:
                ax.text(5, 5, 'STACK OVERFLOW', color='red', fontsize=20, 
                       ha='center', va='center', weight='bold')
                ax.text(5, 4, 'Segmentation fault', color='orange', fontsize=12, 
                       ha='center', va='center')
            
            ax.set_title('Stack Overflow - Recursive Limits', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        # Save as GIF
        output_path = os.path.join(self.output_dir, 'stack_overflow_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_floating_point_anxiety_viz(self, duration=10, fps=30):
        """Create visualization for Floating Point Anxiety - precision loss"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['floating_point_anxiety']
        
        # Perfect circle (represents perfect precision)
        perfect_circle = Circle((5, 5), 3, fill=False, edgecolor='white', linewidth=2, alpha=0.3)
        ax.add_patch(perfect_circle)
        
        # Points that will gradually lose precision
        n_points = 100
        angles = np.linspace(0, 2*np.pi, n_points)
        perfect_x = 5 + 3 * np.cos(angles)
        perfect_y = 5 + 3 * np.sin(angles)
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Redraw perfect circle reference
            perfect_circle = Circle((5, 5), 3, fill=False, edgecolor='white', linewidth=1, alpha=0.2)
            ax.add_patch(perfect_circle)
            
            # Calculate precision loss based on frame
            precision_loss = min(0.5, frame / (frames * 0.5))
            
            # Add noise to simulate precision loss
            noise_x = np.random.normal(0, precision_loss, n_points)
            noise_y = np.random.normal(0, precision_loss, n_points)
            
            noisy_x = perfect_x + noise_x
            noisy_y = perfect_y + noise_y
            
            # Plot with varying alpha based on precision
            alpha = max(0.3, 1.0 - precision_loss * 2)
            color = colors[int(frame / 10) % len(colors)]
            
            ax.scatter(noisy_x, noisy_y, c=color, alpha=alpha, s=20)
            
            # Add precision text
            precision_bits = max(1, int(32 * (1 - precision_loss)))
            ax.text(5, 1, f'Precision: {precision_bits}-bit', color=color, 
                   fontsize=14, ha='center', weight='bold')
            ax.text(5, 0.5, f'Error: {precision_loss:.3f}', color=color, 
                   fontsize=12, ha='center')
            
            ax.set_title('Floating Point Anxiety - Precision Loss', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'floating_point_anxiety_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_null_pointer_dreams_viz(self, duration=10, fps=30):
        """Create visualization for Null Pointer Dreams - emptiness and void"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['null_pointer_dreams']
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Create dream-like floating elements
            n_dreams = 20
            for i in range(n_dreams):
                x = 5 + 3 * np.cos(frame * 0.1 + i)
                y = 5 + 3 * np.sin(frame * 0.1 + i * 1.5)
                
                # Some dreams fade to nothing (null pointer effect)
                alpha = max(0, 0.8 - (frame / frames) - (i * 0.02))
                if alpha > 0:
                    color = colors[i % len(colors)]
                    size = 50 + 30 * np.sin(frame * 0.2 + i)
                    ax.scatter(x, y, c=color, alpha=alpha, s=size)
                    
                    # Add dream text
                    if i < 5 and alpha > 0.3:
                        ax.text(x, y + 0.5, 'dream', color=color, fontsize=8, ha='center')
            
            # Central null pointer
            null_alpha = max(0, 1 - (frame / (frames * 0.7)))
            if null_alpha > 0:
                ax.scatter(5, 5, c='white', alpha=null_alpha, s=200, marker='x', linewidth=3)
                ax.text(5, 4.5, 'NULL', color='white', alpha=null_alpha, 
                       fontsize=16, ha='center', weight='bold')
            
            ax.set_title('Null Pointer Dreams - Emptiness and Void', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'null_pointer_dreams_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_race_condition_viz(self, duration=10, fps=30):
        """Create visualization for Race Condition - competing threads"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['race_condition']
        
        # Two threads represented as moving objects
        thread1_pos = [1, 5]
        thread2_pos = [9, 5]
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Move threads towards center
            speed = 0.1
            thread1_pos[0] += speed
            thread2_pos[0] -= speed
            
            # Bounce off walls
            if thread1_pos[0] > 9 or thread1_pos[0] < 1:
                thread1_pos[0] = np.clip(thread1_pos[0], 1, 9)
            if thread2_pos[0] > 9 or thread2_pos[0] < 1:
                thread2_pos[0] = np.clip(thread2_pos[0], 1, 9)
            
            # Draw threads
            ax.scatter(thread1_pos[0], thread1_pos[1], c=colors[0], s=100, marker='o')
            ax.scatter(thread2_pos[0], thread2_pos[1], c=colors[1], s=100, marker='s')
            
            # Add thread labels
            ax.text(thread1_pos[0], thread1_pos[1] + 0.3, 'Thread A', 
                   color=colors[0], fontsize=10, ha='center')
            ax.text(thread2_pos[0], thread2_pos[1] + 0.3, 'Thread B', 
                   color=colors[1], fontsize=10, ha='center')
            
            # Draw race track
            ax.axhline(y=5, color='gray', alpha=0.3, linewidth=2)
            
            # Show interference when threads are close
            distance = abs(thread1_pos[0] - thread2_pos[0])
            if distance < 2:
                ax.text(5, 8, 'RACE CONDITION!', color='red', fontsize=16, 
                       ha='center', weight='bold')
                # Add interference pattern
                for i in range(5):
                    x = thread1_pos[0] + i * 0.1
                    y = 5 + 0.2 * np.sin(frame * 0.5 + i)
                    ax.scatter(x, y, c='yellow', alpha=0.7, s=20)
            
            ax.set_title('Race Condition - Competing Threads', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'race_condition_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_memory_leak_viz(self, duration=10, fps=30):
        """Create visualization for Memory Leak - accumulating memory"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['memory_leak']
        
        # Memory blocks
        memory_blocks = []
        total_memory = 0
        max_memory = 100
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            nonlocal total_memory
            
            # Add memory leak (gradual memory allocation)
            if frame % 5 == 0 and total_memory < max_memory:
                block_size = np.random.randint(1, 5)
                total_memory += block_size
                
                # Add new memory block
                x = np.random.uniform(1, 9)
                y = np.random.uniform(1, 9)
                memory_blocks.append({'x': x, 'y': y, 'size': block_size, 'frame': frame})
            
            # Draw memory blocks
            for block in memory_blocks:
                alpha = max(0.1, 1.0 - (frame - block['frame']) / (frames * 0.3))
                color = colors[int(block['frame'] / 10) % len(colors)]
                
                rect = Rectangle((block['x'], block['y']), 
                               block['size'] * 0.3, block['size'] * 0.3,
                               fill=True, facecolor=color, alpha=alpha, edgecolor='white')
                ax.add_patch(rect)
            
            # Memory usage bar
            usage_height = (total_memory / max_memory) * 8
            usage_bar = Rectangle((0.5, 0.5), 1, usage_height,
                                fill=True, facecolor='yellow', alpha=0.7)
            ax.add_patch(usage_bar)
            
            # Memory usage text
            ax.text(1, 0.2, f'Memory: {total_memory}/{max_memory}', 
                   color='white', fontsize=12, ha='center')
            ax.text(1, 9.5, 'Memory Leak', color='white', fontsize=14, 
                   ha='center', weight='bold')
            
            # Show warning when memory is high
            if total_memory > max_memory * 0.8:
                ax.text(5, 5, 'MEMORY\nCRITICAL', color='red', fontsize=20, 
                       ha='center', va='center', weight='bold')
            
            ax.set_title('Memory Leak Lullaby - Gradual Memory Loss', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'memory_leak_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_hash_sequence_harmony_viz(self, duration=10, fps=30):
        """Create visualization for Hash Sequence Harmony - mathematical patterns"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['hash_sequence']
        
        # Create hash sequence pattern
        def hash_function(x, seed):
            return (x * 2654435761 + seed) % 32
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Create hash visualization with flowing patterns
            n_sequences = 8
            for i in range(n_sequences):
                y_base = 1 + i * 1.1
                
                # Generate hash values for this sequence
                x_points = np.linspace(0, 10, 50)
                y_points = []
                
                for x in x_points:
                    hash_val = hash_function(int(x * 10 + frame + i * 100), i)
                    y = y_base + (hash_val % 20 - 10) * 0.1
                    y_points.append(y)
                
                # Draw hash sequence
                color = colors[i % len(colors)]
                ax.plot(x_points, y_points, color=color, alpha=0.8, linewidth=2)
                
                # Add hash value labels
                if i < 4:  # Only show labels for first few sequences
                    hash_val = hash_function(frame + i * 100, i)
                    ax.text(0.2, y_base + 0.3, f'hash_{i}: {hash_val:08x}', 
                           color=color, fontsize=8, alpha=0.7)
            
            # Show central harmony
            if frame > frames * 0.3:
                center_x, center_y = 5, 5
                harmony_radius = 1 + 0.5 * np.sin(frame * 0.1)
                harmony_circle = Circle((center_x, center_y), harmony_radius, 
                                      fill=False, edgecolor='white', alpha=0.6, linewidth=2)
                ax.add_patch(harmony_circle)
                ax.text(center_x, center_y, 'HARMONY', color='white', fontsize=12, 
                       ha='center', va='center', alpha=0.8, weight='bold')
            
            ax.set_title('Hash Sequence Harmony - Mathematical Beauty', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'hash_sequence_harmony_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_segmentation_fault_viz(self, duration=10, fps=30):
        """Create visualization for Segmentation Fault - memory violation explosion"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['segmentation_fault']
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # Normal memory regions
            memory_regions = [
                {'x': 1, 'y': 1, 'w': 3, 'h': 3, 'label': 'Code'},
                {'x': 5, 'y': 1, 'w': 3, 'h': 3, 'label': 'Data'},
                {'x': 1, 'y': 5, 'w': 3, 'h': 3, 'label': 'Stack'},
                {'x': 5, 'y': 5, 'w': 3, 'h': 3, 'label': 'Heap'}
            ]
            
            for region in memory_regions:
                rect = Rectangle((region['x'], region['y']), 
                               region['w'], region['h'],
                               fill=False, edgecolor='gray', alpha=0.5, linewidth=1)
                ax.add_patch(rect)
                ax.text(region['x'] + region['w']/2, region['y'] + region['h']/2, 
                       region['label'], color='gray', fontsize=10, ha='center', va='center')
            
            # Show illegal access attempt
            if frame > frames * 0.3:
                # Illegal memory access arrow
                start_x, start_y = 3, 4  # Inside stack
                end_x, end_y = 7, 7      # Outside all regions (segmentation fault)
                
                ax.arrow(start_x, start_y, end_x - start_x, end_y - start_y,
                        head_width=0.2, head_length=0.3, fc='red', ec='red', alpha=0.8)
                
                # Show explosion effect
                explosion_alpha = min(1.0, (frame - frames * 0.3) / (frames * 0.2))
                if explosion_alpha > 0:
                    # Explosion particles
                    n_particles = 20
                    for i in range(n_particles):
                        angle = 2 * np.pi * i / n_particles
                        distance = explosion_alpha * 2
                        particle_x = end_x + distance * np.cos(angle)
                        particle_y = end_y + distance * np.sin(angle)
                        
                        color = colors[i % len(colors)]
                        ax.scatter(particle_x, particle_y, c=color, alpha=explosion_alpha, s=30)
                    
                    # Central explosion
                    ax.scatter(end_x, end_y, c='red', alpha=explosion_alpha, s=100, marker='*')
                    
                    # Error message
                    ax.text(5, 8.5, 'SEGMENTATION FAULT', color='red', fontsize=16, 
                           ha='center', weight='bold', alpha=explosion_alpha)
                    ax.text(5, 8, 'Access violation at 0xdeadbeef', color='orange', fontsize=12, 
                           ha='center', alpha=explosion_alpha)
            
            ax.set_title('Segmentation Fault - Memory Violation', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'segmentation_fault_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_kernel_panic_viz(self, duration=10, fps=30):
        """Create visualization for Kernel Panic - system shutdown"""
        frames = duration * fps
        
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        colors = self.color_schemes['kernel_panic']
        
        # System processes
        processes = []
        for i in range(8):
            processes.append({
                'x': 1 + (i % 4) * 2,
                'y': 7 + (i // 4) * 2,
                'name': f'proc_{i}',
                'alive': True
            })
        
        def animate(frame):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # System panic progress
            panic_progress = min(1.0, frame / (frames * 0.7))
            
            # Draw processes
            for i, proc in enumerate(processes):
                # Kill processes as panic progresses
                if panic_progress > i / len(processes):
                    proc['alive'] = False
                
                color = colors[2] if proc['alive'] else colors[0]  # Gray when dead
                alpha = 0.8 if proc['alive'] else 0.3
                marker = 'o' if proc['alive'] else 'x'
                
                ax.scatter(proc['x'], proc['y'], c=color, alpha=alpha, s=100, marker=marker)
                ax.text(proc['x'], proc['y'] - 0.5, proc['name'], 
                       color=color, fontsize=8, ha='center', alpha=alpha)
            
            # Show kernel panic
            if panic_progress > 0.2:
                panic_alpha = min(1.0, (panic_progress - 0.2) / 0.3)
                
                # Panic screen background
                panic_rect = Rectangle((1, 1), 8, 6, 
                                     fill=True, facecolor='black', alpha=panic_alpha)
                ax.add_patch(panic_rect)
                
                # Panic text
                if panic_alpha > 0.5:
                    ax.text(5, 6, 'KERNEL PANIC', color='red', fontsize=18, 
                           ha='center', weight='bold', alpha=panic_alpha)
                    ax.text(5, 5.5, 'System halted', color='white', fontsize=12, 
                           ha='center', alpha=panic_alpha)
                    
                    # Fake kernel error message
                    error_messages = [
                        'Unable to handle kernel NULL pointer dereference',
                        'Kernel Oops: 0000 [#1] SMP',
                        'CPU: 0 PID: 1 Comm: init Not tainted'
                    ]
                    
                    for i, msg in enumerate(error_messages[:3]):
                        ax.text(5, 4.5 - i * 0.5, msg, color='white', fontsize=10, 
                               ha='center', alpha=panic_alpha * 0.8)
                    
                    # Final shutdown
                    if panic_alpha > 0.8:
                        ax.text(5, 2, 'SYSTEM SHUTDOWN', color='red', fontsize=16, 
                               ha='center', weight='bold', alpha=panic_alpha - 0.8)
            
            # Show system uptime
            uptime = (frames - frame) / fps
            ax.text(9, 9.5, f'Uptime: {uptime:.1f}s', color='white', fontsize=10, 
                   ha='right', alpha=0.7)
            
            ax.set_title('Kernel Panic - System Shutdown', color='white', fontsize=16)
        
        anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/fps)
        
        output_path = os.path.join(self.output_dir, 'kernel_panic_reprise_visualization.gif')
        anim.save(output_path, writer='pillow', fps=fps)
        plt.close()
        
        return output_path
    
    def create_all_visualizations(self):
        """Generate all visualizations"""
        print("Generating enhanced visualizations for Error Garden...")
        
        viz_paths = []
        
        # Generate each visualization
        try:
            viz_paths.append(self.create_stack_overflow_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_floating_point_anxiety_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_null_pointer_dreams_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_race_condition_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_memory_leak_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_hash_sequence_harmony_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_segmentation_fault_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
            viz_paths.append(self.create_kernel_panic_viz())
            print(f"✓ Created: {viz_paths[-1]}")
            
        except Exception as e:
            print(f"✗ Error creating visualization: {e}")
        
        return viz_paths

def main():
    """Main function to generate all visualizations"""
    visualizer = ErrorVisualizer()
    viz_paths = visualizer.create_all_visualizations()
    
    print(f"\n🎨 Generated {len(viz_paths)} visualizations:")
    for path in viz_paths:
        print(f"   - {path}")
    
    print(f"\n📁 Visualizations saved in: {visualizer.output_dir}")

if __name__ == "__main__":
    main()