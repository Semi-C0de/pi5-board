from rgbmatrix import graphics

from ..utils import *


def staticText(matrix, message):
    offscreen_canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
        
    height = message.get("effects").get("yPos", 20)

    # Make path dynamic
    font.LoadFont("pi5/fonts/7x13.bdf")
    messageText = message["value"]

    substrings, colors = colorSplit(message["effects"].get("colors", [{"index": [0, len(messageText) - 1], "color":"#FFFFFF"}]), messageText)

    offscreen_canvas.Clear()
    textLength = 0
    for idx, sub in enumerate(substrings):
        textColor = graphics.Color(*(colors[idx]))
        textLength += graphics.DrawText(offscreen_canvas, font, textLength, height, textColor, sub)

    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

    @interrupt
    def wait(matrix, message):
        time.sleep(0.001)
    
    wait(matrix, message)

    offscreen_canvas.Clear()
    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)