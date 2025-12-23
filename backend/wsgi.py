from __future__ import annotations

import os
from uniyoklama import create_app

CONFIG_PATH = os.getenv("UNIYOKLAMA_CFG", "config.cfg")

app = create_app(CONFIG_PATH)
