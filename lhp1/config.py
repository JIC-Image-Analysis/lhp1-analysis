import ruamel.yaml


class ProcessConfig(object):

    def __init__(self, config_fpath):

        yaml = ruamel.yaml.YAML()
        with open(config_fpath) as fh:
            self.raw_config = yaml.load(fh)