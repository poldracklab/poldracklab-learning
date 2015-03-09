#!/usr/bin/python

# This script will submit a job to run randomise for each list of cope inputs (each is associated with a task-->contrast. The output is a nice group map, whala!

import os
from glob import glob

cope_lists = glob("/scratch/PI/russpold/work/HCP/group_maps/copes/*copes.txt")
output_directory = "/scratch/PI/russpold/work/HCP/group_maps/nii"

# These did not complete due to Sherlock blips - are being rerun
cope_lists =["/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_WM_2BK_TOOL_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_WM_2BK_PLACE_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_WM_0BK_TOOL_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_WM_0BK_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_MOTOR_T_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_MOTOR_neg_LF_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_MOTOR_AVG-LF_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_MOTOR_AVG-CUE_copes.txt","/scratch/PI/russpold/work/HCP/group_maps/copes/tfMRI_LANGUAGE_neg_STORY_copes.txt"]

for cope_file in cope_lists:
  output_nii = os.path.split(cope_file)[1].replace("_copes.txt","")
  merged_nii_path = "%s/%s_copes_4D.nii" %(output_directory,output_nii)
  output_nii_path = "%s/%s.nii" %(output_directory,output_nii)
  copes = open(cope_file,"rb").readlines()
  copes = " ".join([c.strip("\n") for c in copes])
  if not os.path.exists(output_nii_path):
    filey = ".job/%s_randomise.job" %(output_nii)
    filey = open(filey,"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=%s_randomise\n" %(output_nii))
    filey.writelines("#SBATCH --output=.out/coverage_%s.out\n" %(output_nii))
    filey.writelines("#SBATCH --error=.out/coverage_%s.err\n" %(output_nii))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=64000\n")
    filey.writelines("module load fsl\n")
    filey.writelines("fslmerge -t %s %s\n" %(merged_nii_path,copes))
    filey.writelines("randomise -i %s -o %s -1 -T\n" %(merged_nii_path,output_nii_path))
    filey.close()
    os.system("sbatch -p russpold .job/%s_randomise.job" %(output_nii))
