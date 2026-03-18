
"""
测试报告生成工具类 - 第一部分
"""
import os
import json
import shutil
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils
from config.settings import REPORT_CONFIG


class ReportGenerator:
    """测试报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        self.logger = LoggerUtils.get_default_logger()
        self.report_base_dir = Path(REPORT_CONFIG.get('base_dir', 'reports'))
        self.report_dir = self.report_base_dir / 'html'
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_allure_report(self, test_results):
        """
        生成 Allure 测试报告
        :param test_results: 测试结果数据
        :return: 报告文件路径
        """
        try:
            # 获取当前日期
            today = datetime.now().strftime("%Y-%m-%d")

            # 生成报告文件名
            report_filename = f"{today}_test_report.html"
            report_path = self.report_dir / report_filename

            # 生成 JSON 格式报告（便于二次处理）
            json_report_path = self.report_dir / f"{today}_test_report.json"
            self._generate_json_report(test_results, json_report_path)

            # 生成 HTML 格式报告
            self._generate_html_report(test_results, report_path)

            self.logger.info(f"测试报告已生成: {report_path}")
            return str(report_path)

        except Exception as e:
            self.logger.error(f"生成测试报告失败: {e}")
            return None

    def _generate_json_report(self, test_results, json_path):
        """
        生成 JSON 格式报告
        :param test_results: 测试结果数据
        :param json_path: JSON 报告文件路径
        """
        try:
            report_data = {
                'test_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_cases': len(test_results),
                'passed': sum(1 for r in test_results if r['status'] == 'passed'),
                'failed': sum(1 for r in test_results if r['status'] == 'failed'),
                'total_duration': sum(r['duration'] for r in test_results),
                'test_cases': test_results
            }

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, ensure_ascii=False, indent=2)

            self.logger.info(f"JSON 报告已生成: {json_path}")

        except Exception as e:
            self.logger.error(f"生成 JSON 报告失败: {e}")
