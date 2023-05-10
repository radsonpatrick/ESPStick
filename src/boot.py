import st7789
from machine import SPI, Pin


button2 = Pin(27, Pin.IN, Pin.PULL_UP)

##SAFE_MODE
if not button2.value():
    import webrepl
    import network
    wifi_ap = network.WLAN(network.AP_IF)
    wifi_ap.active(True)
    wifi_ap.config(essid='ESP32', password='12345678')
    webrepl.start(password='1234')
    Pin(22, Pin.OUT, value=1).off()
else:

    import variables
    from class_definitions import Wifi

    spi = SPI(1, baudrate=31250000, sck=Pin(18), mosi=Pin(23), polarity=1)
    variables.DISPLAY = st7789.ST7789(spi, 240, 240, reset=Pin(
        4, Pin.OUT), dc=Pin(12, Pin.OUT), backlight=Pin(15, Pin.OUT, Pin.PULL_UP), rotation=0)
    variables.DISPLAY.init()  

    wifi = Wifi()
    wifi.to_client()