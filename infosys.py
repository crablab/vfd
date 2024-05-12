from pyfis.ibis import SerialIBISMaster
import time

MAX_DISPLAY_LENGTH = 24

class display:
    def __init__(self):
        self.master = SerialIBISMaster("/dev/ttyUSB0", debug=False)
        self.lock   = False

    def write_text(self, text: str, effect: str = 'split', wipe: bool = False) -> str:
        """
        Write text to the IBIS device
        """

        if(len(text) > 48):
            ValueError("Text too long")
            return
        
        if(self.lock):
            ConnectionError("Display is locked")
            return
        
        self.lock = True
        if wipe:
            self._wipe_display()

        if effect == "chase":
            self._do_chase(text)
        elif effect == "split":
            self._do_split(text)

        self.lock = False

    def print_time(self):
        """
        Print the current time to the IBIS device
        """

        if(self.lock):
            ConnectionError("Display is locked")
            return
        
        self.lock = True
        self.master.DS009(f'{time.strftime("%H:%M")}')
        self.lock = False

    def _do_split(self, text: str):
        """
        Write text to the IBIS device with a timestamp
        """

        split = [text[i:i+MAX_DISPLAY_LENGTH] for i in range(0, len(text), MAX_DISPLAY_LENGTH)]

        for i in split:
            self.master.DS009(self._pad_string(f'{time.strftime("%H:%M")} {self._pad_string(i)}'))
            time.sleep(5)

        return 

    def _do_chase(self, text: str):
        """
        Write text to the IBIS device with a timestamp
        """

        self.master.DS009(f'{time.strftime("%H:%M")} {self._pad_string(text)}')
        time.sleep(5)
        
        loops = len(text) + 1
        for i in range(0, loops):
            self.master.DS009(f'{time.strftime("%H:%M")} {self._pad_string(text, True)}')

            text = text[1:]
            time.sleep(1)

        return
  
    def _wipe_display(self):
        """
        Wipe the display
        """
        for i in range(0, 30):
            self.master.DS009(f'{" " * i}#{" " * (MAX_DISPLAY_LENGTH + 4 - i)}.')
        
        time.sleep(.1)
        
    def _pad_string(self, text: str, suffix: bool = False):
        """
        Pad the string to the correct length
        """

        if len(text) < MAX_DISPLAY_LENGTH:
            pad = " " * (MAX_DISPLAY_LENGTH - len(text) -1)
            if suffix:
                text = text + pad + '.'
            else: 
                text = pad + text

        return text