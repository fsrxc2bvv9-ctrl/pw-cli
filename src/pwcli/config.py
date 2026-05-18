from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import platformdirs
import tomli_w

if sys.version_info >= (3, 11):
    import tomllib as tomli
else:
    import tomli

CONFIG_DIR = Path(platformdirs.user_config_dir("pwcli"))
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG: dict[str, Any] = {
    "generate": {
        "length": 24,
        "count": 1,
        "uppercase": True,
        "lowercase": True,
        "digits": True,
        "symbols": True,
        "exclude_ambiguous": False,
    },
    "phrase": {
        "words": 6,
        "separator": "-",
        "capitalize": False,
        "numbers": False,
        "count": 1,
    },
}


def load_config() -> dict[str, Any]:
    """Загружает конфиг, мёржит с дефолтами (новые ключи появляются автоматически)."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, "rb") as f:
        user_config = tomli.load(f)

    # Мёрджим, чтобы всегда были все ключи
    config = DEFAULT_CONFIG.copy()
    for section, values in user_config.items():
        if section in config:
            config[section].update(values)
    return config


def save_config(config: dict[str, Any]) -> None:
    """Сохраняет конфиг."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)


def set_config_value(key_path: str, value: Any) -> None:
    """Устанавливает значение по пути типа 'generate.length'."""
    config = load_config()
    keys = key_path.split(".")
    d = config
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value
    save_config(config)


def get_generate_defaults() -> dict[str, Any]:
    config = load_config()
    return config.get("generate", DEFAULT_CONFIG["generate"])


def get_phrase_defaults() -> dict[str, Any]:
    config = load_config()
    return config.get("phrase", DEFAULT_CONFIG["phrase"])
