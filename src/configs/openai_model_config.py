from typing import Dict
import json


class ModelConfig:
    def __init__(self, config_path: str) -> None:
        self.config_path = config_path
        self.config_dict = self.load_config(config_path=config_path)
        self.set_attributes()

    def set_attributes(self) -> None:
        for key, value in self.config_dict.items():
            setattr(self, key, value)

    @staticmethod
    def load_config(config_path: str) -> Dict:
        with open(config_path, "r") as f:
            return json.load(f)
