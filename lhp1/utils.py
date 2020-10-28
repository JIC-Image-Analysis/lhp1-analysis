import numpy as np


def selective_border_region_labels(seg3d):
    rdim, cdim, _ = seg3d.shape
    slices = [np.s_[0,:,:], np.s_[rdim-1,:,:], np.s_[:,0,:], np.s_[:,cdim-1,:]]
    region_sets = [set(np.unique(seg3d[sl])) for sl in slices]
    return set.union(*region_sets)