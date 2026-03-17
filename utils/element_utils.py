import logging
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.appiumby import AppiumBy

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def safe_click(driver, element):
    """
    安全点击封装：原生点击失败时降级为坐标点击
    适配Android端content-desc含换行符等边界场景
    :param driver: Appium驱动实例
    :param element: 目标元素对象
    """
    try:
        element.click()
        logger.info(f"元素点击成功，文本：{element.text}")
    except (ElementClickInterceptedException, StaleElementReferenceException) as e:
        logger.error(f"原生点击失败：{str(e)}")
        logger.error(f"元素信息 - content-desc：{element.get_attribute('content-desc')}，文本：{element.text}")

        # 降级策略：坐标点击
        try:
            x = element.location["x"] + element.size["width"] / 2
            y = element.location["y"] + element.size["height"] / 2
            driver.tap([(x, y)], 100)
            logger.info(f"降级为坐标点击，位置：({x}, {y})")
        except Exception as de:
            logger.error(f"降级点击失败：{str(de)}")
            raise de


def click_submit_button(driver):
    """
    跨平台提交按钮定位与点击
    Android：UiAutomator定位 | iOS：Predicate定位
    :param driver: Appium驱动实例
    """
    platform = driver.capabilities.get("platformName", "").lower()

    if platform == "android":
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Submit")')
    elif platform == "ios":
        locator = (AppiumBy.IOS_PREDICATE, 'name == "Submit" OR label == "Submit"')
    else:
        raise ValueError(f"不支持的平台：{platform}")

    submit_btn = WebDriverWait(driver, 10).until(lambda d: d.find_element(*locator))
    safe_click(driver, submit_btn)