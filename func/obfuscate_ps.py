import random
import string
from pathlib import Path
import base64

def remove_comments(code: str) -> str:
    lines = code.splitlines(True)
    result = []
    for line in lines:
        new_line = []
        i = 0
        in_single = False
        in_double = False
        escape = False
        while i < len(line):
            ch = line[i]
            if not in_single and not in_double:
                if ch == '#':
                    break
                elif ch == "'":
                    in_single = True
                    new_line.append(ch)
                elif ch == '"':
                    in_double = True
                    new_line.append(ch)
                else:
                    new_line.append(ch)
            else:
                if escape:
                    escape = False
                    new_line.append(ch)
                elif ch == '\\':
                    escape = True
                    new_line.append(ch)
                elif in_single and ch == "'":
                    in_single = False
                    new_line.append(ch)
                elif in_double and ch == '"':
                    in_double = False
                    new_line.append(ch)
                else:
                    new_line.append(ch)
            i += 1
        result.append(''.join(new_line))
    return ''.join(result)


def obfuscate_powershell(input_path: str | Path, output_path: str | Path | None = None) -> str:
    input_path = Path(input_path)
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    code_no_comments = remove_comments(code)
    code_bytes = code_no_comments.encode('utf-8')
    b64 = base64.b64encode(code_bytes).decode('ascii')
    result = f"iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{b64}')))"

    if output_path is None:
        output_path = input_path.parent / (input_path.stem + "_obf" + input_path.suffix)
    else:
        output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    return result


if __name__ == "__main__":
    print("Please, run main.py, not this")
