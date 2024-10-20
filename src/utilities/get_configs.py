import yaml


def get_config():

    config = yaml.safe_load(open(r"src\services\config.yml"))

    return config
