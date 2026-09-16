#!/usr/bin/env python3
"""Affiche l’alerte brute reçue du portail de support simulé."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
alert_path = ROOT / "missions" / "03_messager" / "alert.json"
print(json.dumps(json.loads(alert_path.read_text(encoding="utf-8")), indent=2, ensure_ascii=False))

