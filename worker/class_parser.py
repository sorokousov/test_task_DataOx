# -*- coding: utf-8 -*-
# Alexandr Sorokousov
# sorok.web@gmail.com
# TG @sorokousov
# ---------------------
import os
import platform
import time
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from config import time_out_serf, time_out_download
from models import Task
from utils import file_to_db

yahoo_url = 'https://finance.yahoo.com/'

# Папка для скачанных CSV
work_dir = os.path.join(os.getcwd(), 'tmp')

if platform.system() == 'Linux':
    chrome_driver = 'chromedriver'
else:
    chrome_driver = 'chromedriver.exe'


def clear_tmp():
    try:
        os.mkdir(path=os.path.join(work_dir))
    except:
        for file in os.listdir(work_dir):
            try:
                os.remove(os.path.join(work_dir, file))
            except:
                pass


def set_chrome_options() -> Options:
    """Настройки хрома"""
    chrome_prefs = {}
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["download.default_directory"] = work_dir
    chrome_options.experimental_options["prefs"] = chrome_prefs
    return chrome_options


class YahooFinanceHistory:

    def __init__(self, quote):
        # Очистим папку tmp
        # clear_tmp()

        self.time_out = 0
        self.quote = quote
        self.quote_abbr = ''
        self.file_name = ''
        self.not_quote = False

        self.driver = webdriver.Chrome(options=set_chrome_options())
        self.driver.get(url=yahoo_url)

    def step_1(self):
        """Проходим сообщения куки"""
        while self.time_out <= time_out_serf:
            try:
                try:
                    self.driver.find_element_by_name("agree").click()
                except:
                    # Если окно недостаточно раскрыто
                    self.driver.find_element_by_id("scroll-down-btn").click()
                self.time_out = 0
                break
            except:
                self.time_out += 0.1
                time.sleep(0.1)

    def step_2(self):
        """Вводим котировку и жмём Enter"""
        while self.time_out <= time_out_serf:
            try:
                self.driver.find_element_by_id("yfin-usr-qry").click()
                self.driver.find_element_by_id("yfin-usr-qry").clear()
                self.driver.find_element_by_id("yfin-usr-qry").send_keys(self.quote)
                self.driver.find_element_by_id("header-search-form").submit()
                self.time_out = 0
                break
            except:
                self.time_out += 0.1
                time.sleep(0.1)

    def step_3(self):
        """Жмём историю"""
        while self.time_out <= time_out_serf:
            try:
                self.driver.find_element_by_xpath("//div[@id='quote-nav']/ul/li[5]/a/span").click()
                self.time_out = 0
                break
            except:
                self.time_out += 0.1
                time.sleep(0.1)

    def step_4(self):
        """Жмём выбор дат"""
        while self.time_out <= time_out_serf:
            try:
                self.driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span').click()

                # Аббревиатура котировки
                quote_abbr = self.driver.current_url.split('/history')[0].split('/')[-1]
                self.quote_abbr = quote_abbr
                print(f"{self.quote}: quote_abbr:", self.quote_abbr)

                if self.quote_abbr.lower() == self.quote.lower():
                    self.time_out = 0
                else:
                    self.time_out = time_out_serf + 1
                    self.not_quote = True

                break
            except:
                self.time_out += 0.1
                time.sleep(0.1)

    def step_5(self):
        """Жмём max"""
        while self.time_out <= time_out_serf:
            try:
                self.driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button/span').click()
                self.time_out = 0
                break
            except:
                self.time_out += 0.1
                time.sleep(0.1)

    def step_6(self):
        """Жмём загрузить"""
        while self.time_out <= time_out_serf:
            try:
                self.driver.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a/span').click()
                self.time_out = 0
                break
            except:
                self.time_out += 0.1
                time.sleep(0.1)

    def step_7(self):
        """Ожидаем завершения загрузки файла"""

        # Если self.time_out > time_out_limit, значит пришли с пустыми руками и должны
        # пометить задачу как Ошибка открытия страницы
        if self.time_out > time_out_serf:
            reason_stop = f"{self.quote}: Не удалось найти такую котировку" if self.not_quote else f"{self.quote}: Ошибка открытия страницы"
            print(reason_stop)
            task = Task.get_or_none(Task.quote == self.quote)
            if task:
                task.reason_stop = reason_stop
                task.stopped = True
                task.completed_at = datetime.now()
                task.save()
            return False

        while self.time_out <= time_out_download:
            for file_name in list(os.walk(work_dir))[0][2]:

                # Если загрузить файл удалось
                if file_name == self.quote_abbr + '.csv':
                    self.file_name = os.path.join(work_dir, self.quote_abbr + '.csv')
                    print(f"{self.quote}: file_name:", self.file_name)
                    return True
                else:
                    self.time_out += 0.1
                    time.sleep(0.1)

        # Пометить задачу как Не удалось загрузить файл
        reason_stop = f"{self.quote}: Не удалось загрузить файл"
        print(reason_stop)
        task = Task.get_or_none(Task.quote == self.quote)
        if task:
            task.reason_stop = reason_stop
            task.stopped = True
            task.completed_at = datetime.now()
            task.save()
        return False

    def run_magic(self):
        self.step_1()
        self.step_2()
        self.step_3()
        self.step_4()
        self.step_5()
        self.step_6()
        if self.step_7():
            file_to_db(file_name=self.file_name,
                       quote=self.quote)

        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    wd = os.getcwd()
    tmp = os.path.join(wd, 'tmp')
    print(tmp)
    print(list(os.walk(tmp)))
    # print(list(os.walk(tmp))[0][2])