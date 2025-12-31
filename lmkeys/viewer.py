"""TUI viewer for LMDB keys using Textual"""

import lmdb
from pathlib import Path
from typing import Optional, List, Tuple

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable, Static
from textual.binding import Binding
from textual.containers import Container

from .utils import format_key, format_value_info


class LMDBViewer(App):
    """A Textual app to view LMDB keys."""

    CSS = """
    Screen {
        background: $surface;
    }

    #info {
        height: 3;
        content-align: center middle;
        background: $boost;
        color: $text;
        border: solid $primary;
    }

    DataTable {
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("h", "prev_page", "Previous", key_display="h"),
        Binding("l", "next_page", "Next", key_display="l"),
        ("left", "prev_page", "Previous"),
        ("right", "next_page", "Next"),
    ]

    def __init__(self, db_path: str, page_size: int = 30):
        """
        Initialize the LMDB viewer.

        Args:
            db_path: Path to the LMDB directory
            page_size: Number of keys to display per page
        """
        super().__init__()
        self.db_path = Path(db_path)
        self.page_size = page_size
        self.current_page = 0
        self.env: Optional[lmdb.Environment] = None
        self.total_keys: Optional[int] = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            Static(id="info"),
            DataTable(id="keys_table"),
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the application after DOM is ready."""
        # Open LMDB environment
        try:
            self.env = lmdb.open(
                str(self.db_path),
                readonly=True,
                lock=False,
                max_dbs=0
            )
        except Exception as e:
            self.exit(message=f"Error opening LMDB: {e}")
            return

        # Get total number of keys
        with self.env.begin() as txn:
            self.total_keys = txn.stat()['entries']

        # Set up the data table
        table = self.query_one("#keys_table", DataTable)
        table.add_columns("Index", "Key", "Value Type")
        table.cursor_type = "row"

        # Load first page
        self.load_page(0)

    def load_page(self, page: int) -> None:
        """
        Load and display a specific page of keys.

        Args:
            page: Page number to load (0-indexed)
        """
        if self.env is None or self.total_keys is None:
            return

        # Calculate page bounds
        total_pages = (self.total_keys + self.page_size - 1) // self.page_size
        if page < 0 or page >= total_pages:
            return

        self.current_page = page
        start_idx = page * self.page_size
        end_idx = min(start_idx + self.page_size, self.total_keys)

        # Clear existing rows
        table = self.query_one("#keys_table", DataTable)
        table.clear()

        # Fetch keys for this page
        with self.env.begin() as txn:
            cursor = txn.cursor()
            rows = []

            # Skip to the start position
            if cursor.first():
                for _ in range(start_idx):
                    if not cursor.next():
                        break

                # Collect keys for this page
                for i in range(start_idx, end_idx):
                    key = cursor.key()
                    value = cursor.value()

                    if key is not None:
                        key_str = format_key(key)
                        value_info = format_value_info(value) if value is not None else "None"
                        rows.append((str(i + 1), key_str, value_info))

                    if not cursor.next():
                        break

        # Add rows to table
        for row in rows:
            table.add_row(*row)

        # Update info display
        info = self.query_one("#info", Static)
        info.update(
            f"Page {page + 1}/{total_pages} | "
            f"Showing {start_idx + 1}-{end_idx} of {self.total_keys} keys | "
            f"DB: {self.db_path.name}"
        )

    def action_next_page(self) -> None:
        """Move to the next page."""
        if self.total_keys is None:
            return
        total_pages = (self.total_keys + self.page_size - 1) // self.page_size
        if self.current_page < total_pages - 1:
            self.load_page(self.current_page + 1)

    def action_prev_page(self) -> None:
        """Move to the previous page."""
        if self.current_page > 0:
            self.load_page(self.current_page - 1)

    def on_unmount(self) -> None:
        """Clean up when the app is closed."""
        if self.env is not None:
            self.env.close()


def run_viewer(db_path: str, page_size: int = 30) -> None:
    """
    Run the LMDB viewer application.

    Args:
        db_path: Path to the LMDB directory
        page_size: Number of keys to display per page
    """
    app = LMDBViewer(db_path, page_size)
    app.run()
