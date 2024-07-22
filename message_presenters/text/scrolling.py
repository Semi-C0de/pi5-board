from rgbmatrix import graphics
import time
from PIL import ImageColor

def scrollingText(matrix, message):
        
        offscreen_canvas = matrix.CreateFrameCanvas()
        font = graphics.Font()
        
        height = message["value"].get("yPos") or 18

        # Make path dynamic
        font.LoadFont("pi5/fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width
        messageText = message["value"]["text"]

        offscreen_canvas.Clear()
        pixelLength = graphics.DrawText(offscreen_canvas, font, pos , height, textColor, messageText)

        if message["value"].get("colors") is None:

            while (pos + pixelLength > 0):
                offscreen_canvas.Clear()

                graphics.DrawText(offscreen_canvas, font, pos, height, textColor, messageText)
                time.sleep(0.005)

                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
                pos -= 1

        else:
            substrings = []
            for sub in message["value"]["colors"]:
                spl1 = None if sub["index"][0] == 0 else sub["index"][0]
                spl2 = None if sub["index"][1] - len(messageText) + 1 == 0 else sub["index"][1] - len(messageText) + 1
                
                substrings.append(messageText[spl1: spl2])

            while (pos + pixelLength > 0):
                offscreen_canvas.Clear()
                textLength = 0

                for idx, sub in enumerate(substrings):
                    rgb = ImageColor.getcolor(message["value"]["colors"][idx]["color"], "RGB")
                    textColor = graphics.Color(rgb[0], rgb[1], rgb[2])

                    textLength += graphics.DrawText(offscreen_canvas, font, pos + textLength, height, textColor, sub)

                time.sleep(0.005)
                offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
                pos -= 1