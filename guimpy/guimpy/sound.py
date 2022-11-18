"""
Play Sounds in GUIMPy.
Wrapper around bash commands.
Usage:
    import guimpy.sound
    soundsystem = guimpy.sound.System()
    soundsystem.play()
"""


import os


class System:
    
    
    def __init__(self, soundfile: str, background_music: bool=False) -> None:
        self.soundfile = soundfile
        self.background_music = background_music
        self._stop = None
        
        
    def play(self):
        if self.background_music:
            os.system(f'afplay {self.soundfile}')
        elif not self.background_music:
            os.system(f'afplay {self.soundfile} &')
        
        
    def set_block(self, background_music: bool):
        self.background_music = background_music
