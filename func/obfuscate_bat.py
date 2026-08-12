import random
import string
from pathlib import Path

def obfuscate_bat(input_path: str | Path, output_path: str | Path | None = None) -> str:
    input_path = Path(input_path)
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    set_var = "a" + random_suffix
    chars = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(chars)
    letters = ''.join(chars)
    set_line = f"Set {set_var}={letters}"
    lettertab = {}
    
    for i, ch in enumerate(letters):
        lettertab[ch] = f"%{set_var}:~{i},1%"

    codeobfu = ""
    for ch in code:
        codeobfu += lettertab.get(ch, ch)

    result = "@echo off\n" + set_line + "\ncls\n" + codeobfu

    if output_path is None:
        output_path = input_path.parent / (input_path.stem + "_obf" + input_path.suffix)
    else:
        output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    return result


if __name__ == "__main__":
    print("Please, run main.py, not this")
