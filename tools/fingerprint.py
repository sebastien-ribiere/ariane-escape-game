#!/usr/bin/env python3
"""Calcule l’empreinte d’une enveloppe à partir de quatre champs explicites."""

import argparse
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument("incident_id")
parser.add_argument("severity")
parser.add_argument("egress_route")
parser.add_argument("issued_at")
args = parser.parse_args()

value = "|".join((args.incident_id, args.severity, args.egress_route, args.issued_at))
print(hashlib.sha256(value.encode("utf-8")).hexdigest()[:10].upper())

