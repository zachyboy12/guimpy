"""
Source code for the Magic Language Interpreter.

Usage:
    python3 /path/to/guimpy filepath.magic
"""

# Syntax:
#   <widget-type> -<attribute> <attribute-value>


import sys, os, ast, guimpy
from typing import Iterable, List


python = ''
line_number = 1
variables = {'file': 'string'}
p = lambda *values, sep=' ', end='\n', flush=False: print(*values, sep=sep, end=end, flush=flush)


def gfindex(iterable: Iterable, index: int):
    try:
        return iterable[index]
    except IndexError:
        return
    
    
class Error:
    def __init__(self, error_list: List[dict], exit_interpreter: bool=True) -> None:
        self.error_list = error_list
        for item in self.error_list:
            p(f"File \"{item['file']}\", line {item['line']}:\n\t{__class__.__name__}: {item['message']}")
        if exit_interpreter:
            raise SystemExit()
    
    
class Syntaxerror(Error):
    def __init__(self, error_list: List[dict]) -> None:
        super().__init__(error_list, True)


class ArgError(Exception):
    pass


help_message = '''
Magic Language CLI.

If no args, run interactive mode.
Usage:
    -h, --h, --help, -help   -> Prints this message
    Unknown Arg              -> Used as filename
'''


def is_number(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False


def parse_attributes(text: str):
    text += ' -dummy "dummy text"'
    option_list = text.split()
    attribute = {}
    attributes = {}
    for option_index, option in enumerate(option_list):
        if option.startswith('-'):
            if is_number(option):
                attribute['value'] += option + ' '
            if attribute.get('value'):
                if attribute['name'] == 'gui':
                    attribute['value'] = ast.literal_eval(f'''"{attribute['value']}"''')
                else:
                    attribute['value'] = ast.literal_eval(attribute['value'])
                if isinstance(attribute['value'], str):
                    attribute['value'] = attribute['value'].replace('{[~]}', '-')
                attributes[attribute['name']] = attribute['value']
            attribute = {'name': option[1:], 'value': ''}
        else:
            if attribute:
                attribute['value'] += option + ' '
    return attributes
            

def parse(text: str):
    global python
    if text.startswith('\\'):
        python += text[1:] + '\n'
        return
    if not text:
        return
    text = text.split()
    if gfindex(text, 1) == 'is':
        variables[text[0]] = ast.literal_eval(text[2])
        return
    if gfindex(text, 0) == 'write':
        text[1] = text[1].splitlines()[0]
        if ';' in text[1]:
            Syntaxerror([{'file': variables['file'], 'line': line_number, 'message': 'Unknown Character ";".'}])
        variables['exec'] = lambda: Error([{'file': variables['file'], 'line': line_number, 'message': 'Unknown function "exec".'}])
        variables['eval'] = lambda: Error([{'file': variables['file'], 'line': line_number, 'message': 'Unknown function "exec".'}])
        p(eval(' '.join(text[1:]), variables, variables))
        return
    gui = None
    attributes = parse_attributes(' '.join(text[2:]))
    widget_name = text[0].capitalize()
    if widget_name == 'Tabframe':
        widget_name = 'TabFrame'
    if widget_name == 'Run':
        return
    widget_class = getattr(guimpy, widget_name, None)
    if widget_class is None:
        raise guimpy.WidgetError(f'Unknown widget "{widget_name}".')
    if 'gui' in attributes:
        gui = attributes['gui']
        del attributes['gui']
    widget = widget_class(**attributes)
    variables[text[1]] = widget
    if gui:
        gui = gui.strip()
        gui = variables[gui].add(widget)
    line += 1
    
    
def exit(code: int=0):
    raise SystemExit(code)


if __name__ == '__main__':
    if len(sys.argv[1:]) not in [0, 1, 2]:
        raise ArgError('Only 0 or 1 args allowed.')
    try:
        arg = sys.argv[1]
    except IndexError:
        while True:
            try:
                line = input('>>> ')
                splitted_line = line.split()
                beginning = splitted_line[0].lower()
                if beginning == 'gui':
                    attributes = parse_attributes(' '.join(splitted_line[2:]))
                    variables[splitted_line[1]] = guimpy.GUI(**attributes)
                    continue
                parse(line)
            except KeyboardInterrupt:
                break
        exit()
    if arg in ['-h', '-help', '--h', '--help']:
        p(help_message)
        exit()
    variables['file'] = arg
    with open(arg) as file:
        lines = file.read().splitlines()
    gui = None
    for line in lines:
        splitted_line = line.split(' ')
        beginning = splitted_line[0].lower()
        name = None
        if beginning == 'gui':
            attributes = parse_attributes(' '.join(splitted_line[2:]))
            variables[splitted_line[1]] = guimpy.GUI(**attributes)
            continue
        elif beginning == 'run':
            exec(python, variables)
            python = ''
        parse(line)
