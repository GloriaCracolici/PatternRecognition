import SimpleITK as sitk
import matplotlib.pyplot as plt
import os
import glob
import numpy as np
import radiomics
from radiomics import featureextractor

# Set the path to the Fiji executable
os.environ['SITK_SHOW_COMMAND'] = r'C:\Users\39345\fiji-win64\Fiji.app\ImageJ-win64.exe'

# Initialize the feature extractor
extractor = featureextractor.RadiomicsFeatureExtractor()

# Create a directory to the folder containing the MRI and SEG
directory_path_MRI = 'C:\\Users\\39345\\OneDrive\\Desktop\\endometriosis_MRI';

# Create and unsorted list of the patients
unsorted_patients = os.listdir(directory_path_MRI)

# Sort the items of the list unsorted_patients by extracting the numerical part
patients = sorted(unsorted_patients, key=lambda x: int(''.join(filter(str.isdigit, x))))

# Number of patients
n_patients = len(patients)

# Create a cycle in order to retrieve the data
for p in patients:
    
    print(f'Iteration {p}');
    
    pDir = os.path.join(directory_path_MRI, p);
    
    
    # Create variables containing the directories to MRI and segmentation images
    for file_name in os.listdir(pDir):
            if file_name.endswith('.nii'):
                if '_seg' in file_name:
                    pSegdir = os.path.join(pDir, file_name);
                else:
                    pMRIdir = os.path.join(pDir, file_name);
                    
    # Load the MRI image
    pMRI = sitk.ReadImage(pMRIdir)

    # Load the Segmentation image
    pSeg = sitk.ReadImage(pSegdir)
   
   
    # Visualize the MRI image
    #sitk.Show(pMRI, "MRI Image", debugOn=True)
 
    # Visualize the Segmentation image
    #sitk.Show(pSeg, "Segmentation Image")
        
    # Create a binary mask where the label of the region of interest is 1 and everything else is 0
    pmask = sitk.BinaryThreshold(pSeg, lowerThreshold=1, upperThreshold=1, insideValue=1, outsideValue=0)

    # Save the mask to a file
    #sitk.WriteImage(pmask, "mask.nii")
    
    # Check if mask and MRI have the same physical space (origin, spacing, and size) and, if not, skip to the next patient
    if pMRI.GetOrigin() != pmask.GetOrigin() or pMRI.GetSpacing() != pmask.GetSpacing() or pMRI.GetSize() != pmask.GetSize():
        
        print(f"Skipping MRI{p} and mask{p}: Mismatch in origin, spacing, or size.")

        # We check the origin, spacing and size of the two images to find out what the problem is
        
        # Print the origin of the two images (physical coordinates of the first voxel)
        print(f"Origin MRI: {pMRI.GetOrigin()}")
        print(f"Origin Mask: {pmask.GetOrigin()}")
        
        # Print the spacing of the two images
        print(f"Spacing MRI: {pMRI.GetSpacing()}")
        print(f"Spacing Mask: {pmask.GetSpacing()}")
        
        # Print the size of the two images
        print(f"Size MRI: {pMRI.GetSize()}")
        print(f"Size Mask: {pmask.GetSize()}")
        
        continue  # Skip to the next iteration


    # Apply the mask to the MRI image
    maskedMRI = sitk.Mask(pMRI, pmask)

    # Save the masked image to a file
    #sitk.WriteImage(maskedMRI, "masked_mri_image.nii")

