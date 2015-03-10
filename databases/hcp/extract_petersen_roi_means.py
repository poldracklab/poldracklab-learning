#!/usr/bin/python

import os
import sys
import nibabel
import pandas
from glob import glob
from nilearn.region import img_to_signals_labels
from nilearn.image import resample_img

input_file = sys.argv[1]
parcels = sys.argv[2]
output_directory = sys.argv[3]
copes_directory = sys.argv[4]

# Read in Peterson ROIs
parcels = nibabel.load(parcels)

# Get list of subjects, extract subject ids
subjects = "%s/%s" %(copes_directory,os.path.split(input_file)[1].replace("_4D.nii.gz",".txt"))
output_file = "%s/%s" %(output_directory,os.path.split(input_file)[1].replace("copes_4D.nii.gz","hcp_petersen_roi_means.txt"))
subjects = open(subjects,"rb").readlines()
subids = [sub.split("/")[7] for sub in subjects]

# Read in the input file - a 4D timeseries with each timepoint corresponding to the subjects above
nii_obj = nibabel.load(input_file)
if nii_obj.shape[3] != len(subids):
  print "ERROR: number of timepoints in file does not correspond to number of subject IDS!"
  os.exit(32)

# Resample parcel image to match nii_obj - interpolation MUST be nearest because this is an atlas
parcel_resample = resample_img(parcels, target_affine=nii_obj.get_affine(),interpolation="nearest")

# Extract rois from timeseries
tmp = img_to_signals_labels(nii_obj, parcel_resample, mask_img=None, background_label=0, order='F')
df = pandas.DataFrame(tmp[0])

# Save to tsv file.
df.index = subids
df.columns = [int(x) for x in tmp[1]]
df.to_csv(output_file,sep="\t")
