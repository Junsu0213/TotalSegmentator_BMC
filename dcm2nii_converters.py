# -*- coding:utf-8 -*-
"""
Created on Mon. Sep. 30 14:44:22 2024
@author: JUN-SU PARK
"""
import os
import SimpleITK as sitk
from tqdm import tqdm  # Import tqdm for the progress bar


def convert_dicom_to_nii(input_dir, output_dir=None):
    """
    Convert DICOM files to NIfTI format and save them to the output directory.

    Args:
        input_dir (str): Directory containing DICOM files to convert.
        output_dir (str): Directory to save the converted NIfTI file.
                          If None, a 'nii' directory will be created under the parent directory of input_dir.
    """
    if output_dir is None:
        parent_dir = os.path.dirname(input_dir)
        output_dir = os.path.join(parent_dir, 'nii')
    os.makedirs(output_dir, exist_ok=True)

    file_name = os.path.basename(input_dir)

    # Read the DICOM series and convert it to a NIfTI file
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(input_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    # Save the NIfTI file
    sitk.WriteImage(image, f'{output_dir}/{file_name}.nii.gz')

def convert_all_data_to_nii(dcm_dir, nii_dir):
    """
    Convert all DICOM data in the given directory to NIfTI format.

    Args:
        dcm_dir (str): Directory containing subdirectories with DICOM files to convert.
        nii_dir (str): Directory to save the converted NIfTI files.
    """
    os.makedirs(nii_dir, exist_ok=True)

    # List all subdirectories (subjects) to process
    sub_list = os.listdir(dcm_dir)
    total_subjects = len(sub_list)

    # Use tqdm to show progress in a real-time update format
    with tqdm(total=total_subjects, desc="Processing subjects", unit="subject") as pbar:
        for sub in sub_list:
            sub_dcm_path = os.path.join(dcm_dir, sub)
            sub_nii_path = os.path.join(nii_dir, sub)
            os.makedirs(sub_nii_path, exist_ok=True)

            dcm_file_list = os.listdir(sub_dcm_path)

            if len(dcm_file_list) < 5:
                # Skip processing if there are fewer than 5 files (assumed incomplete dataset)
                pass  # Still update the progress bar
            else:
                try:
                    # Convert each DICOM file in the subject folder to NIfTI format
                    for dcm_file in dcm_file_list:
                        dcm_file_path = os.path.join(sub_dcm_path, dcm_file)
                        nii_file_path = os.path.join(sub_nii_path, dcm_file)
                        convert_dicom_to_nii(dcm_file_path, nii_file_path)

                except Exception as e:
                    print(f"\nError processing subject {sub}: {e}")

            # Update progress after processing (including skipped subjects)
            pbar.update(1)


if __name__ == '__main__':
    dcm_dir = r'D:\DATASET\CT\dcm_organizer_test\dcm_output'
    nii_dir = r'D:\DATASET\CT\dcm_organizer_test\nii_output'

    # Convert all DICOM files to NIfTI with progress percentage
    convert_all_data_to_nii(dcm_dir, nii_dir)
