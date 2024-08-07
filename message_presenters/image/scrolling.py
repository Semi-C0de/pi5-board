from rgbmatrix import graphics
import time
from PIL import Image

from ..utils import interrupt

def scrollingImage(matrix, message):
    with Image.open(message["value"]) as image:
        
        pos = 0
        matrix.SetImage(image.convert("RGB"), offset_y = pos)
    
    @interrupt
    def wait(matrix, message):
        nonlocal pos

        if pos + image.height < matrix.height:
            pos = 0

        pos -= 1
        matrix.SetImage(image.convert("RGB"), offset_y = pos)
        time.sleep(0.1)

        
        
        
    wait(matrix, message)