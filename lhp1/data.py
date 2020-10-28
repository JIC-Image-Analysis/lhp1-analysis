import pathlib
from dataclasses import dataclass

from stacktools.io import get_stack_by_imname_sname, load_segmentation3d_from_file

from dtoolbioimage import Image3D
from dtoolbioimage.segment import Segmentation3D


@dataclass
class SegmentationMeasureStack:
    
    segmentation: Segmentation3D
    measure_stack: Image3D
    wall_stack: Image3D


class LHPSMS(SegmentationMeasureStack):

    @classmethod
    def from_ids_dirpath_imname_sname(cls, ids_uri, seg_dirpath, imname, sname):
        wall_stack = get_stack_by_imname_sname(ids_uri, imname, sname, channel=1)
        venus_stack = get_stack_by_imname_sname(ids_uri, imname, sname, channel=0)
    
        level = 0.3
        seg_filename = f'{imname}_{sname}_L{level}.tif'
        seg_dirpath = pathlib.Path(seg_dirpath)
        segmentation = Segmentation3D.from_file(seg_dirpath/seg_filename)

        return cls(segmentation, venus_stack, wall_stack)        