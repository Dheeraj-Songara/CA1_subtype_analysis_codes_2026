import pyabf
import glob
import os
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Parameters based on 20 kHz sampling rate
SAMPLE_RATE = 20000
AP_THRESHOLD_DV_DT = 20    # mV/ms
BASELINE_START = 0.5       # seconds (500 ms)
BASELINE_END = 0.6         # seconds (600 ms)

def main():
    path = input('Paste path and add \\*.abf = ').strip()
    abf_files = glob.glob(os.path.abspath(path))
    
    f_list = []
    c_list = []

    for file in abf_files:
        head, tail = os.path.split(file)
        c_list.append(tail)
        abf = pyabf.ABF(file)
        
        f = []
        rheobase_sweep = -1
        
        for s in range(abf.sweepCount):
            abf.setSweep(sweepNumber=s, channel=0)
            x = abf.sweepX
            y = abf.sweepY
            
            # Calculate dv/dt
            dy = np.diff(y) / np.diff(x)
            
            # AP defined as rise >= 20 mV/ms crossing 0 mV
            ap_indices = np.where((dy >= AP_THRESHOLD_DV_DT) & (y[1:] * y[:-1] <= 0))[0]
            f.append(len(ap_indices))
            
            if len(ap_indices) >= 1 and rheobase_sweep == -1:
                rheobase_sweep = s

        # Extract Rheobase Features
        rebs = np.nan
        amp = np.nan
        ths = np.nan
        adp_ind = np.nan
        delay = np.nan
        
        if rheobase_sweep != -1:
            abf.setSweep(sweepNumber=rheobase_sweep, channel=0)
            
            # Rheobase Current
            rbc, _ = find_peaks(abf.sweepC, height=0)
            if len(rbc) > 0:
                rebs = abf.sweepC[rbc[0]]
                
            # Amplitude
            fp, _ = find_peaks(abf.sweepY, height=0)
            if len(fp) > 0:
                vpeak = abf.sweepY[fp[0]]
                b_start = int(BASELINE_START * SAMPLE_RATE)
                b_end = int(BASELINE_END * SAMPLE_RATE)
                baseline = np.mean(abf.sweepY[b_start:b_end])
                amp = vpeak - baseline
                
                # Threshold
                min_index = max(0, fp[0] - 100)
                for idx in range(min_index, fp[0]):
                    if abf.sweepY[idx + 20] - abf.sweepY[idx] >= AP_THRESHOLD_DV_DT:
                        ths = abf.sweepY[idx]
                        break

        # Extract ADP / Delay from sweep 6
        try:
            abf.setSweep(sweepNumber=6, channel=0)
            peaks, _ = find_peaks(abf.sweepY, height=0)
            if len(peaks) > 1:
                first_isi = peaks[1] - peaks[0]
                last_isi = peaks[-1] - peaks[-2]
                adp_ind = 1 - (abf.sweepX[first_isi] / abf.sweepX[last_isi])
                
                # Delay based on assuming stimulus starts at 620ms (index 12401)
                delay = (abf.sweepX[peaks[0]] - abf.sweepX[12401]) * 1000
        except Exception:
            pass

        f.extend([rebs, amp, delay, ths, adp_ind])
        f_list.append(f)

    # Dynamic index generation for current steps + features
    steps_index = [i * 25 for i in range(17)] # Generates 0, 25, 50... 400
    features = ['rheobase (pA)', 'amp of 1st spike (mV)', 'delay of 1st spike (ms)', 'threshold (mV)', 'adp_ind']
    index = steps_index + features

    df = pd.DataFrame(index=index)
    for i in range(len(c_list)):
        # Ensure list lengths match by padding with NaNs if necessary
        col_data = f_list[i]
        if len(col_data) < len(index):
            col_data.extend([np.nan] * (len(index) - len(col_data)))
        elif len(col_data) > len(index):
            col_data = col_data[:len(index)]
            
        df[c_list[i]] = col_data

    df.to_csv('intrinsic.csv')
    print('FI and AP extraction complete. Saved to intrinsic.csv')

if __name__ == "__main__":
    main()