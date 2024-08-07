from typing import Optional

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from .message_presenters.text.scrolling import *
from .message_presenters.text.static import *
from .message_presenters.image.static import *
from .message_presenters.image.scrolling import *

class LEDDisplay:
    def __init__(self,
                 led_rows=32,
                 led_cols=64,
                 led_chain=1,
                 led_parallel=1,
                 led_pwm_bits=11,
                 led_brightness=100,
                 led_gpio_mapping=None,
                 led_scan_mode=1,
                 led_pwm_lsb_nanoseconds=130,
                 led_show_refresh=False,
                 led_slowdown_gpio=3,
                 led_no_hardware_pulse=None,
                 led_rgb_sequence="RGB",
                 led_pixel_mapper="",
                 led_row_addr_type=0,
                 led_multiplexing=0,
                 led_panel_type="",
                 drop_privileges=True):
        self.led_rows = led_rows
        self.led_cols = led_cols
        self.led_chain = led_chain
        self.led_parallel = led_parallel
        self.led_pwm_bits = led_pwm_bits
        self.led_brightness = led_brightness
        self.led_gpio_mapping = led_gpio_mapping
        self.led_scan_mode = led_scan_mode
        self.led_pwm_lsb_nanoseconds = led_pwm_lsb_nanoseconds
        self.led_show_refresh = led_show_refresh
        self.led_slowdown_gpio = led_slowdown_gpio
        self.led_no_hardware_pulse = led_no_hardware_pulse
        self.led_rgb_sequence = led_rgb_sequence
        self.led_pixel_mapper = led_pixel_mapper
        self.led_row_addr_type = led_row_addr_type
        self.led_multiplexing = led_multiplexing
        self.led_panel_type = led_panel_type
        self.drop_privileges = drop_privileges

        self.process()

        self.messages = []

    def process(self):
        options = RGBMatrixOptions()

        if self.led_gpio_mapping is not None:
            options.hardware_mapping = self.led_gpio_mapping
        options.rows = self.led_rows
        options.cols = self.led_cols
        options.chain_length = self.led_chain
        options.parallel = self.led_parallel
        options.row_address_type = self.led_row_addr_type
        options.multiplexing = self.led_multiplexing
        options.pwm_bits = self.led_pwm_bits
        options.brightness = self.led_brightness
        options.pwm_lsb_nanoseconds = self.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.led_rgb_sequence
        options.pixel_mapper_config = self.led_pixel_mapper
        options.panel_type = self.led_panel_type

        if self.led_show_refresh:
            options.show_refresh_rate = 1

        if self.led_slowdown_gpio is not None:
            options.gpio_slowdown = self.led_slowdown_gpio
        if self.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True
        if not self.drop_privileges:
            options.drop_privileges = False

        self.matrix = RGBMatrix(options=options)

    def addMessage(self, message):
        self.messages.append(message)

    def displayMessages(self, number: Optional[int] =  None):
        
        if number is None:
            for message in self.messages:
                # TODO: Implement
                pass
        
        else:
            for index in range(0, number):
                if self.messages[index]["type"] == "text":
                    self._dislayText(self.messages[index])
                if self.messages[index]["type"] == "image":
                    self._displayImage(self.messages[index])

    def _dislayText(self, message):
        scroll = True if message.get("effects").get("scroll") == "true" else False

        if scroll:  
            scrollingText(self.matrix, message)
        else:
            staticText(self.matrix, message)

    def _displayImage(self, message):
        scroll = True if message.get("effects").get("scroll") == "true" else False

        if scroll:
            scrollingImage(self.matrix, message)
        else:
            staticImage(self.matrix, message)