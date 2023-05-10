import st7789
from config import DISPLAY
from time import sleep
from fonts import vga1_16x32 as font

def connect_terminal():
    DISPLAY.fill(st7789.BLACK)
    DISPLAY.fill_rect(40, 78, 160, 80, st7789.GREEN)
    DISPLAY.text(font, 'Ready for', 50, 88,
                 st7789.BLACK, st7789.GREEN)
    DISPLAY.text(font, 'WebREPL', 50+16, 88+32,
                 st7789.BLACK, st7789.GREEN)
    raise ValueError('webrepl')

def deep_sleep():
    import esp32
    from machine import deepsleep
    from config import BUTTON1
    
    DISPLAY.fill(0)
    print_display('Bye Bye', start=72, end=88)
    sleep(3)
    esp32.wake_on_ext0(pin = BUTTON1, level = esp32.WAKEUP_ALL_LOW)
    DISPLAY.sleep_mode(True)
    DISPLAY.off()
    deepsleep()

def reboot():
    from machine import reset
    DISPLAY.off()
    reset()

def print_display(string: str, start=0, end=0):
    len_font = int(240/font.WIDTH)
    if len(string) <= len_font:
        DISPLAY.text(font, string, start, end)
    else:
        for i in range(0, len(string), len_font):
            DISPLAY.text(font, string[i:i+len_font], start, end)
            end = end+font.HEIGHT