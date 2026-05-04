#!/usr/bin/env python3
"""
Deadlock Dance Advanced Short Test - 短縮版テスト
"""

import algorithms.deadlock_dance_advanced as dda
import time

def main():
    try:
        print("Starting Deadlock Dance Advanced Short Test...")
        
        # 短縮版でテスト (15秒)
        print("Creating composer with 15-second duration...")
        composer = dda.DeadlockDanceAdvanced(duration=15)
        
        print("Generating composition...")
        start_time = time.time()
        
        # 楽曲の生成
        stereo_signal, time_array, deadlock_pattern = composer.generate_composition()
        
        generation_time = time.time() - start_time
        print(f"Composition generated in {generation_time:.2f} seconds")
        
        print("Creating visualization...")
        # 可視化の作成
        fig = composer.create_visualization(time_array, deadlock_pattern, stereo_signal)
        
        print("Saving files...")
        # 音声ファイルの保存
        output_path = composer.output_dir / "07_deadlock_dance_advanced_short.wav"
        import soundfile as sf
        sf.write(output_path, stereo_signal.T, composer.sample_rate)
        print(f"Audio saved to: {output_path}")
        
        # 可視化の保存
        viz_path = composer.output_dir / "07_deadlock_dance_advanced_short_visualization.png"
        fig.savefig(viz_path, dpi=150, bbox_inches='tight')
        print(f"Visualization saved to: {viz_path}")
        
        # ファイルサイズの確認
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"Audio file size: {file_size:,} bytes")
        
        print("Short test completed successfully!")
        
        # 成功した場合、本番版を実行するかどうかの確認
        print("\n" + "="*50)
        print("Short test successful! Ready for full version.")
        print("To run full version (3 minutes):")
        print("python3 algorithms/deadlock_dance_advanced.py")
        print("="*50)
        
    except Exception as e:
        print(f"Error in short test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()