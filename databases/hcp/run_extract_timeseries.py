#!/usr/bin/python

# This script will take as input a 4D image of single subject preprocessed task or resting BOLD map, and extract 
# a complete timeseries for each of the petersen rois. Output will be a table of subject_parcelID (rows) by timepoints (columns) and each value corresponds to the signal for that parcel and timepoint. The timepoints start numbering at 0.

from glob import glob
import pandas
import os
import re


# Output directory
name = "subcortical"
output_directory = "/scratch/PI/russpold/work/HCP/timeseries/%s" %(name)

# The MNI parcels file, 0 should correspond to no label
parcels_file = "/scratch/PI/russpold/data/PARCELS/SUBCORTICAL/HarvardOxford-sub-maxprob-thr50-2mm.nii.gz"

# Read in the full list of the raw timeseries data
timeseries_file = "/scratch/PI/russpold/work/HCP/group_maps/doc/hcp_timeseries_paths_filtered.tsv"
timeseries_file = pandas.read_csv(timeseries_file,sep="\t")
unique_tasks = timeseries_file.tasks.unique()

# Filter out images that are not in Results folder - we just want single subject preprocessed data (without contrast specification)
timeseries_file = timeseries_file[timeseries_file["timeseries_files"].str.contains("Results")]
unique_tasks = timeseries_file.tasks.unique()

# Expression to find subject ID in volume path
expression = re.compile("/[0-9]+/")

for task in unique_tasks:
  output_task_directory = "%s/%s" %(output_directory,task)
  # Subset the data to the task - we are saving within task directories
  df = timeseries_file[timeseries_file.tasks==task]
  func_data = df.timeseries_files.tolist()
  for func in func_data:
    # Use regular expression to find the id, and make labels
    match = expression.search(func)
    subid = func[match.start()+1:match.end()-1]
    output_base = os.path.split(func)[1].replace(".nii.gz","")
    # Make the output directory if it does not exist, and specify output file within it
    if not os.path.exists(output_task_directory): os.mkdir(output_task_directory)
    jobname = "%s_%s" %(subid,task)
    output_file = "%s/%s_%s_%s.tsv" %(output_task_directory,subid,output_base,name)
    # Only run the job if the output file doesn't exist
    if not os.path.exists(output_file):
      filey = ".job/%s_%s_ts.job" %(jobname,name)
      filey = open(filey,"w")
      filey.writelines("#!/bin/bash\n")
      filey.writelines("#SBATCH --job-name=%s_%s_ts\n" %(jobname,name))
      filey.writelines("#SBATCH --output=.out/ts_%s.out\n" %(jobname))
      filey.writelines("#SBATCH --error=.out/ts_%s.err\n" %(jobname))
      filey.writelines("#SBATCH --time=2-00:00\n")
      filey.writelines("#SBATCH --mem=64000\n")
      filey.writelines("python /scratch/PI/russpold/work/HCP/timeseries/script/extract_timeseries.py %s %s %s\n" %(func,parcels_file,output_file))
      filey.close()
      os.system("sbatch -p russpold .job/%s_%s_ts.job" %(jobname,name))
