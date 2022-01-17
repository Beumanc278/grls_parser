import time
import re
from typing import List
import urllib.request
import random
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NavigationHelper:

    def __init__(self, app):
        self.app = app

    def find_rows_for_given_label(self, label: str):
        wd = self.app.wd
        search_link = 'https://grls.rosminzdrav.ru/GRLS.aspx?RegNumber=&MnnR={}&lf=&TradeNmR=&OwnerName=&MnfOrg=&MnfOrgCountry=&isfs=0&regtype=1%2c6&pageSize=10&order=RegDate&orderType=desc&pageNum=1'
        wd.get(search_link.format(label))
        table_element = self.wait_table_element()
        if table_element is None:
            print(f'Не найдено позиций для лекарства - {label}.')
            return
        table_rows = table_element.find_elements(by=By.XPATH, value='//tbody/tr[@class="hi_sys poi"]')
        return table_rows

    def download_instruction(self, preparat_id: str):
        wd = self.app.wd
        certain_row_link = 'https://grls.rosminzdrav.ru/Grls_View_v2.aspx?routingGuid={}&t='
        wd.get(certain_row_link.format(preparat_id))
        preparat_name = wd.find_element_by_id('ctl00_plate_TradeNmR').get_attribute('value')
        preparat_manufacturer = ''
        try:
            preparat_manufacturer = '_' + re.search(r'"[А-Яа-я]+"', wd.find_element_by_id('ctl00_plate_RegNr').get_attribute('value')).group().replace('"', '')
        except AttributeError as ex:
            preparat_manufacturer = f"_{preparat_id.split('-')[1]}"
        file_name = preparat_name + preparat_manufacturer
        wd.find_element_by_id('instructionsCaller').click()
        WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.ID, "instructionsModal")))
        target_link = wd.execute_script('return document.getElementById("instructionsModal").getElementsByClassName("img-preview col-md-11 col-sm-11 col-xs-11")[0].children[0].src')
        self.download_from_url(target_link, file_name)

    def download_from_url(self, target_link: str, file_name: str):
        response = urllib.request.urlopen(target_link)
        # delete trademark from file name
        file_name = file_name.replace(u'\u00AE', '')
        with open(f'./downloaded pdfs/{file_name}.pdf', 'wb') as file:
            file.write(response.read())
        print(f'Файл {file_name}.pdf сохранен успешно.\n')

    def extract_guid(self, row: WebElement) -> str:
        extracted_attribute = row.get_attribute('onclick')
        target_guid = re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
                                extracted_attribute).group()
        return target_guid

    def wait_table_element(self):
        wd = self.app.wd
        try:
            table_element = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_plate_gr')))
        except Exception:
            table_element = None
        finally:
            return table_element



