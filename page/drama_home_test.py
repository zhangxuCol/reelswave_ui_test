"""
首页测试模块
"""
import pytest
from components.DramaHomeComponent import DramaHomeComponent
from utils.logger_utils import LoggerUtils
from utils.screenshot_mixin import ScreenshotMixin
from config.settings import TEST_HOME_URL


@pytest.mark.drama_home
class TestDramaHome(ScreenshotMixin):
    """短剧首页测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, drama_home_page):
        """
        测试夹具，在每个测试方法前执行
        """
        self.logger = LoggerUtils.get_default_logger()
        self.page = drama_home_page
        self.drama_home = DramaHomeComponent(self.page)

        # 导航到剧首页
        self.page.get(TEST_HOME_URL)
        self.logger.info(f"导航到首页: {TEST_HOME_URL}")

        # 等待页面关键元素加载完成
        try:
            self.drama_home.wait_for_elements_loaded()
            self.logger.info("剧首页所有元素加载完成")
            # 页面加载完成后截图
            self.take_screenshot(name="page_loaded")
        except Exception as e:
            self.logger.error(f"等待页面元素加载时出错: {str(e)}")

    @pytest.mark.smoke
    def test_back_button(self):
        """测试点击返回按钮"""
        self.logger.info("测试点击返回按钮")
        result = self.drama_home.click_back_button()
        # 操作完成后截图
        self.take_screenshot(name="after_click_back")
        assert result, "点击返回按钮失败"

    @pytest.mark.smoke
    def test_home_button(self):
        """测试点击Home按钮"""
        self.logger.info("测试点击Home按钮")
        result = self.drama_home.click_home_button()
        self.take_screenshot(name="after_click_home")
        assert result, "点击Home按钮失败"

    @pytest.mark.smoke
    def test_profile_button(self):
        """测试点击个人中心按钮"""
        self.logger.info("测试点击个人中心按钮")
        result = self.drama_home.click_profile_button()
        self.take_screenshot(name="after_click_profile")
        assert result, "点击个人中心按钮失败"

    @pytest.mark.smoke
    def test_watch_button(self):
        """测试点击去看剧按钮"""
        self.logger.info("测试点击去看剧按钮")
        result = self.drama_home.click_watch_button()
        self.take_screenshot(name="after_click_watch")
        assert result, "点击去看剧按钮失败"

    @pytest.mark.regression
    def test_add_to_list(self):
        """测试点击添加收藏按钮"""
        self.logger.info("测试点击添加收藏按钮")
        result = self.drama_home.click_add_to_list()
        self.take_screenshot(name="after_add_to_list")
        assert result, "点击添加收藏按钮失败"

    @pytest.mark.regression
    def test_remove_from_list(self):
        """测试点击取消收藏按钮"""
        self.logger.info("测试点击取消收藏按钮")
        result = self.drama_home.click_remove_from_list()
        self.take_screenshot(name="after_remove_from_list")
        assert result, "点击取消收藏按钮失败"

    @pytest.mark.regression
    def test_description_toggle(self):
        """测试详情的展开和收起"""
        self.logger.info("测试详情的展开和收起")

        # 记录初始状态
        initial_state = self.drama_home.is_description_expanded()
        self.logger.info(f"短剧简介初始状态: {'More' if initial_state else 'Flod'}")
        self.take_screenshot(name="description_initial")

        # 点击切换状态
        toggle_result = self.drama_home.toggle_description()
        self.take_screenshot(name="after_toggle_description")
        assert toggle_result, "无法切换短剧简介状态"

        # 验证状态是否改变
        new_state = self.drama_home.is_description_expanded()
        self.logger.info(f"点击后短剧简介状态: {'More' if new_state else 'Flod'}")
        assert initial_state != new_state, "短剧简介状态未改变，可能功能异常"

        # 点击切换回原始状态
        self.drama_home.toggle_description()
        self.take_screenshot(name="description_toggled_back")
        self.logger.info("成功验证短剧简介收起功能")

    @pytest.mark.regression
    def test_free_episode(self):
        """测试点击随机一集免费剧集"""
        self.logger.info("测试点击随机一集免费剧集")
        result = self.drama_home.click_free_episode()
        self.take_screenshot(name="after_click_free_episode")
        assert result, "点击免费剧集失败"
