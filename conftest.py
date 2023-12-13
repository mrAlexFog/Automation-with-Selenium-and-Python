import pytest
from selenium import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default="chrome",
                     help="Choose browser: chrome or firefox")
    parser.addoption('--language', action='store', default=None,
                     help="Choose from langs en/ru/fr/...")


@pytest.fixture(scope="function")
def browser(request):

    browser_name = request.config.getoption("browser_name")
    language = request.config.getoption("language")
    browser = None

    if browser_name == "chrome":
        if language != None:
            print("\nstart chrome browser for test..")
            options = ChromeOptions()
            options.add_experimental_option('prefs', {'intl.accept_languages': language})
            browser = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        else:
            raise pytest.UsageError("--language should be en/ru/fr/...")
    elif browser_name == "firefox":
        if language != None:
            print("\nstart firefox browser for test..")
            options = FirefoxOptions()
            options.set_preference("intl.accept_languages", language)
            browser = webdriver.Firefox(options=options, service=FirefoxService(GeckoDriverManager().install()))
        else:
            raise pytest.UsageError("--language should be en/ru/fr/...")
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    browser.maximize_window()
    yield browser
    print("\nquit browser..")
    browser.quit()
