

#%%
import bioread
import pandas as pd
import json
from pathlib import Path
import numpy as np
import glob

# Load the .acq file
orig_path = Path("/data/project/anchor_eeg/dataset/anchor_eeg")
bids_path = Path("/data/project/anchor_eeg/dataset/anchor_eeg")

# %%
for path in orig_path.glob("sub-*"):
    print(path)
    subj = path.name
    print(f"Processing {subj}")
    
    single_file = path / 'physio' / f"{subj}_physio.acq"
    percondition_file = path / 'physio' / f"{subj}_task-DB.acq"

    if single_file.exists():
        data = bioread.read_file(single_file)
        condition = 'ALL'  
        channels_all = pd.DataFrame()
        for channel in data.channels:
            channel = pd.DataFrame({f'{channel.name.split(' ')[0]}': channel.data})
            channels_all = pd.concat([channels_all, channel], axis=1)
        channels_all['time'] = data.channels[0].time_index

        channels_all.to_csv(path /
                            'eeg' /
                            f'{subj}_task-{condition}_physio.tsv.gz',
                            sep='\t', index=False, compression='gzip')
                    
    # Create the JSON metadata file
        fs = data.channels[0].samples_per_second  # Sampling frequency
        metadata = {
                        "SignalType" : {
                                "ecg": {
                                    "Name": "Electrocardiogram",
                                    "Description": "continuous ECG signal by electrodes"},
                                "resp":  {
                                    "Name": "Respiration",
                                    "Description": "continuous Respiration signal by respiration belt"
                                },
                                    "trigger": {
                                        "Name": "Syncronization Triggers (DIG)",
                                        "Description": "continuous measurement of the scanner trigger signal (start - sync - end)"
                        }
                            },
                        "SamplingFrequency": fs,
                        "StartTime": 0.0,
                        "TaskName": {
                            "ALL":{
                                "Name": "All task (DB - IHT - Math)",
                                "Description" : "contains all tasks in the same file"
                            }
                        },
                        "Columns": list(channels_all)
                    }
        with open((path /
                    'eeg' /
                                f'{subj}_task-{condition}_physio.json'), 'w') as f:
                        json.dump(metadata, f, indent=4)

    elif percondition_file.exists():
        conditions = ['DB', 'IHT', 'Math', 
                      'Math_VRDT', 'IHT_VRDT', 'DB_VRDT']
        
        
           
