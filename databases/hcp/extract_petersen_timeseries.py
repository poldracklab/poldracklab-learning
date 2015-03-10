#!/usr/bin/python

import os
import sys
import nibabel
import numpy as np
import pandas
from glob import glob
from nilearn.region import img_to_signals_labels
from nilearn.image import resample_img

timeseries_file = sys.argv[1]
parcels = sys.argv[2]
output_directory = sys.argv[3]

# Read in Peterson ROIs
parcels = nibabel.load(parcels)

# Read in the full list of the raw timeseries data
timeseries_file = pandas.read_csv(timeseries_file,sep="\t")
unique_tasks = timeseries_file.tasks.unique()

parcel_ids = [int(x) for x in np.unique(parcels.get_data()).tolist()]
parcel_ids.pop(0) # value of 0

# For each unique task, generate list of filtered func data, one for each petersen roi
for task in unique_tasks:
  print "STARTING TASK %s" %(task)
  # We will append each to this data frame
  df = timeseries_file[timeseries_file.tasks==task]
  func_data = df.timeseries_files.tolist()
  func_data_df = pandas.DataFrame()
  outfile = "%s/%s_timeseries.csv" %(output_directory,task)
  for vol in func_data:
    subid = os.path.split(vol)[1].split("_")[0]
    labels = ["%s_%s" %(subid,x) for x in parcel_ids]
    print "Processing %s" %(vol)
    nii_obj = nibabel.load(vol)
    shape = parcels.get_shape()
    shape = (shape[0],shape[1],shape[2])
    nii_resample = resample_img(nii_obj, target_affine=parcels.get_affine(),target_shape=shape,interpolation="continuous")
    tmp = img_to_signals_labels(nii_resample, parcels, mask_img=None, background_label=0, order='F')
    df_ss = pandas.DataFrame(tmp[0])
    df_ss.columns = labels
    df_ss = df_ss.transpose()    
    func_data_df = func_data_df.append(df_ss)
  # Now we have finished all subjects, save tofile
  func_data_df.to_csv(outfile)
