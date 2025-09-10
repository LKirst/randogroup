"""This module handles the loading and creation of student lists.

It uses the `platformdirs` library to store the student lists in a
user-editable JSON file.
"""

import json
from pathlib import Path

from platformdirs import user_data_dir

APP_NAME = "randogroup"
APP_AUTHOR = "randogroup"


def get_student_lists_path(test_path: Path | None = None) -> Path:
    """Get the path to the student lists JSON file."""
    if test_path:
        return test_path
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "student_lists.json"


def create_default_student_lists(path: Path):
    """Create a default student lists JSON file."""
    default_lists = {}
    with open(path, "w") as f:
        json.dump(default_lists, f, indent=2)


def load_student_lists(test_path: Path | None = None) -> dict[str, list[str]]:
    """Load student lists from the JSON file.

    If the file doesn't exist, create a default one.
    """
    lists_path = get_student_lists_path(test_path)
    if not lists_path.exists():
        create_default_student_lists(lists_path)

    with open(lists_path) as f:
        return json.load(f)


def save_student_lists(
    student_lists: dict[str, list[str]], test_path: Path | None = None
):
    """Save the student lists to the JSON file."""
    lists_path = get_student_lists_path(test_path)
    with open(lists_path, "w") as f:
        json.dump(student_lists, f, indent=2)


STUDENT_LISTS = load_student_lists()
