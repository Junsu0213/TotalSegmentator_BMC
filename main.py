# -*- coding:utf-8 -*-
"""
Created on Wed. Aug. 28 13:46:30 2024
@author: JUN-SU PARK
"""
import os
from totalsegmentator.python_api import totalsegmentator

# Option 1: Process all ROIs at once (may cause memory issues with multiple ROIs)
def create_multiple_labels_for_nii(input_path, output_path, roi_subset=None):
    """
    Generate masks by processing multiple ROIs at once from a NIfTI file.

    Args:
        input_path (str): Path to the input NIfTI file.
        output_path (str): Path to save the generated mask file.
        roi_subset (list of str): List of ROIs to process. Default is ['spleen', 'pancreas', 'liver'].
    """
    if roi_subset is None:
        roi_subset = ['spleen', 'pancreas', 'liver', 'kidney_left', 'kidney_right']
    print(f"Processing all ROIs at once: {', '.join(roi_subset)}")
    totalsegmentator(input_path, output_path, roi_subset=roi_subset, ml=True)
    print(f"Finished processing all ROIs. Output saved to {output_path}")


# Option 2: Process each ROI separately to avoid memory issues
def create_single_label_for_nii(input_path, output_dir, roi_subset=None):
    """
    Generate masks by processing each ROI separately from a NIfTI file.

    Args:
        input_path (str): Path to the input NIfTI file.
        output_dir (str): Directory to save the generated mask files.
        roi_subset (list of str): List of ROIs to process. Default is ['spleen', 'pancreas', 'liver'].
    """
    if roi_subset is None:
        roi_subset = ['spleen', 'pancreas', 'liver', 'kidney_left', 'kidney_right']
    for roi in roi_subset:
        print(f"Processing {roi} ROI...")
        totalsegmentator(input_path, output_dir, roi_subset=[roi])
        print(f"Finished processing {roi} ROI. Output saved to {output_dir}")


def main(database_dir):
    """
    Generate masks for all NIfTI files in the data directory.
    """
    sub_list = os.listdir(database_dir)

    for sub in sub_list:
        sub_path = os.path.join(database_dir, sub)
        file_list = os.listdir(sub_path)

        for file_name in file_list:
            input_path = os.path.join(sub_path, file_name, f'{file_name}.nii.gz')
            output_path = os.path.join(sub_path, file_name, f'{file_name}_mask.nii.gz')
            output_dir = os.path.join(sub_path, file_name)

            print(f'Starting mask generation for subject: {sub}, file: {file_name}')
            create_multiple_labels_for_nii(input_path, output_path)
            create_single_label_for_nii(input_path, output_dir)
            print(f'Completed mask generation for subject: {sub}, file: {file_name}\n')


if __name__ == '__main__':
    database_dir = r'D:\DATASET\CT\liver_pancrease_dataset\nii_output'
    main(database_dir)
