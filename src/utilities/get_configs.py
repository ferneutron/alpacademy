import yaml


def get_config():

    config = yaml.safe_load(open("src/services/config.yml"))

    return config

def get_config_services():

    config = yaml.safe_load(open("config.yml"))

    return config