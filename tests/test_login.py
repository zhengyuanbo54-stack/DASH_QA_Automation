def test_login_flow(appium_driver):
    """登录流程测试用例"""
    from pages.login_page import LoginPage

    login_page = LoginPage(appium_driver)
    login_page.enter_username("test_user_123").tap_login_button()
    print("登录流程测试执行成功")


def test_extract_order(appium_driver):
    """订单编号提取功能测试"""
    from pages.login_page import LoginPage

    login_page = LoginPage(appium_driver)
    login_page.enter_username("test_user").tap_login_button()

    order_num = login_page.extract_first_order_number()
    print(f"提取到的订单编号：{order_num}")
    assert len(order_num) > 0, "订单编号提取失败"