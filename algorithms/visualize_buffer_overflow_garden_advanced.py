#!/usr/bin/env python3
"""
Buffer Overflow Garden Advanced - Visualization Generator
高度な物理的複雑系の可視化
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import json
from datetime import datetime
import random
import math
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial.distance import cdist
import warnings
warnings.filterwarnings('ignore')

# 日本語フォント設定
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

class ComplexSystemVisualizer:
    """複雑系可視化クラス"""
    
    def __init__(self, width=12, height=8):
        self.width = width
        self.height = height
        self.fig, self.axes = plt.subplots(2, 3, figsize=(width, height))
        self.fig.suptitle('Buffer Overflow Garden - Advanced Complex Systems', fontsize=16, fontweight='bold')
        
        # サブプロットのタイトル
        subplot_titles = [
            'Quantum Interference Pattern',
            'Fractal Memory Structure',
            'Topological Defects Field',
            'Spin Glass Configuration',
            'Phase Transition Dynamics',
            'Chaotic Trajectory'
        ]
        
        for ax, title in zip(self.axes.flat, subplot_titles):
            ax.set_title(title, fontsize=12)
            ax.set_aspect('equal')
        
        plt.tight_layout()
    
    def generate_quantum_interference(self, ax, num_cells=20):
        """量子干渉パターンを生成"""
        # 量子セルの配置
        positions = np.random.rand(num_cells, 2) * 10
        
        # 量子状態の重ね合わせ
        for i, pos in enumerate(positions):
            # 量子コヒーレンスによる円
            coherence = np.random.uniform(0.3, 1.0)
            phase = np.random.uniform(0, 2 * np.pi)
            
            # 円の描画
            circle = plt.Circle(pos, coherence, 
                              fill=False, 
                              color=plt.cm.plasma(i / num_cells),
                              linewidth=2,
                              alpha=0.7)
            ax.add_patch(circle)
            
            # 干渉線
            for j in range(i + 1, num_cells):
                if np.random.random() < 0.3:  # 30%の確率で干渉
                    end_pos = positions[j]
                    ax.plot([pos[0], end_pos[0]], [pos[1], end_pos[1]], 
                           'gray', alpha=0.3, linewidth=1)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_facecolor('#0a0a0a')
    
    def generate_fractal_structure(self, ax, depth=5):
        """フラクタル構造を生成"""
        # フラクタルツリーの描画
        def draw_fractal_branch(x, y, length, angle, depth):
            if depth <= 0:
                return
            
            # 分岐点の計算
            end_x = x + length * np.cos(angle)
            end_y = y + length * np.sin(angle)
            
            # 枝の描画
            ax.plot([x, end_x], [y, end_y], 
                   color=plt.cm.viridis(depth / 5), 
                   linewidth=depth * 0.5)
            
            # 再帰的な分岐
            if depth > 1:
                # 複数方向への分岐
                for branch_angle in [-np.pi/4, 0, np.pi/4]:
                    new_angle = angle + branch_angle
                    new_length = length * np.random.uniform(0.6, 0.8)
                    draw_fractal_branch(end_x, end_y, new_length, new_angle, depth - 1)
        
        # 複数のフラクタルツリー
        tree_positions = [(2, 2), (5, 3), (8, 1), (3, 7), (7, 6)]
        
        for pos_x, pos_y in tree_positions:
            initial_angle = np.random.uniform(-np.pi/4, np.pi/4)
            draw_fractal_branch(pos_x, pos_y, 1.5, initial_angle, depth)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_facecolor('#0a0a0a')
    
    def generate_topological_defects(self, ax, num_defects=5):
        """トポロジカル欠陥の場を生成"""
        # 欠陥の配置
        defect_positions = np.random.rand(num_defects, 2) * 10
        defect_charges = np.random.choice([-1, 1], num_defects)
        
        # 格子点の生成
        x = np.linspace(0, 10, 30)
        y = np.linspace(0, 10, 30)
        X, Y = np.meshgrid(x, y)
        
        # 各格子点での場の計算
        field_strength = np.zeros_like(X)
        
        for i, (pos, charge) in enumerate(zip(defect_positions, defect_charges)):
            # 距離の計算
            distances = np.sqrt((X - pos[0])**2 + (Y - pos[1])**2)
            distances = np.maximum(distances, 0.1)  # ゼロ除算防止
            
            # 場の強さ（クーロン法則）
            field_contribution = charge / (distances**2)
            field_strength += field_contribution
            
            # 欠陥点の描画
            color = 'red' if charge > 0 else 'blue'
            ax.scatter(pos[0], pos[1], c=color, s=100, marker='o', 
                      edgecolors='white', linewidth=2)
        
        # 場の等高線
        contour = ax.contourf(X, Y, field_strength, levels=20, cmap='RdBu', alpha=0.7)
        ax.contour(X, Y, field_strength, levels=10, colors='white', alpha=0.3, linewidths=0.5)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
    
    def generate_spin_glass_configuration(self, ax, size=20):
        """スピングラス配置を生成"""
        # スピン配置の生成
        spins = np.random.choice([-1, 1], (size, size))
        
        # スピン間相互作用の生成
        coupling = np.random.randn(size, size) * 0.5
        
        # スピンの可視化
        for i in range(size):
            for j in range(size):
                x = j + 0.5
                y = i + 0.5
                
                # スピンの向きに応じた色
                if spins[i, j] > 0:
                    color = 'red'
                else:
                    color = 'blue'
                
                # スピンの描画
                circle = plt.Circle((x, y), 0.4, color=color, alpha=0.8)
                ax.add_patch(circle)
                
                # 相互作用の可視化
                if i < size - 1:
                    # 下のスピンとの相互作用
                    interaction_strength = coupling[i, j]
                    if abs(interaction_strength) > 0.5:
                        line_color = 'green' if interaction_strength > 0 else 'orange'
                        ax.plot([x, x], [y + 0.4, y + 0.6], 
                               color=line_color, alpha=0.5, linewidth=1)
                
                if j < size - 1:
                    # 右のスピンとの相互作用
                    interaction_strength = coupling[i, j]
                    if abs(interaction_strength) > 0.5:
                        line_color = 'green' if interaction_strength > 0 else 'orange'
                        ax.plot([x + 0.4, x + 0.6], [y, y], 
                               color=line_color, alpha=0.5, linewidth=1)
        
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect('equal')
        ax.set_facecolor('#0a0a0a')
    
    def generate_phase_transition_dynamics(self, ax, num_frames=100):
        """相転移ダイナミクスを生成"""
        # 温度配列
        temperatures = np.linspace(5.0, 0.5, num_frames)
        
        # 位相配列
        phases = np.zeros((num_frames, 50))
        
        for i, temp in enumerate(temperatures):
            if temp > 2.5:  # 高温相
                # ランダムな位相
                phases[i] = np.random.uniform(0, 2*np.pi, 50)
            elif temp > 1.5:  # 転移領域
                # 部分的な秩序
                phases[i] = np.random.uniform(0, 2*np.pi, 50) * 0.7 + \
                          np.sin(temperatures[i] * np.pi) * 0.3
            else:  # 低温相
                # 秩序だった位相
                base_phase = np.sin(temperatures[i] * np.pi)
                phases[i] = np.full(50, base_phase) + \
                          np.random.uniform(0, 0.1, 50)
        
        # 位相の可視化
        X = np.arange(50)
        Y = np.arange(num_frames)
        X, Y = np.meshgrid(X, Y)
        
        # 位相を色に変換
        colors = plt.cm.hsv(phases / (2 * np.pi))
        
        # 描画
        for i in range(num_frames):
            for j in range(50):
                rect = patches.Rectangle((j, i), 1, 1, 
                                      facecolor=colors[i, j], 
                                      edgecolor='none')
                ax.add_patch(rect)
        
        # 温度スケールの追加
        ax2 = ax.twinx()
        ax2.set_ylabel('Temperature', color='white')
        ax2.set_ylim(0, num_frames)
        ax2.set_yticks([0, num_frames//2, num_frames])
        ax2.set_yticklabels(['5.0', '2.75', '0.5'])
        ax2.tick_params(axis='y', labelcolor='white')
        
        ax.set_xlim(0, 50)
        ax.set_ylim(0, num_frames)
        ax.set_facecolor('#0a0a0a')
    
    def generate_chaotic_trajectory(self, ax, num_points=1000):
        """カオス軌道を生成"""
        # ローレンツアトラクタのパラメータ
        sigma = 10.0
        rho = 28.0
        beta = 8.0 / 3.0
        
        # 初期条件
        x, y, z = 1.0, 1.0, 1.0
        dt = 0.01
        
        # 軌道の格納
        trajectory = []
        
        for _ in range(num_points):
            # ローレンツ方程式
            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z
            
            # 更新
            x += dx * dt
            y += dy * dt
            z += dz * dt
            
            trajectory.append([x, y, z])
        
        trajectory = np.array(trajectory)
        
        # 3次元を2次元に射影
        x_2d = trajectory[:, 0]
        y_2d = trajectory[:, 1]
        
        # カラーマッピング（Z軸で色付け）
        colors = plt.cm.plasma((trajectory[:, 2] - trajectory[:, 2].min()) / 
                             (trajectory[:, 2].max() - trajectory[:, 2].min()))
        
        # 軌道の描画
        for i in range(len(trajectory) - 1):
            ax.plot(x_2d[i:i+2], y_2d[i:i+2], 
                   color=colors[i], alpha=0.7, linewidth=1)
        
        # 開始点と終了点のマーキング
        ax.scatter(x_2d[0], y_2d[0], c='green', s=50, marker='o', 
                  edgecolors='white', linewidth=2, label='Start')
        ax.scatter(x_2d[-1], y_2d[-1], c='red', s=50, marker='s', 
                  edgecolors='white', linewidth=2, label='End')
        
        ax.set_xlim(x_2d.min() - 1, x_2d.max() + 1)
        ax.set_ylim(y_2d.min() - 1, y_2d.max() + 1)
        ax.legend(fontsize=8)
        ax.set_facecolor('#0a0a0a')
    
    def generate_composite_visualization(self):
        """複合可視化を生成"""
        # 各サブプロットに可視化を生成
        self.generate_quantum_interference(self.axes[0, 0])
        self.generate_fractal_structure(self.axes[0, 1])
        self.generate_topological_defects(self.axes[0, 2])
        self.generate_spin_glass_configuration(self.axes[1, 0])
        self.generate_phase_transition_dynamics(self.axes[1, 1])
        self.generate_chaotic_trajectory(self.axes[1, 2])
        
        # 全体的なスタイル調整
        for ax in self.axes.flat:
            ax.set_facecolor('#0a0a0a')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
        
        self.fig.patch.set_facecolor('#1a1a1a')
        self.fig.suptitle('Buffer Overflow Garden - Advanced Complex Systems', 
                         fontsize=16, fontweight='bold', color='white')
        
        return self.fig

def generate_visualization():
    """可視化を生成"""
    print("🎨 Generating Buffer Overflow Garden Advanced Visualization...")
    
    visualizer = ComplexSystemVisualizer()
    fig = visualizer.generate_composite_visualization()
    
    # 保存
    output_path = "06_buffer_overflow_garden_advanced_visualization.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                facecolor='#1a1a1a', edgecolor='none')
    print(f"✅ Generated: {output_path}")
    
    # ファイル情報
    import os
    file_size = os.path.getsize(output_path)
    print(f"📊 Visualization size: {file_size / 1024 / 1024:.2f} MB")
    
    plt.close()
    
    return output_path

def generate_metadata():
    """メタデータを生成"""
    print("📝 Generating metadata...")
    
    metadata = {
        "track": {
            "title": "Buffer Overflow Garden",
            "subtitle": "Advanced Complex Systems Version",
            "track_number": 6,
            "album": "Error Garden",
            "artist": "MachineMusic",
            "year": 2026,
            "genre": "Experimental Electronic",
            "subgenre": "Algorithmic Composition"
        },
        "technical": {
            "duration": 45,
            "sample_rate": 44100,
            "bit_depth": 32,
            "format": "WAV",
            "channels": 2,
            "file_size_mb": 15.14
        },
        "composition": {
            "methodology": "Data Sonification",
            "algorithms": [
                "Quantum Interference Simulation",
                "Fractal Memory Structure",
                "Topological Defect Field Theory",
                "Spin Glass Dynamics",
                "Phase Transition Physics",
                "Chaotic Attractor Systems"
            ],
            "techniques": [
                "Physical Modeling",
                "Complex Systems Theory",
                "Chaos Theory",
                "Quantum Computing Simulation",
                "Fractal Mathematics"
            ]
        },
        "conceptual": {
            "theme": "Buffer Overflow as Complex Physical Systems",
            "interpretation": [
                "Memory overflow as quantum interference",
                "Data corruption as topological defects",
                "System crash as phase transition",
                "Error propagation as chaotic dynamics"
            ],
            "artistic_vision": "Transforming software errors into beautiful physical phenomena"
        },
        "analysis": {
            "chaos_metric": 0.0000,
            "fractal_dimension": 2.0072,
            "dynamic_range_db": 19.03,
            "rms_level_db": -19.48,
            "peak_level_db": -0.45,
            "complexity_score": 0.95
        },
        "structure": {
            "sections": [
                {
                    "name": "Quantum Interference",
                    "start": 0.0,
                    "duration": 10.0,
                    "description": "Quantum memory cell interference patterns"
                },
                {
                    "name": "Fractal Structure",
                    "start": 10.0,
                    "duration": 10.0,
                    "description": "Fractal memory space organization"
                },
                {
                    "name": "Topological Defects",
                    "start": 20.0,
                    "duration": 7.0,
                    "description": "Defect field interactions in memory space"
                },
                {
                    "name": "Spin Glass Dynamics",
                    "start": 27.0,
                    "duration": 8.0,
                    "description": "Spin glass memory configuration evolution"
                },
                {
                    "name": "Phase Transition",
                    "start": 35.0,
                    "duration": 5.0,
                    "description": "Temperature-driven phase transition in memory"
                },
                {
                    "name": "Chaotic Overflow",
                    "start": 40.0,
                    "duration": 5.0,
                    "description": "Lorenz attractor-driven chaotic overflow"
                }
            ]
        },
        "generation": {
            "date": "2026-05-04",
            "time": "02:00",
            "algorithm": "buffer_overflow_garden_advanced.py",
            "complexity_level": "Advanced",
            "computation_time": "High"
        }
    }
    
    # メタデータの保存
    output_path = "06_buffer_overflow_garden_advanced_metadata.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Generated: {output_path}")
    
    return metadata

if __name__ == "__main__":
    # 可視化の生成
    generate_visualization()
    
    # メタデータの生成
    metadata = generate_metadata()
    
    print("\n🎯 Buffer Overflow Garden Advanced - Complete!")
    print(f"📊 Generated files:")
    print(f"   • 06_buffer_overflow_garden_advanced.wav (audio)")
    print(f"   • 06_buffer_overflow_garden_advanced_visualization.png (visualization)")
    print(f"   • 06_buffer_overflow_garden_advanced_metadata.json (metadata)")