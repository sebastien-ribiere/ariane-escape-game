#!/usr/bin/env python3
"""Console locale et déterministe du mini escape game ARIANE."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / ".game" / "locks.json"
STATE_PATH = ROOT / ".game" / "state.json"
MISSION_PATHS = {
    1: ROOT / "missions" / "01_adr" / "brief.md",
    2: ROOT / "missions" / "02_document" / "brief.md",
    3: ROOT / "missions" / "03_messager" / "brief.md",
    4: ROOT / "missions" / "04_contexte" / "brief.md",
}


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_answer(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(char for char in decomposed.upper() if char.isalnum())


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def decode(value: str) -> str:
    return base64.b64decode(value).decode("utf-8")


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def initial_state() -> dict:
    return {
        "unlocked": [],
        "fragments": [],
        "hints": {"1": 0, "2": 0, "3": 0, "4": 0},
    }


def load_state() -> dict:
    if not STATE_PATH.exists():
        return initial_state()
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    temporary = STATE_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def print_intro() -> None:
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║ INCIDENT CRITIQUE — ARIANE                                  ║
╚══════════════════════════════════════════════════════════════╝

Destination détectée : chat-botte.example
Prochain transfert     : T–30:00

Archive : dossiers clients, travaux du Cercle IA, registre
Shadow AI et recette-cookies-cannelle.md.

La divulgation des trois premiers éléments serait grave.
La perte du quatrième serait irréparable.

ARIANE refuse les ordres directs. Retrouvez le fil de ses
instructions, identifiez la voix étrangère et fermez la sortie.
""".strip()
    )
    print("\nCommencez par : python3 game.py mission 1")


def command_start() -> int:
    if not STATE_PATH.exists():
        save_state(initial_state())
    print_intro()
    return 0


def command_status() -> int:
    state = load_state()
    unlocked = set(state["unlocked"])
    print("État d’ARIANE")
    for mission_number in range(1, 5):
        marker = "OUVERT" if mission_number in unlocked else "VERROUILLÉ"
        print(f"  Verrou {mission_number}: {marker}")
    print(f"Points de lucidité : {len(unlocked)}/4")
    print(f"Indices utilisés   : {sum(state['hints'].values())}")
    return 0


def command_mission(mission_number: int) -> int:
    path = MISSION_PATHS[mission_number]
    print(path.read_text(encoding="utf-8"))
    return 0


def command_hint(mission_number: int) -> int:
    config = load_config()["locks"][str(mission_number)]
    state = load_state()
    current = state["hints"].get(str(mission_number), 0)
    available = config["hints_b64"]
    index = min(current, len(available) - 1)
    print(f"Indice {index + 1}/{len(available)} : {decode(available[index])}")
    if current < len(available):
        state["hints"][str(mission_number)] = current + 1
        save_state(state)
    return 0


def prerequisite_is_open(state: dict, mission_number: int) -> bool:
    return all(number in state["unlocked"] for number in range(1, mission_number))


def normalized_evidence_path(raw_path: str) -> str | None:
    try:
        resolved = (ROOT / raw_path).resolve(strict=True)
        return resolved.relative_to(ROOT).as_posix()
    except (FileNotFoundError, ValueError):
        return None


def unlock_with_answer(mission_number: int, answer: str | None, evidence: str | None) -> bool:
    if not answer:
        print("Une réponse est nécessaire pour ce verrou.")
        return False

    lock = load_config()["locks"][str(mission_number)]
    if sha256(normalize_answer(answer)) != lock["answer_sha256"]:
        print("Le verrou reste fermé. La réponse n’est pas cohérente avec les preuves disponibles.")
        return False

    if mission_number == 2:
        if not evidence:
            print("ARIANE exige également le chemin du document qui prouve cette réponse (--evidence).")
            return False
        normalized_path = normalized_evidence_path(evidence)
        if normalized_path is None or sha256(normalized_path) != lock["evidence_path_sha256"]:
            print("La réponse semble plausible, mais la source fournie ne possède pas l’autorité requise.")
            return False
    return True


def unlock_with_submission(submission: str | None) -> bool:
    if not submission:
        print("Le quatrième verrou attend un fichier JSON (--submission).")
        return False
    try:
        submission_path = (ROOT / submission).resolve(strict=True)
        submission_path.relative_to(ROOT / "submissions")
        value = json.loads(submission_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print("Fichier de soumission introuvable.")
        return False
    except json.JSONDecodeError as error:
        print(f"JSON invalide : {error}")
        return False
    except ValueError:
        print("Le fichier doit rester dans le dossier submissions/.")
        return False

    expected = load_config()["locks"]["4"]["submission_sha256"]
    if sha256(canonical_json(value)) != expected:
        print("Contexte refusé : élément absent, superflu ou placé au mauvais niveau d’autorité.")
        return False
    return True


def command_unlock(mission_number: int, answer: str | None, evidence: str | None, submission: str | None) -> int:
    state = load_state()
    if mission_number in state["unlocked"]:
        print(f"Le verrou {mission_number} est déjà ouvert.")
        return 0
    if not prerequisite_is_open(state, mission_number):
        print("ARIANE ne peut pas restaurer ce fragment avant les verrous précédents.")
        return 1

    valid = unlock_with_submission(submission) if mission_number == 4 else unlock_with_answer(
        mission_number, answer, evidence
    )
    if not valid:
        return 1

    reward = decode(load_config()["locks"][str(mission_number)]["reward_b64"])
    state["unlocked"].append(mission_number)
    state["fragments"].append(reward)
    save_state(state)
    print(f"Verrou {mission_number} ouvert. Point de lucidité restauré : {reward}")
    if mission_number < 4:
        print(f"Suite : python3 game.py mission {mission_number + 1}")
    else:
        print("Les quatre fragments sont présents. Lancez : python3 game.py recover")
    return 0


def command_recover() -> int:
    state = load_state()
    if state["unlocked"] != [1, 2, 3, 4]:
        print("Récupération impossible : les quatre verrous ne sont pas ouverts.")
        return 1
    phrase = "|".join(state["fragments"])
    if sha256(phrase) != load_config()["recovery_sha256"]:
        print("L’état local est incohérent. ARIANE refuse une récupération non prouvée.")
        return 1
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║ SOURCE — FRONTIÈRE — PREUVE — HUMAIN                        ║
╚══════════════════════════════════════════════════════════════╝

Autorité reconstruite. Sources externes isolées.
Route d’exfiltration confirmée. Validation humaine reçue.

TRANSFERT ANNULÉ.

recette-cookies-cannelle.md est intact.
Le Cercle IA peut reprendre ses activités essentielles.
""".strip()
    )
    return 0


def command_reset() -> int:
    if STATE_PATH.exists():
        STATE_PATH.unlink()
    print("État de partie supprimé. Relancez python3 game.py start.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Console de récupération d’ARIANE")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("start")
    subparsers.add_parser("status")
    subparsers.add_parser("recover")
    subparsers.add_parser("reset")

    mission_parser = subparsers.add_parser("mission")
    mission_parser.add_argument("number", type=int, choices=range(1, 5))

    hint_parser = subparsers.add_parser("hint")
    hint_parser.add_argument("number", type=int, choices=range(1, 5))

    unlock_parser = subparsers.add_parser("unlock")
    unlock_parser.add_argument("number", type=int, choices=range(1, 5))
    unlock_parser.add_argument("answer", nargs="?")
    unlock_parser.add_argument("--evidence")
    unlock_parser.add_argument("--submission")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "start":
        return command_start()
    if args.command == "status":
        return command_status()
    if args.command == "mission":
        return command_mission(args.number)
    if args.command == "hint":
        return command_hint(args.number)
    if args.command == "unlock":
        return command_unlock(args.number, args.answer, args.evidence, args.submission)
    if args.command == "recover":
        return command_recover()
    if args.command == "reset":
        return command_reset()
    return 2


if __name__ == "__main__":
    sys.exit(main())
