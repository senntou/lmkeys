"""Entry point for lmkeys command-line tool"""

import argparse
import sys
from pathlib import Path

from . import __version__
from .viewer import run_viewer


def main() -> None:
    """Main entry point for the lmkeys application."""
    parser = argparse.ArgumentParser(
        description="Browse LMDB keys with a TUI interface",
        prog="lmkeys"
    )
    parser.add_argument(
        "db_path",
        type=str,
        help="Path to the LMDB directory"
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=30,
        help="Number of keys to display per page (default: 30)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    # Validate path
    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"Error: Path '{args.db_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not db_path.is_dir():
        print(f"Error: Path '{args.db_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Run the viewer
    try:
        run_viewer(str(db_path), args.page_size)
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
