import os
import signal
import psutil
from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage
from utils.logger_utils import LoggerUtils
from config.settings import BASE_URL

def kill_processes_using_port(port):
    """
    杀死占用指定端口的进程
    :param port: 端口号
    """
    logger = LoggerUtils.get_default_logger()
    logger.info(f"检查并清理端口 {port}...")

    try:
        # 使用netstat命令查找占用该端口的进程
        import subprocess
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[1]
                    process_name = parts[0]
                    logger.info(f"发现占用端口 {port} 的进程: PID {pid}, 名称: {process_name}")

                    try:
                        # 尝试优雅地终止进程
                        os.kill(int(pid), signal.SIGTERM)
                        logger.info(f"已发送SIGTERM信号给进程 PID {pid}")

                        # 等待一段时间让进程优雅退出
                        import time
                        time.sleep(2)

                        # 检查进程是否仍在运行
                        if psutil.pid_exists(int(pid)):
                            logger.info(f"进程 PID {pid} 仍在运行，强制终止")
                            os.kill(int(pid), signal.SIGKILL)
                            logger.info(f"已发送SIGKILL信号给进程 PID {pid}")
                    except ProcessLookupError:
                        logger.info(f"进程 PID {pid} 已不存在")
                    except Exception as e:
                        logger.error(f"终止进程 PID {pid} 时出错: {e}")
        else:
            logger.info(f"端口 {port} 未被占用")
    except Exception as e:
        logger.error(f"清理端口 {port} 时出错: {e}")

def open_mobile_browser():
    logger = LoggerUtils.get_default_logger()

    # 清理可能占用的端口
    kill_processes_using_port(9223)

    co = ChromiumOptions()
    co.set_local_port(9223)

    # 设置为 iPhone Safari UA
    co.set_user_agent(
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )

    # 添加启动参数，控制窗口大小
    co.set_argument("--window-size=430,932")
    co.set_argument("--disable-blink-features=AutomationControlled")

    page = ChromiumPage(co)
    page.get(BASE_URL)
    logger.info("启动为移动端模拟模式")
    logger.info(f"User-Agent: {page.user_agent}")
    return page


def get_current_url(page):
    """
    获取当前页面的URL
    :param page: 页面对象
    :return: 当前页面的URL字符串
    """
    logger = LoggerUtils.get_default_logger()
    try:
        current_url = page.url
        logger.info(f"当前页面URL: {current_url}")
        return current_url
    except Exception as e:
        logger.error(f"获取当前页面URL时出错: {e}")
        return None


def navigate_to_url(page, url):
    """
    导航到指定的URL
    :param page: 页面对象
    :param url: 目标URL
    :return: 是否成功导航到指定URL
    """
    logger = LoggerUtils.get_default_logger()
    try:
        logger.info(f"正在导航到URL: {url}")
        page.get(url)
        logger.info(f"成功导航到URL: {url}")
        return True
    except Exception as e:
        logger.error(f"导航到URL {url} 时出错: {e}")
        return False