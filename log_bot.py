import logging

import requests

from conf import apiURL, chat_id


def send_to_telegram():
    try:
        files = {'photo': open(r'screenshot.png', 'rb')}
        data = {'chat_id': chat_id}

        requests.post(apiURL, files=files, data=data)

    except Exception as ex:
        logging.error(ex)
