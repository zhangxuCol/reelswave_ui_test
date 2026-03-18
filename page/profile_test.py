
"""
个人中心测试模块
"""
import pytest
from components.ProfileComponent import ProfileComponent
from utils.logger_utils import LoggerUtils
from utils.screenshot_utils import get_screenshot_utils
from config.settings import PROFILE_URL


@pytest.mark.profile
class TestProfile:
    """个人中心测试类"""

    @pytest.fixture(autouse=True)  # 使用autouse=True自动应用此fixture到所有测试用例，无需在每个测试中显式调用
    def setup(self, page):  # setup fixture方法，接收self和page两个参数
        """
        测试夹具，在每个测试方法前执行
        此夹具用于初始化测试环境，包括设置日志记录器、页面实例、个人中心组件，
        并导航到个人中心页面，确保页面加载完成
        """
        self.logger = LoggerUtils.get_default_logger()  # 获取默认日志记录器实例
        self.page = page  # 保存页面实例
        self.profile = ProfileComponent(self.page)  # 初始化个人中心组件，传入页面实例

        # 导航到个人中心页面
        self.page.get(PROFILE_URL)  # 使用页面实例导航到个人中心URL
        self.logger.info(f"导航到个人中心页面: {PROFILE_URL}")  # 记录导航信息

        # 等待页面加载完成
        try:  # 尝试等待页面加载
            self.profile.wait_for_page_load()  # 调用个人中心组件的等待页面加载方法
            self.logger.info("个人中心页面加载完成")  # 记录页面加载成功信息
            
            # 捕获截图
            screenshot_utils = get_screenshot_utils()
            screenshot_utils.take_screenshot(self.page, name="profile_page_loaded")
            
        except Exception as e:  # 捕获可能发生的异常
            self.logger.error(f"等待个人中心页面加载时出错: {str(e)}")  # 记录错误信息
            raise  # 重新抛出异常，使测试失败

    @pytest.mark.smoke
    def test_top_up_button(self):
        """测试充值按钮"""
        self.logger.info("测试充值按钮")
        top_up_button = self.profile.get_top_up_button()
        assert top_up_button is not None, "未找到充值按钮"
        self.logger.info("充值按钮存在")
        top_up_button.click()  # 点击充值按钮
        self.logger.info("成功点击充值按钮")
        self.page.wait(5)  # 等待5秒
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="top_up_page")
        
        # 返回上一页
        self.profile.click_back_button()
        self.logger.info("返回上一页")
        self.page.wait(2)  # 等待页面加载

    @pytest.mark.smoke
    def test_transaction_history_link(self):
        """测试交易历史链接"""
        self.logger.info("测试交易历史链接")
        transaction_history = self.profile.get_transaction_history_link()
        assert transaction_history is not None, "未找到交易历史链接"
        self.logger.info("交易历史链接存在")
        transaction_history.click()  # 点击交易历史链接
        self.logger.info("成功点击交易历史链接")
        self.page.wait(5)  # 等待5秒
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="transaction_history_page")
        
        # 返回上一页
        self.profile.click_back_button()
        self.logger.info("返回上一页")
        self.page.wait(2)  # 等待页面加载

    @pytest.mark.smoke
    def test_my_list_and_history_link(self):
        """测试我的列表和历史记录链接"""
        self.logger.info("测试我的列表和历史记录链接")
        my_list_and_history = self.profile.get_my_list_and_history_link()
        assert my_list_and_history is not None, "未找到我的列表和历史记录链接"
        self.logger.info("我的列表和历史记录链接存在")
        my_list_and_history.click()  # 点击我的列表和历史记录链接
        self.logger.info("成功点击我的列表和历史记录链接")
        self.page.wait(5)  # 等待5秒
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="my_list_and_history_page")
        
        # 返回上一页
        self.profile.click_back_button()
        self.logger.info("返回上一页")
        self.page.wait(2)  # 等待页面加载

    @pytest.mark.smoke
    def test_contact_us_link(self):
        """测试联系我们链接"""
        self.logger.info("测试联系我们链接")
        contact_us = self.profile.get_contact_us_link()
        assert contact_us is not None, "未找到联系我们链接"
        self.logger.info("联系我们链接存在")
        contact_us.click()  # 点击联系我们链接
        self.logger.info("成功点击联系我们链接")
        self.page.wait(5)  # 等待5秒
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="contact_us_page")
        
        # 返回上一页
        self.profile.click_back_button()
        self.logger.info("返回上一页")
        self.page.wait(2)  # 等待页面加载

    @pytest.mark.smoke
    def test_settings_link(self):
        """测试设置链接"""
        self.logger.info("测试设置链接")
        settings = self.profile.get_settings_link()
        assert settings is not None, "未找到设置链接"
        self.logger.info("设置链接存在")
        settings.click()  # 点击设置链接
        self.logger.info("成功点击设置链接")
        self.page.wait(5)  # 等待5秒
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="settings_page")
        
        # 返回上一页
        self.profile.click_back_button()
        self.logger.info("返回上一页")
        self.page.wait(2)  # 等待页面加载

    @pytest.mark.smoke
    def test_vip_status(self):
        """测试VIP状态"""
        self.logger.info("测试VIP状态")
        vip_avatar = self.profile.get_vip_avatar()
        assert vip_avatar is not None, "未找到VIP头像"
        self.logger.info("VIP头像存在")
        vip_avatar.click()  # 点击VIP头像
        self.logger.info("成功点击VIP头像")
        self.page.wait(5)  # 等待5秒
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="vip_page")
        
        # 返回上一页
        self.profile.click_back_button()
        self.logger.info("返回上一页")
        self.page.wait(2)  # 等待页面加载


