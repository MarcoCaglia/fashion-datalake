"""Constants module for fashion datalake."""

from pathlib import Path

ROOT_DIR = Path(__file__).parents[3].resolve()
SPIDER_CONFIG_PATH = ROOT_DIR.joinpath("properties", "spider_config.yml")
