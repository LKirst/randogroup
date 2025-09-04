import random

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, Input, Static, Switch, TextArea


class RandogroupApp(App):
    """A Textual app to create random groups."""

    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        with Horizontal(id="mode_selection_container"):
            yield Static("Group Assignment", id="group_assignment_label")
            yield Switch(id="mode_switch")
            yield Static("Student Draw", id="student_draw_label")
        yield TextArea(id="students", text="Enter student names, one per line")
        yield Input(placeholder="Number", id="number_input", type="integer")
        yield Button("Run", id="run_button", variant="primary")
        yield Static(id="results")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "run_button":
            if self.query_one("#mode_switch", Switch).value:
                self.draw_students()
            else:
                self.create_groups()

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

        results_str = ""
        for i, group in enumerate(groups):
            results_str += f"[bold]Group {i + 1}:[/bold] {', '.join(group)}\n"

        self.query_one("#results", Static).update(results_str)

    def create_groups_logic(
        self, students: list[str], num_groups: int
    ) -> list[list[str]]:
        """The logic to create the groups."""
        random.shuffle(students)
        groups = [[] for _ in range(num_groups)]
        for i, student in enumerate(students):
            groups[i % num_groups].append(student)
        return groups


def randogrouper():
    app = RandogroupApp()
    app.run()


if __name__ == "__main__":
    randogrouper()
