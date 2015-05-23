#!/usr/bin/python

import fnmatch
import filecmp
import sys
import os


search_directory = "/scratch/PI/russpold/data/HCP"
output_directory = "/scratch/PI/russpold/work/HCP/group_maps"
doc_directory = "%s/doc" %(output_directory)

# STEP 1: GENERATE LOGS & CHECK DATA -------------------------------------------------

# First we will find all the volume feat directories
volume_folders = []
for root, dirnames, filenames in os.walk(search_directory):
  for dirname in fnmatch.filter(dirnames, '*vol.feat'):
      #print "Found %s/%s" %(root,dirname)
      volume_folders.append(os.path.join(root, dirname))

# Now break into the different tasks, and find Contrasts.txt files
tasks = [os.path.split(os.path.split(x)[0])[1] for x in volume_folders]
contrast_files = [p.replace("vol.feat",".feat/Contrasts.txt") for p in volume_folders]
for filename in contrast_files:
  if not os.path.isfile(filename):
    print "Warning: cannot find %s" %(s)

# Put them into the same data frame
df = pandas.DataFrame()
df["volume_folders"] = volume_folders
df["tasks"] = tasks
df["contrast_files"] = contrast_files
df.to_pickle("%s/hcp_datalog.pkl" %(doc_directory))
df.to_csv("%s/hcp_datalog.tsv" %(doc_directory),sep="\t")

# We would assume that the cope maps (the contrasts) are equivalent for the same tasks.
# But we really should check. We can select each unique task, and assert that the contrast files are equal
unique_tasks = df.tasks.unique()
for task in unique_tasks:
  print "Checking task %s" %(task)
  contrasts = df.contrast_files[df.tasks==task].tolist()
  for contrast in contrasts:
     if not filecmp.cmp(contrasts[0], contrast):
       print "ERROR: %s is not equivalent to others!" %(contrast)

# Now get list of contrasts for each. The order corresponds with cope1, cope2, etc.
contrasts = dict()
all_contrasts = pandas.DataFrame()
for task in unique_tasks:
  subset = df.loc[df.tasks==task]
  filey = open(subset.contrast_files.tolist()[0],"rb")
  contrast_list = filey.readlines()
  filey.close()
  contrast_list = [x.strip("\n") for x in contrast_list]
  cope_list = []
  for x in range(0,len(contrast_list)):
    c = x+1
    cope_list.append("cope%s.feat/stats/cope1.nii.gz" %(c))
  tmp = pandas.DataFrame()
  tmp["contrasts"] = contrast_list
  tmp["copes"] = cope_list
  tmp["task"] = [task for x in range(0,len(contrast_list))]
  contrasts[task] = tmp
  all_contrasts = all_contrasts.append(tmp)

all_contrasts.to_csv("%s/hcp_contrasts.tsv" %(doc_directory),sep="\t")



# STEP 2: COPE IMAGE LIST FILES -------------------------------------------------

# Now we need input files for each task, each contrast, to make the group maps.
for contrast in all_contrasts.iterrows():
  # Here is the output file for the contrast
  output_file = "%s/copes/%s_%s_copes.txt" %(output_directory,contrast[1].task,contrast[1].contrasts)
  print "Generating file of copes for %s" %(output_file)
  # Find all volumes for that contrast
  subset = df.loc[df.tasks==contrast[1].task]
  volume_dirs = subset.volume_folders.tolist()
  nii_paths = ["%s/%s" %(path,contrast[1].copes) for path in volume_dirs]
  for nii in nii_paths:
    if not os.path.exists(nii):
      print "ERROR: Missing cope %s" %(nii)
  filey = open(output_file,"wb")
  for nii_path in nii_paths:
    filey.writelines("%s\n" %(nii_path))
  filey.close()


# STEP 2: RAW TIMESERIES DATA LISTS -------------------------------------------------
# First we will find all the volume feat directories
timeseries_files = []
for root, dirnames, filenames in os.walk(search_directory):
  for filename in fnmatch.filter(filenames, '*_RL.nii.gz'):
      print "Found %s/%s" %(root,filename)
      timeseries_files.append(os.path.join(root, filename))

# Extract the unique tasks from each
tdf = pandas.DataFrame()
ttasks = [os.path.split(os.path.split(x)[0])[1] for x in timeseries_files]
images = [os.path.split(x)[1] for x in timeseries_files]
tdf["timeseries_files"] = timeseries_files
tdf["tasks"] = ttasks
tdf["images"] = images
tdf.to_csv("%s/hcp_timeseries_paths_RL.tsv" %(doc_directory),sep="\t")

# Get rid of spin echo field maps
filtered = tdf[~tdf['images'].str.contains("SpinEchoFieldMap")]
filtered = filtered[~filtered['images'].str.contains("DWI")]
filtered.to_csv("%s/hcp_timeseries_paths_RL_filtered.tsv" %(doc_directory),sep="\t")
