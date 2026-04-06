# PDF Compressor for macOS

A powerful GUI application to compress PDF files using Ghostscript, built with Python and Tkinter.

## Features

- **Simple GUI** — Easy-to-use interface with file browsers
- **Multiple compression levels** — Light, medium, and heavy compression options
- **Effective compression** — Uses Ghostscript for industry-standard PDF compression (30-70% size reduction)
- **Auto-naming** — Automatically suggests output filename
- **Progress indication** — Shows compression progress
- **File size comparison** — Displays original vs compressed file sizes
- **Error handling** — Comprehensive error checking and user feedback
- **macOS optimized** — Designed specifically for macOS but works cross-platform

## Compression Levels

- **Light**: 150 DPI image quality (good for general use)
- **Medium**: 150 DPI with /ebook preset (balanced quality and size)
- **Heavy**: 72 DPI image quality (maximum compression, smaller files)

## Dependencies

- Python 3
- [Ghostscript](https://www.ghostscript.com/) — Industry-standard PDF processor
- Tkinter (included with Python on macOS)

## Installation & Usage

### Install Ghostscript

On macOS using Homebrew:

```bash
brew install ghostscript
```

### Run the app directly

```bash
python3 pdf_compressor.py
```

## Build macOS App Bundle

To create a native macOS .app bundle:

1. Install build dependencies:

```bash
pip3 install py2app
```

2. Build the app:

```bash
python3 setup.py py2app
```

3. The app bundle will be created in the `dist/` folder. You can move `pdf_compressor.app` to your Applications folder.

## Notes

- The app automatically handles encrypted PDFs
- Compression times may vary depending on PDF size and complexity
- Built app bundle includes all dependencies except Ghostscript (must be installed separately)
