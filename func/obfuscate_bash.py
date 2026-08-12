import random
import re
import string
from pathlib import Path

def obfuscate_bash(input_path: str | Path, output_path: str | Path | None = None) -> str:
    input_path = Path(input_path)
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()

    keywords = {
        'if', 'then', 'else', 'elif', 'fi', 'while', 'until', 'do', 'done',
        'case', 'esac', 'for', 'select', 'function', 'time', 'in', '!', '{', '}',
        '[[', ']]'
    }

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    set_var = 'a' + random_suffix
    chars = list(string.ascii_letters + string.digits + '_')
    random.shuffle(chars)
    letters = ''.join(chars)
    set_line = f"{set_var}={letters}"
    lettertab = {ch: f"${{{set_var}:{i}:1}}" for i, ch in enumerate(letters)}
    literal_tab = {ch: letters[i] for i, ch in enumerate(letters)}

    cache = {}
    literal_cache = {}

    def peek_non_space(text, index):
        while index < len(text) and text[index].isspace():
            index += 1
        return text[index] if index < len(text) else None

    def is_name_position(word, next_char, prev_word):
        if prev_word and prev_word.lower() in {
            'for', 'select', 'function', 'local', 'declare', 'typeset', 'readonly', 'export', 'unset'
        }:
            return True
        if next_char == '=':
            return True
        if next_char == '(':
            return True
        return False

    def collect_special_words(text):
        special = set()
        i = 0
        n = len(text)
        in_single = False
        in_double = False
        escape = False
        word = []
        prev_word = None

        def flush_current(next_char):
            nonlocal word, prev_word
            if word:
                word_str = ''.join(word)
                if word_str.lower() not in keywords and is_name_position(word_str, next_char, prev_word):
                    special.add(word_str)
                prev_word = word_str
                word = []

        while i < n:
            ch = text[i]
            if escape:
                escape = False
                i += 1
                continue
            if ch == '\\':
                escape = True
                i += 1
                continue
            if in_single:
                if ch == "'":
                    in_single = False
                i += 1
                continue
            if in_double:
                if ch == '"':
                    in_double = False
                if ch.isalpha() or ch == '_' or ch.isdigit():
                    word.append(ch)
                    i += 1
                    continue
                flush_current(peek_non_space(text, i))
                i += 1
                continue
            if ch == '#':
                flush_current(peek_non_space(text, i))
                while i < n and text[i] != '\n':
                    i += 1
                continue
            if ch == "'":
                in_single = True
                flush_current(peek_non_space(text, i + 1))
                i += 1
                continue
            if ch == '"':
                in_double = True
                flush_current(peek_non_space(text, i + 1))
                i += 1
                continue
            if ch.isalpha() or ch == '_' or ch.isdigit():
                word.append(ch)
                i += 1
                continue
            flush_current(peek_non_space(text, i))
            i += 1
        flush_current(None)
        return special

    def obfuscate_literal_word(word):
        if word in literal_cache:
            return literal_cache[word]
        result = []
        for idx, ch in enumerate(word):
            mapped = literal_tab.get(ch, ch)
            if idx == 0 and mapped.isdigit():
                mapped = '_'
            result.append(mapped)
        obf = ''.join(result)
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', obf):
            obf = '_' + obf
        literal_cache[word] = obf
        return obf

    def obfuscate_word(word, next_char=None, prev_word=None, special_words=None):
        if word in cache:
            return cache[word]
        if word.lower() in keywords:
            return word
        if special_words is not None and word in special_words:
            obf = obfuscate_literal_word(word)
        elif is_name_position(word, next_char, prev_word):
            obf = obfuscate_literal_word(word)
            if special_words is not None:
                special_words.add(word)
        else:
            obf = ''.join(lettertab.get(ch, ch) for ch in word)
        cache[word] = obf
        return obf

    def process(text, special_words):
        result = []
        i = 0
        n = len(text)
        in_single = False
        in_double = False
        escape = False
        word = []
        prev_word = None

        def flush():
            nonlocal word, prev_word
            if word:
                word_str = ''.join(word)
                next_char = peek_non_space(text, i)
                obf = obfuscate_word(word_str, next_char, prev_word, special_words)
                result.append(obf)
                prev_word = word_str
                word = []

        while i < n:
            ch = text[i]
            if escape:
                result.append(ch)
                escape = False
                i += 1
                continue
            if ch == '\\':
                escape = True
                result.append(ch)
                i += 1
                continue
            if in_single:
                result.append(ch)
                if ch == "'":
                    in_single = False
                i += 1
                continue
            if in_double:
                if ch == '"':
                    in_double = False
                    result.append(ch)
                    i += 1
                    continue
                if ch.isalpha() or ch == '_' or ch.isdigit():
                    word.append(ch)
                    i += 1
                    continue
                flush()
                result.append(ch)
                i += 1
                continue
            if ch == '#':
                flush()
                while i < n and text[i] != '\n':
                    result.append(text[i])
                    i += 1
                continue
            if ch == "'":
                in_single = True
                flush()
                result.append(ch)
                i += 1
                continue
            if ch == '"':
                in_double = True
                flush()
                result.append(ch)
                i += 1
                continue
            if ch.isalpha() or ch == '_' or ch.isdigit():
                word.append(ch)
                i += 1
                continue
            flush()
            result.append(ch)
            i += 1
        flush()
        return ''.join(result)

    lines = code.splitlines(keepends=True)
    shebang = ''
    rest = code
    if lines and lines[0].startswith('#!'):
        shebang = lines[0]
        rest = ''.join(lines[1:])

    special_words = collect_special_words(rest)
    rest_obf = process(rest, special_words)
    if shebang:
        result = shebang + '\n' + set_line + '\n' + rest_obf
    else:
        result = set_line + '\n' + rest_obf

    if output_path is None:
        output_path = input_path.parent / (input_path.stem + "_obf" + input_path.suffix)
    else:
        output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(result)

    return result


if __name__ == "__main__":
    print("Please, run main.py, not this")
