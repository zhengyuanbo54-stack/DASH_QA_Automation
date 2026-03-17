from base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy


class LoginPage(BasePage):
    """
    登录页面对象
    封装登录流程所有元素定位与操作
    """
    # 跨平台定位器库
    LOCATORS = {
        "android": {
            "username_input": (AppiumBy.ID, "com.example.app:id/et_username"),
            "login_button": (AppiumBy.ID, "com.example.app:id/btn_login")
        },
        "ios": {
            "username_input": (AppiumBy.ACCESSIBILITY_ID, "usernameTextField"),
            "login_button": (AppiumBy.IOS_PREDICATE, 'name == "登录" AND type == "XCUIElementTypeButton"')
        }
    }

    def __init__(self, driver):
        super().__init__(driver)
        self.platform = self.driver.capabilities.get("platformName", "Android").lower()
        self.locators = self.LOCATORS[self.platform]

    def enter_username(self, text):
        """输入用户名"""
        input_box = self.wait_for_clickable_element(self.locators["username_input"])
        input_box.clear()
        input_box.send_keys(text)
        return self

    def tap_login_button(self):
        """点击登录按钮"""
        login_btn = self.wait_for_clickable_element(self.locators["login_button"])
        from utils.element_utils import safe_click
        safe_click(self.driver, login_btn)
        return self

    def extract_first_order_number(self):
        """
        提取订单列表中首个可见订单编号
        正则匹配"订单#12345"格式，返回纯数字编号
        :return: str 订单编号
        """
        import re
        order_locator = (AppiumBy.XPATH, "//*[contains(@text, '订单#') or contains(@name, '订单#')]")
        self.wait_for_visible_element(order_locator)

        order_text = self.driver.find_element(*order_locator).text
        match = re.search(r"订单#(\d+)", order_text)

        if match:
            return match.group(1)
        raise ValueError(f"无法从 '{order_text}' 中提取订单编号")