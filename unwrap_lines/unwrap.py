def unwrap_lines(text: str):
    result = []
    lines = []

    def _add_to_result(newline: bool = True):
        if lines:
            result.append(' '.join(lines))
            lines.clear()
        if newline:
            result.append('')

    def _is_list_line(line: str) -> bool:
        first, _ = line.split(maxsplit=1)
        return (first[:-1].isdigit() and first[-1] == '.') or (first == '-')

    for part in text.splitlines(keepends=False):
        if part:
            if _is_list_line(part):
                _add_to_result(newline=False)
            lines.append(part.strip())
            if part.endswith('  '):
                lines[-1] = part
                _add_to_result(newline=False)
        else:
            _add_to_result()

    _add_to_result()

    return '\n'.join(result)
