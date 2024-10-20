import yaml


def get_config():

    config = yaml.safe_load(open("config.yml"))

    return config