import random
import re
import string
from pathlib import Path

def obfuscate_bat(input_path: str | Path, output_path: str | Path | None = None) -> str:
    input_path = Path(input_path)
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    label_pattern = re.compile(r'^:(\w+)', re.MULTILINE)
    labels = set(label_pattern.findall(code))

    new_labels = {}
    for label in labels:
        new_label = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        new_label = '_' + new_label
        new_labels[label] = new_label

    for old, new in new_labels.items():
        code = re.sub(r'(?<=:)' + re.escape(old) + r'\b', new, code)

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    set_var = "a" + random_suffix
    chars = list("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(chars)
    letters = ''.join(chars)
    set_line = f"Set {set_var}={letters}"

    keep_chars = set()
    for new in new_labels.values():
        keep_chars.update(new)

    lettertab = {}

    for i, ch in enumerate(letters):
        if ch not in keep_chars:
            lettertab[ch] = f"%{set_var}:~{i},1%"

    def replace_char(ch):
        if ch in keep_chars:
            return ch
        return lettertab.get(ch, ch)

    codeobfu = ''.join(replace_char(ch) for ch in code)

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
