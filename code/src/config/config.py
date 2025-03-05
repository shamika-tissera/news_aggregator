import os
import yaml

def load_config(cfg_path: str) -> dict:
    """
    Load configuration from a YAML file.

    Args:
        cfg_path (str): Path to the YAML configuration file.

    Returns:
        dict: Dictionary with configuration parameters.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_path, cfg_path)

    with open(full_path, "r") as f:
        config = yaml.safe_load(f)
    return config
