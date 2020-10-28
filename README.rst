LHP1 data analysis
==================

Repository holding analysis scripts and pipelines for analysing LHP1 roots
using a novel pipeline

The repository also contains diagnostic and visualisation tools for testing
the pipeline.

Method
------

This pipeline requires both root images and segmentations (which can be
produced by dtoolbioimage).

The pipeline carries out the following steps:

1. Load the cell wall and venus channels from the image datasets as 3D images.
2. Scale these images to correct for differences in physical size to voxel size
   conversion along axes.
3. Load segmentation for the image.
4. Removes all segmented regions touching the border of the image.
5. Order segmented regions by volume and take the top n (300 by default) 
   regions.
6. Measure and report the mean FLC-Venus intensity in each segmented cell.

