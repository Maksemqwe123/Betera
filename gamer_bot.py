from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver
from selenium.webdriver.chrome.options import Options


from main import get_number_from_img_v2

from conf import *

import cv2
import numpy as np
import pyautogui
import time
import logging

logging.basicConfig(filename='betera.log', filemode='w+', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def detected_color():
    # Загрузка изображения
    image = cv2.imread('save_screen.png')

    # Определение диапазона красного цвета в формате BGR
    lower_red = np.array([0, 0, 200])
    upper_red = np.array([50, 50, 255])

    # Поиск пикселей красного цвета в заданном диапазоне
    mask = cv2.inRange(image, lower_red, upper_red)
    red_present = cv2.countNonZero(mask) > 0

    return red_present


class RoleteBot:
    def __init__(self):
        self.red_number_list = RED_NUMBER_LIST
        self.api_keys = API_KEYS

        self._get_html()

    def _get_html(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get('https://pm.by/ru/popup/login')
        logging.info('connection')
        time.sleep(10)

        self._auth(driver)

    def _auth(self, driver):
        try:
            iframe = driver.find_element(By.ID, "iFrameResizer0")

            driver.switch_to.frame(iframe)
            time.sleep(2)

            input_phone = driver.find_element(By.CSS_SELECTOR, 'div.PhoneInput_telInputMask__4bIfr input#login-phone')
            time.sleep(2)

            input_phone.click()
            time.sleep(2)

            input_phone.send_keys(PHONE_NUMBER)
            time.sleep(1)

            input_password = driver.find_element(By.CLASS_NAME, 'Password_passwordField__input__tUCEf')
            input_password.click()
            time.sleep(2)

            input_password.send_keys(PASSWORD)
            time.sleep(1)

            input_password.send_keys(Keys.ENTER)
            time.sleep(5)
            driver.get('https://pm.by/ru/play/livecasino/106/Mega%20Roulette/standard/playreal/10514')

            time.sleep(30)

            time.sleep(10)

            pyautogui.FAILSAFE = False

            pyautogui.moveTo(2112, 527)
            time.sleep(1)
            pyautogui.click()

            time.sleep(10)

            pyautogui.moveTo(1292, 831)
            time.sleep(1)
            pyautogui.click()

            time.sleep(3)

            pyautogui.moveTo(2305, 1445)
            time.sleep(2)
            pyautogui.doubleClick()

            time.sleep(5)

            pyautogui.moveTo(1223, 1356)
            time.sleep(2)

            self._game_in_roulete(driver)

        except Exception as ex:
            logging.error(ex)
            driver.close()
            raise Exception(ex)

    def _game_in_roulete(self, driver):
        black_number = []
        count_black_number = [0, 0]
        index_api_key = 0

        start_time = time.time()

        while True:
            if time.time() - start_time > 480 and count_black_number[-1] == 1:
                raise Exception('exceeding the time limit')
            driver.save_screenshot("screenshot.png")
            time.sleep(2)

            if len(black_number) > 15 and int(black_number[-1]) in self.red_number_list:
                if index_api_key == 7:
                    index_api_key = 0
                else:
                    index_api_key += 1

                last_number = black_number[-1]
                black_number.clear()

                black_number.append(last_number)

            rolete_number = get_number_from_img_v2(api_key=self.api_keys[index_api_key])
            logging.info('info rolete_number: ', rolete_number)

            if rolete_number == 'LL':
                rolete_number = '17'

            if not rolete_number and int(black_number[-1]) != 0:
                logging.error('not detected number')

                red_present = detected_color()

                if red_present:
                    logging.info("There is a red color in the image")
                    rolete_number = '5'
                else:
                    logging.info("There is no red color in the image.")
                    rolete_number = '0'

            if not black_number or len(rolete_number) < 3 and rolete_number and int(black_number[-1]) != int(rolete_number):
                logging.info('---------------------------')

                black_number.append(int(rolete_number))

                logging.info(f'Rollet number: {rolete_number}')
                logging.info(f'Black List number: {black_number}')
                logging.info(f'count: {count_black_number}')
                logging.info('\n\n')

                if int(black_number[-1]) not in self.red_number_list:
                    if count_black_number[-1] == 0:
                        count = [1, 1]
                    elif count_black_number[-1] == 1:
                        count = [1, 2]

                    elif count_black_number[-1] == 2:
                        count = [3, 3]

                    elif count_black_number[-1] > 2:
                        count = [count_black_number[0] * 2, 3]
                    else:
                        logging.info('hello world')
                        count = [count_black_number[0] + 1, 3]

                    count_black_number.clear()

                    count_black_number.extend(count)
                else:
                    logging.info('red number')
                    count_black_number.clear()
                    count_black_number.extend([1, 1])

                if count_black_number[0] == 1:
                    print(count_black_number)
                    pyautogui.click()
                else:
                    for i in range(count_black_number[0]):
                        pyautogui.click()

                logging.info('------------------------')
            else:
                dubl_rolete_number = get_number_from_img_v2(api_key=self.api_keys[index_api_key], area=True)

                if not dubl_rolete_number and int(black_number[-1]) != 0:
                    logging.error('not detected dubl rolete number')

                    red_present = detected_color()

                    if red_present:
                        logging.info("There is a red color in the image")
                        dubl_rolete_number = '5'
                    else:
                        logging.info("There is no red color in the image.")
                        dubl_rolete_number = '0'

                if int(dubl_rolete_number) == int(black_number[-1]) and int(black_number[-1]) not in self.red_number_list:
                    logging.info('detected dubl rolete number')

                    logging.info(f'Dubl Rollet number: {dubl_rolete_number}')
                    logging.info(f'Black List number: {black_number}')
                    logging.info(f'count: {count_black_number}')
                    logging.info('\n\n')

                    black_number.append(int(dubl_rolete_number))

                    if count_black_number[-1] == 0:
                        count = [1, 1]
                    elif count_black_number[-1] == 1:
                        count = [1, 2]

                    elif count_black_number[-1] == 2:
                        count = [3, 3]

                    elif count_black_number[-1] > 2:
                        count = [count_black_number[0] * 2, 3]
                    else:
                        logging.info('hello world')
                        count = [count_black_number[0] + 1, 3]

                    count_black_number.clear()

                    count_black_number.extend(count)

                    for i in range(count_black_number[0]):
                        pyautogui.click()

                elif int(dubl_rolete_number) == int(black_number[-1]) and int(black_number[-1]) in self.red_number_list:
                    black_number.append(int(dubl_rolete_number))

                    logging.info('dubl rolete red number')
                    count_black_number.clear()
                    count_black_number.extend([1, 1])

                    pyautogui.click()
                else:
                    time.sleep(2)


start = time.time()
RoleteBot()
end = time.time()

logging.info(f'Время работы: {(end - start) // 60}')

