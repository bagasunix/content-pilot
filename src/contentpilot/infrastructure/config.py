"""YAML config adapter."""
from __future__ import annotations

import yaml

from ..application.ports import ConfigPort
from .paths import Workspace


class YamlConfig(ConfigPort):
    def __init__(self, ws: Workspace):
        self._ws = ws

    def load(self) -> dict:
        return yaml.safe_load(self._ws.config.read_text()) or {}
