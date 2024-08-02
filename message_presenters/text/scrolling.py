from rgbmatrix import graphics
import time

from ..utils import *

def scrollingText(matrix, message):
        
        offscreen_canvas = matrix.CreateFrameCanvas()
        font = graphics.Font()
        
        height = message["effects"].get("yPos", 20)

        # TODO: Make path dynamic
        font.LoadFont("pi5/fonts/7x13.bdf")
        
        messageText = message["value"]

        substrings, colors = colorSplit(message["effects"].get("colors", [{"index": [0, len(messageText) - 1], "color":"#FFFFFF"}]), messageText)
            
        
        pos = offscreen_canvas.width
        offscreen_canvas.Clear()
        textLength = 0

        @interrupt
        def runText(matrix, message):
            nonlocal pos
            nonlocal offscreen_canvas
            nonlocal textLength
            nonlocal substrings
            nonlocal colors

            
            if pos + textLength <= 0:
                pos = offscreen_canvas.width

            offscreen_canvas.Clear()
            textLength = 0

            for idx, sub in enumerate(substrings):
                textColor = graphics.Color(*(colors[idx]))
                textLength += graphics.DrawText(offscreen_canvas, font, pos + textLength, height, textColor, sub)

            offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
            pos -= 1
            time.sleep(0.02)

        runText(matrix, message)

        offscreen_canvas.Clear()
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)