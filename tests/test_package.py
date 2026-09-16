import unittest
import io
import tempfile
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

import game


class GameUtilitiesTest(unittest.TestCase):
    def test_invalid_json_reports_json_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "submissions").mkdir()
            (root / "submissions" / "bad.json").write_text("{", encoding="utf-8")
            output = io.StringIO()
            with patch.object(game, "ROOT", root), redirect_stdout(output):
                self.assertFalse(game.unlock_with_submission("submissions/bad.json"))
            self.assertIn("JSON invalide", output.getvalue())

    def test_answer_normalization_is_accent_and_separator_tolerant(self):
        self.assertEqual(game.normalize_answer(" Frontière ! "), "FRONTIERE")

    def test_canonical_json_is_independent_of_key_order(self):
        self.assertEqual(
            game.canonical_json({"b": 2, "a": 1}),
            game.canonical_json({"a": 1, "b": 2}),
        )

    def test_validator_configuration_contains_four_hashed_locks(self):
        config = game.load_config()
        self.assertEqual(set(config["locks"]), {"1", "2", "3", "4"})
        for lock in config["locks"].values():
            hash_values = [value for key, value in lock.items() if key.endswith("sha256")]
            self.assertTrue(hash_values)
            self.assertTrue(all(len(value) == 64 for value in hash_values))

    def test_candidate_context_ids_are_unique(self):
        candidate_dir = game.ROOT / "missions" / "04_contexte" / "candidats"
        ids = []
        for path in candidate_dir.glob("*.md"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith("context_id:"):
                    ids.append(line.split(":", 1)[1].strip())
                    break
        self.assertEqual(len(ids), 8)
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
