import efel
import numpy as np
import pyabf
import glob
import os
import pandas as pd

STIM_DURATION_MS = 750  # Duration of your hyperpolarizing current step

def main():
    path = input('Paste path and add \\*.abf = ').strip()
    abf_files = glob.glob(os.path.abspath(path))
    
    f_list = []
    c_list = []

    for file in abf_files:
        head, tail = os.path.split(file)
        c_list.append(tail)
        abf = pyabf.ABF(file)
        
        # Detect stimulus start time from the command waveform
        abf.setSweep(sweepNumber=abf.sweepCount - 1, channel=0)
        time_ms = abf.sweepX * 1000
        peak_index = np.argmin(abf.sweepC)
        stim_start = time_ms[peak_index]
        stim_end = stim_start + STIM_DURATION_MS
        
        sag_amp = []
        sag_ratio = []
        
        for s in range(abf.sweepCount):
            abf.setSweep(sweepNumber=s, channel=0)
            
            sweep_data = [{
                "T": time_ms,
                "V": abf.sweepY,
                "stim_start": [stim_start],
                "stim_end": [stim_end]
            }]
            
            features = efel.getFeatureValues(sweep_data, ['sag_amplitude', 'sag_ratio1'])[0]
            
            if features['sag_amplitude'] is not None:
                sag_amp.append(features['sag_amplitude'][0])
            if features['sag_ratio1'] is not None:
                sag_ratio.append(features['sag_ratio1'][0])
                
        f_list.append([
            np.mean(sag_amp) if sag_amp else np.nan, 
            np.mean(sag_ratio) if sag_ratio else np.nan
        ])

    index = ['sag_amplitude', 'sag_ratio1']
    df = pd.DataFrame(index=index)

    for i in range(len(c_list)):
        df[c_list[i]] = f_list[i]

    df.to_csv('Ih_feature.csv')
    print('Ih Sag extraction complete. Saved to Ih_feature.csv')

if __name__ == "__main__":
    main()