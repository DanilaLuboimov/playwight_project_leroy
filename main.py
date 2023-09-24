from playwright.sync_api import sync_playwright
from selenium import webdriver

user_data_dir = r"C:\Users\Hiazmond\AppData\Local\Google\Chrome\User Data"

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


with sync_playwright() as playwright:
    driver = playwright.chromium
    browser = driver.launch(headless=False, args=[
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
    page = browser.new_page()
    # page.add_init_script("""
    #         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
    #         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
    #         delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
    #     """)

    url = 'https://spb.leroymerlin.ru/catalogue/'
    # url = 'https://www.auchan.ru/'
    # url = 'https://playwright.dev/python/docs/handles'
    page.goto(url)
    page.wait_for_selector(LEROY_CONST["xpath_category"])

    categories = page.locator('//li[@data-qa="category-item"]').all()

    for category in categories:
    # sub categories
        print(category.locator('//a[@data-qa="subtitle"]').inner_text())
        sub_categories = category.locator('//ul[@data-qa="sub-list"]/a').all()
        print([i.inner_text() for i in sub_categories])
    browser.close()
