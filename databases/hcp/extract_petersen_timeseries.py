#!/usr/bin/python

import os
import re
import sys
import nibabel
import numpy as np
import pandas
from glob import glob
from nilearn.region import img_to_signals_labels
from nipy.algorithms.registration.histogram_registration import HistogramRegistration
from nilearn.image import resample_img

vol = sys.argv[1]
parcels = sys.argv[2]
output_file = sys.argv[3]

# Read in Peterson ROIs
parcels = nibabel.load(parcels)
parcel_ids = [int(x) for x in np.unique(parcels.get_data()).tolist()]
parcel_ids.pop(0) # value of 0

print "Processing %s" %(vol)

# Use regular expression to find the id, and make labels
expression = re.compile("/[0-9]+/")
match = expression.search(vol)
subid = vol[match.start()+1:match.end()-1]
labels = ["%s_%s" %(subid,x) for x in parcel_ids]
nii_obj = nibabel.load(vol)
nii_resample = resample_img(nii_obj, target_affine=parcels.get_affine(),interpolation="continuous")
tmp = img_to_signals_labels(nii_resample, parcels, mask_img=None, background_label=0, order='F')
df_ss = pandas.DataFrame(tmp[0])
df_ss.columns = labels
df_ss = df_ss.transpose()    
df_ss.to_csv(output_file,sep="\t")
