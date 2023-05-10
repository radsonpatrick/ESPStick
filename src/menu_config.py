from gc import collect
from machine import deepsleep, Pin,reset
import st7789
from umenu import *
from class_definitions import *
import config
from functions import * 

config.BUTTON1 = Pin(config.BUTTON1, Pin.IN, Pin.PULL_UP)
config.BUTTON2 = Pin(config.BUTTON2, Pin.IN, Pin.PULL_UP) 
led = Device(Pin(config.LED, Pin.OUT, value=1))

menu = Menu(config.DISPLAY, 5, 35, 16, 32)

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
    config.DISPLAY.fill(st7789.BLACK)
    print_display('ERRO :'+str(e))
