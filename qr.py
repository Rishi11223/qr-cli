#!/usr/bin/env python3

import sys
import os
import argparse

GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
DIM = '\033[2m'
RESET = '\033[0m'

QR_CHARS = {
    "light": "  ",
    "dark": "██",
}


def qr_to_ascii(qr_matrix, invert=False):
    dark, light = QR_CHARS["dark"], QR_CHARS["light"]
    if invert:
        dark, light = light, dark

    lines = []
    n = len(qr_matrix)
    border = 2

    lines.append(" " * border + "█" * (n + 2 * border))
    for _ in range(border):
        lines.append(" " * border + "█" + " " * n + "█")
    for row in qr_matrix:
        line = " " * border + "█"
        for cell in row:
            line += light if cell else dark
        line += "█"
        lines.append(line)
    for _ in range(border):
        lines.append(" " * border + "█" + " " * n + "█")
    lines.append(" " * border + "█" * (n + 2 * border))

    return "\n".join(lines)


def generate_qr(data, version=1, box_size=10, border=4):
    try:
        import qrcode
    except ImportError:
        print(f"{RED}Error: 'qrcode' library not found.{RESET}")
        print(f"Install: {YELLOW}pip install qrcode[pil]{RESET}")
        sys.exit(1)

    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.get_matrix()


def save_image(data, filename, fill="black", back="white"):
    try:
        import qrcode
        from PIL import Image, ImageDraw
    except ImportError:
        print(f"{RED}Error: 'qrcode[pil]' not installed.{RESET}")
        print(f"Install: {YELLOW}pip install qrcode[pil]{RESET}")
        sys.exit(1)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")

    if fill.startswith("#") or back.startswith("#"):
        pass
    else:
        color_map = {
            "red": "#FF0000", "blue": "#0000FF", "green": "#00AA00",
            "cyan": "#00AAAA", "magenta": "#AA00AA", "yellow": "#AAAA00",
            "orange": "#FF8800", "purple": "#8800AA",
        }
        fill = color_map.get(fill, fill)
        back = color_map.get(back, back)

    if fill.startswith("#") or back.startswith("#"):
        img = qr.make_image(fill_color=fill, back_color=back).convert("RGB")

    img.save(filename)
    print(f"{GREEN}✓{RESET} QR code saved to {YELLOW}{filename}{RESET}")


def read_stdin():
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return None


def main():
    parser = argparse.ArgumentParser(
        prog="qr",
        description="Generate QR codes from the terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{BOLD}Examples:{RESET}
  {CYAN}qr \"https://example.com\"{RESET}
  {CYAN}echo \"Hello World\" | qr{RESET}
  {CYAN}qr -o code.png \"https://example.com\"{RESET}
  {CYAN}qr -o code.png -c red \"Text\"{RESET}
  {CYAN}qr -i \"Text\"{RESET}
""",
    )
    parser.add_argument("text", nargs="?", help="Text or URL to encode")
    parser.add_argument("-o", "--output", help="Save QR as PNG image")
    parser.add_argument("-c", "--color", default="black", help="QR color (default: black)")
    parser.add_argument("-b", "--background", default="white", help="Background color (default: white)")
    parser.add_argument("-i", "--invert", action="store_true", help="Invert terminal colors (for dark themes)")

    args = parser.parse_args()

    text = args.text or read_stdin()

    if not text:
        parser.print_help()
        print(f"\n{RED}Error: No input provided{RESET}")
        print(f"Usage: {CYAN}qr \"your text here\"{RESET}")
        print(f"   or: {CYAN}echo \"your text\" | qr{RESET}")
        sys.exit(1)

    if args.output:
        save_image(text, args.output, args.color, args.background)
    else:
        matrix = generate_qr(text)
        ascii_qr = qr_to_ascii(matrix, invert=args.invert)
        print()
        print(ascii_qr)
        print()
        print(f"{DIM}Data: {text[:60]}{'...' if len(text) > 60 else ''}{RESET}")
        print(f"{DIM}Size: {len(matrix)}x{len(matrix)}{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Error:{RESET} {e}")
        sys.exit(1)
