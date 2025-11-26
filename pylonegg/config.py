import json
import os
from pathlib import Path
import typer


# -----------------------------
# Config commands
# -----------------------------
config_app = typer.Typer(help="Manage Pylonegg config")

@config_app.command("set")
def config_set(key: str, value: str):
    set_config(key, value)
    typer.echo(f"✔ Config '{key}' set.")

@config_app.command("get")
def config_get(key: str):
    value = get(key)
    typer.echo(f"{key} = {value}")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR,"config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_config(config: dict):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def get(key: str, default=None):
    config = load_config()
    return config.get(key, default)

def set_config(key: str, value):
    config = load_config()
    config[key] = value
    save_config(config)