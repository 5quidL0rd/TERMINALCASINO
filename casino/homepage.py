from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.widgets import Button, Footer, Header, Input, Label, Static

DEFAULT_PLAYER_NAME = "Player"


class HomePage(App):
    """Homepage with the casino header, a name input, and a button for each game."""

    TITLE = "Terminal Casino"

    CSS = """
    Screen {
        align: center top;
    }
    #casino-header {
        width: auto;
        color: gold;
        text-style: bold;
    }
    #name-input {
        width: 44;
    }
    #game-prompt {
        margin-top: 1;
    }
    #game-buttons {
        grid-size: 3;
        grid-gutter: 1;
        width: 80;
        height: auto;
    }
    #game-buttons Button {
        width: 100%;
    }
    #exit {
        margin-top: 1;
    }
    """

    def __init__(self, header: str, game_names: list[str], player_name: str = "") -> None:
        """Store the header text, the games to show, and any name entered earlier."""
        super().__init__()
        self.header = header
        self.game_names = game_names
        self.player_name = player_name

    def compose(self) -> ComposeResult:
        """Build the header, name input, game buttons, and exit button."""
        yield Header()
        yield Static(self.header, id="casino-header")
        yield Input(value=self.player_name, placeholder="Enter your name", id="name-input")
        yield Label("Choose a game to play:", id="game-prompt")
        with Grid(id="game-buttons"):
            for game in self.game_names:
                # The button's name holds the game key so we know which one was clicked
                yield Button(game.title(), name=game)
        yield Button("Exit", id="exit", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Close Textual and hand back the player's name and the chosen game."""
        if event.button.id == "exit":
            self.exit(None)
            return

        name = self.query_one("#name-input", Input).value.strip()
        if not name:
            name = DEFAULT_PLAYER_NAME
        self.exit((name, event.button.name))
