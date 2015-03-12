#!/usr/bin/python

# This script will take as input a 4D image of single subject cope maps, and extract the mean value for
# each of the petersen rois. Output will be a table of subjects (rows) by parcels (columns) and each
# value corresponds to the mean signal within the parcel

from glob import glob
import pandas
import os


# Output directory
output_directory = "/scratch/PI/russpold/work/HCP/timeseries/petersen_timeseries"

# The MNI parcels file, 0 should correspond to no label
parcels_file = "/scratch/PI/russpold/data/PARCELS/PETERSEN/Parcels_MNI_222.nii"

# Read in the full list of the raw timeseries data
timeseries_file = "/scratch/PI/russpold/work/HCP/group_maps/doc/hcp_timeseries_paths_filtered.tsv"
timeseries_file = pandas.read_csv(timeseries_file,sep="\t")
unique_tasks = timeseries_file.tasks.unique()

# Filter out images that are not in Results folder - we just want unprocessed
timeseries_file = timeseries_file[timeseries_file["timeseries_files"].str.contains("Results")]
unique_tasks = timeseries_file.tasks.unique()

for task in unique_tasks:
  output_task_directory = "%s/%s" %(output_directory,task)
  df = timeseries_file[timeseries_file.tasks==task]
  func_data = df.timeseries_files.tolist()
  for func in func_data:
    output_base = os.path.split(func)[1].replace(".nii.gz","")
    if not os.path.exists(output_task_directory): os.mkdir(output_task_directory)
    output_file = "%s/%s_petersen.tsv" %(output_task_directory,output_base)
    if not os.path.exists(output_file):
      filey = ".job/%s_petersen_ts.job" %(task)
      filey = open(filey,"w")
      filey.writelines("#!/bin/bash\n")
      filey.writelines("#SBATCH --job-name=%s_petersen_ts\n" %(task))
      filey.writelines("#SBATCH --output=.out/ts_%s.out\n" %(task))
      filey.writelines("#SBATCH --error=.out/ts_%s.err\n" %(task))
      filey.writelines("#SBATCH --time=2-00:00\n")
      filey.writelines("#SBATCH --mem=64000\n")
      filey.writelines("python /scratch/PI/russpold/work/HCP/timeseries/script/extract_petersen_timeseries.py %s %s %s\n" %(func,parcels_file,output_file))
      filey.close()
      os.system("sbatch -p russpold .job/%s_petersen_ts.job" %(task))
