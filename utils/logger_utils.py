import logging
import os
from datetime import datetime

class LoggerUtils:
    """日志工具类，提供统一的日志记录方法"""

    _loggers = {}

    @classmethod
    def get_logger(cls, name=None, log_file=None, level=logging.INFO):
        """
        获取日志记录器
        :param name: 日志记录器名称，默认使用调用模块名
        :param log_file: 日志文件路径，默认不写入文件
        :param level: 日志级别
        :return: 日志记录器实例
        """
        if name is None:
            # 获取调用者的模块名
            import inspect
            frame = inspect.currentframe().f_back
            name = frame.f_globals.get('__name__', 'default')

        # 如果已存在相同名称的日志记录器，直接返回
        if name in cls._loggers:
            return cls._loggers[name]

        # 创建新的日志记录器
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 避免重复添加处理器
        if not logger.handlers:
            # 创建格式化器
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # 添加控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # 如果指定了日志文件，添加文件处理器
            if log_file:
                # 确保日志目录存在
                os.makedirs(os.path.dirname(log_file), exist_ok=True)

                # 文件处理器，每天一个日志文件
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        # 缓存日志记录器
        cls._loggers[name] = logger
        return logger

    @classmethod
    def get_default_logger(cls, name=None):
        """
        获取默认日志记录器，使用默认日志文件
        :param name: 日志记录器名称
        :return: 日志记录器实例
        """
        # 创建默认日志文件路径
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 使用当前日期作为日志文件名
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f'application_{today}.log')

        return cls.get_logger(name, log_file)
