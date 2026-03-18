
"""
定时任务管理工具类
"""
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.logger_utils import LoggerUtils
from config.settings import SCHEDULE_CONFIG


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self):
        """初始化调度器"""
        self.logger = LoggerUtils.get_default_logger()
        self.scheduler = BackgroundScheduler()
        self.task_id = None

    def start_scheduled_test(self, test_func):
        """
        启动定时测试任务
        :param test_func: 要执行的测试函数
        """
        try:
            # 获取定时配置
            schedule_type = SCHEDULE_CONFIG.get('type', 'cron')

            if schedule_type == 'cron':
                # 使用 cron 表达式
                cron_expr = SCHEDULE_CONFIG.get('cron_expression')
                if not cron_expr:
                    raise ValueError("未配置 cron_expression")

                # 解析 cron 表达式
                parts = cron_expr.split()
                if len(parts) != 5:
                    raise ValueError("cron_expression 格式错误，应为: 分 时 日 月 周")

                minute, hour, day, month, day_of_week = parts

                # 添加定时任务
                self.scheduler.add_job(
                    func=self._wrap_test_function(test_func),
                    trigger=CronTrigger(
                        minute=minute,
                        hour=hour,
                        day=day,
                        month=month,
                        day_of_week=day_of_week
                    ),
                    id='scheduled_test',
                    name='自动化测试任务',
                    replace_existing=True
                )

                self.logger.info(f"已配置定时任务: {cron_expr}")

            elif schedule_type == 'fixed_time':
                # 使用固定时间
                fixed_time = SCHEDULE_CONFIG.get('fixed_time')
                if not fixed_time:
                    raise ValueError("未配置 fixed_time")

                # 添加一次性定时任务
                self.scheduler.add_job(
                    func=self._wrap_test_function(test_func),
                    trigger='date',
                    run_date=fixed_time,
                    id='scheduled_test',
                    name='自动化测试任务',
                    replace_existing=True
                )

                self.logger.info(f"已配置定时任务: {fixed_time}")

            else:
                raise ValueError(f"不支持的定时类型: {schedule_type}")

            # 启动调度器
            self.scheduler.start()
            self.logger.info("定时任务调度器已启动")

        except Exception as e:
            self.logger.error(f"启动定时任务失败: {e}")
            raise

    def _wrap_test_function(self, test_func):
        """
        包装测试函数，添加日志记录
        :param test_func: 原始测试函数
        :return: 包装后的函数
        """
        def wrapped():
            try:
                start_time = datetime.now()
                self.logger.info(f"定时任务开始执行: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

                # 执行测试
                test_func()

                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                self.logger.info(f"定时任务执行完成，耗时: {duration:.2f}秒")

            except Exception as e:
                self.logger.error(f"定时任务执行失败: {e}")
                # 发送错误通知
                from utils.email_notifier import EmailNotifier
                notifier = EmailNotifier()
                notifier.send_error_notification(str(e), datetime.now().strftime('%Y-%m-%d'))

        return wrapped

    def stop(self):
        """停止调度器"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown(wait=False)
                self.logger.info("定时任务调度器已停止")
        except Exception as e:
            self.logger.error(f"停止调度器失败: {e}")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.stop()
