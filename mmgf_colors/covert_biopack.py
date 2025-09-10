

datalad create-sibling-ria --storage-sibling only --shared group -s ria-datalad-test --alias datalad-test --new-store-ok "ria+ssh://massstorage.giga.priv/massstorage/URT/CRC/PC/SHARE/01_DATASETS/DATALAD/2024_datalad_test"
#%%
import bioread
import pandas as pd
import json
from pathlib import Path
import numpy as np

# Load the .acq file
orig_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/Experiment")
bids_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/bids")

participants_df = pd.read_csv(bids_path / "participants.tsv", sep='\t')
# %%
subjects = participants_df['experiment_id'].values


ids = np.array(range(23, 34))
conditions = ['Rest', 'Green', 'Red']
sesions = ['Day1', 'Day2']
physio_signals = {
        'ecg': 0,  # ECG is 1st channel
        'eda': 1,  # EDA is 2nd channel
        'resp': 2   # RESP is 3rd channel
    }

participants_df = pd.read_csv(bids_path / "participants.tsv", sep='\t')
condition_mapping = {}
for _, row in participants_df.iterrows():
    condition_mapping[row["experiment_id"]] = {
        "red_session": row["red_session"],
        "green_session": row["green_session"]
    }
    
# %%
for id in ids:
    subj_bids = f"sub-{id:02d}"
    subj_exp = subjects[id - 23]
    print(f"Processing {subj_exp} -> {subj_bids}")

    # Load the .acq file for each subject]
    subj_conditions = condition_mapping[subj_exp]
    for condition in conditions:
        print(f"Processing condition: {condition}")
        for sesion in sesions:
            if condition == 'Rest':
                actual_condition = 'Rest'
            else:
                # Check if this session was Red or Green
                if sesion == 'Day1':
                    ses_bids = 'ses-01'
                else:
                    ses_bids = 'ses-02'
                
                if subj_conditions["red_session"] == ses_bids:
                    actual_condition = 'Red'
                elif subj_conditions["green_session"] == ses_bids:
                    actual_condition = 'Green'
                else:
                    raise ValueError(f"Invalid session mapping for {subj_exp}")

            data = bioread.read_file(orig_path /
                                    subj_exp /
                                    "Bio" /
                                    f"{subj_exp}_{sesion}_{actual_condition}.acq")
            
            df = pd.DataFrame({
                'time': data.channels[0].time_index,
                'ecg': data.channels[0].data,
                'eda': data.channels[1].data,
                'resp': data.channels[2].data,
                'trigger': data.channels[11].data
            })
            if sesion == 'Day1':
                sesion_bids = 'ses-01'
            else:
                sesion_bids = 'ses-02'
            df.to_csv(bids_path /
                    subj_bids /
                    sesion_bids /
                    'eeg' /
                    f'{subj_bids}_{sesion_bids}_task-{actual_condition.lower()}_physio.tsv.gz',
                    sep='\t', index=False, compression='gzip')
                
                # Create the JSON metadata file
            fs = data.channels[0].samples_per_second  # Sampling frequency
            metadata = {
                    "SignalType" : {
                            "ecg": {
                                "Name": "Electrocardiogram",
                                "Description": "continuous ECG signal by electrodes"},
                            "eda": {
                                "Name": "Electrodermal Activity",
                                "Description": "continuous EDA signal by electrodes placed on the fingers"
                            },
                            "resp":  {
                                "Name": "Respiration",
                                "Description": "continuous Respiration signal by respiration belt"
                            },
                                "trigger": {
                                     "Name": "Syncronization Triggers",
                                     "Description": "continuous measurement of the scanner trigger signal (start - sync - end)"
                    }
                        },
                    "SamplingFrequency": fs,
                    "StartTime": 0.0,
                    "TaskName": actual_condition,
                     "Columns": [
                                "time",
                                "ecg",
                                "eda",
                                "resp",
                                "trigger"
                            ]
                }
            with open((bids_path /
                        subj_bids /
                        sesion_bids /
                        'eeg' /
                        f'{subj_bids}_{sesion_bids}_task-{actual_condition.lower()}_physio.json'), 'w') as f:
                    json.dump(metadata, f, indent=4)

# %%
