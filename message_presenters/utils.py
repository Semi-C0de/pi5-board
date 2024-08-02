import time
from threading import Thread, Event
from functools import wraps
from PIL import ImageColor

def colorSplit(colorsDict:list[dict], text:str) -> list[str]:

    substrings = []
    colors = []
    for sub in colorsDict:
        spl1 = None if sub["index"][0] == 0 else sub["index"][0]
        spl2 = None if sub["index"][1] - len(text) + 1 == 0 else sub["index"][1] - len(text) + 1

        substrings.append(text[spl1: spl2])
        colors.append(ImageColor.getcolor(sub["color"], "RGB"))

    return substrings, colors


def interrupt(func):
    exitEvent = Event()

    def forever(fn):
        @wraps(fn)
        def wpr(matrix, message):
            while not exitEvent.is_set():
                fn(matrix, message)
        return wpr

    @wraps(func)
    def wrapper(matrix, message):
        nonlocal exitEvent
        exitEvent.clear()  # Reset the event at the start

        wrapped_func = forever(func)  # Get the wrapped function
        
        p = Thread(target=wrapped_func, args=(matrix, message))
        p.start()
        try:
            time.sleep(message["duration"])
        finally:
            exitEvent.set()
            p.join()
    return wrapper