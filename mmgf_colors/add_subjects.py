# %% Imports
import numpy as np
import pandas as pd
from pathlib import Path
import mne
import pandas as pd
from mne_bids.copyfiles import copyfile_brainvision

# %%

orig_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/Experiment")
bids_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/bids")

subjects = [ #'xOkoxy', '15mylQ','LCICX2','edjLpb','aE0coZ', 
            #'IO0rKz', '8tqhpL','6XszFa',  'xKyNgi', 'JjqSZG',
            ##'YU7rtf3', 29 tiene problemas hacerlo despues manual
              'I9NFNr',
            'eDHRnz', 'hJ89u1', 'Zk7NxE']

ids = np.array(range(30, 34))
participants = pd.read_csv(bids_path / "participants.tsv", sep="\t", dtype=str)

# participant = {
#     "participant_id": [],
#     "experiment_id": [],
#     "green_session": [],
#     "red_session": [],
# }
# %%
for id in ids:
    subj_bids = f"sub-{id:02d}"
    subj_exp = subjects[id - 30]
    print(f"Processing {subj_exp} -> {subj_bids}")

    subj_dir = bids_path / subj_bids
    subj_dir.mkdir(parents=True, exist_ok=True)

    # Create the EEG directory
    eeg_dir = subj_dir / "eeg"
    eeg_dir.mkdir(parents=True, exist_ok=True)

    # Create the sessions directories
    ses_1_dir = eeg_dir / "ses-01"
    ses_2_dir = eeg_dir / "ses-02"
    ses_1_dir.mkdir(parents=True, exist_ok=True)
    ses_2_dir.mkdir(parents=True, exist_ok=True)

    # Copy the EEG files
    day1_rest_fname = orig_path / subj_exp / "EEG" / f"{subj_exp}_Day1_Rest.vhdr"
    day2_rest_fname = orig_path / subj_exp / "EEG" / f"{subj_exp}_Day2_Rest.vhdr"
    day1_green_fname = orig_path / subj_exp / "EEG" / f"{subj_exp}_Day1_Green.vhdr"
    day2_green_fname = orig_path / subj_exp /"EEG" / f"{subj_exp}_Day2_Green.vhdr"
    day1_red_fname = orig_path / subj_exp / "EEG" / f"{subj_exp}_Day1_Red.vhdr"
    day2_red_fname = orig_path / subj_exp / "EEG" / f"{subj_exp}_Day2_Red.vhdr"

    if not day1_rest_fname.exists():
        raise RuntimeError(f"File {day1_rest_fname} does not exist")
    print(f"Copying {day1_rest_fname} to {ses_1_dir}")
    copyfile_brainvision(
        day1_rest_fname,
        ses_1_dir / f"{subj_bids}_ses-01_task-rest_eeg.vhdr",
    )
    if not day2_rest_fname.exists():
        raise RuntimeError(f"File {day2_rest_fname} does not exist")
    print(f"Copying {day2_rest_fname} to {ses_2_dir}")
    copyfile_brainvision(
        day2_rest_fname,
        ses_2_dir / f"{subj_bids}_ses-02_task-rest_eeg.vhdr",
    )
    if not day1_green_fname.exists() and not day2_green_fname.exists():
        raise RuntimeError("No GREEN stim")
    day1 = None
    day2 = None
    if not day1_green_fname.exists() and day2_green_fname.exists():
        day1 = "red"
        day2 = "green"
    elif day1_green_fname.exists() and not day2_green_fname.exists():
        day1 = "green"
        day2 = "red"

    if day1 == "green":
        if not day1_green_fname.exists():
            raise RuntimeError(f"File {day1_green_fname} does not exist")
        print(f"Copying {day1_green_fname} to {ses_1_dir}")
        copyfile_brainvision(
            day1_green_fname,
            ses_1_dir / f"{subj_bids}_ses-01_task-green_eeg.vhdr",
        )
    elif day1 == "red":
        if not day1_red_fname.exists():
            raise RuntimeError(f"File {day1_red_fname} does not exist")
        print(f"Copying {day1_red_fname} to {ses_1_dir}")
        copyfile_brainvision(
            day1_red_fname,
            ses_1_dir / f"{subj_bids}_ses-01_task-red_eeg.vhdr",
        )
    if day2 == "green":
        if not day2_green_fname.exists():
            raise RuntimeError(f"File {day2_green_fname} does not exist")
        print(f"Copying {day2_green_fname} to {ses_2_dir}")
        copyfile_brainvision(
            day2_green_fname,
            ses_2_dir / f"{subj_bids}_ses-02_task-green_eeg.vhdr",
        )
    elif day2 == "red":
        if not day2_red_fname.exists():
            raise RuntimeError(f"File {day2_red_fname} does not exist")
        print(f"Copying {day2_red_fname} to {ses_2_dir}")
        copyfile_brainvision(
            day2_red_fname,
            ses_2_dir / f"{subj_bids}_ses-02_task-red_eeg.vhdr",
        )

    participant["participant_id"].append(subj_bids)
    participant["experiment_id"].append(subj_exp)
    if day1 == "green":
        participant["green_session"].append("ses-01")
        participant["red_session"].append("ses-02")
    else:
        participant["red_session"].append("ses-01")
        participant["green_session"].append("ses-02")

# %%
participant_df = pd.DataFrame(participant)
participants = pd.concat([participants, participant_df], ignore_index=True)

# %% Save participants.tsv
participants.to_csv(bids_path / "participants.tsv", sep="\t", index=False)
