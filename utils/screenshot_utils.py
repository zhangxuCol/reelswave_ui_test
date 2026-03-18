"""
截图工具类 - 用于在测试过程中捕获屏幕截图
"""
import os
import time
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils


class ScreenshotUtils:
    """截图工具类"""

    def __init__(self, report_dir=None):
        self.logger = LoggerUtils.get_default_logger()
        # 使用ReportDirManager管理报告目录
        from utils.report_dir_manager import get_report_dir_manager
        self.dir_manager = get_report_dir_manager(report_dir)
        self.screenshot_dir = self.dir_manager.get_screenshot_dir()
        self._screenshots = []
        self.logger.info(f"截图目录: {self.screenshot_dir}")

    def take_screenshot(self, page, name=None):
        """
        捕获屏幕截图
        :param page: 页面对象 (DrissionPage)
        :param name: 截图名称（可选）
        :return: 截图文件路径
        """
        try:
            # 生成截图文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if name:
                filename = f"{timestamp}_{name}.png"
            else:
                filename = f"{timestamp}.png"

            screenshot_path = self.screenshot_dir / filename

            # 捕获截图
            page.get_screenshot(str(screenshot_path))

            self.logger.info(f"截图已保存: {screenshot_path}")
            self._screenshots.append(str(screenshot_path))

            return str(screenshot_path)

        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}")
            return None

    def take_screenshot_with_delay(self, page, name=None, delay=1):
        """
        延迟后捕获屏幕截图
        :param page: 页面对象
        :param name: 截图名称
        :param delay: 延迟时间（秒）
        :return: 截图文件路径
        """
        time.sleep(delay)
        return self.take_screenshot(page, name)

    def get_screenshots(self):
        """
        获取所有截图路径
        :return: 截图路径列表
        """
        return self._screenshots

    def clear_screenshots(self):
        """
        清空截图记录
        """
        self._screenshots = []

    def clean_old_screenshots(self, days=7):
        """
        清理旧的截图文件
        :param days: 保留天数
        """
        try:
            current_time = time.time()
            for file in self.screenshot_dir.glob('*.png'):
                if (current_time - file.stat().st_mtime) > (days * 86400):
                    file.unlink()
                    self.logger.info(f"删除旧截图: {file}")
        except Exception as e:
            self.logger.error(f"清理旧截图失败: {str(e)}")


# 全局截图工具实例
_screenshot_utils = None


def get_screenshot_utils():
    """
    获取截图工具实例
    :return: ScreenshotUtils 实例
    """
    global _screenshot_utils
    if _screenshot_utils is None:
        _screenshot_utils = ScreenshotUtils()
    return _screenshot_utils
