import logging
import yaml
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    log_level = getattr(logging, config['logging']['level'].upper(), logging.INFO)
    log_file = Path(config['logging']['file_path']).resolve()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    if not logger.handlers:
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_file)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
    return logger
