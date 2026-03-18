from utils.page_actions import PageActions
from utils.logger_utils import LoggerUtils
from config.locators import PROFILE_PAGE
from utils.decorators import element_wait_decorator


class ProfileComponent:
    """个人中心页面组件类"""

    def __init__(self, page):
        """
        初始化个人中心页面组件
        :param page: 页面对象
        """
        self.page = page
        self.page_actions = PageActions(page)
        self.logger = LoggerUtils.get_default_logger()
        self.locators = PROFILE_PAGE
        self.logger.info("初始化个人中心页面组件")

    def wait_for_page_load(self, timeout=20):
        """等待个人中心页面加载完成"""
        self.logger.info("等待个人中心页面加载完成...")
        locator = self.locators["top_up_button"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception("个人中心页面加载超时或'Top UP'按钮未找到")
        self.logger.info("个人中心页面加载完成")

    def back(self):
        """返回上一页"""
        self.page.back()
        self.logger.info("执行浏览器后退操作")

    def get_back_button(self):
        """获取返回按钮"""
        self.logger.info("获取返回按钮")
        self.logger.info(f"当前页面URL: {self.page.url}")

        # 尝试多个定位器
        locator = self.locators["profile_back_button"]

        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if element:
            self.logger.info(f"成功找到元素，使用定位器: {locator}")
            return element

        if not element:
            raise Exception(f"未找到返回按钮，尝试了以下定位器: {locator}")


    def click_back_button(self):
        """点击返回按钮"""
        self.logger.info("点击返回按钮")
        back_button = self.get_back_button()
        back_button.click()
        self.logger.info("成功点击返回按钮")

    def get_top_up_button(self):
        """获取充值按钮"""
        self.logger.info("获取充值按钮")
        locator = self.locators["top_up_button"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element

    def get_transaction_history_link(self):
        """获取交易历史链接"""
        self.logger.info("获取交易历史链接")
        locator = self.locators["transaction_history"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element

    def get_my_list_and_history_link(self):
        """获取我的列表和历史记录链接"""
        self.logger.info("获取我的列表和历史记录链接")
        locator = self.locators["my_list_and_history_link"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element

    def get_contact_us_link(self):
        """获取联系我们链接"""
        self.logger.info("获取联系我们链接")
        locator = self.locators["contact_us_link"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element

    def get_settings_link(self):
        """获取设置链接"""
        self.logger.info("获取设置链接")
        locator = self.locators["settings_link"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element

    def get_vip_avatar(self):
        """获取VIP头像"""
        self.logger.info("获取VIP头像")
        locator = self.locators["vip_avatar"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element
