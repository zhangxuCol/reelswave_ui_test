"""
基础测试类 - 添加截图支持
"""
from utils.screenshot_utils import get_screenshot_utils


class ScreenshotMixin:
    """截图混入类，为测试类添加截图功能"""

    def take_screenshot(self, name=None):
        """
        捕获屏幕截图
        :param name: 截图名称
        :return: 截图路径
        """
        if hasattr(self, 'page') and self.page:
            screenshot_utils = get_screenshot_utils()
            return screenshot_utils.take_screenshot(self.page, name)
        return None

    def take_screenshot_after_action(self, action_name):
        """
        在执行操作后捕获截图
        :param action_name: 操作名称
        :return: 截图路径
        """
        return self.take_screenshot(name=f"after_{action_name}")
