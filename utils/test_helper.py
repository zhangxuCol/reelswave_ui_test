
"""
统一的测试辅助工具类
整合了截图和测试结果收集功能
"""
import os
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils
from config.settings import REPORT_CONFIG


class TestHelper:
    """测试辅助类，提供截图和测试结果收集功能"""

    def __init__(self, test_name, base_dir=None):
        """
        初始化测试辅助类
        :param test_name: 测试用例名称
        :param base_dir: 截图基础目录（可选）
        """
        self.test_name = test_name
        self.logger = LoggerUtils.get_default_logger()
        self.screenshots = []
        self.step_num = 0
        
        # 获取截图目录
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(REPORT_CONFIG.get('screenshot_dir', 'reports/screenshots'))
        
        today = datetime.now().strftime("%Y-%m-%d")
        self.screenshot_dir = self.base_dir / today / test_name
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def take_screenshot(self, page, description):
        """
        执行截图操作
        :param page: 页面对象
        :param description: 操作描述
        :return: 截图文件路径
        """
        if not REPORT_CONFIG.get('enable_screenshots', True):
            return None

        try:
            self.step_num += 1
            # 清理描述中的非法字符
            clean_desc = self._sanitize_filename(description)
            filename = f"{self.test_name}_{self.step_num:02d}_{clean_desc}.png"
            screenshot_path = self.screenshot_dir / filename

            # 使用 DrissionPage 的截图方法
            page.get_screenshot(path=str(screenshot_path))

            self.screenshots.append(str(screenshot_path))
            self.logger.info(f"截图已保存: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"截图失败: {e}")
            return None

    def get_screenshot_path(self, step_num, description):
        """
        生成截图文件路径（不执行截图）
        :param step_num: 步骤序号
        :param description: 操作描述
        :return: 截图文件完整路径
        """
        # 清理描述中的非法字符
        clean_desc = self._sanitize_filename(description)
        filename = f"{self.test_name}_{step_num:02d}_{clean_desc}.png"
        return str(self.screenshot_dir / filename)

    def _sanitize_filename(self, filename):
        """
        清理文件名中的非法字符
        :param filename: 原始文件名
        :return: 清理后的文件名
        """
        illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in illegal_chars:
            filename = filename.replace(char, '_')
        return filename

    def get_screenshots(self):
        """获取所有截图路径"""
        return self.screenshots

    def reset_step_counter(self):
        """重置步骤计数器"""
        self.step_num = 0

    def clear_screenshots(self):
        """清空截图列表"""
        self.screenshots = []
