import pytest
import os
import sys
from pathlib import Path

import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))
from config.config import load_config

def test_load_config_simple_yaml():
    config_content = """
    dataset_name: "sh0416/ag_news"
    split: "test"
    """
    config_path = "simple_config.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)

    config = load_config(config_path)
    assert config["dataset_name"] == "sh0416/ag_news"
    assert config["split"] == "test"

    os.remove(config_path)

def test_load_config_complex_yaml():
    config_content = """
    dataset:
      name: "sh0416/ag_news"
      split: "test"
    model:
      type: "bert"
      version: "base"
    """
    config_path = "complex_config.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)

    config = load_config(config_path)
    assert config["dataset"]["name"] == "sh0416/ag_news"
    assert config["dataset"]["split"] == "test"
    assert config["model"]["type"] == "bert"
    assert config["model"]["version"] == "base"

    os.remove(config_path)

def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yaml")

def test_load_config_invalid_yaml():
    config_content = """
    dataset_name: "sh0416/ag_news"
    split: "test
    """  # Note: there is a missing double quote in the "split" value
    config_path = "invalid_config.yaml"
    with open(config_path, "w") as f:
        f.write(config_content)

    with pytest.raises(yaml.YAMLError):
        load_config(config_path)

    os.remove(config_path)
