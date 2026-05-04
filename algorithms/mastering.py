#!/usr/bin/env python3
"""
MachineMusic - Error Garden Mastering Script

各トラックの音量を分析・調整し、アルバム全体の統一感を作る
"""

import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import os
from pathlib import Path

def read_wav_file(filepath):
    """WAVファイルを読み込む"""
    sample_rate, data = wavfile.read(filepath)
    
    # ステレオの場合はモノラルに変換
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    
    # 正規化（-1.0から1.0の範囲に）
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.uint8:
        data = (data.astype(np.float32) - 128.0) / 128.0
    
    return sample_rate, data

def calculate_rms(audio):
    """RMSレベルを計算"""
    return np.sqrt(np.mean(audio**2))

def calculate_peak(audio):
    """ピークレベルを計算"""
    return np.max(np.abs(audio))

def normalize_audio(audio, target_peak_db=-1.0):
    """音声を正規化する（指定されたピークレベルに）"""
    current_peak = calculate_peak(audio)
    if current_peak > 0:
        target_peak = 10 ** (target_peak_db / 20.0)
        scaling_factor = target_peak / current_peak
        return audio * scaling_factor
    return audio

def analyze_track(filepath):
    """トラックの音量分析"""
    sample_rate, audio = read_wav_file(filepath)
    
    rms_db = 20 * np.log10(calculate_rms(audio) + 1e-10)
    peak_db = 20 * np.log10(calculate_peak(audio) + 1e-10)
    
    return {
        'sample_rate': sample_rate,
        'duration': len(audio) / sample_rate,
        'rms_db': rms_db,
        'peak_db': peak_db,
        'audio': audio
    }

def apply_mastering(audio, target_rms_db=-16.0, target_peak_db=-1.0):
    """マスタリング処理を適用"""
    # まずピーク正規化
    normalized = normalize_audio(audio, target_peak_db)
    
    # RMSレベルを調整
    current_rms_db = 20 * np.log10(calculate_rms(normalized) + 1e-10)
    if current_rms_db < target_rms_db:
        gain_db = target_rms_db - current_rms_db
        gain_linear = 10 ** (gain_db / 20.0)
        mastered = normalized * gain_linear
        # 再度ピーククリップ
        mastered = np.clip(mastered, -10 ** (target_peak_db / 20.0), 
                          10 ** (target_peak_db / 20.0))
    else:
        mastered = normalized
    
    return mastered

def save_wav_file(filepath, sample_rate, audio):
    """WAVファイルを保存する"""
    # 16-bit intに変換
    audio_int16 = (audio * 32767.0).astype(np.int16)
    wavfile.write(filepath, sample_rate, audio_int16)

def master_album(samples_dir, mastered_dir):
    """アルバム全体のマスタリング"""
    samples_path = Path(samples_dir)
    mastered_path = Path(mastered_dir)
    
    # マスタリング用ディレクトリを作成
    mastered_path.mkdir(exist_ok=True)
    
    # トラックファイルをソート
    track_files = sorted([f for f in samples_path.glob("*.wav")])
    
    analysis_results = []
    
    print("🎵 MachineMusic - Error Garden Mastering")
    print("=" * 50)
    
    for track_file in track_files:
        track_name = track_file.name
        print(f"\n🔍 Analyzing: {track_name}")
        
        # トラック分析
        analysis = analyze_track(str(track_file))
        analysis['name'] = track_name
        analysis_results.append(analysis)
        
        print(f"   Duration: {analysis['duration']:.2f}s")
        print(f"   RMS: {analysis['rms_db']:.1f} dB")
        print(f"   Peak: {analysis['peak_db']:.1f} dB")
        
        # マスタリング適用
        mastered_audio = apply_mastering(analysis['audio'])
        
        # マスタリング後の分析
        mastered_rms = 20 * np.log10(calculate_rms(mastered_audio) + 1e-10)
        mastered_peak = 20 * np.log10(calculate_peak(mastered_audio) + 1e-10)
        
        print(f"   Mastered RMS: {mastered_rms:.1f} dB")
        print(f"   Mastered Peak: {mastered_peak:.1f} dB")
        
        # 保存
        output_path = mastered_path / f"mastered_{track_name}"
        save_wav_file(str(output_path), analysis['sample_rate'], mastered_audio)
        print(f"   ✅ Saved: {output_path}")
    
    # 全体のサマリー
    print("\n" + "=" * 50)
    print("📊 Mastering Summary")
    print("=" * 50)
    
    total_duration = sum(result['duration'] for result in analysis_results)
    print(f"Total Duration: {total_duration/60:.1f} minutes")
    
    avg_rms = np.mean([result['rms_db'] for result in analysis_results])
    avg_peak = np.mean([result['peak_db'] for result in analysis_results])
    print(f"Average RMS (original): {avg_rms:.1f} dB")
    print(f"Average Peak (original): {avg_peak:.1f} dB")
    
    print("\n🎉 Mastering completed!")
    print(f"📁 Mastered files saved to: {mastered_path}")
    
    return analysis_results

if __name__ == "__main__":
    # マスタリング実行
    results = master_album("samples", "samples_mastered")
    
    # 可視化（オプション）
    try:
        plt.figure(figsize=(12, 8))
        
        # RMSレベルの比較
        plt.subplot(2, 1, 1)
        original_rms = [r['rms_db'] for r in results]
        track_names = [r['name'] for r in results]
        
        plt.bar(range(len(original_rms)), original_rms, alpha=0.7, label='Original')
        plt.axhline(y=-16, color='r', linestyle='--', label='Target RMS')
        plt.ylabel('RMS Level (dB)')
        plt.title('MachineMusic - Error Garden: Track RMS Levels')
        plt.xticks(range(len(track_names)), [name.replace('.wav', '') for name in track_names], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # ピークレベルの比較
        plt.subplot(2, 1, 2)
        original_peaks = [r['peak_db'] for r in results]
        
        plt.bar(range(len(original_peaks)), original_peaks, alpha=0.7, color='orange', label='Original')
        plt.axhline(y=-1, color='r', linestyle='--', label='Target Peak')
        plt.ylabel('Peak Level (dB)')
        plt.xlabel('Tracks')
        plt.title('MachineMusic - Error Garden: Track Peak Levels')
        plt.xticks(range(len(track_names)), [name.replace('.wav', '') for name in track_names], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('mastering_analysis.png', dpi=150, bbox_inches='tight')
        print("📊 Visualization saved: mastering_analysis.png")
        
    except Exception as e:
        print(f"⚠️  Visualization failed: {e}")