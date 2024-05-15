import time
from log_bot import send_to_telegram

count = 0

while True:
    try:
        send_to_telegram()
        exec(open("gamer_bot.py", encoding='utf-8').read())
        break
    except Exception as ex:
        send_to_telegram()
        time.sleep(3700)

    count += 1

    if count > 9:
        break
