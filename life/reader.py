from pathlib import Path
import tomllib

from life.classes import Pattern


PATTERNS_FILE = Path(__file__).parent / "../patterns.toml"


def get_pattern(name: str, file=PATTERNS_FILE) -> Pattern:
    return Pattern.from_toml(name, tomllib.loads(file.read_text())[name])


def get_all_patterns(file=PATTERNS_FILE) -> list[Pattern]:
    data = tomllib.loads(file.read_text())
    return [Pattern.from_toml(name, data[name]) for name in data]
