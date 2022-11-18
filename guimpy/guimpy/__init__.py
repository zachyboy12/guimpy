"""
GUIMPy - TKinter On Steroids.
"""


# 906 Lines Of Code!


from io import TextIOWrapper
import tkinter, threading, time, _tkinter, tkinter.ttk as ttk, difflib, os, sys
from typing import Any, Callable, Protocol


__version__ = 1.0
_mainwin = tkinter.Tk()
_mainwin.overrideredirect(1)
_mainwin.withdraw()
_when_dark_modeglvarobaliabel = None
all_guis = []
next_menu_id = 1
closed_all = False
_created_button = False

sys.path.insert(0, os.path.dirname(__file__))


import guiml


class GuimpyThreadError:
    """
    Raised If There Is A Problem With The Data The User Passed.
    """


class GuimpyThread:
    
    
    def __init__(self, gui=None, target=None, args=(), kwargs={}, daemon=False) -> None:
        self.gui: GUI = gui
        self.target: None | Callable = target
        self.args: list | tuple = args
        self.kwargs: dict = kwargs
        self.daemon: bool = daemon
        self.value: Any = None
        self._called_start = False
        
        
    def start(self):
        if self._called_start:
            raise RuntimeError('threads can only be started once.')
        if self.gui is None:
            raise GuimpyThreadError('"gui" attribute is None.')
        self._called_start = True
        def true_target():
            event, attributes = self.gui.get_current_event()
            if event == 'close':
                if self.daemon:
                    true_target.stop = True
            self.target(*self.args, **self.kwargs)
        self.gui.schedule(1, self.target)


def when_dark_mode(hour: int, minute: int=0, second: int=0, AM_or_PM: str='AM'):
    global _when_dark_modeglvarobaliabel
    _when_dark_modeglvarobaliabel = (hour, minute, second, AM_or_PM)
    
    
def dark_mode():
    global _when_dark_modeglvarobaliabel
    try:
        formatted_time = time.strftime('%I:%M:%S:%p').split(':')
        formatted_time = list(map(lambda item: int(item) if item.isdigit() else item, formatted_time))
        return _when_dark_modeglvarobaliabel == formatted_time or formatted_time[0] >= _when_dark_modeglvarobaliabel[0] and formatted_time[1] >= _when_dark_modeglvarobaliabel[1] and formatted_time[2] >= _when_dark_modeglvarobaliabel[2] and formatted_time[3] == _when_dark_modeglvarobaliabel[3]
    except TypeError:
        pass
    
    
class DragFunction(Protocol):
    
    
    """
    Type Of Protocol For Making Function For The guimpy.make_draggable Function.
    """
    
    
    def __call__(self, x: int, y: int):
        ...
    
    
def make_draggable(widget, func: DragFunction=None):
    widget = widget.elem
    def on_drag_start(event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y

    def on_drag_motion(event):
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        if func:
            func(x, y)
        widget.place(x=x, y=y)
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)


class WidgetError(Exception):
    pass


class LayoutError(Exception):
    """
    Raise If Using Unknown Layout Or If Layout Is Already Set.
    """


class Text:
    
    
    def __init__(self, text: Any='', name=None, text_color: str='default', font: tuple='default', copy_pasteable: bool=True, background: str='default', border_thickness: int='default', border_type: str='default', padding_x: int=1, padding_y: int=1, border_padding_x: int=0, border_padding_y: int=0, pull: str='default', x: int | float='default', y: int | float='default') -> None:
        self.text = str(text) + ' '
        self.text_color = text_color.lower()
        if self.text_color == 'default':
            if dark_mode():
                self.text_color = 'white'
            else:
                self.text_color = '#2f2f30'
        self.copy_pastable = copy_pasteable
        self.background = background.lower()
        if self.background == 'default':
            if dark_mode():
                self.background = '#2f2f30'
            else:
                self.background = 'white'
        self.padding_y = padding_y * 5
        self.padding_x = padding_x * 5
        self.pull = pull
        self.border_padding_x = border_padding_x
        self.border_padding_y = border_padding_y
        self.border_thickness = border_thickness
        self.border_type = border_type.lower()
        self.font = font
        self.name = name
        self.hidden = False
        self.x = x
        self.y = y
        
        
    def hide(self):
        self.hidden = True
        self.elem.grid_forget()
        
        
    def show(self):
        self.hidden = False
        self.elem.grid(**self.grid_args)
        
        
    def update(self, **options):
        elem = self.elem
        newline = '\n'
        for key, value in list(options.items()):
            name = elem.__class__.__name__
            if key == 'text':
                self.text = str(value) + ' '
                if name == 'Label':
                    elem.configure(text=self.text)
                elif name == 'Text':
                    self.text_lines = self.text.splitlines()
                    self.number_of_lines = len(self.text_lines)
                    self.max_text_chars = 0
                    for text_line in self.text_lines:
                        if len(text_line) > self.max_text_chars:
                            self.max_text_chars = len(text_line)
                    self.elem.configure(width=self.max_text_chars, height=self.number_of_lines)
                    elem.configure(state='normal')
                    elem.delete('1.0', 'end')
                    elem.insert('1.0', value)
                    elem.configure(state='disabled')
            elif key == 'border_padding_x':
                if isinstance(value, list) or isinstance(value, tuple):
                    left_padding = value[0]
                    right_padding = value[1]
                    self.update(text=left_padding + self.text + right_padding)
                elif isinstance(value, int):
                    padding = '\n' * value
                    self.update(text=padding + self.text + padding)
            elif key == 'border_padding_y':
                if isinstance(value, list) or isinstance(value, tuple):
                    up_padding = value[0]
                    down_padding = value[1]
                    self.update(text=f"{newline * up_padding}{self.text.strip(newline)}{newline * down_padding}")
                elif isinstance(value, int):
                    self.update(text=f"{newline * value}{self.text.strip(newline)}{newline * value}")
            elif key == 'padding_x':
                elem.configure(padx=value)
            elif key == 'padding_y':
                elem.configure(pady=value)
            elif key == 'font':
                elem.configure(font=value)
            elif key == 'background':
                elem.configure(bg=value)
            elif key == 'border_thickness':
                elem.configure(bd=value)
            elif key == 'border_type':
                if value == 'thin':
                    elem.configure(relief='ridge')
                elif value == 'dent':
                    elem.configure(relief='groove')
                elif value == 'default':
                    elem.configure(relief='flat')
                else:
                    if value in ['ridge', 'groove']:
                        raise WidgetError(f'Unknown border type "{value}".')
                    try:
                        elem.configure(relief=value)
                    except _tkinter.TclError:
                        raise WidgetError(f'Unknown border type "{value}".')
            elif key == 'pull':
                self.hide()
                self.grid_args['sticky'] = value.replace(' ', '').lower().replace('up', 'n').replace('down', 's').replace('right', 'e').replace('left', 'w').replace('northwest', 'nw').replace('northeast', 'ne').replace('southwest', 'sw').replace('southeast', 'se')
                self.show()
            elif key == 'x':
                self.hide()
                self.grid_args['column'] = value
                self.show()
            elif key == 'y':
                self.hide()
                self.grid_args['row'] = value
                self.show()
        
        
    def init(self, root):
        if isinstance(self.border_padding_x, tuple) or isinstance(self.border_padding_x, list):
            self.text = (' ' * self.border_padding_x[0]) + self.text + (' ' * self.border_padding_x[1])
        elif isinstance(self.border_padding_x, int):
            self.text = (' ' * self.border_padding_x) + self.text + (' ' * self.border_padding_x)
        if isinstance(self.border_padding_y, tuple) or isinstance(self.border_padding_y, list):
            self.text = ('\n' * self.border_padding_y[0]) + self.text + ('\n' * self.border_padding_y[1])
        elif isinstance(self.border_padding_y, int) and self.border_padding_y > 0:
            padding = '\n' * self.border_padding_y
            self.text = padding + self.text + padding + '\n'
        self.text_lines = self.text.splitlines()
        self.number_of_lines = len(self.text_lines)
        self.max_text_chars = 0
        for text_line in self.text_lines:
            if len(text_line) > self.max_text_chars:
                self.max_text_chars = len(text_line)
        elem = tkinter.Label(root, text=self.text, bg=self.background, fg=self.text_color)
        if self.copy_pastable:
            elem = tkinter.Text(root, fg=self.text_color, bd=0, bg=self.background, width=self.max_text_chars, height=self.number_of_lines, cursor='xterm', highlightthickness=0)
            elem.insert('1.0', self.text)
            elem.configure(state='disabled')
        if self.font != 'default':
            elem.configure(font=self.font)
        if self.border_type != 'default':
            if self.border_type == 'thin':
                elem.configure(relief='ridge')
            elif self.border_type == 'dent':
                elem.configure(relief='groove')
            else:
                if self.border_type in ['ridge', 'groove']:
                    raise WidgetError(f'Unknown border type "{self.border_type}".')
                try:
                    elem.configure(relief=self.border_type)
                except _tkinter.TclError:
                    raise WidgetError(f'Unknown border type "{self.border_type}".')
        if self.border_thickness != 'default':
            elem.configure(borderwidth=self.border_thickness)
        elem.configure(padx=self.padding_x, pady=self.padding_y)
        self.elem = elem
        return elem
    
    
    def bind_key(self, key: str, callback: Callable):
        if key != '+':
            key = key.replace('+', '-')
        else:
            pass
        self.elem.bind(f'<{key}>', callback)
        
        
class TabFrame:
    
    
    def __init__(self, gui, pull: str='default', padding_x: int=5, padding_y: int=5, color: str = 'white', width: int='default', height: int='default', x=0, y=0) -> None:
        self.pull = pull
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.color = color
        self.width = width
        self.height = height
        self.name = None
        self.width = width
        self.gui = gui
        self.x = x
        self.y = y
        self.root = ttk.Notebook(self.gui.root)
        if self.width != 'default':
            self.root.configure(width=self.width)
        if self.height != 'default':
            self.root.configure(height=self.height)
        self.frames = []
        self.__previous_frames = self.frames
        def handle_frames():
            if self.gui.stopall:
                return
            if self.__previous_frames != self.frames:
                frames_added = list(reversed(list(set(self.frames + self.__previous_frames))))
                for added_frame in frames_added:
                    self.root.add(added_frame.root, text=added_frame.name)
            self.root.after(2, handle_frames)
        self.gui.root.after(2, handle_frames)
        
        
class Button(Text):
    
    
    def __init__(self, text: Any = '', name: str = None, highlight_color: str='default', text_color: str = 'default', font: tuple = 'default', background: str = 'default', border_thickness: int = 1, padding_x: int = 1, padding_y: int = 1, border_padding_x: int = 0, border_padding_y: int = 0, pull: str = 'default', x: int | float = 'default', y: int | float = 'default', x_span: int='default', y_span: int='default') -> None:
        super().__init__(text, name, text_color, font, False, background, border_thickness, 'raised', padding_x, padding_y, border_padding_x, border_padding_y, pull, x, y)
        self.highlight_color = highlight_color
    
        
    def init(self, root):
        elem = super().init(root)
        def onclick(event):
            nonlocal elem
            elem.configure(relief='sunken')
        def onrelease(event):
            nonlocal elem
            elem.configure(relief='raised')
            
            root.root.start_event(self.name, {'action': 'click'})
        def onhover(event):
            nonlocal elem
            if self.highlight_color != 'default':
                elem.configure(bg=self.highlight_color)
            else:
                if dark_mode():
                    elem.configure(bg='#646665')
                else:
                    elem.configure(bg='#ebf6fc')
        def onexithover(event):
            nonlocal elem
            elem.configure(bg=self.background)
        elem.bind('<1>', onclick)
        elem.bind('<ButtonRelease-1>', onrelease)
        elem.bind('<Enter>', onhover)
        elem.bind('<Leave>', onexithover)
        self.click = onrelease
        return elem
    
    
class Input:
    
    
    def __init__(self, placeholder: str=None, name: str = None, highlight_border_thickness: int=1, autocomplete_choices: list=None, autocomplete_case_sensitive: bool=False, default_value_autocomplete=None, autocomplete_ratio: float=0.2, multiline: bool=False, editable: bool=True, width: int=50, height: int=1, border_type: str='default', highlight_background_color: str='default', text_color: str = 'default', font: tuple = 'default', background: str = 'default', border_thickness: int = 1, padding_x: int = 1, padding_y: int = 1, border_padding_x: int = 0, border_padding_y: int = 0, pull: str = 'default', x: int | float = 'default', y: int | float = 'default') -> None:
        self.text_color = text_color
        if self.text_color == 'default':
            if dark_mode():
                self.text_color = 'white'
            else:
                self.text_color = '#2f2f30'
        self.background = background.lower()
        if self.background == 'default':
            if dark_mode():
                self.background = '#2f2f30'
            else:
                self.background = 'white'
        self.placeholder = placeholder
        self.highlight_color = highlight_background_color
        if self.highlight_color == 'default':
            if dark_mode():
                self.highlight_color = '#2f2f30'
            else:
                self.highlight_color = 'white'
        self.padding_y = padding_y * 5
        self.padding_x = padding_x * 5
        self.pull = pull
        self.border_padding_x = border_padding_x
        self.border_padding_y = border_padding_y
        self.border_thickness = border_thickness
        self.border_type = border_type.lower()
        self.font = font
        self.name = name
        self.hidden = False
        self.editable = editable
        self.highlight_border_thickness = highlight_border_thickness
        self.limit = multiline
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clicked = False
        self.endy = 0
        self.value = ''
        self.autocomplete = []
        self.start_auto_fill = False
        self.autocomplete_case_sensitive = autocomplete_case_sensitive
        self.choices = autocomplete_choices
        if default_value_autocomplete is None:
            self.default_value_autocomplete = []
        else:
            self.default_value_autocomplete = default_value_autocomplete
        self.autocomplete_ratio = autocomplete_ratio
    
    
    def update(self, **options):
        elem = self.elem
        newline = '\n'
        for key, value in list(options.items()):
            if key == 'placeholder':
                self.placeholder = value
                self.text_lines = self.placeholder.splitlines()
                self.number_of_lines = len(self.text_lines)
                self.max_text_chars = 0
                for text_line in self.text_lines:
                    if len(text_line) > self.max_text_chars:
                        self.max_text_chars = len(text_line)
                self.elem.configure(width=self.max_text_chars, height=self.number_of_lines)
                elem.configure(state='normal')
                elem.delete('1.0', 'end')
                elem.insert('1.0', value)
                elem.configure(state='disabled')
            elif key == 'border_padding_x':
                if isinstance(value, list) or isinstance(value, tuple):
                    left_padding = value[0]
                    right_padding = value[1]
                    self.update(text=left_padding + self.text + right_padding)
                elif isinstance(value, int):
                    padding = '\n' * value
                    self.update(text=padding + self.text + padding)
            elif key == 'border_padding_y':
                if isinstance(value, list) or isinstance(value, tuple):
                    up_padding = value[0]
                    down_padding = value[1]
                    self.update(text=f"{newline * up_padding}{self.text.strip(newline)}{newline * down_padding}")
                elif isinstance(value, int):
                    self.update(text=f"{newline * value}{self.text.strip(newline)}{newline * value}")
            elif key == 'padding_x':
                elem.configure(padx=value)
            elif key == 'padding_y':
                elem.configure(pady=value)
            elif key == 'font':
                elem.configure(font=value)
            elif key == 'background':
                elem.configure(bg=value)
            elif key == 'border_thickness':
                elem.configure(bd=value)
            elif key == 'border_type':
                if value == 'thin':
                    elem.configure(relief='ridge')
                elif value == 'dent':
                    elem.configure(relief='groove')
                elif value == 'default':
                    elem.configure(relief='flat')
                else:
                    if value in ['ridge', 'groove']:
                        raise WidgetError(f'Unknown border type "{value}".')
                    try:
                        elem.configure(relief=value)
                    except _tkinter.TclError:
                        raise WidgetError(f'Unknown border type "{value}".')
            elif key == 'highlight_background_color':
                elem.configure(highlightbackground=value)
            elif key == 'highlight_border_thickness':
                elem.configure(highlightthickness=value)
            elif key == 'editable':
                elem.configure(state='disabled' if not value else 'normal')
            elif key == 'pull':
                self.hide()
                self.grid_args['sticky'] = value.replace(' ', '').lower().replace('up', 'n').replace('down', 's').replace('right', 'e').replace('left', 'w').replace('northwest', 'nw').replace('northeast', 'ne').replace('southwest', 'sw').replace('southeast', 'se')
                self.show()
            elif key == 'x':
                self.hide()
                self.grid_args['column'] = value
                self.show()
            elif key == 'y':
                self.hide()
                self.grid_args['row'] = value
                self.show()
                
                
    def hide(self):
        self.hidden = True
        self.elem.grid_forget()
        
        
    def show(self):
        self.hidden = False
        self.elem.grid(**self.grid_args)
        
        
    def init(self, root: tkinter.Misc):
        elem = tkinter.Text(root, width=self.width, height=self.height, bd=self.border_thickness, padx=self.padding_x, pady=self.padding_y, fg=self.text_color, bg=self.background, highlightthickness=self.highlight_border_thickness)
        if self.limit:
            def char_limit_handler():
                if root.root.stopall:
                    return
                value_lines = self.value.splitlines()
                if self.height < len(value_lines) + 1:
                    elem.delete('end-1c', 'end')
                root.after(1, char_limit_handler)
            root.after(1, char_limit_handler)
        if self.border_type != 'default':
            if self.border_type == 'thin':
                elem.configure(relief='ridge')
            elif self.border_type == 'dent':
                elem.configure(relief='groove')
            else:
                if self.border_type in ['ridge', 'groove']:
                    raise WidgetError(f'Unknown border type "{self.border_type}".')
                try:
                    elem.configure(relief=self.border_type)
                except _tkinter.TclError:
                    raise WidgetError(f'Unknown border type "{self.border_type}".')
        if self.font != 'default':
            elem.configure(font=self.font)
        if self.placeholder:
            def placeholder_click_handler(event):
                if not self.clicked:
                    elem.delete('1.0', 'end')
                    self.clicked = True
            def placeholder_focus_out(event):
                if not self.value:
                    elem.insert('1.0', self.placeholder)
                    self.clicked = False
            elem.bind('<1>', placeholder_click_handler)
            elem.bind('<FocusOut>', placeholder_focus_out)
            elem.insert('1.0', self.placeholder)
        if not self.editable:
            elem.configure(state='disabled')
        def handle_input():
            nonlocal elem
            elem.value = elem.get('1.0', 'end-1c')
            if elem.value != self.value:
                self.value = elem.value
            if self.start_auto_fill:
                if self.choices is not None:
                    matches = []
                    input_value = self.value
                    og_choices = self.choices
                    if not self.autocomplete_case_sensitive:
                        input_value = input_value.lower()
                        self.choices = [item.lower() for item in self.choices]
                    for index, possible_match in enumerate(self.choices):
                        ratio = difflib.SequenceMatcher(a=possible_match, b=input_value).ratio()
                        if ratio > self.autocomplete_ratio:
                            matches.append(og_choices[index])
                    if matches:
                        self.autocomplete = matches
                    else:
                        self.autocomplete = self.default_value_autocomplete
                    self.choices = og_choices
            if not root.root.stopall:
                root.after(1, handle_input)
            else:
                return
        def onkey(event):
            self.start_auto_fill = True
        root.after(1, handle_input)
        elem.bind('<Key>', onkey)
        self.root = root
        self.elem = elem
        return elem
    
    
class Menu:
    
    
    def __init__(self, *items, option_type: type=str, name: str=None, text_color: str='default', default_value: str=None, pull: str='default', x: int='default', y: int='default', padding_x: int=1, padding_y: int=1) -> None:
        if text_color == 'default':
            if dark_mode():
                text_color = 'white'
            else:
                text_color = '#2f2f30'
        self.text_color = text_color
        self.items = items
        self.option_type = option_type
        self.__previous_default_value = default_value
        self.default_value = default_value
        self.pull = pull
        self.x = x
        self.y = y
        self.name = name
        self.padding_x = padding_x
        self.padding_y = padding_y
        
        
    def __get_tkinter_var_class(self, type_: type):
        if type_ == str:
            var = tkinter.StringVar()
        elif type_ == int:
            var = tkinter.IntVar()
        elif type_ == float:
            var = tkinter.DoubleVar()
        elif type_ == bool:
            var = tkinter.BooleanVar()
        if self.default_value != None:
            var.set(self.default_value)
        self.value = var.get()
        self.__var = var
        
        
    def __onselect(self, root):
        if self.name != None:
            root.root.start_event(self.name, {})
        
        
    def init(self, root: tkinter.Misc | tkinter.Menu, is_window_menu: bool=False):
        if not is_window_menu:
            self.__get_tkinter_var_class(self.option_type)
            elem = tkinter.OptionMenu(root, self.__var, *self.items, command=lambda event: self.__onselect(root))
            elem.configure(bg=root.root.color, fg=self.text_color)
            def handle_menu():
                if self.default_value != self.__previous_default_value:
                    self.__var.set(self.default_value)
                    self.__previous_value = self.default_value
                if self.__var.get() != self.value:
                    self.value = self.__var.get()
                if root.root.stopall:
                    return
                root.after(1, handle_menu)
            root.after(1, handle_menu)
        elif is_window_menu:
            elem = tkinter.Menu(root)
            for item in self.items:
                if isinstance(item, Menu):
                    submenu = item.init(elem, True)
                    elem.add_cascade(label=item.name, menu=submenu)
                elif isinstance(item, str):
                    elem.add_command(label=item)
        self.root = root
        self.elem = elem
        return elem


class GUI:
    
    
    widget_dict = {}
    
    
    def __init__(self, title: str='GUIMagicPy', width: int=700, height: int=300, color: str='white', layout_type: str='grid', window_menu: Menu=None, x=0, y=0) -> None:
        global _when_dark_modeglvarobaliabel, all_guis
        self.root = tkinter.Toplevel()
        self.root.title(title)
        self.root.root = self
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        if color != 'default':
            self.root.configure(bg=color)
        if color == 'default' and _when_dark_modeglvarobaliabel != None:
            if dark_mode():
                self.color = '#2f2f30'
                self.root.configure(bg='#2f2f30')
                self.root.attributes('-alpha', 0.9999)
            else:
                self.color = 'white'
                self.root.configure(bg='white')
        elif color == 'default'  and _when_dark_modeglvarobaliabel == None:
            self.root.configure(bg='white')
        self.last_event = None
        self.color = color
        self.last_event_attributes = None
        self.stopall = False
        self.title = title
        self.__previous_title = title
        self.handle_attributes_id = None
        self.geometry = (width, height, x, y)
        self.__previous_geometry = (width, height, x, y)
        self.handle_window()
        def handle_attributes():
            if self.title != self.__previous_title:
                self.root.title(self.title)
                self.__previous_title = self.title
            if self.geometry != self.__previous_geometry:
                if len(self.geometry) <= 1 or len(self.geometry) == 3:
                    raise ValueError('Not enough values for geometry.')
                if len(self.geometry) > 4:
                    raise ValueError('Too much values for geometry.')
                if len(self.geometry) == 2:
                    self.root.geometry(f'{self.geometry[0]}x{self.geometry[1]}')
                if len(self.geometry) == 4:
                    self.root.geometry(f'{self.geometry[0]}x{self.geometry[1]}+{self.geometry[2]}+{self.geometry[3]}')
                self.__previous_geometry = self.geometry
            if not self.stopall:
                self.handle_attributes_id = self.root.after(1, handle_attributes)
            else:
                return
        def delete_window_protocol():
            self.last_event = 'close'
            self.last_event_attributes = {}
        self.root.after(1, handle_attributes)
        self.root.protocol('WM_DELETE_WINDOW', delete_window_protocol)
        self.layout_type = layout_type
        self.root_widgets = []
        self.widgets = {}
        self.window_menu = window_menu
        if isinstance(self.window_menu, Menu):
            root_menu = self.window_menu.init(self.root, True)
            self.root.configure(menu=root_menu)
        self.endy = 0
        self._place_func = 'd'
        self._delay = 0.012
        all_guis.append(self)
        
    
    def set(self, layout: list | tuple | str | TextIOWrapper):
        if not layout:
            return
        if isinstance(layout, list) or isinstance(layout, tuple):
            lowercase_layout_type = self.layout_type.lower()
            if lowercase_layout_type == 'grid' or lowercase_layout_type == 'centered':
                for y, row in enumerate(layout):
                    self.root_widgets.insert(0, [])
                    for x, widget in enumerate(row):
                        try:
                            elem = widget.init(self.root)
                        except AttributeError:
                            elem = widget.root
                        self.root_widgets[y].append(elem)
                        args = {'row': widget.y, 'column': widget.x, 'padx': widget.padding_x, 'pady': widget.padding_y}
                        if widget.pull != 'default':
                            args['sticky'] = widget.pull.replace(' ', '').lower().replace('up', 'n').replace('down', 's').replace('right', 'e').replace('left', 'w').replace('northwest', 'nw').replace('northeast', 'ne').replace('southwest', 'sw').replace('southeast', 'se')
                        if widget.name != None:
                            self.widgets[widget.name] = widget
                        if widget.y != 'default' and widget.x != 'default':
                            try:
                                if self._place_func == 'd':
                                    elem.grid(**args)
                                else:
                                    self.root.add(elem, **args)
                            except _tkinter.TclError as te:
                                pass
                        else:
                            args['row'] = y
                            args['column'] = x
                            try:
                                if self._place_func == 'd':
                                    elem.grid(**args)
                                else:
                                    self.root.add(elem)
                            except _tkinter.TclError:
                                pass
                        widget.grid_args = args
                if not self.root_widgets[0]:
                    del self.root_widgets[0]
                self.endy = y + 1
            elif lowercase_layout_type == 'stack':
                for y, widget in enumerate(layout):
                    self.root_widgets.insert(0, [])
                    try:
                        elem = widget.init(self.root)
                    except AttributeError:
                        elem = widget.root
                    self.root_widgets[y].append(elem)
                    args = {'padx': widget.padding_x, 'pady': widget.padding_y}
                    if widget.name != None:
                        self.widgets[widget.name] = widget
                    try:
                        elem.pack(**args)
                    except _tkinter.TclError:
                        pass
            else:
                raise LayoutError(f'No layout named "{self.layout_type}".')
        elif isinstance(layout, str):
            #lang_interpreter.interpret(self, layout)
            lang_interpreter.interpret(sys.modules[__name__], self, layout)
        elif isinstance(layout, TextIOWrapper):
            with layout:
                self.set(layout.read())
                
                
    def default_event_handler(self):
        while True:
            event, attributes = self.get_current_event()
            if event == 'close':
                break
        self.stop()
                
                
    def add(self, widget):
        elem = widget.init(self.root)
        lowercase_layout_name = self.layout_type.lower()
        if lowercase_layout_name == 'grid':
            if widget.x == 'default':
                widget.x = 0
            if widget.y == 'default':
                widget.y = self.endy
            try:
                self.root_widgets[widget.y].insert(widget.x, elem)
            except IndexError:
                self.root_widgets.append([elem])
            args = {'row': widget.y, 'column': widget.x, 'padx': widget.padding_x, 'pady': widget.padding_y}
            if widget.pull != 'default':
                args['sticky'] = widget.pull.replace(' ', '').lower().replace('up', 'n').replace('down', 's').replace('right', 'e').replace('left', 'w').replace('northwest', 'nw').replace('northeast', 'ne').replace('southwest', 'sw').replace('southeast', 'se')
            if widget.name != None:
                self.widgets[widget.name] = widget
            try:
                if self._place_func == 'd':
                    elem.grid(**args)
                else:
                    self.root.add(elem, **args)
            except _tkinter.TclError:
                raise LayoutError('Layout already set.')
            widget.grid_args = args
            if not self.root_widgets[0]:
                del self.root_widgets[0]
        elif lowercase_layout_name == 'stack':
            try:
                self.root_widgets[widget.y].append(elem)
            except (IndexError, TypeError):
                self.root_widgets.append([elem])
            args = {'padx': widget.padding_x, 'pady': widget.padding_y}
            if widget.pull != 'default':
                args['sticky'] = widget.pull.replace(' ', '').lower().replace('up', 'n').replace('down', 's').replace('right', 'e').replace('left', 'w').replace('northwest', 'nw').replace('northeast', 'ne').replace('southwest', 'sw').replace('southeast', 'se')
            if widget.name != None:
                self.widgets[widget.name] = widget
            try:
                elem.pack(**args)
            except _tkinter.TclError:
                raise LayoutError('Layout already set.')
            widget.grid_args = args
        if lowercase_layout_name == 'grid' and args.get('row') != self.endy + 1:
            pass
        else:
            self.endy += 1
        
            
    def handle_click(self, widget_name, eventname):
        if eventname == '2':
            self.start_event(f'{widget_name}', {'mouse button': 'right'})
            
            
    def handle_window(self):
        def button_handler(event):
            button_name = event.num
            if button_name == 2:
                self.start_event('window', {'mouse button': 'right'})
        self.root.bind('<Button>', button_handler)
        
        
    def start_event(self, event, attributes: dict=None):
        def inner():
            time.sleep(self._delay)
            self.last_event = None
            self.last_event_attributes = None
        self.last_event = event
        self.last_event_attributes = attributes
        thread = threading.Thread(target=inner, daemon=True)
        thread.start()
        
        
    def get_current_event(self):
        self.root.update()
        return self.last_event, self.last_event_attributes
    
    
    def stop(self):
        global _mainwin, closed_all
        self.stopall = True
        try:
            all_guis.remove(self)
        except ValueError:
            pass
        if not all_guis:
            closed_all = True
        try:
            self.root.destroy()
        except _tkinter.TclError:
            pass
        
        
    def schedule(self, milliseconds: int, func: Callable):
        def scheduled_function():
            function_object = func()
            if not self.stopall or not function_object.stop:
                self.root.after(milliseconds * 1000, scheduled_function)
        self.root.after(milliseconds * 1000, scheduled_function)


class Frame(GUI):
    
    
    def __init__(self, gui: GUI, name: str = '', pull: str='default', layout_type: str='grid', orient: str='default', border: str='default', padding_x: int=5, padding_y: int=5, border_padding_x: int=5, border_padding_y: int=5, color: str = 'white', width: int='default', height: int='default', resizable: bool=False, x: int=0, y: int=0) -> None:
        global _when_dark_modeglvarobaliabel
        self.padding_x, self.padding_y, self.pull, self.border_padding_x, self.border_padding_y = padding_x, padding_y, pull, border_padding_x, border_padding_y
        if not resizable:
            self.root = tkinter.Frame(gui.root, padx=self.padding_y, pady=self.padding_y)
        elif resizable:
            root_args = {}
            if orient != 'default':
                root_args['orient'] = orient
            self.root = tkinter.PanedWindow(gui.root, **root_args)
        self.name = name
        self.grid_args = {'row': y, 'column': x}
        if pull != 'default':
            pull = pull.replace(' ', '').lower().replace('up', 'n').replace('down', 's').replace('right', 'e').replace('left', 'w').replace('northwest', 'nw').replace('northeast', 'ne').replace('southwest', 'sw').replace('southeast', 'se')
            self.grid_args['sticky'] = pull
        if width != 'default':
            self.root.configure(width=width)
        if height != 'default':
            self.root.configure(height=height)
        self.root.grid(**self.grid_args)
        self.root.root = self
        if color != 'default':
            self.root.configure(bg=color)
        if color == 'default' and _when_dark_modeglvarobaliabel != None:
            if dark_mode():
                self.root.configure(bg='#2f2f30')
                self.root.attributes('-alpha', 0.9999)
            else:
                self.root.configure(bg='white')
        elif color == 'default'  and _when_dark_modeglvarobaliabel == None:
            self.root.configure(bg='white')
        self.last_event = None
        self.last_event_attributes = None
        self.stopall = False
        self.title = name
        self.__previous_title = name
        self.handle_attributes_id = None
        self.title = None
        def handle_attributes():
            if self.title != self.__previous_title:
                self.root.configure(text=self.title)
                self.__previous_title = self.title
        self.root.after(1, handle_attributes)
        self.root_widgets = []
        self.widgets = {}
        self.endy = 0
        self.layout_type = layout_type
        self._place_func = 'j'
        
        
def main():
    gui = GUI(layout_type='stack')
    gui.set([
        Text(f'This is GUIMPy Version {__version__}'),
        Text('This should be a cedilla: ç'),
        Button('Click me!', 'mybtn'),
        Button('QUIT', 'quitbtn')
    ])
    gui.default_event_handler()


if __name__ == '__main__':
    main()
