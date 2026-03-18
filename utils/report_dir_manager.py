
"""
报告目录管理器 - 统一管理测试报告的目录结构
"""
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils
from config.settings import REPORT_CONFIG


class ReportDirManager:
    """报告目录管理器"""

    def __init__(self, report_dir=None):
        """
        初始化报告目录管理器
        :param report_dir: 报告基础目录（可选）
        """
        self.logger = LoggerUtils.get_default_logger()

        # 如果提供了report_dir，使用它作为基础目录
        if report_dir:
            self.report_base_dir = Path(report_dir)
        else:
            # 获取项目根目录
            project_root = Path(__file__).parent.parent
            self.report_base_dir = project_root / REPORT_CONFIG.get('base_dir', 'reports')

        # 使用时间戳创建报告目录
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        self.report_dir = self.report_base_dir / timestamp
        self.report_dir.mkdir(parents=True, exist_ok=True)

        # 创建截图目录
        self.screenshot_dir = self.report_dir / 'screenshots'
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"报告目录: {self.report_dir}")
        self.logger.info(f"截图目录: {self.screenshot_dir}")

    def get_report_dir(self):
        """
        获取报告目录
        :return: 报告目录路径
        """
        return self.report_dir

    def get_screenshot_dir(self):
        """
        获取截图目录
        :return: 截图目录路径
        """
        return self.screenshot_dir

    def get_report_path(self, filename='test_report.html'):
        """
        获取报告文件路径
        :param filename: 报告文件名
        :return: 报告文件路径
        """
        return self.report_dir / filename

    def get_screenshot_path(self, filename):
        """
        获取截图文件路径
        :param filename: 截图文件名
        :return: 截图文件路径
        """
        return self.screenshot_dir / filename


# 全局报告目录管理器实例
_report_dir_manager = None


def get_report_dir_manager(report_dir=None):
    """
    获取报告目录管理器实例
    :param report_dir: 报告基础目录（可选）
    :return: ReportDirManager 实例
    """
    global _report_dir_manager
    if _report_dir_manager is None:
        _report_dir_manager = ReportDirManager(report_dir)
    return _report_dir_manager
