#!/usr/bin/env python

# A quick script to print the number of subjects, and dof, for each HCP group map
from glob import glob
import nibabel
import os

tmaps = glob("/scratch/PI/russpold/work/HCP/group_maps/nii/*4D.nii.gz")
for tmap in tmaps:
  nii = nibabel.load(tmap)
  map_name = os.path.split(tmap)[1]
  number_subjects = nii.shape[3]
  dof = number_subjects - 2
  print "%s: %s subjects, %s degrees of freedom." %(map_name,number_subjects,dof)
