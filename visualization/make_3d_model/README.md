# Make a 3D Brain!

This uses freesurfers mri_convert to convert a surface file (.srf) to an .asc file.  A .asc file is essentially the same as .srf, so we just rename.  We can then use the script srf2obj to convert from srf to obj, and an obj file.  I did not figure this out, credit goes [here](http://brainder.org/2012/05/08/importing-freesurfer-cortical-meshes-into-blender/)

# Blender
Blender is tricky if you've never used it, and still tricky if you have :)

1. File --> Import --> Obj
2. On the right side bar there are little picture tabs about 3/4 from the top, and one when you mouseover says: "Type of Active Data to Display and Edit."  This is where you should change the scale of your model to be in cm or inches: http://www.katsbits.com/tutorials/blender/metric-imperial-units.php. You have to pay for the material for your model, so keep this in mind :)
3. Manually resize the mode with your mouse/keys, see instructions here: http://wiki.blender.org/index.php/Doc:2.4/Manual/3D_interaction/Transformations/Basics/Scale
4. The orientation of the model is important.  It should sit flat on the plane, so that the 3D printer can add scaffolding to the bottom, and it will clealy break away.  Also remember that whatever is on the bottom may have scaffolding (gray bits of plastic) that you have a hard time removing, so the "pretty side" will be on the top.
5. Export at stl.  Other formats would probably work too, but this is what I did.
6. Here is the lab: https://productrealization.stanford.edu/resources/processes/3d-printing
7. Have fun! :O)
