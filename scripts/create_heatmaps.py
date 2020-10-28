import logging
import pathlib

import click
import numpy as np
import pandas as pd

import skimage.restoration

from dtoolbioimage import Image as dbiImage, scale_to_uint8
from dtoolbioimage.segment import Segmentation, Segmentation3D

from stacktools.segmentation import filter_segmentation_by_region_list

from data import LHPSMS
from config import ProcessConfig
from utils import selective_border_region_labels


def get_borderless_seg_plane(sms, z):
    # TODO - make this more explicitly about volume
    blessed_regions = list(range(3, 300))
    sms.filtered_seg_by_region_size = filter_segmentation_by_region_list(sms.segmentation, blessed_regions).view(Segmentation3D)

    regions_in_plane = set(np.unique(sms.filtered_seg_by_region_size[:,:,z]))
    border_regions = selective_border_region_labels(sms.filtered_seg_by_region_size)
    selected_regions = regions_in_plane - border_regions
    filtered_by_plane_regions = filter_segmentation_by_region_list(sms.filtered_seg_by_region_size, selected_regions)

    seg_plane = filtered_by_plane_regions[:,:,z]

    return Segmentation.from_array(seg_plane)


def visualise_segmentation(sms, z):

    seg_plane = get_borderless_seg_plane(sms, z)

    return Segmentation.from_array(seg_plane).label_id_image


def visualise_segmentation_and_dn_measure(sms, z):
    seg_plane = get_borderless_seg_plane(sms, z)
    measure_plane = sms.measure_stack[:,:,z]
    dn2d = skimage.restoration.denoise_tv_chambolle(measure_plane)

    return (0.7 * np.dstack(3 * [scale_to_uint8(dn2d)]) + 0.3 * seg_plane.pretty_color_image).view(dbiImage)


def create_colour_func(values):
    vmin = min(values)
    vmax = max(values)
    vdiff = vmax - vmin
    
    def colour_func(v):
        G = int(255 * ((v - vmin) / vdiff))
        R = 255 - G
        return R, G, 0
    
    return colour_func


def measure_rid(sms, rid):
    coords = np.where(sms.segmentation==rid)
    return np.mean(sms.measure_stack[coords])


def get_regions_to_measure(sms):
    blessed_regions = set(range(3, 300))
    sms.filtered_seg_by_region_size = filter_segmentation_by_region_list(sms.segmentation, blessed_regions).view(Segmentation3D)

    border_regions = selective_border_region_labels(sms.filtered_seg_by_region_size)
    selected_regions = blessed_regions - border_regions

    return selected_regions


def measure_mean_region_intensities(sms, z):
    measurements = {
        rid: measure_rid(sms, rid)
        for rid in get_regions_to_measure(sms)
    }


def measure_properties(sms, rid):
    mean_intensity = measure_rid(sms, rid)

    measurement = {
        "label": rid,
        "mean_intensity": mean_intensity
    }

    return measurement


def create_heatmap(sms, z):
    measurements = [
        measure_properties(sms, rid)
        for rid in get_regions_to_measure(sms)
    ]

    intensities_by_label = {
        measurement['label']: measurement['mean_intensity']
        for measurement in measurements
    }

    rdim, cdim, _ = sms.measure_stack.shape
    heatmap = np.zeros((rdim, cdim, 3), dtype=np.uint8)
    colour_func = create_colour_func(intensities_by_label.values())

    seg_plane = get_borderless_seg_plane(sms, z)
    for l, intensity in intensities_by_label.items():
        coords = np.where(seg_plane==l)
        heatmap[coords] = colour_func(intensity)

    return heatmap.view(dbiImage)


@click.command()
@click.argument('config_fpath')
def main(config_fpath):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("visSegmentation")

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
        heatmap = create_heatmap(sms, 50)
        heatmap.save(output_dirpath/output_fname)
    


if __name__ == "__main__":
    main()