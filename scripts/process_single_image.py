import logging
import pathlib

import click
import numpy as np

import ruamel.yaml

from dtoolbioimage import Image as dbiImage, scale_to_uint8

from data import LHPSMS
from config import ProcessConfig


def thresh_and_merge(sms, z):
    measure_thresh = 0
    wall_thresh = 3
    
    measure_thresh_plane = scale_to_uint8(sms.measure_stack[:,:,z] > measure_thresh)
    wall_thresh_plane = scale_to_uint8(sms.wall_stack[:,:,z] > wall_thresh)
    blank_plane = np.zeros(sms.wall_stack[:,:,z].shape, dtype=np.uint8)
    
    return np.dstack((wall_thresh_plane, measure_thresh_plane, blank_plane)).view(dbiImage)


@click.command()
@click.argument('config_fpath')
def main(config_fpath):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("processSingleImage")
    # ids_uri = "azure://imagedatasets/7ba46b33-f8b2-4bd0-98dc-c7b0d307cc29"
    # imname = '20200309_lhp1_W10_T14'
    # sname = 'SDB995-5_05'
    # seg_dirpath = "local-data/segmentations"

    # sms = LHPSMS.from_ids_dirpath_imname_sname(ids_uri, seg_dirpath, imname, sname)

    # output_fname = f"{imname}-{sname}-thresh-and-merge.png"
    # tmerge = thresh_and_merge(sms, 50)
    # tmerge.save(output_fname)

    config = ProcessConfig(config_fpath)
    ids_uri = config.raw_config["ids_uri"]
    seg_dirpath = config.raw_config["seg_dirpath"]
    output_dirpath = pathlib.Path(config.raw_config["output_dirpath"])
    output_dirpath.mkdir(exist_ok=True, parents=True)

    def quickrep(d):
        return ", ".join(f"{k}={v}" for k, v in d.items())

    for item in config.raw_config["to_process"]:
        logger.info(f"Processing {quickrep(item)}")
        sms = LHPSMS.from_ids_dirpath_imname_sname(ids_uri, seg_dirpath, **item)
        output_fname = config.raw_config["output_fname_template"].format(**item)
        tmerge = thresh_and_merge(sms, 50)
        tmerge.save(output_dirpath/output_fname)

    


if __name__ == "__main__":
    main()