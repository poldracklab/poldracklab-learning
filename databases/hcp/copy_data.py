#!/usr/bin/python

from glob import glob
import shutil
import pandas
import sys
import os

# Copy all data from an old location to a new one
old_directory = "/corral-tacc/tacc/HCP"
base_directory = "/scratch/projects/UT/poldracklab/data/HCP"
doc_directory = "%s/doc" %(base_directory)
copes_lists_directory = "%s/doc/copes" %(base_directory)
copes_files = glob("%s/*copes_hcp.txt" %copes_lists_directory)

# We must replace these names
disks = {"Disk1of5":"disk1",
        "Disk2of5":"disk2",
        "Disk3of5":"disk3",
        "Disk4of5":"disk4",
        "Disk5of5":"disk5"}

# Copy old files to new path. This can be run multiple times (while data is copying)
for cope_file in copes_files:
    print "Processing %s" %(cope_file)
    copes = pandas.read_csv(cope_file,header=None)[0].tolist()
    for diskold,disknew in disks.iteritems():
        copes = [c.replace(diskold,disknew) for c in copes]
    new_cope_file = cope_file.replace("_hcp","")
    # Write updated cope paths file (delete old after)
    filey = open(new_cope_file,"wb")
    filey.writelines("/n".join(copes))
    filey.close()
    # For each cope file
    for cope in copes:
        old_path = "%s%s" %(old_directory,cope)
        if os.path.exists(old_path):
            new_path = "%s%s" %(base_directory,cope)
            new_directory = os.path.split(new_path)[0]
            if not os.path.exists(new_directory):
                os.makedirs(new_directory)
            if not os.path.exists(new_path):
                shutil.copyfile(old_path,new_path)
        else:
            print "ERROR: Missing %s" %(old_path)
        
