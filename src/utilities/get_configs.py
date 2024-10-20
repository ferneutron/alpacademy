import yaml


def get_config():

    config = yaml.safe_load(open("src/services/config.yml"))

    return config
