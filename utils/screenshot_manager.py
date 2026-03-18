
"""
截图管理工具类
"""
import os
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils


class ScreenshotManager:
    """截图管理器，负责管理测试过程中的截图"""

    def __init__(self, base_dir="reports/screenshots"):
        """
        初始化截图管理器
        :param base_dir: 截图基础目录
        """
        self.base_dir = Path(base_dir)
        self.logger = LoggerUtils.get_default_logger()

    def get_screenshot_path(self, test_name, step_num, description):
        """
        生成截图文件路径
        :param test_name: 测试用例名称
        :param step_num: 步骤序号
        :param description: 操作描述
        :return: 截图文件完整路径
        """
        # 获取当前日期
        today = datetime.now().strftime("%Y-%m-%d")

        # 创建目录结构: reports/screenshots/{日期}/{用例名}/
        screenshot_dir = self.base_dir / today / test_name
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # 生成文件名: {用例名}_{步骤序号}_{操作描述}.png
        # 清理描述中的非法字符
        clean_desc = self._sanitize_filename(description)
        filename = f"{test_name}_{step_num:02d}_{clean_desc}.png"

        return screenshot_dir / filename

    def _sanitize_filename(self, filename):
        """
        清理文件名中的非法字符
        :param filename: 原始文件名
        :return: 清理后的文件名
        """
        # 替换非法字符为下划线
        illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename

    def take_screenshot(self, page, test_name, step_num, description):
        """
        执行截图操作
        :param page: 页面对象
        :param test_name: 测试用例名称
        :param step_num: 步骤序号
        :param description: 操作描述
        :return: 截图文件路径，失败返回None
        """
        try:
            screenshot_path = self.get_screenshot_path(test_name, step_num, description)

            # 使用 DrissionPage 的截图方法
            page.get_screenshot(path=str(screenshot_path))

            self.logger.info(f"截图已保存: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            return None
