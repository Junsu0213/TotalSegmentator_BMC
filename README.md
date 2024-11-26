# CT Organ Masking with TotalSegmentation

This project utilizes the [TotalSegmentation](https://github.com/wasserth/TotalSegmentator) library to automatically generate masks for organs such as the liver, pancreas, and spleen from CT data. It can process multiple NIfTI files at once and offers an option to handle each organ individually to avoid memory issues.

## Features
- Automatically mask organs such as the liver, pancreas, spleen, left, and right kidneys from CT images.
- Option to process each organ individually to prevent memory overload.
- Automatically generate masks for all NIfTI files in the data directory.

## Installation

To use this project, you need to install the [TotalSegmentation](https://github.com/wasserth/TotalSegmentator) library. Please refer to the link for installation instructions.

## Usage

You can run the `main.py` script to generate masks from CT data:

## License

This project uses the [TotalSegmentator](https://github.com/wasserth/TotalSegmentator) library, which is licensed under the Apache-2.0 License.

## Directory structure
```bash
python main.py --data_dir /path/to/your/data

/data/
├── subject1/
│   └── modality1/
│       └── ct.nii.gz
│   └── modality2/
│       └── ct.nii.gz
└── subject2/
    └── modality1/
        └── ct.nii.gz
    └── modality2/
        └── ct.nii.gz
