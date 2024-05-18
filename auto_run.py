import time
from log_bot import send_to_telegram
import pyautogui

import logging

count = 0

while True:
    try:
        send_to_telegram()
        with open("gamer_bot.py", encoding='utf-8') as f:
            exec(f.read())
        logging.info('The end')
        break
    except Exception as ex:
        f.close()
        logging.error(ex)
        send_to_telegram()
        time.sleep(3700)
        pyautogui.moveTo(1000, 1000)
        time.sleep(5)
        pyautogui.doubleClick()
        time.sleep(7)

    count += 1

    if count > 24:
        break
