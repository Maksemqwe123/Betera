from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from main import get_number_from_img_v2
from conf import *

import pyautogui
import time


class RoleteBot:
    def __init__(self):
        self.red_number_list = RED_NUMBER_LIST
        self.api_keys = API_KEYS

        self._get_html()

    def _get_html(self):
        options = webdriver.FirefoxOptions()

        driver = webdriver.Firefox(
            options=options
        )
        driver.maximize_window()
        driver.get('https://pm.by/ru/popup/login')
        print('connection')
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

            pyautogui.moveTo(2100, 540)
            time.sleep(1)
            pyautogui.click()
            time.sleep(10)

            pyautogui.moveTo(1200, 780)
            time.sleep(1)
            pyautogui.click()

            time.sleep(3)

            pyautogui.moveTo(2305, 1445)
            time.sleep(2)
            pyautogui.doubleClick()

            time.sleep(3)

            pyautogui.moveTo(1200, 1340)
            time.sleep(2)

            self._game_in_roulete(driver)
        except Exception as ex:
            return ex

    def _game_in_roulete(self, driver):
        black_number = []
        count_black_number = [0, 0]
        try:
            # iframe = driver.find_element(By.ID, "iFrameResizer0")
            #
            # driver.switch_to.frame(iframe)
            # time.sleep(2)
            #
            # input_phone = driver.find_element(By.CSS_SELECTOR, 'div.PhoneInput_telInputMask__4bIfr input#login-phone')
            # time.sleep(2)
            #
            # input_phone.click()
            # time.sleep(2)
            #
            # input_phone.send_keys('298555344')
            # time.sleep(1)
            #
            # input_password = driver.find_element(By.CLASS_NAME, 'Password_passwordField__input__tUCEf')
            # input_password.click()
            # time.sleep(2)
            #
            # input_password.send_keys('Makcemjoi990')
            # time.sleep(1)
            #
            # input_password.send_keys(Keys.ENTER)
            # time.sleep(5)
            # driver.get('https://pm.by/ru/play/livecasino/106/Mega%20Roulette/standard/playreal/10514')
            #
            # time.sleep(30)
            #
            # pyautogui.moveTo(2100, 540)
            # time.sleep(1)
            # pyautogui.click()
            # time.sleep(10)
            #
            # pyautogui.moveTo(1200, 780)
            # time.sleep(1)
            # pyautogui.click()
            #
            # time.sleep(3)
            #
            # pyautogui.moveTo(2305, 1445)
            # time.sleep(2)
            # pyautogui.doubleClick()
            #
            # time.sleep(3)
            #
            # pyautogui.moveTo(1200, 1340)
            # time.sleep(2)

            index_api_key = 0
            while True:
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

                if rolete_number == 'LL':
                    rolete_number = '17'

                if not rolete_number and int(black_number[-1]) != 0:
                    print('not detected number')
                    rolete_number = '0'

                if not black_number or len(rolete_number) < 3 and rolete_number and int(black_number[-1]) != int(rolete_number):
                    print('---------------------------')

                    black_number.append(int(rolete_number))

                    print(f'Rollet number: ', rolete_number)
                    print('Black List number: ', black_number)
                    print('count: ', count_black_number)
                    print('\n\n')

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
                            print('hello world')
                            count = [count_black_number[0] + 1, 3]

                        count_black_number.clear()

                        count_black_number.extend(count)
                    else:
                        print('red number')
                        count_black_number.clear()
                        count_black_number.extend([1, 1])

                    if count_black_number[0] == 1:
                        print(count_black_number)
                        pyautogui.click()
                    else:
                        for i in range(count_black_number[0]):
                            pyautogui.click()

                    print('------------------------')

        except Exception as ex:
            print(f'Error: {repr(ex)}')
            print(ex)

        finally:
            driver.close()


start = time.time()
RoleteBot()
end = time.time()

print('Время работы: ', (end - start) // 60)
