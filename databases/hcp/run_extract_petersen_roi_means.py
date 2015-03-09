#!/usr/bin/python

# This script will take as input a 4D image of single subject cope maps, and extract the mean value for
# each of the petersen rois. Output will be a table of subjects (rows) by parcels (columns) and each
# value corresponds to the mean signal within the parcel

from glob import glob
import os

# We will extract timeseries for each 4D file from out task data
inputs_nii = glob("/scratch/PI/russpold/work/HCP/group_maps/nii/*4D.nii.gz")

# Output directory
output_directory = "/scratch/PI/russpold/work/HCP/timeseries"

# Directory with subject lists
copes_directory = "/scratch/PI/russpold/work/HCP/group_maps/copes"

# The MNI parcels file, 0 should correspond to no label
parcels_file = "/scratch/PI/russpold/data/PARCELS/PETERSEN/Parcels_MNI_222.nii"

for input_nii in inputs_nii:
  base_name = os.path.split(input_nii)[1]
  output_file = "%s/%s" %(output_directory,base_name.replace("copes_4D.nii.gz","hcp_petersen_ts.txt"))
  if not os.path.exists(output_file):
    filey = ".job/%s_petersen_ts.job" %(base_name)
    filey = open(filey,"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=%s_randomise\n" %(base_name))
    filey.writelines("#SBATCH --output=.out/coverage_%s.out\n" %(base_name))
    filey.writelines("#SBATCH --error=.out/coverage_%s.err\n" %(base_name))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=64000\n")
    filey.writelines("python /scratch/PI/russpold/work/HCP/timeseries/script/extract_petersen_roi_means.py %s %s %s %s\n" %(input_nii,parcels_file,output_directory,copes_directory))
    filey.close()
    os.system("sbatch -p russpold .job/%s_petersen_ts.job" %(base_name))
