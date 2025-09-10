import random

from rich.console import Group as RichGroup
from rich.panel import Panel
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Right, VerticalScroll
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Select,
    Static,
    Switch,
    TextArea,
)

from .student_lists import load_student_lists, save_student_lists


class RandogroupApp(App):
    def __init__(self, student_lists: dict[str, list[str]] | None = None):
        super().__init__()
        self.initial_student_lists = student_lists
        if student_lists is not None:
            self.student_lists = student_lists
        else:
            self.student_lists = load_student_lists()

    """A Textual app to create random groups."""

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(name="Randogroup")
        yield Footer()

        with Horizontal(id="mode_selection_container"):
            yield Static("Group Assignment", id="group_assignment_label")
            yield Switch(id="mode_switch")
            yield Static("Student Draw", id="student_draw_label")

        with Horizontal(id="global_horizontal"):
            with VerticalScroll(id="student_list_container"):
                yield Select(
                    options=[(key, key) for key in self.student_lists],
                    id="student_list_select",
                    prompt="New student list",
                )
                yield Input(placeholder="List name", id="list_name_input")
                yield TextArea(id="students", text="")
                with Horizontal(id="student_list_buttons_container"):
                    yield Button(chr(int("eb4b", 16)), id="save_button")
                    yield Button(chr(int("f01b4", 16)), id="delete_button")
                yield Input(placeholder="Number", id="number_input", type="integer")
                with Right(id="run_container"):
                    yield Button(
                        chr(int("eb2c", 16)), id="run_button", variant="primary"
                    )

            # TODO: make the results scrollable
            yield Static(id="results")

    def on_select_changed(self, event: Select.Changed) -> None:
        """Event handler called when a select option is changed."""
        if event.select.id == "student_list_select":
            self.update_student_list(str(event.value))

    def update_student_list(self, list_name: str) -> None:
        """Update the TextArea with the selected student list."""
        students = self.student_lists.get(list_name, [])
        self.query_one("#students", TextArea).text = "\n".join(students)
        self.query_one("#list_name_input", Input).value = list_name

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "run_button":
            if self.query_one("#mode_switch", Switch).value:
                self.draw_students()
            else:
                self.create_groups()
        elif event.button.id == "save_button":
            self.save()
        elif event.button.id == "delete_button":
            self.delete_list()

    def delete_list(self) -> None:
        """Delete the selected student list."""
        select = self.query_one(Select)
        list_name = str(select.value)
        if list_name in self.student_lists:
            del self.student_lists[list_name]
            select.set_options([(key, key) for key in self.student_lists])
            if self.student_lists:
                first_list_name = next(iter(self.student_lists))
                select.value = first_list_name
                self.update_student_list(first_list_name)
            else:
                self.query_one("#students", TextArea).text = ""
                self.query_one("#list_name_input", Input).value = ""

    def save(self) -> None:
        """Save the changes to the student lists."""
        old_list_name = str(self.query_one(Select).value)
        new_list_name = self.query_one("#list_name_input", Input).value
        if not new_list_name:
            return

        if old_list_name != new_list_name and old_list_name in self.student_lists:
            del self.student_lists[old_list_name]

        students = self.query_one("#students", TextArea).text.splitlines()
        self.student_lists[new_list_name] = [
            name.strip() for name in students if name.strip()
        ]
        save_student_lists(self.student_lists, None)

        select = self.query_one(Select)
        select.set_options([(key, key) for key in self.student_lists])
        select.value = new_list_name

    def draw_students(self) -> None:
        """Draw a number of students from the list."""
        students_text = self.query_one("#students", TextArea).text
        students = [name.strip() for name in students_text.splitlines() if name.strip()]

        try:
            number_input = self.query_one("#number_input", Input)
            num_to_draw = int(number_input.value)
        except (ValueError, TypeError):
            self.query_one("#results", Static).update(
                "[bold red]Please enter a valid number.[/bold red]"
            )
            return

        if not students:
            self.query_one("#results", Static).update(
                "[bold red]Please enter some student names.[/bold red]"
            )
            return

        if num_to_draw <= 0:
            self.query_one("#results", Static).update(
                "[bold red]Number to draw must be greater than 0.[/bold red]"
            )
            return

        drawn_students = self.draw_students_logic(students, num_to_draw)

        results_str = f"[bold]Drawn students:[/bold] {', '.join(drawn_students)}"

        self.query_one("#results", Static).update(results_str)

    def draw_students_logic(self, students: list[str], num_to_draw: int) -> list[str]:
        """The logic to draw students."""
        return random.sample(students, min(num_to_draw, len(students)))

    def create_groups(self) -> None:
        """Create the groups and display them."""
        students_text = self.query_one("#students", TextArea).text
        students = [name.strip() for name in students_text.splitlines() if name.strip()]

        try:
            num_groups_input = self.query_one("#number_input", Input)
            num_groups = int(num_groups_input.value)
        except (ValueError, TypeError):
            self.query_one("#results", Static).update(
                "[bold red]Please enter a valid number of groups.[/bold red]"
            )
            return

        if not students:
            self.query_one("#results", Static).update(
                "[bold red]Please enter some student names.[/bold red]"
            )
            return

        if num_groups <= 0:
            self.query_one("#results", Static).update(
                "[bold red]Number of groups must be greater than 0.[/bold red]"
            )
            return

        groups = self.create_groups_logic(students, num_groups)

        # Use Rich to create panels for each group
        panels = []
        colors = ["red", "green", "blue", "yellow", "magenta", "cyan"]
        for i, group in enumerate(groups):
            panel = Panel(
                f"[bold]Group {i + 1}:[/bold] {', '.join(group)}",
                title=f"Group {i + 1}",
                border_style=colors[i % len(colors)],
            )
            panels.append(panel)

        # Combine all panels into a single Rich Group
        rich_group = RichGroup(*panels)

        # Update the results with the Rich Group
        self.query_one("#results", Static).update(rich_group)

    def create_groups_logic(
        self,
        students: list[str],
        num_groups: int,
    ) -> list[list[str]]:
        """The logic to create the groups."""
        random.shuffle(students)
        groups = [[] for _ in range(num_groups)]
        for i, student in enumerate(students):
            groups[i % num_groups].append(student)
        return groups


def randogrouper():
    student_lists = load_student_lists()
    app = RandogroupApp(student_lists=student_lists)
    app.run()


if __name__ == "__main__":
    randogrouper()
