
"""
统一的测试运行脚本
支持单文件测试、并发测试和定时测试模式
"""
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils
from utils.scheduler import TaskScheduler
from utils.screenshot_utils import get_screenshot_utils
from config.settings import REPORT_CONFIG


def parse_pytest_output(stdout, stderr, duration):
    """
    解析 pytest 输出
    :param stdout: 标准输出
    :param stderr: 标准错误
    :param duration: 执行耗时
    :return: 测试结果列表
    """
    test_results = []
    lines = stdout.split('\n')

    for line in lines:
        # 解析通过的测试
        if '::test_' in line and 'PASSED' in line:
            test_name = line.split('::')[-1].split()[0]
            # 尝试从行中提取执行时间
            test_duration = 0.1  # 默认值
            if 'in ' in line and 's' in line:
                try:
                    # 格式通常是 "in X.XXs"
                    duration_str = line.split('in ')[-1].split('s')[0]
                    test_duration = float(duration_str)
                except (IndexError, ValueError):
                    pass

            test_results.append({
                'name': test_name,
                'status': 'passed',
                'duration': test_duration,
                'screenshots': [],  # 通过的测试用例不显示截图
                'error': None
            })

        # 解析失败的测试
        elif '::test_' in line and 'FAILED' in line:
            test_name = line.split('::')[-1].split()[0]
            # 尝试从行中提取执行时间
            test_duration = 0.1  # 默认值
            if 'in ' in line and 's' in line:
                try:
                    # 格式通常是 "in X.XXs"
                    duration_str = line.split('in ')[-1].split('s')[0]
                    test_duration = float(duration_str)
                except (IndexError, ValueError):
                    pass

            # 获取截图
            screenshot_utils = get_screenshot_utils()
            screenshots = screenshot_utils.get_screenshots()

            test_results.append({
                'name': test_name,
                'status': 'failed',
                'duration': test_duration,
                'screenshots': screenshots,  # 失败的测试用例显示所有截图
                'error': stderr
            })

    return test_results


def run_single_test(test_file):
    """
    运行单个测试文件
    :param test_file: 测试文件路径
    :return: 测试结果
    """
    logger = LoggerUtils.get_default_logger()

    try:
        start_time = time.time()
        logger.info(f"开始执行测试: {test_file}")

        # 构建 pytest 命令
        cmd = [
            'pytest',
            test_file,
            '-v',
            '--tb=short'
        ]

        logger.info(f"执行命令: {' '.join(cmd)}")

        # 执行测试
        result = subprocess.run(cmd)

        duration = time.time() - start_time

        # 解析测试结果（不解析输出，使用自定义插件生成的报告）
        test_results = []

        # 生成中文报告
        report_generator = ReportGenerator(report_type='chinese')
        # 添加时间戳到报告文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        original_report_path = report_generator.generate_report(test_results)
        if original_report_path:
            # 重命名报告文件，添加时间戳
            original_path = Path(original_report_path)
            new_report_name = f"{timestamp}_{original_path.name}"
            new_report_path = original_path.parent / new_report_name
            original_path.rename(new_report_path)
            report_path = str(new_report_path)
        else:
            report_path = None

        if report_path:
            logger.info(f"中文报告已生成: {report_path}")
            print(f"\n请查看测试报告: {report_path}")
        else:
            logger.error("生成报告失败")

        return test_results

    except Exception as e:
        logger.error(f"执行测试失败: {str(e)}")
        return None


def run_concurrent_test(test_file=None, workers=4):
    """
    运行并发测试
    :param test_file: 测试文件路径（可选，不指定则运行所有测试）
    :param workers: 并发进程数
    :return: 测试结果
    """
    logger = LoggerUtils.get_default_logger()

    print("")
    print("=" * 60)
    print("并发测试运行器")
    print("=" * 60)
    print("")

    if test_file:
        logger.info(f"测试文件: {test_file}")
    else:
        logger.info("测试范围: 所有测试文件")

    logger.info(f"并发进程数: {workers}")
    print("")

    # 构建 pytest 命令
    cmd = [
        "pytest",
        "-n", str(workers),  # 使用 -n 参数指定并发数
        "-v",
        "-s",
        "--tb=short"
    ]

    # 如果指定了测试文件，添加到命令中
    if test_file:
        cmd.append(test_file)

    logger.info(f"执行命令: {' '.join(cmd)}")
    print("")
    print("=" * 60)
    print("")

    # 运行测试
    result = subprocess.run(cmd)
    
    # 解析测试结果
    test_results = []  # 并发模式下不解析输出，使用自定义插件生成的报告
    
    # 查找最新的报告文件
    report_base_dir = Path(REPORT_CONFIG.get('base_dir', 'reports'))
    report_files = list(report_base_dir.glob('report_*.html'))
    if report_files:
        # 按修改时间排序，获取最新的报告
        latest_report = max(report_files, key=lambda f: f.stat().st_mtime)
        report_path = str(latest_report)
    else:
        report_path = None
    if report_path:
        logger.info(f"请查看测试报告: {report_path}")
    else:
        logger.warning("未找到测试报告")

    print("")
    print("=" * 60)

    if result.returncode == 0:
        logger.info("测试执行完成！")
        if report_path:
            logger.info(f"请查看测试报告: {report_path}")
    else:
        logger.error(f"测试执行失败，返回码: {result.returncode}")

    print("=" * 60)
    print("")

    return result.returncode == 0


def run_all_tests():
    """执行所有测试"""
    logger = LoggerUtils.get_default_logger()
    logger.info("开始执行自动化测试...")

    try:
        # 构建 pytest 命令
        cmd = [
            'pytest',
            '-v',
            '--tb=short',
            '--capture=no'
        ]

        logger.info(f"执行命令: {' '.join(cmd)}")

        # 执行测试
        result = subprocess.run(cmd)

        # 解析测试结果（不解析输出，使用自定义插件生成的报告）
        test_results = []

        # 生成报告
        report_generator = ReportGenerator(report_type='chinese')
        report_path = report_generator.generate_report(test_results)

        if test_results:
            total = len(test_results)
            passed = sum(1 for r in test_results if r['status'] == 'passed')
            failed = sum(1 for r in test_results if r['status'] == 'failed')
            logger.info(f"测试执行完成: 总数 {total}, 通过 {passed}, 失败 {failed}")
        else:
            logger.error("测试执行失败")

        return test_results

    except Exception as e:
        logger.error(f"执行测试时发生异常: {str(e)}")
        return None


def run_scheduled_tests():
    """运行定时测试"""
    logger = LoggerUtils.get_default_logger()

    # 检查是否使用定时任务
    if len(sys.argv) > 2 and sys.argv[2] == '--schedule':
        logger.info("启动定时任务模式...")

        scheduler = TaskScheduler()

        try:
            # 启动定时任务
            scheduler.start_scheduled_test(run_all_tests)

            # 保持程序运行
            logger.info("定时任务已启动，按 Ctrl+C 退出...")
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("收到退出信号，停止定时任务...")
            scheduler.stop()

    else:
        # 立即执行测试
        logger.info("立即执行测试...")
        run_all_tests()


def main():
    """主函数"""
    logger = LoggerUtils.get_default_logger()

    if len(sys.argv) < 2:
        print("使用方法: python run_test.py <模式> [选项]")
        print("")
        print("模式:")
        print("  single      - 运行单个测试文件")
        print("  concurrent  - 运行并发测试")
        print("  schedule    - 运行定时测试")
        print("")
        print("选项:")
        print("  -n <进程数>    指定并发进程数（默认: 4）")
        print("  --schedule      启动定时任务模式")
        print("")
        print("示例:")
        print("  # 运行单个测试文件")
        print("  python run_test.py single page/profile_test.py")
        print("")
        print("  # 运行所有测试，使用4个进程")
        print("  python run_test.py concurrent")
        print("")
        print("  # 运行所有测试，使用8个进程")
        print("  python run_test.py concurrent -n 8")
        print("")
        print("  # 运行单个测试文件，使用2个进程")
        print("  python run_test.py concurrent -n 2 page/profile_test.py")
        print("")
        print("  # 立即执行所有测试")
        print("  python run_test.py schedule")
        print("")
        print("  # 启动定时任务")
        print("  python run_test.py schedule --schedule")
        sys.exit(1)

    mode = sys.argv[1]

    # 根据模式执行不同的测试
    if mode == 'single':
        if len(sys.argv) < 3:
            print("错误: 请指定测试文件路径")
            print("示例: python run_test.py single page/profile_test.py")
            sys.exit(1)

        test_file = sys.argv[2]

        # 检查文件是否存在
        if not Path(test_file).exists():
            logger.error(f"测试文件不存在: {test_file}")
            sys.exit(1)

        # 运行单个测试
        run_single_test(test_file)

    elif mode == 'concurrent':
        # 解析参数
        workers = 4  # 默认并发数
        test_file = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "-n" and i + 1 < len(sys.argv):
                workers = int(sys.argv[i + 1])
                i += 2
            elif not sys.argv[i].startswith("-"):
                test_file = sys.argv[i]
                i += 1
            else:
                i += 1

        # 运行并发测试
        run_concurrent_test(test_file, workers)

    elif mode == 'schedule':
        # 运行定时测试
        run_scheduled_tests()

    else:
        logger.error(f"未知的模式: {mode}")
        print("可用的模式: single, concurrent, schedule")
        sys.exit(1)


if __name__ == '__main__':
    main()
