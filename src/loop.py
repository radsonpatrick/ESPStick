import uasyncio as asyncio
from utime import sleep_ms


async def loop(menu):
    from config import BUTTON1,BUTTON2
    while True:
        if not BUTTON1.value():
            menu.move()
        if not BUTTON2.value():
            menu.click()
        sleep_ms(100)


def start(menu):
    asyncio.run(loop(menu))
