import uasyncio as asyncio
from machine import Pin
from utime import sleep_ms

button1 = Pin(14, Pin.IN, Pin.PULL_UP)
button2 = Pin(27, Pin.IN, Pin.PULL_UP)


async def assincrono(menu):
    while True:
        if not button1.value():
            menu.move()
        if not button2.value():
            menu.click()
        sleep_ms(100)


def start(menu):
    asyncio.run(assincrono(menu))
