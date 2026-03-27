#!/usr/bin/env python3
"""
freezing_analysis.py

Automated pipeline for detecting freezing behavior in rodent video recordings.
Designed for contextual fear memory assays. 

This script quantifies motion via pixel-intensity differences across consecutive 
frames using OpenCV library and extracts freezing bouts based on customizable threshold and duration parameters.


"""

import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Tuple, Dict

def calculate_motion_scores(video_path: str, start_time: int, duration: int, fps: int) -> Tuple[List[float], int]:
    """
    Reads a video and calculates frame-by-frame motion scores using absolute pixel differences.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video file: {video_path}")

    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_duration = total_frames / fps
    end_time = min(start_time + duration, video_duration)
    
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Set video to the specific start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ret, prev_frame = cap.read()
    if not ret:
        raise ValueError(f"Could not read frame at start time {start_time}s for {video_path}")

    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    
    motion_scores = []
    frame_count = start_frame

    while cap.isOpened() and frame_count < end_frame:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference and threshold
        diff = cv2.absdiff(prev_frame_gray, frame_gray)
        _, diff_thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        motion_score = np.sum(diff_thresh)
        motion_scores.append(motion_score)

        prev_frame_gray = frame_gray
        frame_count += 1

    cap.release()
    return motion_scores, start_frame

def extract_freezing_bouts(motion_scores: List[float], start_frame: int, fps: int, 
                           threshold: int, min_duration_sec: float) -> List[Tuple[float, float, float]]:
    """
    Identifies continuous periods where motion remains below a set threshold.
    """
    freezing_times = []
    freeze_frames = 0
    current_frame = start_frame
    
    for score in motion_scores:
        if score < threshold:
            freeze_frames += 1
        else:
            if (freeze_frames / fps) >= min_duration_sec:
                bout_start = current_frame - freeze_frames
                freezing_times.append((bout_start, current_frame))
            freeze_frames = 0
            
        current_frame += 1

    # Catch any freezing bout that extends to the very last frame
    if (freeze_frames / fps) >= min_duration_sec:
        bout_start = current_frame - freeze_frames
        freezing_times.append((bout_start, current_frame))

    # Convert frames to seconds
    freezing_seconds = [
        (start / fps, end / fps, (end - start) / fps)
        for start, end in freezing_times
    ]
    
    return freezing_seconds

def plot_and_save_trace(motion_scores: List[float], freezing_bouts: List[Tuple[float, float, float]], 
                        start_time: int, fps: int, threshold: int, out_path: str):
    """
    Generates and saves a visual trace of the motion score with freezing bouts highlighted.
    """
    plt.figure(figsize=(12, 4))
    time_axis = np.arange(len(motion_scores)) / fps + start_time
    
    plt.plot(time_axis, motion_scores, label="Motion Score", color='#2c3e50', linewidth=1)
    plt.axhline(y=threshold, color='#e74c3c', linestyle='--', label="Freezing Threshold")
    
    for start, end, _ in freezing_bouts:
        plt.axvspan(start, end, color='#3498db', alpha=0.3)
        
    plt.xlabel("Time (seconds)", fontsize=12)
    plt.ylabel("Motion Score (A.U.)", fontsize=12)
    plt.title("Locomotor Activity and Freezing Bouts", fontsize=14)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # --- Experimental Parameters ---
    FPS = 25 #chnaged based on the video                              
    DURATION_SEC = 180                     
    MOTION_THRESHOLD = 200000 
    #Try different threshhold 100000, 200000 and calibrate with manual freezing detection         
    MIN_FREEZE_DUR_SEC = 0.5               
    
    # Map of video files to their respective start times (in seconds)
    experimental_metadata: Dict[str, int] = {
        "animal_1": 25,
        "animal_2": 27"
       
    }

    # Setup output directories for clean repository management
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    summary_data = []

    print("Starting automated freezing analysis...\n" + "-"*40)

    for video_name, start_time in experimental_metadata.items():
        if not os.path.exists(video_name):
            print(f"Warning: {video_name} not found in directory. Skipping.")
            continue
            
        base_name = os.path.splitext(video_name)[0]
        print(f"Processing: {video_name}")

        # 1. Calculate Motion
        scores, start_frame = calculate_motion_scores(
            video_name, start_time, DURATION_SEC, FPS
        )

        # 2. Extract Bouts
        freezing_bouts = extract_freezing_bouts(
            scores, start_frame, FPS, MOTION_THRESHOLD, MIN_FREEZE_DUR_SEC
        )

        # 3. Save Bouts to Excel
        total_freezing = sum(dur for _, _, dur in freezing_bouts)
        
        df = pd.DataFrame(freezing_bouts, columns=["Start (s)", "End (s)", "Duration (s)"])
        total_row = pd.DataFrame([["", "Total Freezing Duration (s)", total_freezing]], columns=df.columns)
        df = pd.concat([df, total_row], ignore_index=True)
        
        excel_path = output_dir / f"{base_name}_bouts.xlsx"
        df.to_excel(excel_path, index=False)

        # 4. Generate Plot
        plot_path = output_dir / f"{base_name}_trace.png"
        plot_and_save_trace(scores, freezing_bouts, start_time, FPS, MOTION_THRESHOLD, plot_path)

        # Append to summary
        summary_data.append({
            'Subject_ID': base_name,
            'Total_Freezing_Duration_s': total_freezing,
            'Percentage_Freezing': (total_freezing / DURATION_SEC) * 100
        })

    # Save final aggregate summary
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_path = output_dir / "Total_Cohort_Summary.xlsx"
        summary_df.to_excel(summary_path, index=False)
        print(f"\nAnalysis complete. All outputs saved to: ./{output_dir}/")

if __name__ == "__main__":
    main()