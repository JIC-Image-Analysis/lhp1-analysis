import sys
import collections

import click
import ruamel.yaml

from dtoolbioimage import ImageDataSet


@click.command()
@click.argument("ids_uri")
@click.argument("imname")
def main(ids_uri, imname):
    output_dirpath = "results/merges"
    seg_dirpath = "local-data/segmentations"

    config_dict = collections.OrderedDict()
    config_dict["ids_uri"] = ids_uri
    config_dict["output_dirpath"] = output_dirpath
    config_dict["seg_dirpath"] = seg_dirpath
    config_dict["output_fname_template"] = "{imname}-{sname}-thresh-and-merge.png"

    ids = ImageDataSet(ids_uri)

    config_dict["to_process"] = [
        {
            "imname": imname,
            "sname": sname
        }
        for sname in ids.get_series_names(imname)
    ]

    yaml = ruamel.yaml.YAML()
    yaml.dump(config_dict, sys.stdout)


if __name__ == "__main__":
    main()