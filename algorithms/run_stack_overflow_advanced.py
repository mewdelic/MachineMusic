#!/usr/bin/env python3
"""
Stack Overflow Advanced 簡易実行スクリプト
"""

import os
import sys

# カレントディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms.stack_overflow_advanced import StackOverflowAdvanced

def main():
    """メイン実行関数"""
    print("MachineMusic - Stack Overflow Advanced")
    print("=" * 50)
    
    # 生成器のインスタンス化と実行
    generator = StackOverflowAdvanced(
        sample_rate=44100,
        duration=180  # 3分
    )
    
    generator.run()
    
    print("\n生成完了！")
    print("ファイルは samples/ ディレクトリに保存されています。")

if __name__ == "__main__":
    main()