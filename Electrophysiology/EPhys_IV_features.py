import pyabf
import glob
import os
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import linregress

# --- Parameters ---
SAMPLE_RATE = 20000             # Hz
STIM_DURATION_MS = 1000        # Total length of your current injection step (adjust if yours is 500ms, etc.)
STEADY_STATE_WINDOW_MS = 250    # Averages the last 250ms of the step to get the steady-state voltage

def main():
    path = input('Paste path and add \\*.abf = ').strip()
    abf_files = glob.glob(os.path.abspath(path))
    
    slp_list = []
    c_list = []

    for file in abf_files:
        head, tail = os.path.split(file)
        c_list.append(tail)
        abf = pyabf.ABF(file)
        
        v = []
        I = []
        

        # Sweep 0 is the most hyperpolarized, making it perfect for finding the step onset
        abf.setSweep(sweepNumber=0, channel=0)
        
        # Find the index where the command current drops to its minimum
        stim_start_idx = np.argmin(abf.sweepC)
        
        # Convert MS parameters to data point indices
        stim_duration_idx = int((STIM_DURATION_MS / 1000) * SAMPLE_RATE)
        steady_window_idx = int((STEADY_STATE_WINDOW_MS / 1000) * SAMPLE_RATE)
        
        # Define the exact window to measure (the tail end of the stimulus)
        end_idx = stim_start_idx + stim_duration_idx
        start_idx = end_idx - steady_window_idx
        
        # --- IV EXTRACTION ---
        # Sweeps 0-4 (Hyperpolarizing)
        for s in range(5):
            abf.setSweep(sweepNumber=s, channel=0)
            av = np.mean(abf.sweepY[start_idx:end_idx])
            cur, _ = find_peaks(-abf.sweepC, height=0)
            ic = abf.sweepC[cur[0]] if len(cur) > 0 else 0
            v.append(av)
            I.append(ic)

        # Sweep 5 (0 pA)
        abf.setSweep(sweepNumber=5, channel=0)
        av = np.mean(abf.sweepY[start_idx:end_idx])
        v.append(av)
        I.append(0)

        # Sweep 6 (Mild depolarization, check for no APs)
        abf.setSweep(sweepNumber=6, channel=0)
        peaks, _ = find_peaks(abf.sweepY, height=0)
        if len(peaks) == 0:
            av = np.mean(abf.sweepY[start_idx:end_idx])
            cur, _ = find_peaks(abf.sweepC, height=0)
            ic = abf.sweepC[cur[0]] if len(cur) > 0 else 0
            v.append(av)
            I.append(ic)

        # Linear Regression (V = I * R)
        if len(I) > 1:
            slope, _, _, _, _ = linregress(I, v)
            slp_list.append(slope * 1000) # Convert to MegaOhms
        else:
            slp_list.append(np.nan)

    # --- SAVE RESULTS ---
    df = pd.DataFrame(index=['IR (MegaOhms)'])
    for i in range(len(c_list)):
        df[c_list[i]] = [slp_list[i]]

    df.to_csv('IR.csv')
    print('Input Resistance extraction complete. Saved to IR.csv')

if __name__ == "__main__":
    main()