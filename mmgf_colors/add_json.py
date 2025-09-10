# %%
import json
from pathlib import Path

bids_path = Path("/data/project/mmgf_colors/2025_MMGF_Colors/bids")

# Template with your specific metadata
eeg_metadata = {
    "TaskName": "",  # Will be filled from filename
    "EEGReference": "FCz",
    "SamplingFrequency": 500,
    "PowerLineFrequency": 50,
    "SoftwareFilters": "n/a",
    "Manufacturer": "BrainVision",
    "ManufacturersModelName": "actiCHamp",
    "EEGResolution": 0.0488281,
    "EEGUnits": "µV"
}

# %%
for eeg_file in bids_path.glob("**/*_eeg.vhdr"):
    json_file = eeg_file.with_suffix('.json')
    
    # Get task name from filename
    task = eeg_file.name.split('task-')[1].split('_')[0]
    
    # Create metadata with task-specific info
    metadata = eeg_metadata.copy()
    metadata["TaskName"] = task.capitalize()  # "green" → "Green"
    
    # Write JSON file
    with open(json_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Created: {json_file}")



# %%
