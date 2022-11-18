"""
Language Interpreter For GUI.set For The Magic Language.
"""


import ast
from typing import SupportsIndex


def get_indented_code(code: list, start: int | SupportsIndex):
    indented_code = ''
    for line in code[start + 1:]:
        if line.startswith(' '):
            indented_code += line.lstrip() + '\n'
        else:
            break
    return indented_code


def next_line_is_indented(code: list, start: int | SupportsIndex):
    try:
        next_line = code[start + 1]
    except IndexError:
        return False
    if next_line.startswith(' '):
        return True
    return False


def interpret(module, gui, string: str):
    file_contents = string
    lines = file_contents.splitlines()
    layout = []
    current_row = 0
    python = ''
    for line_number, line in enumerate(lines):
        if next_line_is_indented(lines, line_number) and not line.startswith(' ') and line != 'window':
            layout.append([])
            widget_name = line.title()
            attribute_lines = get_indented_code(lines, line_number).splitlines()
            for attribute_number, attribute_line in enumerate(attribute_lines):
                attribute = attribute_line.split(' ', 1)
                attribute[1] = ast.literal_eval(attribute[1])
                attribute_lines[attribute_number] = attribute
            attribute_lines = dict(attribute_lines)
            widget_class = getattr(module, widget_name)
            if widget_class is None:
                print(f'''Magic Mistake! Widget Name "{widget_name}"? What's That?''')
                raise SystemExit()
            widget = widget_class(**attribute_lines)
            layout[current_row].insert(current_row, widget)
            current_row += 1
        elif line.startswith('\\'):
            python += line[1:] + '\n'
    gui.set(layout)
    exec(python, {'gui': gui, 'guimpy': module})
