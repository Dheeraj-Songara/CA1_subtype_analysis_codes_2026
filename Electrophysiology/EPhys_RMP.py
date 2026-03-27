import pyabf
import glob
import os
import numpy as np
import pandas as pd

# Parameters based on 20 kHz sampling rate
SAMPLE_RATE = 20000  # Hz (points per second)
RMP_START_SEC = 50   # Start averaging at 50 seconds
RMP_END_SEC = 60     # End averaging at 60 seconds

def main():
    path = input('Paste path and add \\*.abf = ').strip()
    abf_files = glob.glob(os.path.abspath(path))
    
    rmp_list = []
    c_list = []

    for file in abf_files:
        head, tail = os.path.split(file)
        c_list.append(tail)
        abf = pyabf.ABF(file)

        abf.setSweep(sweepNumber=0, channel=0)
        y = abf.sweepY

        # Convert time in seconds to data indices
        start_idx = int(RMP_START_SEC * SAMPLE_RATE)
        end_idx = int(RMP_END_SEC * SAMPLE_RATE)
        
        # Calculate mean voltage over the specified window
        rmp = np.mean(y[start_idx:end_idx])
        rmp_list.append(rmp)

    df = pd.DataFrame(index=['RMP (mV)'])
    for i in range(len(c_list)):
        df[c_list[i]] = [rmp_list[i]]

    df.to_csv('RMP.csv')
    print('RMP extraction complete. Saved to RMP.csv')

if __name__ == "__main__":
    main()