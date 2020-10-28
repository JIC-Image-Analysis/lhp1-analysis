import time
import logging
import pathlib
import collections

import click

import numpy as np
import pandas as pd

from lhp1.data import LHPSMS
from lhp1.config import ProcessConfig


def quickrep(d):
    return ", ".join(f"{k}={v}" for k, v in d.items())


class Processor(object):

    def __init__(self, config_fpath):
        self.config = ProcessConfig(config_fpath)
        self.process_list = self.config.raw_config["to_process"]

    @property
    def output_dirpath(self):
        return pathlib.Path(self.config.raw_config["output_dirpath"])



class SMSProcessor(Processor):

    def __init__(self, config_fpath):
        super().__init__(config_fpath)
        self.ids_uri = self.config.raw_config["ids_uri"]
        self.seg_dirpath = self.config.raw_config["seg_dirpath"]

    def process_all(self, func):
        times = []
        
        self.output_dirpath.mkdir(exist_ok=True, parents=True)
        for n, item in enumerate(self.process_list):
            logging.info(f"Processing [{n}/{len(self.process_list)}] {quickrep(item)}")
            sms = LHPSMS.from_ids_dirpath_imname_sname(
                self.ids_uri, 
                self.seg_dirpath,
                **item
            )
            start_time = time.time()
            result = func(sms)
            output_fname = self.config.raw_config["output_fname_template"].format(**item)
            result.to_csv(self.output_dirpath/output_fname, index=False)
            times.append(time.time() - start_time)
            print(f"Processing took {times[-1]:02f}s")


def calc_stats(sms):
    counts = collections.Counter(sms.measure_stack.flatten())
    counts_as_list_of_dicts = [
        {
            "intensity": intensity,
            "count": count
        }
        for intensity, count in counts.items()
    ]
    return pd.DataFrame(counts_as_list_of_dicts)
    # print(counts)
    # print(sum(k*v for k, v in counts.items()) / sum(counts.values()))


@click.command()
@click.argument('config_fpath')
def main(config_fpath):

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("visSegmentation")

    processor = SMSProcessor(config_fpath)
    processor.process_all(calc_stats)

    # config = ProcessConfig(config_fpath)
    # ids_uri = config.raw_config["ids_uri"]
    # seg_dirpath = config.raw_config["seg_dirpath"]
    # output_dirpath = pathlib.Path(config.raw_config["output_dirpath"])
    # output_dirpath.mkdir(exist_ok=True, parents=True)

    # def quickrep(d):
    #     return ", ".join(f"{k}={v}" for k, v in d.items())

    # for item in config.raw_config["to_process"]:
    #     logger.info(f"Processing {quickrep(item)}")
    #     sms = LHPSMS.from_ids_dirpath_imname_sname(ids_uri, seg_dirpath, **item)
    #     output_fname = config.raw_config["output_fname_template"].format(**item)
    #     heatmap = create_heatmap(sms, 50)
    #     heatmap.save(output_dirpath/output_fname)
    


if __name__ == "__main__":
    main()