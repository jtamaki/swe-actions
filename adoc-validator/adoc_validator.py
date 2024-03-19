from typing import List
import argparse
import chardet
import glob
import os
import re
import sys

class Error:
    def __init__(self, filename: str, line: int, message: str) -> None:
        self.filename = filename
        self.line = line
        self.message = message

def validate_encoding(filename: str, raw: bytes) -> List[Error]:
    errors: List[Error] = []
    res = chardet.detect(raw)
    if (res['encoding'] != 'utf-8'):
        errors.append(Error(filename, 0, 'File encoding is not UTF-8'))
    return errors

def validate_line_ending(filename: str, lines: List[str]) -> List[Error]:
    def is_lf(line) -> bool:
        return line.endswith('\n') and not line.endswith('\r\n')
    errors = list(
        map(lambda x: Error(filename, x[0], 'File line endings are not LF'),
            filter(lambda x: not is_lf(x[1]), enumerate(lines, start = 1))))
    return errors[0:1]

def validate_char(filename: str, lines: List[str]) -> List[Error]:
    errors: List[Error] = []

    def has_fullwidth_space(line) -> bool:
        return '　' in line
    errors += list(
        map(lambda x: Error(filename, x[0], 'Contains invalid char(full width space)'),
            filter(lambda x: has_fullwidth_space(x[1]), enumerate(lines, start = 1))))

    def has_fullwidth_paren(line) -> bool:
        return '（' in line or '）' in line
    errors += list(
        map(lambda x: Error(filename, x[0], 'Contains invalid char(full width paren)'),
            filter(lambda x: has_fullwidth_paren(x[1]), enumerate(lines, start = 1))))

    def has_fullwidth_alphabet(line) -> bool:
        return re.search('[Ａ-Ｚａ-ｚ]', line) is not None
    errors += list(
        map(lambda x: Error(filename, x[0], 'Contains invalid char(full width alphabet)'),
            filter(lambda x: has_fullwidth_alphabet(x[1]), enumerate(lines, start = 1))))

    def has_fullwidth_numeric(line) -> bool:
        return re.search('[０-９]', line) is not None
    errors += list(
        map(lambda x: Error(filename, x[0], 'Contains invalid char(full width numeric)'),
            filter(lambda x: has_fullwidth_numeric(x[1]), enumerate(lines, start = 1))))

    def has_fullwidth_symbol(line) -> bool:
        return re.search('[！“”＃＄％＆‘’＊＋，．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～]', line) is not None
    errors += list(
        map(lambda x: Error(filename, x[0], 'Contains invalid char(full width symbol)'),
            filter(lambda x: has_fullwidth_symbol(x[1]), enumerate(lines, start = 1))))

    return sorted(errors, key=lambda x: x.line)

def validate_multiple_whitespaces(filename: str, lines: List[str]) -> List[Error]:
    def has_double_whitespace(line) -> bool:
        return '  ' in line
    errors = list(
        map(lambda x: Error(filename, x[0], 'Multiple consecutive whitespaces'),
            filter(lambda x: has_double_whitespace(x[1]), enumerate(lines, start = 1))))
    return errors

def validate_multiple_empty_lines(filename: str, lines: List[str]) -> List[Error]:
    errors: List[Error] = []
    count = 0
    for i, line in enumerate(lines,start = 1):
        if line.strip() == '':
            count += 1
        else:
            count = 0

        if count >= 2:
            errors.append(Error(filename, i, 'Multiple consecutive empty lines'))
    return errors

def validate_blank_line_at_file_end(filename: str, lines: List[str]) -> List[Error]:
    errors: List[Error] = []
    if not lines[-1].endswith('\n'):
        errors.append(Error(filename, len(lines), 'File does not end with a newline'))
    return errors

def validate_adoc_file(filepath: str) -> List[Error]:
    filename = os.path.basename(filepath)
    errors: List[Error] = []

    with open(filepath, 'rb') as f:
        raw = f.read()
    errors += validate_encoding(filename, raw)
    if errors != []:
        return errors

    with open(filepath, newline = '') as f:
        lines = f.readlines()
    errors += validate_line_ending(filename, lines)
    errors += validate_char(filename, lines)
    errors += validate_multiple_whitespaces(filename, lines)
    errors += validate_multiple_empty_lines(filename, lines)
    errors += validate_blank_line_at_file_end(filename, lines)
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, metavar='DIR', help='input asciidoc directory path')
    args = parser.parse_args()
    
    filepaths = glob.glob(f'{args.i}/**/*.adoc', recursive=True)

    errors: List[Error] = []
    for filepath in filepaths:
        errors += validate_adoc_file(filepath)

    if errors != []:
        for e in errors:
            print(f'{e.filename} {e.line} {e.message}', file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
