import random
import string
from pathlib import Path

def obfuscate_bash(input_path: str | Path, output_path: str | Path | None = None) -> str:
    input_path = Path(input_path)
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    set_var = 'a' + random_suffix
    chars = list(string.ascii_letters + string.digits)
    random.shuffle(chars)
    letters = ''.join(chars)
    set_line = f"{set_var}={letters}"
    lettertab = {}

    for i, ch in enumerate(letters):
        lettertab[ch] = f"${{{set_var}:{i}:1}}"

    codeobfu = ''.join(lettertab.get(ch, ch) for ch in code)

    lines = code.splitlines(keepends=True)
    if lines and lines[0].startswith('#!'):
        shebang = lines[0]
        rest_code = ''.join(lines[1:])
        rest_obfuscated = ''.join(lettertab.get(ch, ch) for ch in rest_code)
        result = shebang + '\n' + set_line + '\n' + rest_obfuscated
    else:
        result = set_line + '\n' + codeobfu

    if output_path is None:
        output_path = input_path.parent / (input_path.stem + "_obf" + input_path.suffix)
    else:
        output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    return result


if __name__ == "__main__":
    print("Please, run main.py, not this")
