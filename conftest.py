"""
pytest 配置文件，提供测试夹具（fixtures）
"""
import pytest
import os
from datetime import datetime
from DrissionPage._pages.chromium_page import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions
from page.base import kill_processes_using_port
from utils.screenshot_utils import get_screenshot_utils
from utils.pytest_html_plugin import ChineseHTMLReportPlugin


# 注册中文报告插件
def pytest_configure(config):
    """pytest 配置钩子，注册自定义插件"""
    # 只在主进程中注册插件，避免并发时生成多个报告
    if hasattr(config, 'workerinput') is False:
        config.pluginmanager.register(ChineseHTMLReportPlugin(config), "chinese_html_report")
        
        # 初始化报告目录管理器
        from utils.report_dir_manager import get_report_dir_manager
        from config.settings import REPORT_CONFIG
        
        report_base_dir = REPORT_CONFIG.get('base_dir', 'reports')
        get_report_dir_manager(report_dir=report_base_dir)


# 全局变量存储浏览器实例（用于非并发模式）
_browser_instance = None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_setup(item):
    """
    在每个测试开始前清空截图记录
    注意：这个hook在fixture执行之前调用，所以会清空setup中的截图
    我们需要在fixture执行之后清空截图，所以在pytest_runtest_call中处理
    """
    # 不在这里清空截图，因为会在fixture执行之前调用
    # 改为在pytest_runtest_call中清空
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item):
    """
    在测试方法执行前清空截图记录
    这个hook在fixture执行之后、测试方法执行之前调用
    """
    screenshot_utils = get_screenshot_utils()
    screenshot_utils.clear_screenshots()
    yield


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    在测试执行后捕获截图并保存到测试报告中
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # 获取截图
        screenshot_utils = get_screenshot_utils()
        screenshots = screenshot_utils.get_screenshots()

        print(f"[DEBUG] pytest_runtest_makereport: item.name={item.name}, report.failed={report.failed}, screenshots={len(screenshots)}")

        # 如果测试失败，自动捕获失败截图
        if report.failed:
            print(f"[DEBUG] 测试失败，尝试捕获失败截图")
            # 尝试获取 page fixture
            page = None
            if hasattr(item, "funcargs") and "page" in item.funcargs:
                page = item.funcargs["page"]
            elif hasattr(item, "funcargs") and "drama_home_page" in item.funcargs:
                page = item.funcargs["drama_home_page"]
            elif hasattr(item, "funcargs") and "player_page" in item.funcargs:
                page = item.funcargs["player_page"]

            if page:
                try:
                    # 捕获失败截图
                    screenshot_path = screenshot_utils.take_screenshot(
                        page, name=f"failure_{item.name}"
                    )
                    print(f"[DEBUG] 失败截图已保存: {screenshot_path}")
                    if screenshot_path and screenshot_path not in screenshots:
                        screenshots.append(screenshot_path)
                        print(f"[DEBUG] 失败截图已添加到截图列表")
                except Exception as e:
                    print(f"[DEBUG] 捕获失败截图时出错: {e}")
            else:
                print(f"[DEBUG] 无法获取page对象，无法捕获失败截图")

        if screenshots:
            # 将截图路径添加到测试报告中
            print(f"[DEBUG] 将{len(screenshots)}个截图添加到测试报告")
            report.user_properties.append(("screenshots", screenshots))
        else:
            print(f"[DEBUG] 没有截图需要添加到测试报告")


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """会话级别的夹具，在整个测试会话开始前执行"""
    print("\n=== 开始测试会话 ===")
    kill_processes_using_port(9223)
    yield
    print("\n=== 结束测试会话 ===")
    kill_processes_using_port(9223)


def get_or_create_browser():
    """获取或创建浏览器实例（非并发模式）"""
    global _browser_instance

    if _browser_instance is None:
        kill_processes_using_port(9223)

        co = ChromiumOptions()
        co.set_local_port(9223)
        co.set_user_agent(
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36"
        )
        co.set_argument("--window-size=430,932")
        co.set_argument("--disable-blink-features=AutomationControlled")

        _browser_instance = ChromiumPage(co)

    return _browser_instance


def create_browser_for_worker(worker_id):
    """
    为每个 worker 创建独立的浏览器实例（并发模式）
    :param worker_id: worker ID，如 gw0, gw1, gw2 等
    :return: 浏览器实例
    """
    # 根据 worker_id 计算唯一的端口号
    worker_num = int(worker_id.replace("gw", "")) if worker_id.startswith("gw") else 0
    port = 9223 + worker_num

    # 清理可能占用该端口的进程
    kill_processes_using_port(port)

    co = ChromiumOptions()
    co.set_local_port(port)
    co.set_user_agent(
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Mobile/15E148 Safari/604.1"
    )
    co.set_argument("--window-size=430,932")
    co.set_argument("--disable-blink-features=AutomationControlled")

    return ChromiumPage(co)


@pytest.fixture(scope="function")
def screenshot_utils():
    """
    截图工具夹具
    """
    utils = get_screenshot_utils()
    utils.clear_screenshots()  # 每个测试前清空截图记录
    yield utils


@pytest.fixture(scope="class")
def page(worker_id):
    """
    类级别的夹具，根据是否并发执行创建浏览器实例
    在整个测试类执行完毕后才关闭浏览器
    :param worker_id: pytest-xdist 提供的 worker ID
    """
    # 如果 worker_id 是 "master"，说明是非并发模式，使用共享浏览器
    if worker_id == "master":
        browser = get_or_create_browser()
    else:
        # 并发模式，为每个 worker 创建独立的浏览器
        browser = create_browser_for_worker(worker_id)

    yield browser

    # 如果是并发模式，测试类完成后关闭浏览器
    if worker_id != "master":
        try:
            browser.quit()
        except:
            pass


@pytest.fixture(scope="class")
def player_page(worker_id):
    """
    类级别的夹具，根据是否并发执行创建浏览器实例（用于播放器测试）
    在整个测试类执行完毕后才关闭浏览器
    :param worker_id: pytest-xdist 提供的 worker ID
    """
    # 如果 worker_id 是 "master"，说明是非并发模式，使用共享浏览器
    if worker_id == "master":
        browser = get_or_create_browser()
    else:
        # 并发模式，为每个 worker 创建独立的浏览器
        browser = create_browser_for_worker(worker_id)

    yield browser

    # 如果是并发模式，测试类完成后关闭浏览器
    if worker_id != "master":
        try:
            browser.quit()
        except:
            pass


@pytest.fixture(scope="class")
def drama_home_page(worker_id):
    """
    类级别的夹具，根据是否并发执行创建浏览器实例（用于播放器测试）
    在整个测试类执行完毕后才关闭浏览器
    :param worker_id: pytest-xdist 提供的 worker ID
    """
    # 如果 worker_id 是 "master"，说明是非并发模式，使用共享浏览器
    if worker_id == "master":
        browser = get_or_create_browser()
    else:
        # 并发模式，为每个 worker 创建独立的浏览器
        browser = create_browser_for_worker(worker_id)

    yield browser

    # 如果是并发模式，测试类完成后关闭浏览器
    if worker_id != "master":
        try:
            browser.quit()
        except:
            pass
