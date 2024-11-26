# -*- coding:utf-8 -*-
import os
import pydicom
import shutil
import re
from tqdm import tqdm


class DICOMOrganizer:
    def __init__(self, input_dir, output_dir=None):
        """
        Initialize the DICOM organizer with the input and output directories.

        Args:
            input_dir (str): Path to the directory containing the DICOM subject folders.
            output_dir (str, optional): Path to the directory where organized DICOM files will be saved.
                                        If not specified, '_output' will be appended to the input directory.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir if output_dir else self._get_default_output_dir()

    def _get_default_output_dir(self):
        """Generate a default output directory name by appending '_output' to the input directory."""
        return os.path.join(self.input_dir + "_output")

    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize the filename by removing special characters and spaces.

        Args:
            filename (str): The original filename.

        Returns:
            str: The sanitized filename.
        """
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        sanitized_name = re.sub(r'\s+', '_', sanitized_name)
        return sanitized_name

    def organize_dicom_files(self):
        """
        Organize DICOM files by 'SeriesDescription' and 'SliceThickness',
        and place them in subject-specific folders within the output directory.
        """
        os.makedirs(self.output_dir, exist_ok=True)

        # Walk through all subdirectories (subject folders) in the input directory
        subject_dirs = [os.path.join(self.input_dir, subject) for subject in os.listdir(self.input_dir)
                        if os.path.isdir(os.path.join(self.input_dir, subject))]
        total_files = sum(len(files) for _, _, files in os.walk(self.input_dir))

        processed_files = 0
        for subject_dir in tqdm(subject_dirs, desc="Processing subjects", unit="subject"):
            subject_name = os.path.basename(subject_dir)
            subject_output_dir = os.path.join(self.output_dir, subject_name)
            os.makedirs(subject_output_dir, exist_ok=True)

            # Process all DICOM files within the subject folder
            for root, _, files in os.walk(subject_dir):
                for file in files:
                    if file.endswith('.dcm'):
                        self._process_dicom_file(root, file, subject_output_dir)
                        processed_files += 1

        print(f"All DICOM files processed. Total: {processed_files}/{total_files}")

    def _process_dicom_file(self, root, file, subject_output_dir):
        """
        Process a single DICOM file, extract its metadata, and move it to the appropriate folder
        inside the subject's output directory.

        Args:
            root (str): The directory containing the DICOM file.
            file (str): The name of the DICOM file.
            subject_output_dir (str): The directory where the processed DICOM file will be saved.
        """
        try:
            file_path = os.path.join(root, file)
            dicom_file = pydicom.dcmread(file_path)

            # Extract the SeriesDescription and SliceThickness attributes
            slice_thickness = getattr(dicom_file, 'SliceThickness', None)
            series_description = getattr(dicom_file, 'SeriesDescription', 'Unknown')

            # Skip files without valid SliceThickness
            if slice_thickness is None or slice_thickness == 0:
                return

            # Create a folder name using sanitized SeriesDescription and SliceThickness
            folder_name = f"{self.sanitize_filename(series_description)}_{int(slice_thickness)}mm"
            target_dir = os.path.join(subject_output_dir, folder_name)
            os.makedirs(target_dir, exist_ok=True)

            # Copy the DICOM file to the target directory
            sanitized_file = self.sanitize_filename(file)
            shutil.copy2(file_path, os.path.join(target_dir, sanitized_file))

        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")


if __name__ == '__main__':
    # Set the input and output directories
    input_dir = r'D:\DATASET\CT\dcm_organizer_test\dcm_input'
    output_dir = r'D:\DATASET\CT\dcm_organizer_test\dcm_output'  # Optional: Can be set to None

    # Initialize and run the DICOM organizer
    organizer = DICOMOrganizer(input_dir, output_dir)
    organizer.organize_dicom_files()
