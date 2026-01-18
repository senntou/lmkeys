# lmkeys

A TUI tool for browsing LMDB database keys in the terminal.

## Features

- Browse LMDB database keys in a list view
- Pagination support (default: 30 items per page)
- Navigate pages with h/l keys (or arrow keys)
- Display key and value type information
- UTF-8 decodable keys shown as strings, others as hexadecimal
- Safe read-only access mode

## Installation

### Development Installation

```bash
# Clone or navigate to the repository
cd /path/to/lmkeys

# Install in development mode
pip install -e .
```

### Standard Installation

```bash
pip install .
```

## Usage

Basic usage:

```bash
lmkeys /path/to/lmdb/directory
```

Specify page size:

```bash
lmkeys /path/to/lmdb/directory --page-size 50
```

## Key Bindings

- `h` or `←`: Previous page
- `l` or `→`: Next page
- `q`: Quit

## Value Type Display

Value types are determined as follows:

- **str**: UTF-8 decodable and printable strings
- **int/bytes**: Data that could be 1, 2, 4, or 8 byte integers
- **bytes**: Other binary data

Each value shows its type name and byte size (e.g., `str (256 bytes)`)

## Technical Specifications

- **Python**: 3.8 or higher
- **Dependencies**:
  - lmdb >= 1.4.0
  - textual >= 0.47.0

## Project Structure

```
lmkeys/
├── lmkeys/
│   ├── __init__.py      # Package initialization
│   ├── __main__.py      # Command-line entry point
│   ├── viewer.py        # TUI implementation
│   └── utils.py         # Utility functions
├── pyproject.toml       # Project configuration
├── setup.py             # Setup script
├── requirements.txt     # Dependencies
└── README.md            # This file
```

## License

MIT License
