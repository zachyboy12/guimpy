"""
Parser for the GUIML Language, a varient of the famous HTML.

Usage:
    GUIMLTextParser:
        from guimpy.guiml import *
        parser = GUIMLTextParser()
        parser.feed('<text>This is a test.</text>')
        print(parser.text)
    parse_text (with GUIMLTextParser):
        from guimpy.guiml import *
        parser = GUIMLTextParser()
        print(parse_text('<text>This is a test.</text>'))
    parse_text (without GUIMLTextParser):
        from guimpy.guiml import *
        print(parse_text('<text>This is a test.</text>'))
"""


from html.parser import HTMLParser
import __init__ as guimpy, ast


class TagError(Exception):
    """
    Error if tag is unknown.
    Args:
        args (tuple): Message to raise.
    """


class GUIMLTextParser(HTMLParser):
    
    
    text = guimpy.Text()
    start_tag = ''
    
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key, value in list(attrs.items()):
            attrs[key] = ast.literal_eval(value)
        self.start_tag = tag
        self.attributes = attrs
        

    def handle_data(self, data):
        if data.strip():
            if self.start_tag == 'text' or self.start_tag == 't':
                self.text.update(**self.attributes)
            else:
                raise TagError(f'Unknown GUIML tag "{self.start_tag}".')
        
        
    def feed(self, data) -> None:
        if isinstance(data, bytes):
            data = data.decode()
        else:
            data = str(data)
        new_data = data.replace('\n', '')
        for line in data.splitlines():
            if line.startswith(' ') or line.endswith(' '):
                new_data += line.strip()
        return super().feed(new_data)
        
        
def parse_text(markup: str, parser: GUIMLTextParser=None):
    if parser is None:
        parser = GUIMLTextParser()
        parser.feed(markup)
    else:
        parser.feed(markup)
    return parser.markup_dict
