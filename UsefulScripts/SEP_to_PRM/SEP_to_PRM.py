import pandas as pd
import numpy as np
import random
import os


# Function to calculate R(i) - Range
def calculate_range(x, y, z):
    return np.sqrt(x**2 + y**2 + z**2)


# Function to calculate alpha (azimuth angle)
def calculate_alpha(x, y):
    return np.arctan2(y, x)


# Function to calculate PRM status for a frame within a segment
def calculate_prm_status(segment_frame):
    # Calculate R(i) for each object in the frame
    segment_frame["R"] = calculate_range(
        segment_frame["X"], segment_frame["Y"], segment_frame["Z"]
    )
    segment_frame["alpha"] = calculate_alpha(segment_frame["X"], segment_frame["Y"])

    # Centripetal movement (V > 0)
    centripetal = segment_frame[segment_frame["Doppler"] > 0]
    NCP = len(centripetal)
    RCP = (
        np.average(centripetal["R"], weights=centripetal["Intensity"]) if NCP > 0 else 0
    )
    VCP = (
        np.average(centripetal["Doppler"], weights=centripetal["Intensity"])
        if NCP > 0
        else 0
    )

    # Centrifugal movement (V <= 0)
    centrifugal = segment_frame[segment_frame["Doppler"] <= 0]
    NCF = len(centrifugal)
    RCF = (
        np.average(centrifugal["R"], weights=centrifugal["Intensity"]) if NCF > 0 else 0
    )
    VCF = (
        np.average(centrifugal["Doppler"], weights=centrifugal["Intensity"])
        if NCF > 0
        else 0
    )

    # Overall movement (MEC)
    NEC = len(segment_frame)
    REC = np.average(segment_frame["R"], weights=segment_frame["Intensity"])
    VEC = np.average(segment_frame["Doppler"], weights=segment_frame["Intensity"])

    # Azimuth angle of the nearest SEP (minimum R)
    nearest_alpha = segment_frame.loc[segment_frame["R"].idxmin()]["alpha"]

    # Return the PRM status rounded to 3 decimal places
    return np.round([NEC, REC, VEC, NCP, RCP, VCP, NCF, RCF, VCF, nearest_alpha], 3)


# Main function to process the data and save each PRM matrix separately
def process_and_save_prm_matrices(file_path, output_dir):

    min_segment_len = 3

    min_frame_diff = 8

    segment_len = 20
    # Load the CSV file
    data = pd.read_csv(file_path)

    # Convert 'Frame #' to integer for processing
    data["Frame #"] = data["Frame #"].astype(int)

    # Identify unique frame numbers and calculate differences between consecutive frames
    frame_numbers = data["Frame #"].unique()
    frame_diffs = pd.Series(frame_numbers).diff().fillna(0)

    # Detect where the gaps are larger than 1 (these are delimiters)
    delimiters = frame_diffs[frame_diffs > min_frame_diff].index

    # Split the data into segments based on the delimiters
    segments = []
    start_idx = 0

    for delim in delimiters:
        end_idx = data[data["Frame #"] == frame_numbers[delim - 1]].index[-1] + 1
        segments.append(data.iloc[start_idx:end_idx])
        start_idx = end_idx

    # Adding the last segment (if any)
    if start_idx < len(data):
        segments.append(data.iloc[start_idx:])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate and save PRM matrices
    sample_count = 0
    for segment in segments:
        if len(segment["Frame #"].unique()) < min_segment_len:
            continue

        # Group by 'Frame #' to process each frame individually
        frame_groups = segment.groupby("Frame #")
        prm_matrix = [calculate_prm_status(frame) for _, frame in frame_groups]

        # Split and pad segments to ensure segment_len frames per matrix
        while len(prm_matrix) > segment_len:
            sample_count += 1
            matrix = prm_matrix[:segment_len]
            np.savez_compressed(
                f"{output_dir}/sample_{sample_count}.npz", prm_matrix=matrix
            )
            prm_matrix = prm_matrix[segment_len:]

        # If fewer than segment_len frames, apply random zero-padding
        if len(prm_matrix) < min_segment_len:
            continue
        if len(prm_matrix) < segment_len:
            zeros_to_add = segment_len - len(prm_matrix)
            zeros_before = random.randint(0, zeros_to_add)
            zeros_after = zeros_to_add - zeros_before
            prm_matrix = (
                [[0] * 10] * zeros_before + prm_matrix + [[0] * 10] * zeros_after
            )

        sample_count += 1
        np.savez_compressed(
            f"{output_dir}/sample_{sample_count}.npz", prm_matrix=prm_matrix
        )

    print(f"Generated and saved {sample_count} PRM matrices in '{output_dir}'.")
