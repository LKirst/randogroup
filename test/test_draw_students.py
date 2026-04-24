import pytest

from randogroup.app import RandogroupApp


@pytest.fixture
def app():
    """Fixture to create an instance of the app."""
    return RandogroupApp()


def test_draw_students(app):
    """Test the student drawing logic."""
    students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
    num_to_draw = 3
    drawn_students = app.draw_students_logic(students, num_to_draw)

    assert len(drawn_students) == num_to_draw
    assert set(drawn_students).issubset(set(students))


def test_draw_students_empty_students(app):
    """Test student drawing with no students."""
    students = []
    num_to_draw = 3
    drawn_students = app.draw_students_logic(students, num_to_draw)
    assert len(drawn_students) == 0


def test_draw_more_students_than_available(app):
    """Test drawing more students than available."""
    students = ["Alice", "Bob"]
    num_to_draw = 3
    drawn_students = app.draw_students_logic(students, num_to_draw)

    assert len(drawn_students) == len(students)
    assert set(drawn_students) == set(students)


def test_draw_students_deterministic(app):
    """Test that drawing students with a seed is deterministic."""
    students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
    num_to_draw = 3
    seed = "test-seed"

    drawn_1 = app.draw_students_logic(students, num_to_draw, seed=seed)
    drawn_2 = app.draw_students_logic(students, num_to_draw, seed=seed)

    assert drawn_1 == drawn_2
