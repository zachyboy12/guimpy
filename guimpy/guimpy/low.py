import os, inspect, re
from typing import Callable


def file(path: str, mode: str='r', arg: str='\\~(r)'):
    with open(path, mode) as fp:
        if arg == '\\~(r)':
            return fp.read()
        else:
            return fp.write(arg)


file(f'{os.path.dirname(__file__)}/low.magic', 'w', '')
interpreter = os.path.dirname(os.path.dirname(__file__))


def add(widget: str, __name: str, **attrs):
    if interpreter is None:
        raise ValueError('Interpreter path contained in "self" should be set; got "None".')
    widget = widget.lower()
    magic_code = f'{widget} {__name} '
    for attr in attrs:
        magic_code += f'-{attr} {repr(attrs[attr])} '
    magic_code = magic_code[:-1]
    file(f'{os.path.dirname(__file__)}/low.magic', 'a', magic_code + '\n')
    
    
def run(event_handler: Callable):
    func_lines = inspect.getsource(event_handler).splitlines()[1:]
    lines = '\n'
    for line_number, line in enumerate(func_lines):
        if line_number == 0 or line_number == len(func_lines) - 1:
            line = line.lstrip()
        lines += f'\{line}\n'
    file(f'{os.path.dirname(__file__)}/low.magic', 'a', f'{lines}\nrun')
    os.system(f'python3 {interpreter} {os.path.dirname(__file__)}/low.magic')
    
    
def main():
    def event_handler():
        while True:
            event, attributes = gui.get_current_event()
            if event == 'close':
                break
        gui.stop()
    

    add('gui', 'gui', title='My Window')
    add('text', 'mytext', text='Hello, World!', gui='gui')
    run(event_handler)
    
    
if __name__ == '__main__':
    main()
