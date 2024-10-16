from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import geckodriver_autoinstaller
import logging
logging.basicConfig(level=logging.DEBUG)


ITEMS = [
    {"item_id": "title", "mode": By.ID, "selector": "ad-title", "parameter": "text"},
    {
        "item_id": "price",
        "mode": By.CSS_SELECTOR,
        "selector": 'span[data-testid="prime-price"]',
        "parameter": "text",
        "getter": lambda x: int(x.split(" ")[0].replace(".", "")),
    },
    {
        "item_id": "image_url",
        "mode": By.CSS_SELECTOR,
        "selector": "#gallery-img-0 > img",
        "parameter": "src",
    },
]


def get_techical_data(browser):
    technical_data_elements = browser.find_elements(
        By.CSS_SELECTOR, "#td-box .u-margin-bottom-9"
    )

    technical_data = {}

    for elem in technical_data_elements:
        cols = elem.find_elements(By.TAG_NAME, "div")
        if len(cols) == 0:
            continue
        technical_data[cols[0].find_element(By.TAG_NAME, "strong").text] = cols[1].text

    return technical_data


def get_features(browser):
    features_elems = browser.find_elements(By.CSS_SELECTOR, "#features .g-row .g-col-6")
    features = [
        elem.find_element(By.CSS_SELECTOR, ".bullet-list p").text
        for elem in features_elems
    ]
    return features


def button_click(browser, by, selector):
    browser.find_element(by, selector).click()


def browser_init():
    firefoxdriver_bin = "/usr/local/bin/geckodriver"
    options = Options()
    options.binary_location = "/usr/bin/firefox/firefox"
    options.add_argument("--headless")
    options.add_argument("--incognito")
    service = Service(executable_path=firefoxdriver_bin, service_args=['--log', 'debug'], log_output="gecko.log")
    browser = webdriver.Firefox(options=options, service=service)
    browser.delete_all_cookies()

    return browser


def parse_by_link(link):
    browser = browser_init()

    browser.get(link)

    wait = WebDriverWait(browser, 15)

    errors = [NoSuchElementException, ElementNotInteractableException]
    wait.until(
        lambda _: browser.find_element(
            By.XPATH, '//button[text()="Einverstanden"]'
        ).is_displayed()
    )

    button_click(browser, By.XPATH, '//button[text()="Einverstanden"]')

    car = {}

    for item in ITEMS:
        elem = browser.find_element(item["mode"], item["selector"])
        if item["parameter"] == "text":
            if "getter" in item:
                car[item["item_id"]] = item["getter"](elem.text)
            else:
                car[item["item_id"]] = elem.text
        else:
            car[item["item_id"]] = elem.get_attribute(item["parameter"])

    button_click(browser, By.XPATH, '//a[text()="Alles anzeigen"]')

    car["technical_data"] = get_techical_data(browser)

    button_click(browser, By.XPATH, '//a[text()="Alles anzeigen"]')

    car["equipment"] = get_features(browser)

    browser.quit()

    return car


def parse_price(link):
    print("init")
    browser = browser_init()
    print("init done")
    wait = WebDriverWait(browser, 1)

    print("waiting...")
    browser.get(link)
    print("waiting done")

    try:
        price = browser.find_element(By.CSS_SELECTOR, ".header-price-box")
    except NoSuchElementException:
        browser.quit()
        return -1

    price = int(price.text.split("€")[0].replace(" ", "")) * 102
    browser.quit()

    return price

if __name__ == '__main__':
    parse_price('https://www.mobile.de/ru/%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C/Volkswagen-Golf-VII-Vari.-2.0D-GTD-DSG-NAVI/vhc:car/pg:vipcar/405789074.html')

