import pytest

from randogroup.app import RandogroupApp


@pytest.fixture
def app():
    """Fixture to create an instance of the app."""
    return RandogroupApp()


def test_create_groups(app):
    """Test the group creation logic."""
    students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
    num_groups = 3
    groups = app.create_groups_logic(students, num_groups)

    assert len(groups) == num_groups

    # Check that all students are in the groups
    all_grouped_students = [student for group in groups for student in group]
    assert set(all_grouped_students) == set(students)

    # Check that the groups are roughly equal in size
    min_group_size = len(students) // num_groups
    max_group_size = min_group_size + 1
    for group in groups:
        assert min_group_size <= len(group) <= max_group_size


def test_create_groups_empty_students(app):
    """Test group creation with no students."""
    students = []
    num_groups = 3
    groups = app.create_groups_logic(students, num_groups)
    assert len(groups) == num_groups
    for group in groups:
        assert len(group) == 0


def test_create_groups_more_groups_than_students(app):
    """Test group creation with more groups than students."""
    students = ["Alice", "Bob"]
    num_groups = 3
    groups = app.create_groups_logic(students, num_groups)

    assert len(groups) == num_groups

    # Check that all students are in the groups
    all_grouped_students = [student for group in groups for student in group]
    assert set(all_grouped_students) == set(students)

    # Check that some groups are empty
    assert any(len(group) == 0 for group in groups)


def test_create_groups_deterministic(app):
    """Test that creating groups with a seed is deterministic."""
    students = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
    num_groups = 3
    seed = "test-seed"

    groups_1 = app.create_groups_logic(list(students), num_groups, seed=seed)
    groups_2 = app.create_groups_logic(list(students), num_groups, seed=seed)

    assert groups_1 == groups_2
