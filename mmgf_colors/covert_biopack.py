#%%
import bioread
import pandas as pd
import json
from pathlib import Path
import numpy as np

# Load the .acq file
orig_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/Experiment")
bids_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/bids")

# %%
subjects = [ 'JLThF', 'v5JIp3', 'slgYBn', # 'Q1j7zZ',
            'dtBMqk', 'HGilrt', 'TQGSAt', '8G4Toy',
            'h9xeMl', 'X6Squs', '8S8MzT', 'hUw3f5',
            '1UN2mL', 'LzzOuF', 'o3bo3y', 'VKS9r8',
            'BA20Azs', 'PxRS25', 'xOkoxy', '15mylQ',
            'LCICX2','edjLpb','aE0coZ', 'IO0rKz',
            '8tqhpL','6XszFa', 'xKyNgi', 'JjqSZG',
            'YU7rtf3', 'I9NFNr','eDHRnz', 'hJ89u1',
            'Zk7NxE']


ids = np.array(range(2, 34))
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
    subj_exp = subjects[id - 2]
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
            

            # Create the subject files
            for signal, idx in physio_signals.items():
                print(f"Processing signal: {signal}")
                df = pd.DataFrame({
                    'time': data.channels[idx].time_index,
                    'signal': data.channels[idx].data
                })
                if sesion == 'Day1':
                    sesion_bids = 'ses-01'
                else:
                    sesion_bids = 'ses-02'
                df.to_csv(bids_path /
                        subj_bids /
                        'eeg' /
                        sesion_bids /
                        f'{subj_bids}_{sesion_bids}_task-{actual_condition.lower()}_recording-{signal}_physio.tsv.gz',
                        sep='\t', index=False, compression='gzip')
                
                # Create the JSON metadata file
                fs = data.channels[idx].samples_per_second  # Sampling frequency
                metadata = {
                    "SignalType": signal.upper(),
                    "SamplingFrequency": fs,
                    "StartTime": 0.0,
                    "Columns": ["time", "signal"],
                    "TaskName": actual_condition
                }
                with open((bids_path /
                        subj_bids /
                        'eeg' /
                        sesion_bids /
                        f'{subj_bids}_{sesion_bids}_task-{actual_condition.lower()}_recording-{signal}_physio.json'), 'w') as f:
                    json.dump(metadata, f, indent=4)
            # Events file
            print("Processing events")
            triggers = np.unique((data.channels[11].time_index[data.channels[11].data > 0]).astype(int))


            events = pd.DataFrame({
                'onset': triggers,
                'duration': [0] * len(triggers),
                'trial_type': ["start"] + ['sync_trigger'] * (len(triggers) - 2) + ["end"]
            })
            events.to_csv(bids_path /
                        subj_bids /
                        'eeg' /
                        sesion_bids /
                        f'{subj_bids}_{sesion_bids}_task-{actual_condition.lower()}_recording-physio_events.tsv',
                        sep='\t', index=False)
            
            # Create the JSON metadata file for events  
            metadata_events = {
                "onset": "Time in seconds when the event starts",
                "duration": "Duration of the event in seconds",
                "trial_type":
                    {
                        "Description" : "Type of event",
                        "Levels":
                            {
                                "start": "Start of the session",
                                "sync_trigger": "Sync trigger for the session",
                                "end": "End of the session"
                            }
                    }
            }
            with open((bids_path /
                        subj_bids /
                        'eeg' /
                        sesion_bids /
                        f'{subj_bids}_{sesion_bids}_task-{actual_condition.lower()}_recording-physio_events.json'), 'w') as f:
                json.dump(metadata_events, f, indent=4)
            print(f"Processed {subj_bids} {sesion_bids} {actual_condition} successfully.")
           





# %%
