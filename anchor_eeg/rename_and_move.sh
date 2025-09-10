#!/bin/bash

cd /data/project/anchor_eeg/dataset/anchor_eeg


# Loop through each subject directory
# for sub_dir in sub-*/; do
#     # Extract subject number (remove 'sub-' prefix)
#     sub_num=${sub_dir#sub-}
#     sub_num=${sub_num%/}
    
#     echo "Processing $sub_dir"
    
#     # Process CSV, LOG, and PSYDAT files
#     for file in "$sub_dir"*.csv "$sub_dir"*.log "$sub_dir"*.psydat; do
#         if [[ -f "$file" ]]; then
#             # Extract filename without path
#             filename=$(basename "$file")
            
#             # Extract task name (DB, IHT, or Math)
#             if [[ $filename == DB_* ]]; then
#                 task="DB"
#             elif [[ $filename == IHT_* ]]; then
#                 task="IHT"
#             elif [[ $filename == Math_* ]]; then
#                 task="MATH"
#             elif [[ $filename == MATH_* ]]; then
#                 task="MATH"
#             else
#                 continue # Skip files that don't match expected patterns
#             fi
            
#             # Extract file extension
#             extension="${filename##*.}"
            
#             # Create new filename
#             new_filename="sub-${sub_num}_task-${task}_events.${extension}"
            
#             # Rename the file
#             mv "$file" "$sub_dir$new_filename"
#             echo "Renamed: $filename -> $new_filename"
#         fi
#     done
# done

# for sub_dir in "sub-01/" "sub-02/"; do
#     # Process physio files
#     sub_num=${sub_dir#sub-}
#     sub_num=${sub_num%/}
#     if [[ -f "$sub_dir"sub${sub_num}.acq ]]; then
#         mv "$sub_dir"sub${sub_num}.acq "$sub_dir"physio/sub-${sub_num}_physio.acq
#         echo "Renamed: sub${sub_num}.acq -> sub-${sub_num}_physio.acq"
#     fi
    
#     # Process EEG files
#     if [[ -f "$sub_dir"sub${sub_num}.eeg ]]; then
#         mv "$sub_dir"sub${sub_num}.eeg "$sub_dir"eeg/sub-${sub_num}_eeg.eeg
#         echo "Renamed: sub${sub_num}.eeg -> sub-${sub_num}_eeg.eeg"
#     fi
#     if [[ -f "$sub_dir"sub${sub_num}.vhdr ]]; then
#         mv "$sub_dir"sub${sub_num}.vhdr "$sub_dir"eeg/sub-${sub_num}_eeg.vhdr
#         echo "Renamed: sub${sub_num}.vhdr -> sub-${sub_num}_eeg.vhdr"
#     fi
#     if [[ -f "$sub_dir"sub${sub_num}.vmrk ]]; then
#         mv "$sub_dir"sub${sub_num}.vmrk "$sub_dir"eeg/sub-${sub_num}_eeg.vmrk
#         echo "Renamed: sub${sub_num}.vmrk -> sub-${sub_num}_eeg.vmrk"
#     fi
    
  
#     echo "Files moved to appropriate folders"
#     echo "----------------------------------"
# done


for sub_dir in sub-{03..26}/; do
    # Process physio files
    sub_num=${sub_dir#sub-}
    sub_num=${sub_num%/}

    mkdir -p "$sub_dir"eeg
    mkdir -p "$sub_dir"physio
    mkdir -p "$sub_dir"beh

    if [[ -f "$sub_dir"sub${sub_num}.acq ]]; then
        mv "$sub_dir"sub${sub_num}.acq "$sub_dir"physio/sub-${sub_num}_physio.acq
        echo "Renamed: sub${sub_num}.acq -> sub-${sub_num}_physio.acq"
    fi
    
    if [[ -f "$sub_dir"sub${sub_num}.eeg ]]; then
        mv "$sub_dir"sub${sub_num}.eeg "$sub_dir"eeg/sub-${sub_num}_eeg.eeg
        echo "Renamed: sub${sub_num}.eeg -> sub-${sub_num}_eeg.eeg"
    fi
    if [[ -f "$sub_dir"sub${sub_num}.vhdr ]]; then
        mv "$sub_dir"sub${sub_num}.vhdr "$sub_dir"eeg/sub-${sub_num}_eeg.vhdr
        echo "Renamed: sub${sub_num}.vhdr -> sub-${sub_num}_eeg.vhdr"
    fi
    if [[ -f "$sub_dir"sub${sub_num}.vmrk ]]; then
        mv "$sub_dir"sub${sub_num}.vmrk "$sub_dir"eeg/sub-${sub_num}_eeg.vmrk
        echo "Renamed: sub${sub_num}.vmrk -> sub-${sub_num}_eeg.vmrk"
    fi
    
    for task_file in "$sub_dir"sub-${sub_num}_task-*; do
        if [[ -f "$task_file" ]]; then
            mv "$task_file" "$sub_dir"beh/
            echo "Moved: $(basename "$task_file") -> beh/"
        fi
    done
  
    echo "Files moved to appropriate folders"
    echo "----------------------------------"
done