from Data import data4
from Locators import locator4
import pytest

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



# Explicit Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:


    def __init__(self):
        # Initializes the WebDriver and WebDriverWait
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 30)


    def boot(self):
        """
        This method is to open up the firefox browser with the URL and makes the browser to go fullscreen.
        """

        self.driver.get(data4.Webdata().url)
        self.driver.maximize_window()



    def enterText(self, locator, textValue):
        element = self.wait.until(EC.visibility_of_element_located((By.NAME, locator)))
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(textValue)

    def clickButton(self, locator):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, locator))).click()


    def login(self, username, password):
        try:


        # Username = 2
        # Password = 3
        # Test Results = 7
        # Rows - 2 to End

            self.enterText(locator4.WebLocators().usernameLocator, username)
            self.enterText(locator4.WebLocators().passwordLocator, password)
            self.clickButton(locator4.WebLocators().buttonLocator)
            return self.driver.current_url


        except Exception as e:
            print("Error", e)


    def logout(self):
        self.clickButton(locator4.WebLocators().topRightLocator)
        self.clickButton(locator4.WebLocators().logoutButtonLocator)
        self.driver.quit()

    def quit(self):
        self.driver.quit()

@pytest.fixture
def login_page():
        page = LoginPage()
        page.boot()
        yield page
        page.quit()

def test_login(login_page):
    for row in range(2, data4.Webdata().rowCount() + 1):
        username = data4.Webdata().readData(row, 2)
        password = data4.Webdata().readData(row, 3)
        url = login_page.login(username, password)

        if url == data4.Webdata().dashboardURL:
            assert ("Successfully Logged in")
            data4.Webdata().writeData(row, 7, "PASSED")
        else:
            assert("Login unsuccessful")
            data4.Webdata().writeData(row, 7, "FAILED")































