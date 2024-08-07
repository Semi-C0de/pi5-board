import time
from PIL import Image

from ..utils import interrupt

def staticImage(matrix, message):
    with Image.open(message["value"]) as image:

        image.thumbnail((matrix.width, matrix.height))

        matrix.SetImage(image.convert('RGB'))

        @interrupt
        def wait(matrix, message):
            time.sleep(0.001)
        
        wait(matrix, message)
