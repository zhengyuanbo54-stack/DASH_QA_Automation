import pytest
import yaml
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def load_config():
    """加载yaml配置文件"""
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = load_config()


@pytest.fixture(scope="session")
def appium_driver(request):
    """
    会话级Appium驱动夹具
    单会话仅初始化一次，会话结束自动销毁
    :param request: pytest request对象
    :return: Appium驱动实例
    """
    platform = request.config.getoption("--platform", default="android")

    if platform == "android":
        caps = config["android"]
        options = UiAutomator2Options().load_capabilities(caps)
    elif platform == "ios":
        caps = config.get("ios", {})
        options = XCUITestOptions().load_capabilities(caps)
    else:
        raise ValueError(f"不支持的平台：{platform}")

    driver = webdriver.Remote(config["common"]["appium_server"], options=options)

    def driver_quit():
        driver.quit()

    request.addfinalizer(driver_quit)

    return driver


def pytest_addoption(parser):
    """添加平台选择命令行参数"""
    parser.addoption("--platform", action="store", default="android", help="测试平台：android/ios")