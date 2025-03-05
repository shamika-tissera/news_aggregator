import yaml

def load_config(cfg_path: str) -> dict:
    """
    Load configuration from a YAML file.

    Args:
        cfg_path (str): Path to the YAML configuration file.

    Returns:
        dict: Dictionary with configuration parameters.
    """
    with open(cfg_path, "r") as f:
        config = yaml.safe_load(f)
    return config
