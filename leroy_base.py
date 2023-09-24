import time

from scrapy import Request, Spider
from scrapy.http.response.html import HtmlResponse

from core.db_utils import create_db_objects
from core.utils import (get_pagintaion, get_price,
                        get_random_user_agent)
from db.connect import get_session
from db.tables import leroy_products
from scrapy import Request, Spider
from src.parser.settings import LEROY_CONST

import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class LeroySpiderBase(Spider):

    name = 'leroy'
    allowed_domains = ['spb.leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/']

    slices = None

    def __init__(self):
        self.options = uc.ChromeOptions()
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--disable-application-cache')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-setuid-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument(f'User-Agent="{get_random_user_agent()}"')

        self.driver = uc.Chrome(
            options=self.options,
            user_multi_procs=True,
        )

        time.sleep(10)
        self.db_session = next(get_session())

        
    def __get_categories_urls(self, response: HtmlResponse) -> list[str]:
        """
        """
        categories = response.xpath(
            LEROY_CONST['xpath_category']).getall()
        return categories
    
    def __get_pagination_amount(self, response: HtmlResponse) -> int:
        """
        """
        return get_pagintaion(response, LEROY_CONST)

    def start_requests(self) -> None:
        """Начало запросов."""

        self.driver.get('https://leroymerlin.ru/catalogue/')

        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, LEROY_CONST['xpath_category'])
                )
            )
        categories = self.driver.find_elements(
            By.XPATH, LEROY_CONST['xpath_category'])
        categories_urls = [
            category.get_attribute('href') for category in categories
        ]
        # Разделение категорий через срезы
        categories_urls = (categories_urls[self.slices[0]],) if len(self.slices) == 1 else categories_urls[self.slices[0]:self.slices[1]]
        for url in categories_urls:
            print(categories_urls)
            self.driver.delete_all_cookies()
            self.driver.get(url)
            time.sleep(5)

            counter = 1
            pagination = int(self.driver.find_element(
                By.XPATH, LEROY_CONST['xpath_pagination']).text)

            while counter != pagination:

                product_list = []
                data_list = self.driver.find_elements(
                    By.XPATH, LEROY_CONST['xpath_data_list'])

                for element in data_list:
                        
                    product_name = element.find_element(
                        By.XPATH, LEROY_CONST['xpath_name']).text
                    product_category = self.driver.find_element(
                        By.XPATH, LEROY_CONST['xpath_category_name']).text

                    try:
                        product_price = element.find_element(
                            By.XPATH, LEROY_CONST['xpath_price']).text
                        product_price = get_price(product_price)
                    except Exception:
                        try:
                            product_price = element.find_element(
                                By.XPATH, LEROY_CONST['xpath_best_price']).text
                            product_price = get_price(product_price)
                        except Exception:
                            product_price = None

                    try:
                        product_measurement = element.find_element(
                            By.XPATH, LEROY_CONST['xpath_measurement']).text
                    except Exception:
                        try:
                            product_measurement = element.find_element(
                                By.XPATH, LEROY_CONST['xpath_best_measurement']).text
                        except Exception:
                            product_measurement = None
                            
                    product_url = element.find_element(
                        By.XPATH, LEROY_CONST['xpath_url']).get_attribute('href') 
                        
                    product = {
                        'name': product_name,
                        'category': product_category,
                        'price': product_price,
                        'currency': 'Руб.',
                        'measurement': product_measurement,
                            'url': product_url,
                    }
                    product_list.append(product)

                create_db_objects(leroy_products, product_list, self.db_session)

                try:
                    next_page_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, LEROY_CONST['xpath_next_page'])
                            )
                        )
                    next_page_button.click()
                except Exception:
                    break
                
                counter += 1
                time.sleep(6)


        self.driver.quit()
            


fetch("https://spb.leroymerlin.ru/catalogue/vodosnabzhenie/?page=4", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,ru;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "uid_experiment=3c0dadd6-b942-4480-886a-0eb8e5864b99; cookie_accepted=true; _ym_uid=1695219089592472816; _ym_d=1695219089; tmr_lvid=c857326cd88021778e101473cdbcc355; tmr_lvidTS=1695219089280; aplaut_distinct_id=wUddQpVY1U6o; iap.uid=4f706298aebd4a3b8c864e7c94432fb3; uxs_uid=98295640-57bf-11ee-8879-a7b7365292a2; adrcid=APpLLvlilQhY1JoVzSWlXwg; sawOPH=true; GACookieStorage=GA1.2.1165048839.1695219089; _ym_isad=2; adrdel=1; _ym_visorc=b; _gid=GA1.2.369233556.1695387718; st_uid=2a29a55390b5b13785aebb1dae2e5379; ___dmpkit___=3e31cbc2-d0cf-4bee-8446-276f03e35021; _showSberPay=true; _slfs=1695388071536; aplaut_distinct_id=wUddQpVY1U6o; _slid=650d91a75a3b7f401c0ec606; _slsession=B30B2697-E800-4A67-8A9F-DE4729CB4C44; _sl_user_has_affinity=false; _slfreq=64774d714d117a0d260055a8%3A64774d714d117a0d260055ac%3A1695395273; DY_SS_CART_SYNC_NECESSARY=false; _slid_server=650d91a75a3b7f401c0ec606; pageExperiment=dummy_store_list_aa_test:A+dummy_catalogue_aa_test:B; qrator_jsid=1695387709.319.obLGvvbKubD6ahOM-5gdo8mepekhn3gqdh1ho2rjftf05nn9i; X-API-Experiments-sub=B; _regionID=506; _gat_UA-20946020-1=1; _ga_Y706PSX1XZ=GS1.1.1695388607.2.1.1695389524.0.0.0; _spx=eyJpZCI6IjI5ODBiN2IyLTcyMWUtNGQxNy1hYzY0LWRjZTMyMTE4MmE2ZCIsInNvdXJjZSI6IiIsImZpeGVkIjp7InN0YWNrIjpbNDIyODExMDA5LDAsMCwwLC05MTc1OTYzMTVdfX0%3D; _ga=GA1.2.1165048839.1695219089; tmr_detect=0%7C1695389530301; _ga_Z72HLV7H6T=GS1.1.1695387711.2.1.1695389531.0.0.0"
  },
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET"
})