#!/usr/bin/python

# This script will convert group tstat maps to Zmaps. For details on the method see:
# https://github.com/vsoch/TtoZ

# To install TtoZ, do:
# pip install git+https://github.com/vsoch/TtoZ.git --user
# It will tell you that the executable has been placed in your home .local
# You can add this to your path to always find it:
#     vim /home/vsochat/.bash_profile

#     # TtoZ program
#     PATH=$PATH:/home/vsochat/.local/bin
#     export PATH

# Save and exit, and source your bash profile to make it findable
# source /home/vsochat/.bash_profile

#$ which TtoZ
#~/.local/bin/TtoZ

# You can also just call it using the whole path
# ./home/vsochat/.local/bin/TtoZ

# We will submit the command to the command line with os.system.

from glob import glob
import os

# The degrees of freedom is the number of subjects -2.
# We will need to look this up for each map by looking at the number of images
# in the cope files.
cope_directory = "/scratch/PI/russpold/work/HCP/group_maps/copes" 

# Each of these tstat maps was produced with randomise, using all subjects with data for the task
# For the STORY contrasts, there is activation in ventricles (strong negative values) that might be of concern
tmaps = glob("/scratch/PI/russpold/work/HCP/group_maps/nii/*nii_tstat1.nii.gz")
for tmap in tmaps:
  task_name = os.path.split(tmap)[1].replace(".nii_tstat1.nii.gz","")
  cope_file = "%s/%s_copes.txt" %(cope_directory,task_name)
  filey = open(cope_file,"rb")
  number_subjects = len(filey.readlines())
  filey.close()
  dof = number_subjects - 2
  zmap = tmap.replace(".nii_tstat1.nii.gz","_zstat1.nii.gz")
  os.system("TtoZ %s %s --output_nii=%s" %(tmap,dof,zmap)) 
