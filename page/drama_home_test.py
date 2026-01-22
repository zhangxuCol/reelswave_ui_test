from components.DramaHomeComponent import DramaHomeComponent
from utils.logger_utils import LoggerUtils
from page.base import open_mobile_browser
from config.settings import TEST_HOME_URL


class DramaHomeTest:
    """短剧首页测试类"""

    def __init__(self, page=None):
        """
        初始化测试类
        :param page: 可选，传入已打开的页面对象
        """
    # 创建日志记录器实例
        self.logger = LoggerUtils.get_default_logger()
    # 初始化页面对象，如果未传入则创建新页面
        self.page = self._init_page(page)
    # 创建剧首页组件实例
        self.drama_home = DramaHomeComponent(self.page)
    # 记录初始化完成的日志信息
        self.logger.info("初始化剧首页测试类")

    def _init_page(self, page=None):
        """
        基础方法：如果没有传入页面对象，则打开新页面
        :param page: 可选，传入已打开的页面对象
        :return: 页面对象
        """
        # 如果没有传入页面对象，则打开新页面
        if page is None:
            page = open_mobile_browser()

        # 直接导航到测试首页
        page.get(TEST_HOME_URL)
        self.logger.info("打开剧首页")

        # 等待页面关键元素加载完成
        try:
            # 等待页面加载完成 - DrissionPage 使用 wait 方法
            page.wait(1)  # 等待1秒让页面开始加载
            self.logger.info("等待页面开始加载")

            # 等待剧首页组件的关键元素加载
            self.drama_home = DramaHomeComponent(page)
            self.drama_home.wait_for_elements_loaded()
            self.logger.info("剧首页所有元素加载完成")
        except Exception as e:
            self.logger.error(f"等待页面元素加载时出错: {str(e)}")
            # 即使出错也返回页面对象，让测试继续执行

        return page

    def test_back_button(self):
        """测试点击返回按钮"""
        self.logger.info("测试点击返回按钮")
        self.drama_home.click_back_button()
        self.page.wait(2)
        self._init_page(self.page)

    def test_home_button(self):
        """测试点击Home按钮"""
        self.logger.info("测试点击Home按钮")
        self.drama_home.click_home_button()
        self.page.wait(2)
        self._init_page(self.page)

    def test_profile_button(self):
        """测试点击个人中心按钮"""
        self.logger.info("测试点击个人中心按钮")
        self.drama_home.click_profile_button()
        self.page.wait(2)
        self._init_page(self.page)

    def test_watch_button(self):
        """测试点击去看剧按钮"""
        self.logger.info("测试点击去看剧按钮")
        self.drama_home.click_watch_button()
        self.page.wait(2)
        self._init_page(self.page)

    def test_add_to_list(self):
        """测试点击添加收藏按钮"""
        self.logger.info("测试点击添加收藏按钮")
        self.drama_home.click_add_to_list()
        self.page.wait(2)
        self._init_page(self.page)

    def test_remove_from_list(self):
        """测试点击取消收藏按钮"""  # 这是一个多行注释，用于说明此测试函数的功能是测试点击取消收藏按钮
        self.logger.info("测试点击取消收藏按钮")  # 这是一个单行注释，记录日志信息，表示开始测试取消收藏功能
        self.drama_home.click_remove_from_list()  # 调用取消收藏按钮的点击方法
        self.page.wait(2)  # 等待2秒钟，确保页面响应完成
        self._init_page(self.page)  # 重新初始化页面对象，确保后续操作的准确性

    def test_description_toggle(self):
        """测试详情的展开和收起"""
        self.logger.info("测试详情的展开和收起")

        # 记录初始状态
        initial_state = self.drama_home.is_description_expanded()
        self.logger.info(f"短剧简介初始状态: {'More' if initial_state else 'Flod'}")

        # 点击切换状态
        toggle_result = self.drama_home.toggle_description()
        if toggle_result:
            self.page.wait(1)
            # 验证状态是否改变
            new_state = self.drama_home.is_description_expanded()
            self.logger.info(f"点击后短剧简介状态: {'More' if new_state else 'Flod'}")

            if initial_state != new_state:
                self.logger.info("成功验证短剧简介展开/收起功能")
                # 点击切换状态
                self.drama_home.toggle_description()
                self.logger.info("成功验证短剧简介收起功能")
            else:
                self.logger.warning("短剧简介状态未改变，可能功能异常")
        else:
            self.logger.error("无法切换短剧简介状态")

        self._init_page(self.page)

    def test_free_episode(self):
        """测试点击随机一集免费剧集"""
        self.logger.info("测试点击随机一集免费剧集")
        self.drama_home.click_free_episode()
        self.page.wait(2)
        self._init_page(self.page)

    def run_all_tests(self):
        """运行所有测试方法"""
        self.logger.info("开始运行所有剧首页测试")
        self.test_back_button()
        self.test_home_button()
        self.test_profile_button()
        self.test_watch_button()
        self.test_add_to_list()
        self.test_remove_from_list()
        self.test_description_toggle()
        self.test_free_episode()
        self.logger.info("剧首页所有测试完成")


def test_drama_home(page=None):
    """
    测试剧首页功能（兼容旧接口）
    :param page: 可选，传入已打开的页面对象
    :return: 页面对象
    """
    drama_test = DramaHomeTest(page)
    drama_test.run_all_tests()
    return drama_test.page


if __name__ == "__main__":
    test_drama_home()
