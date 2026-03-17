from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """
    页面对象模型基类
    封装所有页面通用的等待与元素操作方法
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def wait_for_clickable_element(self, locator, timeout=15):
        """
        显式等待元素可点击
        :param locator: 定位器元组 (By, 定位值)
        :param timeout: 超时时间(秒)
        :return: WebElement元素对象
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_visible_element(self, locator, timeout=15):
        """显式等待元素可见"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))