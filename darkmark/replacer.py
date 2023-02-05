def get_line_from_text(text, row):
    lines = text.split("\n")
    return lines[row - 1]


def update_line_in_text(text, row, line):
    lines = text.split("\n")
    lines[row - 1] = line
    return "\n".join(lines)


def replace_text(text, capture, replacement):
    if isinstance(capture, tuple):
        capture, capture_name = capture

    start_row, start_col = (i + 1 for i in capture.start_point)
    end_row, end_col = (i + 1 for i in capture.end_point)

    get_line_from_text(text, start_row)
    get_line_from_text(text, end_row)

    text_lines = text.split("\n")
    if start_row > 1:
        lines = text_lines[: start_row - 1]
        lines[-1] = (
            lines[-1]
            + text_lines[start_row][: start_col - 1]
            + replacement
            + text_lines[end_row - 1][end_col - 1 :]
        )
    elif firstline := replacement + text_lines[end_row - 1][end_col - 1 :] != "":
        lines = [firstline]
    else:
        lines = []

    lines.extend(text_lines[end_row:])

    return "\n".join(lines)


def insert_text(text, row, insertion):
    lines = text.split("\n")
    lines.insert(row, insertion)
    return "\n".join(lines)


def get_text(text, capture):
    if isinstance(capture, tuple):
        capture, capture_name = capture
    start_row, start_col = (i + 1 for i in capture.start_point)
    end_row, end_col = (i + 1 for i in capture.end_point)
    start_line = get_line_from_text(text, start_row)
    end_line = get_line_from_text(text, end_row)
    if start_row == end_row:
        return start_line[start_col - 1 : end_col]
    result = start_line[start_col - 1 :] + "\n"
    for i in range(start_row + 1, end_row):
        result += get_line_from_text(text, i) + "\n"
    result += end_line[:end_col]
    return result
