
"""
测试执行器
"""
import time
import subprocess
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils
from utils.email_notifier import EmailNotifier
from config.settings import REPORT_CONFIG, EMAIL_CONFIG


class TestRunner:
    """测试执行器，负责运行测试并生成报告"""

    def __init__(self):
        """初始化测试执行器"""
        self.logger = LoggerUtils.get_default_logger()
        self.email_notifier = EmailNotifier()
        self.test_results = []

    def run_tests(self, test_path=None, markers=None):
        """
        运行测试
        :param test_path: 测试文件路径（可选）
        :param markers: pytest标记（可选）
        :return: 测试结果
        """
        try:
            start_time = time.time()
            self.logger.info("开始执行测试...")

            # 构建 pytest 命令
            cmd = ['pytest']

            # 添加测试路径
            if test_path:
                cmd.append(test_path)

            # 添加标记
            if markers:
                for marker in markers:
                    cmd.extend(['-m', marker])

            # 添加其他参数
            cmd.extend([
                '-v',  # 详细输出
                '--tb=short'  # 简短的错误信息
            ])

            self.logger.info("执行命令: " + ' '.join(cmd))

            # 执行测试
            result = subprocess.run(cmd, capture_output=True, text=True)

            # 解析测试结果
            duration = time.time() - start_time
            self._parse_test_results(result.stdout, result.stderr, duration)

            # 报告已由ChineseHTMLReportPlugin自动生成，无需手动生成
            # 发送邮件通知时会自动查找最新的报告文件
            
            # 发送邮件通知
            self._send_email_notification(None, duration)

            return self.test_results

        except Exception as e:
            self.logger.error("执行测试失败: " + str(e))
            return None

    def _parse_test_results(self, stdout, stderr, duration):
        """
        解析测试结果
        :param stdout: 标准输出
        :param stderr: 标准错误
        :param duration: 执行耗时
        """
        # 简单解析 pytest 输出
        lines = stdout.split('\n')
        for line in lines:
            if '::test_' in line and 'PASSED' in line:
                test_name = line.split('::')[-1].split()[0]
                self.test_results.append({
                    'name': test_name,
                    'status': 'passed',
                    'duration': duration / len(self.test_results) if self.test_results else duration,
                    'screenshots': [],
                    'error': None
                })
            elif '::test_' in line and 'FAILED' in line:
                test_name = line.split('::')[-1].split()[0]
                self.test_results.append({
                    'name': test_name,
                    'status': 'failed',
                    'duration': duration / len(self.test_results) if self.test_results else duration,
                    'screenshots': [],
                    'error': stderr
                })

    def _send_email_notification(self, report_path, duration):
        """
        发送邮件通知
        :param report_path: 报告路径
        :param duration: 总耗时
        """
        try:
            # 查找最新的报告文件
            report_dir = Path(REPORT_CONFIG['base_dir'])
            report_files = list(report_dir.glob('report_*.html'))
            if report_files:
                # 按修改时间排序，获取最新的报告
                latest_report = max(report_files, key=lambda f: f.stat().st_mtime)
                report_path = str(latest_report)
                self.logger.info(f"使用最新报告: {report_path}")
            
            total_cases = len(self.test_results)
            passed = sum(1 for r in self.test_results if r['status'] == 'passed')
            failed = sum(1 for r in self.test_results if r['status'] == 'failed')

            self.email_notifier.send_test_report(
                test_date=datetime.now().strftime('%Y-%m-%d'),
                total_cases=total_cases,
                passed=passed,
                failed=failed,
                report_path=report_path,
                total_duration=duration
            )
        except Exception as e:
            self.logger.error("发送邮件通知失败: " + str(e))
