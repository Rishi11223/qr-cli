# qr-cli

[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Generate QR codes right from your terminal. Works with any text or URL — output as ASCII art or save as PNG.

## Features

- Generate QR codes from any text/URL
- Display as ASCII art in terminal
- Save as PNG image
- Custom colors for PNG output
- Pipe input support (`echo "text" | qr`)
- Dark theme support (inverted colors)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic QR in terminal
qr "https://github.com"

# Pipe input
echo "Hello World" | qr

# Save as PNG
qr -o myqr.png "https://example.com"

# Colored QR
qr -o code.png -c blue "Text"

# Inverted (for dark terminals)
qr -i "https://example.com"
```

## Example

```
$ qr "https://github.com"

  ██████████████      ██████████████
  ██          ██  ██  ██          ██
  ██  ██████  ████████  ██████  ██
  ██  ██████  ██  ██  ██  ██████  ██
  ██  ██████  ██  ██  ████  ██  ██
  ██          ██  ██  ████████████
  ██████████████  ██  ██  ██  ██
              ██  ██  ██    ██████
  ████  ████████    ████████  ██
    ████  ██    ██  ██████████████
  ████████████  ████    ██    ██
  ██  ██  ████████  ██████████
    ████████  ██  ██████  ██  ██
  ██████████████    ████████  ██████
  ██          ██  ██  ██████  ██
  ██  ██████  ██    ██  ██  ██████
  ██  ██████  ██  ██  ██      ██
  ██  ██████  ██  ██  ██  ████
  ██          ██    ████  ████████
  ██████████████  ██  ██  ██

Data: https://github.com
Size: 29x29
```

## Requirements

- Python 3.8+
- qrcode[pil]

## Options

| Flag | Description |
|------|-------------|
| `-o, --output FILE` | Save QR as PNG |
| `-c, --color COLOR` | QR color (red, blue, green, or hex) |
| `-b, --background`   | Background color (default: white) |
| `-i, --invert`       | Invert for dark terminals |
