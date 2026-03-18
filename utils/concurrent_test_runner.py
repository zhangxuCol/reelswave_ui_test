
"""
并发测试执行器
"""
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.logger_utils import LoggerUtils
from utils.email_notifier import EmailNotifier
from config.settings import REPORT_CONFIG


class ConcurrentTestRunner:
    """并发测试执行器"""

    def __init__(self, max_workers=4):
        """
        初始化并发测试执行器
        :param max_workers: 最大并发数
        """
        self.logger = LoggerUtils.get_default_logger()
        self.max_workers = max_workers
        self.email_notifier = EmailNotifier()
        self.test_results = []
        self.lock = threading.Lock()

    def run_concurrent_tests(self, test_functions):
        """
        并发执行测试
        :param test_functions: 测试函数列表
        :return: 测试结果
        """
        try:
            start_time = time.time()
            self.logger.info(f"开始并发执行测试，并发数: {self.max_workers}")

            # 使用线程池并发执行测试
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 提交所有测试任务
                future_to_test = {
                    executor.submit(self._run_single_test, func): func 
                    for func in test_functions
                }

                # 等待所有测试完成
                for future in as_completed(future_to_test):
                    test_func = future_to_test[future]
                    try:
                        result = future.result()
                        with self.lock:
                            self.test_results.append(result)
                    except Exception as e:
                        self.logger.error(f"测试执行异常: {str(e)}")
                        with self.lock:
                            self.test_results.append({
                                'name': test_func.__name__,
                                'status': 'failed',
                                'duration': 0,
                                'screenshots': [],
                                'error': str(e)
                            })

            duration = time.time() - start_time
            self.logger.info(f"并发测试完成，总耗时: {duration:.2f}秒")

            # 报告已由ChineseHTMLReportPlugin自动生成，无需手动生成
            # 发送邮件通知时会自动查找最新的报告文件
            
            # 发送邮件通知
            self._send_email_notification(None, duration)

            return self.test_results

        except Exception as e:
            self.logger.error(f"并发执行测试失败: {str(e)}")
            return None

    def _run_single_test(self, test_func):
        """
        执行单个测试
        :param test_func: 测试函数
        :return: 测试结果
        """
        try:
            start_time = time.time()
            self.logger.info(f"开始执行测试: {test_func.__name__}")

            # 执行测试
            test_func()

            duration = time.time() - start_time
            self.logger.info(f"测试完成: {test_func.__name__}, 耗时: {duration:.2f}秒")

            return {
                'name': test_func.__name__,
                'status': 'passed',
                'duration': duration,
                'screenshots': [],
                'error': None
            }
        except Exception as e:
            duration = time.time() - start_time
            self.logger.error(f"测试失败: {test_func.__name__}, 错误: {str(e)}")

            return {
                'name': test_func.__name__,
                'status': 'failed',
                'duration': duration,
                'screenshots': [],
                'error': str(e)
            }

    def _send_email_notification(self, report_path, duration):
        """
        发送邮件通知
        :param report_path: 报告路径
        :param duration: 总耗时
        """
        try:
            from datetime import datetime
            from pathlib import Path
            
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
            self.logger.error(f"发送邮件通知失败: {str(e)}")
