import argparse
import sys
from pathlib import Path

FUNC_DIR = Path(__file__).parent / "func"
sys.path.insert(0, str(FUNC_DIR))

from obfuscate_ps import obfuscate_powershell
from obfuscate_bash import obfuscate_bash
from obfuscate_bat import obfuscate_bat

def main() -> None:
    parser = argparse.ArgumentParser(description="Obfuscate script files")
    parser.add_argument(
        "-f", "--file",
        required=True,
        help="path to the script file to obfuscate"
    )
    parser.add_argument(
        "-o", "--output",
        required=False,
        help="output file path (optional)"
    )
    args = parser.parse_args()

    input_path = Path(args.file)

    if not input_path.exists():
        print(f"Error: File '{input_path}' not found.", file=sys.stderr)
        sys.exit(1)

    ext = input_path.suffix.lower()
    if ext == ".ps1":
        obf_func = obfuscate_powershell
    elif ext == ".sh":
        obf_func = obfuscate_bash
    elif ext == ".bat":
        obf_func = obfuscate_bat
    else:
        print(
            f"Error: Unsupported file extension '{ext}'. Supported: .ps1, .sh, .bat",
            file=sys.stderr
        )
        sys.exit(1)

    output_path = Path(args.output) if args.output else None

    try:
        obf_func(input_path, output_path)

        if output_path is None:
            default_output = input_path.parent / (input_path.stem + "_obf" + input_path.suffix)
            print(f"Obfuscated script saved to: {default_output}")
        else:
            print(f"Obfuscated script saved to: {output_path}")

    except Exception as e:
        print(f"Error during obfuscation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
