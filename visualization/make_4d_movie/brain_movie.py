# Let's try making a 4d movie from a 4d nifti in python
# Will be incoporated into pycomparebrain, just learning for now

from nilearn.plotting import plot_stat_map
import matplotlib.pyplot as plt
import nibabel as nib
import contextlib
import numpy as np
import tempfile
import shutil
import contextlib
import os, sys


# Function to make temporary directory
@contextlib.contextmanager
def make_tmp_folder():
  temp_dir = tempfile.mkdtemp()
  yield temp_dir
  shutil.rmtree(temp_dir)

four_dee_file = sys.argv[1]
gif_name = sys.argv[2]
header = nib.load(four_dee_file)
data = header.get_data()

all_images = []
with make_tmp_folder() as tmp_dir:
  print "Reading in images to temp..."
  for tp in range(0,np.shape(data)[3]):
    timepoint = data[:,:,:,tp]
    timepoint_img = nib.Nifti1Image(timepoint,affine=header.get_affine())    
    display = plot_stat_map(timepoint_img)  
    image_name = '%s/%s_chicken.png' %(tmp_dir,tp)
    display.savefig(image_name) 
    plt.close()
    all_images.append(image_name)  
  command = " ".join(all_images)
  os.system("convert -delay 50 %s -loop 1 %s" %(command,gif_name))
