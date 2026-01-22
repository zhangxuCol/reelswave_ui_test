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
        if not self.page_actions.wait_for_element(self.locators["top_up_button"], timeout=timeout):
            raise Exception("个人中心页面加载超时或'Top UP'按钮未找到")
        self.logger.info("个人中心页面加载完成")

    def back(self):
        """返回上一页"""
        self.page.back()
        self.logger.info("执行浏览器后退操作")

    @element_wait_decorator(wait_type="clickable", timeout=20, raise_err=True)
    def get_top_up_button(self):
        """获取充值按钮"""
        self.logger.info("获取充值按钮")
        element = self.page_actions.find_element(self.locators["top_up_button"])
        if not element:
            raise Exception(f"Element not found for locator: {self.locators['top_up_button']}")
        return element

    @element_wait_decorator(wait_type="clickable", timeout=20, raise_err=True)
    def get_transaction_history_link(self):
        """获取交易历史链接"""
        self.logger.info("获取交易历史链接")
        element = self.page_actions.find_element(self.locators["transaction_history_link"])
        if not element:
            raise Exception(f"Element not found for locator: {self.locators['transaction_history_link']}")
        return element

    @element_wait_decorator(wait_type="clickable", timeout=20, raise_err=True)
    def get_my_list_and_history_link(self):
        """获取我的列表和历史记录链接"""
        self.logger.info("获取我的列表和历史记录链接")
        element = self.page_actions.find_element(self.locators["my_list_and_history_link"])
        if not element:
            raise Exception(f"Element not found for locator: {self.locators['my_list_and_history_link']}")
        return element

    @element_wait_decorator(wait_type="clickable", timeout=20, raise_err=True)
    def get_contact_us_link(self):
        """获取联系我们链接"""
        self.logger.info("获取联系我们链接")
        element = self.page_actions.find_element(self.locators["contact_us_link"])
        if not element:
            raise Exception(f"Element not found for locator: {self.locators['contact_us_link']}")
        return element

    @element_wait_decorator(wait_type="clickable", timeout=20, raise_err=True)
    def get_settings_link(self):
        """获取设置链接"""
        self.logger.info("获取设置链接")
        element = self.page_actions.find_element(self.locators["settings_link"])
        if not element:
            raise Exception(f"Element not found for locator: {self.locators['settings_link']}")
        return element
