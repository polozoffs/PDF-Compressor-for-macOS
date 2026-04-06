# PDF Compressor for macOS

A simple GUI application to compress PDF files, built with Python and Tkinter.

## Features

- **Simple GUI** — Easy-to-use interface with file browsers
- **Multiple compression levels** — Light, medium, and heavy compression options
- **Auto-naming** — Automatically suggests output filename
- **Progress indication** — Shows compression progress
- **File size comparison** — Displays original vs compressed file sizes
- **Error handling** — Comprehensive error checking and user feedback
- **macOS optimized** — Designed specifically for macOS but works cross-platform

## Dependencies

- Python 3
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- Tkinter (included with Python on macOS)

## Installation & Usage

Install the required dependency:

```bash
pip3 install PyPDF2
```

Make it executable (optional):

```bash
chmod +x pdf_compressor.py
```

Run the app:

```bash
python3 pdf_compressor.py
```

## Optional: Create a macOS App Bundle

To make it feel more like a native macOS app, you can create an app bundle.

Install py2app:

```bash
pip3 install py2app
```

Create `setup.py`:

```python
from setuptools import setup

APP = ['pdf_compressor.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'PyPDF2'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

Build the app:

```bash
python3 setup.py py2app
```

This will create a `.app` bundle in the `dist` folder that you can move to your Applications folder.
