"""
自定义 pytest 插件，生成中文 HTML 测试报告并包含截图
"""
import os
import sys
import time
import base64
from datetime import datetime
from pathlib import Path


# 简单的 HTML 转义函数
def escape_html(text):
    """转义 HTML 特殊字符"""
    return (str(text)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


class ChineseHTMLReportPlugin:
    """中文 HTML 报告插件，支持截图"""

    def __init__(self, config):
        self.config = config
        # 使用ReportDirManager管理报告目录
        from utils.report_dir_manager import get_report_dir_manager
        self.dir_manager = get_report_dir_manager()
        self.report_dir = self.dir_manager.get_report_dir()
        self.screenshot_dir = self.dir_manager.get_screenshot_dir()
        print(f"[DEBUG] 报告目录: {self.report_dir}")
        
        # 检查是否是主进程（pytest-xdist的worker_id为'master'）
        self.is_master = hasattr(config, 'workerinput') is False or getattr(config, 'workerinput', {}).get('workerid') == 'master'
        print(f"[DEBUG] 是否为主进程: {self.is_master}")

        # 存储测试结果
        self.results = []
        self.start_time = None
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0

    def pytest_sessionstart(self, session):
        """测试会话开始时"""
        self.start_time = time.time()

    def pytest_runtest_logreport(self, report):
        """收集测试结果"""
        print(f"[DEBUG] report.when = {report.when}, report.nodeid = {report.nodeid}, report.passed={report.passed}, report.failed={report.failed}")

        if report.when == 'call':
            self.total_tests += 1

            # 确定测试状态
            if report.passed:
                status = '通过'
                self.passed_tests += 1
            elif report.failed:
                status = '失败'
                self.failed_tests += 1
            elif report.skipped:
                status = '跳过'
                self.skipped_tests += 1
            else:
                status = '未知'

            # 提取测试名称和类文件信息
            nodeid_parts = report.nodeid.split('::')
            test_name = nodeid_parts[-1]
            if 'test_' in test_name:
                test_name = test_name.replace('test_', '')
            
            # 提取测试类文件名（用于分组）
            class_file = nodeid_parts[0] if len(nodeid_parts) > 1 else '未分类'
            # 去掉.py后缀，只保留文件名
            if class_file.endswith('.py'):
                class_file = class_file[:-3]
            # 只保留文件名，去掉路径
            class_file = class_file.split('/')[-1] if '/' in class_file else class_file
            class_file = class_file.split('\\')[-1] if '\\' in class_file else class_file
            
            print(f"[DEBUG] 测试类文件: {class_file}")

            # 提取描述
            description = ''
            if hasattr(report, 'user_properties'):
                for prop in report.user_properties:
                    if prop[0] == 'description':
                        description = prop[1]
                        break

            # 如果没有描述，使用函数名
            if not description:
                description = test_name.replace('_', ' ')

            # 获取截图路径
            screenshots = []
            if hasattr(report, 'user_properties'):
                for prop in report.user_properties:
                    if prop[0] == 'screenshots':
                        screenshots = prop[1]
                        print(f"[DEBUG] 找到截图: {screenshots}")
                        break

            # 如果测试失败且没有截图，尝试添加默认截图
            if report.failed and not screenshots:
                print(f"[DEBUG] 测试失败但没有截图，尝试添加失败截图")
                # 这里可以添加默认的失败截图逻辑

            # 获取错误信息
            error_message = ''
            if report.longrepr:
                error_message = str(report.longrepr)

            # 打印调试信息
            print(f"[DEBUG] 添加测试结果: name={test_name}, status={status}, screenshots_count={len(screenshots)}")

            self.results.append({
                'name': test_name,
                'description': description,
                'status': status,
                'duration': report.duration,
                'screenshots': screenshots,
                'error': error_message,
                'class_file': class_file  # 添加测试类文件信息
            })

    def pytest_sessionfinish(self, session):
        """测试会话结束时生成报告"""
        # 只在主进程中生成报告
        if not self.is_master:
            print(f"[DEBUG] 非主进程，跳过生成报告")
            return
            
        total_duration = time.time() - self.start_time
        print(f"[DEBUG] 主进程，开始生成报告，测试用例数: {len(self.results)}")
        
        # 生成报告
        report_path = self._generate_report(total_duration)

        # 输出报告路径
        print(f"\n{'=' * 60}")
        print(f"中文测试报告已生成: {report_path}")
        print(f"{'=' * 60}\n")

    def _generate_report(self, total_duration):
        """生成中文 HTML 报告"""
        # 使用固定名称作为报告文件名
        report_filename = 'test_report.html'
        report_path = self.report_dir / report_filename

        # 计算通过率
        executed_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / executed_tests * 100) if executed_tests > 0 else 0

        # 构建 HTML 内容
        html_content = self._build_html_content(
            total_duration, pass_rate
        )

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(report_path)

    def _build_html_content(self, total_duration, pass_rate):
        """构建 HTML 内容"""
        date_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')

        html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自动化测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .header h1 {{
            font-size: 32px;
            color: #333;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        .stat-value {{
            font-size: 36px;
            font-weight: bold;
        }}
        .stat-value.pass {{ color: #4CAF50; }}
        .stat-value.fail {{ color: #f44336; }}
        .stat-value.skip {{ color: #ff9800; }}
        .stat-value.total {{ color: #667eea; }}
        .filter-bar {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .filter-btn {{
            padding: 10px 25px;
            margin-right: 10px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s;
            color: white;
        }}
        .filter-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .filter-btn.all {{ background: #667eea; }}
        .filter-btn.pass {{ background: #4CAF50; }}
        .filter-btn.fail {{ background: #f44336; }}
        .filter-btn.skip {{ background: #ff9800; }}
        .filter-btn.active {{
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.5);
        }}
        .test-cases {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .test-case {{
            border-bottom: 1px solid #eee;
            transition: all 0.3s;
        }}
        .test-case:hover {{
            background: #f8f9fa;
        }}
        .test-case:last-child {{
            border-bottom: none;
        }}
        .case-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            cursor: pointer;
        }}
        .case-info {{
            flex: 1;
        }}
        .case-name {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        .case-description {{
            color: #666;
            font-size: 13px;
        }}
        .case-meta {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .case-status {{
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}
        .case-status.pass {{
            background: #e8f5e9;
            color: #4CAF50;
        }}
        .case-status.fail {{
            background: #ffebee;
            color: #f44336;
        }}
        .case-status.skip {{
            background: #fff3e0;
            color: #ff9800;
        }}
        .case-duration {{
            color: #999;
            font-size: 13px;
        }}
        .expand-icon {{
            font-size: 20px;
            color: #999;
            transition: transform 0.3s;
        }}
        .test-case.expanded .expand-icon {{
            transform: rotate(180deg);
        }}
        .case-details {{
            display: none;
            padding: 0 20px 20px;
            background: #fafafa;
            border-top: 1px solid #eee;
        }}
        .test-case.expanded .case-details {{
            display: block;
        }}
        .screenshots-section {{
            margin-top: 15px;
        }}
        .section-title {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .screenshots-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }}
        .screenshot-item {{
            position: relative;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s;
            cursor: pointer;
        }}
        .screenshot-item:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }}
        .screenshot-item img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .screenshot-label {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 5px 10px;
            font-size: 12px;
        }}
        .error-section {{
            margin-top: 15px;
            background: #ffebee;
            border-radius: 8px;
            padding: 15px;
            border-left: 4px solid #f44336;
        }}
        .error-title {{
            font-weight: bold;
            color: #f44336;
            margin-bottom: 10px;
        }}
        .error-content {{
            color: #c62828;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 300px;
            overflow-y: auto;
        }}
        .no-screenshots {{
            color: #999;
            font-style: italic;
            padding: 20px;
            text-align: center;
        }}
        .test-class-section {{
            margin-bottom: 30px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .class-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .class-header h2 {{
            margin: 0;
            font-size: 20px;
        }}
        .class-stats {{
            display: flex;
            gap: 15px;
        }}
        .class-stat {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
        }}
        .class-stat.pass {{
            background: rgba(76, 175, 80, 0.2);
            color: #4CAF50;
        }}
        .class-stat.fail {{
            background: rgba(244, 67, 54, 0.2);
            color: #f44336;
        }}
        .class-stat.total {{
            background: rgba(255, 255, 255, 0.2);
            color: white;
        }}
        .class-cases {{
            background: rgba(255, 255, 255, 0.95);
        }}
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            margin-top: 10px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            border-radius: 4px;
            transition: width 0.5s ease;
        }}
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}
        .modal.active {{
            display: flex;
        }}
        .modal img {{
            max-width: 90%;
            max-height: 90%;
            border-radius: 8px;
        }}
        .modal-close {{
            position: absolute;
            top: 20px;
            right: 40px;
            color: white;
            font-size: 40px;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 自动化测试报告</h1>
            <div class="subtitle">生成时间：{date_str}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">总用例数</div>
                <div class="stat-value total">{self.total_tests}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">通过</div>
                <div class="stat-value pass">{self.passed_tests}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">失败</div>
                <div class="stat-value fail">{self.failed_tests}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">跳过</div>
                <div class="stat-value skip">{self.skipped_tests}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">通过率</div>
                <div class="stat-value pass">{pass_rate:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pass_rate:.1f}%"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">总耗时</div>
                <div class="stat-value total">{total_duration:.2f}s</div>
            </div>
        </div>

        <div class="filter-bar">
            <button class="filter-btn all active" onclick="filterCases('all')">全部 ({self.total_tests})</button>
            <button class="filter-btn pass" onclick="filterCases('pass')">通过 ({self.passed_tests})</button>
            <button class="filter-btn fail" onclick="filterCases('fail')">失败 ({self.failed_tests})</button>
            <button class="filter-btn skip" onclick="filterCases('skip')">跳过 ({self.skipped_tests})</button>
        </div>

        <div class="test-cases">
'''

        # 按测试类文件分组
        results_by_class = {}
        for result in self.results:
            class_file = result.get('class_file', '未分类')
            if class_file not in results_by_class:
                results_by_class[class_file] = []
            results_by_class[class_file].append(result)
        
        print(f"[DEBUG] 测试类文件分组: {list(results_by_class.keys())}")
        
        # 按测试类文件添加测试用例
        for class_file, class_results in results_by_class.items():
            html_template += f'''
            <div class="test-class-section">
                <div class="class-header">
                    <h2>📁 {class_file}</h2>
                    <div class="class-stats">
                        <span class="class-stat pass">通过: {sum(1 for r in class_results if r['status'] == '通过')}</span>
                        <span class="class-stat fail">失败: {sum(1 for r in class_results if r['status'] == '失败')}</span>
                        <span class="class-stat total">总计: {len(class_results)}</span>
                    </div>
                </div>
                <div class="class-cases">
            '''
            
            for idx, result in enumerate(class_results, 1):
                status_class = result['status']
                screenshots_html = self._build_screenshots_html(result['screenshots'], idx)
                error_html = self._build_error_html(result['error'])

                html_template += f'''
                <div class="test-case" data-status="{status_class}" onclick="toggleCase(this)">
                    <div class="case-header">
                        <div class="case-info">
                            <div class="case-name">{idx}. {result['name']}</div>
                            <div class="case-description">{result['description']}</div>
                        </div>
                        <div class="case-meta">
                            <span class="case-status {status_class}">{status_class}</span>
                            <span class="case-duration">{result['duration']:.3f}s</span>
                            <span class="expand-icon">▼</span>
                        </div>
                    </div>
                    <div class="case-details">
                        {screenshots_html}
                        {error_html}
                    </div>
                </div>
            '''
            
            html_template += '''
                </div>
            </div>
            '''

        html_template += '''
        </div>
    </div>

    <div class="modal" id="imageModal" onclick="closeModal()">
        <span class="modal-close">&times;</span>
        <img id="modalImage" src="" alt="截图">
    </div>

    <script>
        function filterCases(status) {
            // 获取点击事件
            const event = window.event;
            // 移除所有按钮的active类
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            // 为当前点击的按钮添加active类
            if (event && event.target) {
                event.target.classList.add('active');
            }
            
            // 将英文状态转换为中文状态
            const statusMap = {
                'pass': '通过',
                'fail': '失败',
                'skip': '跳过'
            };
            const chineseStatus = statusMap[status] || status;
            
            // 筛选测试用例，但保留模块显示
            document.querySelectorAll('.test-case').forEach(caseEl => {
                if (status === 'all' || caseEl.dataset.status === chineseStatus) {
                    caseEl.style.display = 'block';
                } else {
                    caseEl.style.display = 'none';
                }
            });
            
            // 始终显示所有模块，不隐藏模块区块
            document.querySelectorAll('.test-class-section').forEach(classSection => {
                classSection.style.display = 'block';
            });
        }

        function toggleCase(element) {
            element.classList.toggle('expanded');
        }

        function openModal(src) {
            document.getElementById('modalImage').src = src;
            document.getElementById('imageModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('imageModal').classList.remove('active');
        }

        // 点击图片放大
        document.querySelectorAll('.screenshot-item img').forEach(img => {
            img.addEventListener('click', function(e) {
                e.stopPropagation();
                openModal(this.src);
            });
        });
    </script>
</body>
</html>
'''
        return html_template

    def _build_screenshots_html(self, screenshots, case_idx):
        """构建截图 HTML"""
        print(f"[DEBUG] _build_screenshots_html: case_idx={case_idx}, screenshots_count={len(screenshots) if screenshots else 0}")
        
        if not screenshots:
            print(f"[DEBUG] 没有截图，显示暂无截图")
            return '<div class="screenshots-section"><div class="section-title">📸 测试截图</div><div class="no-screenshots">暂无截图</div></div>'

        html = '<div class="screenshots-section"><div class="section-title">📸 测试截图</div><div class="screenshots-grid">'

        for idx, screenshot_path in enumerate(screenshots, 1):
            print(f"[DEBUG] 处理截图 {idx}: {screenshot_path}")
            if os.path.exists(screenshot_path):
                # 将图片转为 base64
                try:
                    with open(screenshot_path, 'rb') as f:
                        img_data = base64.b64encode(f.read()).decode('utf-8')
                    img_src = f'data:image/png;base64,{img_data}'
                    print(f"[DEBUG] 截图 {idx} 已转换为 base64")
                except Exception as e:
                    print(f"[DEBUG] 转换截图 {idx} 为 base64 时出错: {e}")
                    img_src = screenshot_path

                html += f'''
                <div class="screenshot-item">
                    <img src="{img_src}" alt="截图 {idx}" onclick="openModal('{img_src}')">
                    <div class="screenshot-label">截图 {idx}</div>
                </div>
'''
            else:
                print(f"[DEBUG] 截图文件不存在: {screenshot_path}")

        html += '</div></div>'
        print(f"[DEBUG] 截图 HTML 已生成")
        return html

    def _build_error_html(self, error):
        """构建错误信息 HTML"""
        if not error:
            return ''

        # 转义 HTML 特殊字符
        escaped_error = escape_html(error)

        return f'''
        <div class="error-section">
            <div class="error-title">❌ 错误信息</div>
            <div class="error-content">{escaped_error}</div>
        </div>
'''


def pytest_configure(config):
    """配置 pytest"""
    config._chinese_html = ChineseHTMLReportPlugin(config)
    config.pluginmanager.register(config._chinese_html)


def pytest_unconfigure(config):
    """卸载插件"""
    if hasattr(config, '_chinese_html'):
        config.pluginmanager.unregister(config._chinese_html)
        del config._chinese_html
