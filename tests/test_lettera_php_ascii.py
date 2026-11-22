import subprocess
import string
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".apm/skills/lettera-php-ascii/scripts/genera_ascii.py"
)


class AsciiPhpTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)

    def run_script(self, *paths):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(path) for path in paths)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_counts_case_sensitive_content_and_generates_per_file(self):
        first = self.root / "first.php"
        first.write_text("<?php // AAAAAaaa ?>", encoding="utf-8")
        nested = self.root / ".nested"
        nested.mkdir()
        second = nested / "second.php"
        second.write_text("<?php // zzzzzzZZ ?>", encoding="utf-8")

        result = self.run_script(self.root, first)

        self.assertEqual(result.returncode, 0, result.stderr)
        first_art = Path(str(first) + ".ascii.txt").read_text(encoding="utf-8")
        second_art = Path(str(second) + ".ascii.txt").read_text(encoding="utf-8")
        self.assertTrue(first_art.startswith("Lettera: A\nOccorrenze: 5\n\n"))
        self.assertTrue(second_art.startswith("Lettera: z\nOccorrenze: 6\n\n"))
        self.assertIn("#####", first_art)
        self.assertIn("#####", second_art)
        self.assertEqual(first.read_text(encoding="utf-8"), "<?php // AAAAAaaa ?>")

    def test_tie_selects_first_appearance(self):
        source = self.root / "tie.php"
        source.write_text("<?php // zzzZZZ ?>", encoding="utf-8")

        result = self.run_script(source)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Lettera: z\nOccorrenze: 3\n", Path(str(source) + ".ascii.txt").read_text())

    def test_art_is_generated_for_every_supported_letter(self):
        for letter in string.ascii_letters:
            (self.root / f"{ord(letter)}.php").write_text(
                f"<?= '{letter * 10}'; ?>", encoding="utf-8"
            )

        result = self.run_script(self.root)

        self.assertEqual(result.returncode, 0, result.stderr)
        for letter in string.ascii_letters:
            output = (self.root / f"{ord(letter)}.php.ascii.txt").read_text(
                encoding="utf-8"
            )
            header, drawing = output.split("\n\n")
            self.assertEqual(header, f"Lettera: {letter}\nOccorrenze: 10")
            self.assertEqual(len(drawing.splitlines()), 7)
            self.assertTrue(all(len(row) == 5 for row in drawing.splitlines()))
            self.assertIn("#", drawing)
        self.assertNotEqual(
            (self.root / "65.php.ascii.txt").read_text().split("\n\n")[1],
            (self.root / "97.php.ascii.txt").read_text().split("\n\n")[1],
        )

    def test_existing_output_is_not_overwritten_and_other_files_continue(self):
        first = self.root / "a.php"
        second = self.root / "b.php"
        first.write_text("<?php ?>", encoding="utf-8")
        second.write_text("<?php ?>", encoding="utf-8")
        output = Path(str(first) + ".ascii.txt")
        output.write_text("da conservare", encoding="utf-8")

        result = self.run_script(self.root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Errore:", result.stderr)
        self.assertEqual(output.read_text(), "da conservare")
        self.assertTrue(Path(str(second) + ".ascii.txt").exists())

    def test_invalid_inputs_are_reported(self):
        no_letters = self.root / "empty.php"
        no_letters.write_text("123 !!!", encoding="utf-8")
        bad_encoding = self.root / "invalid.php"
        bad_encoding.write_bytes(b"\xff")

        result = self.run_script(no_letters, bad_encoding, self.root / "missing.php")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nessuna lettera ASCII", result.stderr)
        self.assertIn("invalid.php", result.stderr)
        self.assertIn("missing.php", result.stderr)
        self.assertFalse(Path(str(no_letters) + ".ascii.txt").exists())
        self.assertFalse(Path(str(bad_encoding) + ".ascii.txt").exists())

    def test_symbolic_directories_are_reported(self):
        target = self.root / "target"
        target.mkdir()
        (target / "example.php").write_text("<?php ?>", encoding="utf-8")
        (self.root / "link").symlink_to(target, target_is_directory=True)

        result = self.run_script(self.root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("directory simbolica non esplorata", result.stderr)
        self.assertTrue((target / "example.php.ascii.txt").exists())


if __name__ == "__main__":
    unittest.main()
