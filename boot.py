import variables
import st7789
from machine import SPI, Pin 
import webrepl
from class_definitions import Wifi

##start display 

# try:
spi = SPI(1, baudrate=31250000, sck=Pin(18), mosi=Pin(23), polarity=1)
variables.DISPLAY = st7789.ST7789(spi, 240, 240, reset=Pin(
    4, Pin.OUT), dc=Pin(12, Pin.OUT), backlight=Pin(15, Pin.OUT, Pin.PULL_UP), rotation=0)
variables.DISPLAY.init()
variables.DISPLAY.fill(0xffff)  

wifi = Wifi()
wifi.to_client()
# except Exception as e :
#     print(e)    
#     wifi = variables.WIFI_STA
#     wifi.active(True)
#     #wifi.connect(variables.WIFI_SSID,variables.WIFI_PASS)
#     webrepl.start(password=variables.WEBREPL_PASS)
#     print('DeuF')
#     variables.DISPLAY.fill(0xff2c) 