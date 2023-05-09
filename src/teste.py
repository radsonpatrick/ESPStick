from utime import sleep
from gc import collect
from machine import SPI, deepsleep, Pin,reset
import st7789
from fonts import vga1_16x32 as font
from umenu import *
from class_definitions import *
from variables import WIFI_AP,WIFI_STA,DISPLAY
import webrepl

button1 = Pin(14, Pin.IN, Pin.PULL_UP)
led = Device(Pin(22, Pin.OUT, value=1))
display = DISPLAY


def print_display(string: str, start=0, end=0):
    len_font = int(240/font.WIDTH)
    if len(string) <= len_font:
        display.text(font, string, start, end)
    else:
        for i in range(0, len(string), len_font):
            display.text(font, string[i:i+len_font], start, end)
            end = end+font.HEIGHT


collect()
menu = Menu(display, 5, 35, 16, 32)


def connect_terminal():
    display.fill(st7789.BLACK)
    display.fill_rect(40, 78, 160, 80, st7789.GREEN)
    display.text(font, 'Ready for', 50, 88,
                 st7789.BLACK, st7789.GREEN)
    display.text(font, 'WebREPL', 50+16, 88+32,
                 st7789.BLACK, st7789.GREEN)
    raise ValueError('webrepl')


def deep_sleep():
    import esp32
    display.fill(0)
    print_display('Bye Bye', start=72, end=88)
    sleep(3)
    esp32.wake_on_ext0(pin = button1, level = esp32.WAKEUP_ALL_LOW)
    display.sleep_mode(True)
    collect()
    display.off()
    deepsleep()

def reboot():
    display.off()
    reset()

wifi = Wifi()
try:
    menu.set_screen(MenuScreen('Main Menu')
                    .add(SubMenuItem('WiFi')
                        .add(EnumItem("Mode", ['AP', 'CLIENT'], wifi.mode,wifi.mode))
                        .add(InfoItem('Status:',wifi.status))
                        .add(InfoItem('IP:',wifi.ip))
                        .add(CallbackList('Scan',wifi.scan))
                        )
                    .add(SubMenuItem('Lights')
                            .add(ToggleItem('LED', (led.stat), (led.toggle)))
                            
                            )
                    .add(SubMenuItem('Advanced')
                            .add(FileList('Scripts'))
                            .add(CallbackItem('Start WebRepl', (connect_terminal)))
                            .add(CallbackItem('Deep Sleep', (deep_sleep)))
                            .add(ConfirmItem("Reboot", (reboot), "Reboot?", ('Yes', 'No')))
                            )
                    )
    collect()
    menu.draw()
except Exception as e:
    print(e)
    display.fill(st7789.BLACK)
    print_display('ERRO :'+str(e))
