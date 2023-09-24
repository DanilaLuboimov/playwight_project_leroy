import asyncio
from playwright.async_api import async_playwright

LEROY_CONST = {
    'site': 'leroy',
    'xpath_data_list': '//div[@data-qa-product]',
    'xpath_category': '//a[@data-qa="subtitle"]',
    'xpath_category_name': '//h1',
    'xpath_sub_category': '',
    'xpath_sub_sub_category': '',
    'xpath_pagination': '//div[@data-qa-pagination]/div[2]/a/span',
    'xpath_next_page': '//a[@data-qa-pagination-item="right"]',
    'xpath_name': './/a[@data-qa="product-name"]/span/span',
    'xpath_price': './/div[@data-qa="product-primary-price"]/span[1]',
    'xpath_discount_price': './/span[@data-qa="new-price-main"]',
    'xpath_best_price': './/div[@data-qa="product-best-price"]/div[2]/div/span[1]',
    'xpath_cart_price': '',
    'xpath_measurement': './/div[@data-qa="product-primary-price"]/span[3]',
    'xpath_best_easurement': './/div[@data-qa="product-best-price"]/div[2]/div/span[2]',
    'xpath_url': './/a',
    'page_items_amount': 25,
}


async def main():
    async with async_playwright() as playwright:
        driver = playwright.chromium
        browser = await driver.launch(headless=False, args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--disable-application-cache",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        ])

        # browser = playwright.chromium.launch_persistent_context(
        #     user_data_dir,
        #     headless=False,
        #     args=[
        #         "--disable-blink-features=AutomationControlled",
        #         "--disable-extensions",
        #         "--disable-application-cache",
        #         "--no-sandbox",
        #         "--disable-setuid-sandbox",
        #         "--disable-dev-shm-usage",
        #     ]
        # )
        # page = browser.new_page(extra_http_headers={
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"
        # })
        page = await browser.new_page()
        await page.add_init_script("""
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """)
        main_url = 'https://spb.leroymerlin.ru'
        url = 'https://spb.leroymerlin.ru/catalogue/'
        await page.goto(url)
        await page.wait_for_selector(LEROY_CONST["xpath_category"])

        categories = await page.locator('//li[@data-qa="category-item"]').all()

        for category in categories[:1]:
            # sub categories
            print(await category.locator('//a[@data-qa="subtitle"]').inner_text())
            sub_categories = await category.locator('//ul[@data-qa="sub-list"]/a').all()
            print([await i.inner_text() for i in sub_categories])
            for sub_cat in sub_categories[:5]:
                sub_href = await sub_cat.get_attribute("href")
                # print(sub_href)
                sub_page = await browser.new_page()
                await sub_page.add_init_script("""
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                            """)
                await sub_page.goto(main_url + sub_href)
                await page.wait_for_timeout(10000)
        await browser.close()


asyncio.run(main())
