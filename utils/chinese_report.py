
"""
中文测试报告生成器
"""
import json
from datetime import datetime
from pathlib import Path
from utils.logger_utils import LoggerUtils
from config.settings import REPORT_CONFIG


class ChineseReportGenerator:
    """中文测试报告生成器"""

    def __init__(self):
        """初始化报告生成器"""
        self.logger = LoggerUtils.get_default_logger()
        self.report_base_dir = Path(REPORT_CONFIG.get('base_dir', 'reports'))
        self.report_dir = self.report_base_dir / 'html'
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, test_results):
        """
        生成测试报告
        :param test_results: 测试结果数据列表
        :return: 报告文件路径
        """
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            report_filename = today + "_test_report.html"
            report_path = self.report_dir / report_filename

            # 生成 HTML 报告
            self._save_html_report(test_results, report_path)

            self.logger.info("测试报告已生成: " + str(report_path))
            return str(report_path)
        except Exception as e:
            self.logger.error("生成测试报告失败: " + str(e))
            return None

    def _save_html_report(self, test_results, html_path):
        """保存 HTML 格式报告"""
        try:
            total_cases = len(test_results)
            passed = sum(1 for r in test_results if r['status'] == 'passed')
            failed = sum(1 for r in test_results if r['status'] == 'failed')
            total_duration = sum(r['duration'] for r in test_results)
            pass_rate = (passed / total_cases * 100) if total_cases > 0 else 0

            html_content = self._build_html_content(
                total_cases, passed, failed, total_duration, pass_rate, test_results
            )

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            self.logger.info("HTML 报告已保存: " + str(html_path))
        except Exception as e:
            self.logger.error("保存 HTML 报告失败: " + str(e))

    def _build_html_content(self, total_cases, passed, failed, total_duration, pass_rate, test_results):
        """构建 HTML 内容"""
        date_str = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')

        # 构建 HTML
        html = '<!DOCTYPE html>\n'
        html += '<html lang="zh-CN">\n'
        html += '<head>\n'
        html += '    <meta charset="UTF-8">\n'
        html += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        html += '    <title>自动化测试报告</title>\n'
        html += '    <style>\n'
        html += '        * { margin: 0; padding: 0; box-sizing: border-box; }\n'
        html += '        body { font-family: "Microsoft YaHei", Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }\n'
        html += '        .container { max-width: 1200px; margin: 0 auto; }\n'
        html += '        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }\n'
        html += '        .header h1 { font-size: 28px; margin-bottom: 10px; }\n'
        html += '        .header p { font-size: 14px; opacity: 0.9; }\n'
        html += '        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }\n'
        html += '        .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; }\n'
        html += '        .stat-label { color: #666; font-size: 14px; margin-bottom: 10px; }\n'
        html += '        .stat-value { font-size: 32px; font-weight: bold; }\n'
        html += '        .stat-value.pass { color: #4CAF50; }\n'
        html += '        .stat-value.fail { color: #f44336; }\n'
        html += '        .filters { margin-bottom: 20px; }\n'
        html += '        .filter-btn { padding: 10px 25px; margin-right: 10px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold; transition: all 0.3s; }\n'
        html += '        .filter-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }\n'
        html += '        .filter-btn.active { background: #667eea; color: white; }\n'
        html += '        .filter-btn.pass { background: #4CAF50; color: white; }\n'
        html += '        .filter-btn.fail { background: #f44336; color: white; }\n'
        html += '        .test-cases { background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }\n'
        html += '        .test-case { padding: 20px; border-bottom: 1px solid #eee; transition: background-color 0.3s; }\n'
        html += '        .test-case:hover { background-color: #f9f9f9; }\n'
        html += '        .case-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }\n'
        html += '        .case-name { font-weight: bold; font-size: 16px; color: #333; }\n'
        html += '        .case-status { padding: 8px 20px; border-radius: 20px; font-size: 12px; font-weight: bold; }\n'
        html += '        .case-status.pass { background: #e8f5e9; color: #4CAF50; }\n'
        html += '        .case-status.fail { background: #ffebee; color: #f44336; }\n'
        html += '        .case-details { margin-top: 15px; padding: 15px; background: #f9f9f9; border-radius: 8px; }\n'
        html += '        .detail-item { margin-bottom: 10px; color: #555; }\n'
        html += '        .case-screenshots { margin-top: 15px; }\n'
        html += '        .screenshot { display: inline-block; margin-right: 10px; margin-bottom: 10px; }\n'
        html += '        .screenshot img { max-width: 200px; border-radius: 5px; cursor: pointer; transition: transform 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n'
        html += '        .screenshot img:hover { transform: scale(1.05); }\n'
        html += '        .error-message { color: #f44336; margin-top: 15px; padding: 15px; background: #ffebee; border-radius: 8px; border-left: 4px solid #f44336; }\n'
        html += '    </style>\n'
        html += '</head>\n'
        html += '<body>\n'
        html += '    <div class="container">\n'
        html += '        <div class="header">\n'
        html += '            <h1>自动化测试报告</h1>\n'
        html += '            <p>测试时间：' + date_str + '</p>\n'
        html += '        </div>\n'
        html += '        <div class="stats">\n'
        html += '            <div class="stat-card">\n'
        html += '                <div class="stat-label">总用例数</div>\n'
        html += '                <div class="stat-value">' + str(total_cases) + '</div>\n'
        html += '            </div>\n'
        html += '            <div class="stat-card">\n'
        html += '                <div class="stat-label">通过</div>\n'
        html += '                <div class="stat-value pass">' + str(passed) + '</div>\n'
        html += '            </div>\n'
        html += '            <div class="stat-card">\n'
        html += '                <div class="stat-label">失败</div>\n'
        html += '                <div class="stat-value fail">' + str(failed) + '</div>\n'
        html += '            </div>\n'
        html += '            <div class="stat-card">\n'
        html += '                <div class="stat-label">通过率</div>\n'
        html += '                <div class="stat-value">' + str(round(pass_rate, 1)) + '%</div>\n'
        html += '            </div>\n'
        html += '            <div class="stat-card">\n'
        html += '                <div class="stat-label">总耗时</div>\n'
        html += '                <div class="stat-value">' + str(round(total_duration, 2)) + '秒</div>\n'
        html += '            </div>\n'
        html += '        </div>\n'
        html += '        <div class="filters">\n'
        html += '            <button class="filter-btn active" onclick="filterCases(\'all\')">全部</button>\n'
        html += '            <button class="filter-btn pass" onclick="filterCases(\'passed\')">通过</button>\n'
        html += '            <button class="filter-btn fail" onclick="filterCases(\'failed\')">失败</button>\n'
        html += '        </div>\n'
        html += '        <div class="test-cases">\n'

        # 添加测试用例
        for idx, case in enumerate(test_results, 1):
            status_class = 'pass' if case['status'] == 'passed' else 'fail'
            status_text = '通过' if case['status'] == 'passed' else '失败'

            html += '            <div class="test-case" data-status="' + case['status'] + '">\n'
            html += '                <div class="case-header">\n'
            html += '                    <div class="case-name">' + str(idx) + '. ' + case['name'] + '</div>\n'
            html += '                    <div class="case-status ' + status_class + '">' + status_text + '</div>\n'
            html += '                </div>\n'
            html += '                <div class="case-details">\n'
            html += '                    <div class="detail-item">执行耗时：' + str(round(case['duration'], 3)) + '秒</div>\n'

            # 添加截图
            if case.get('screenshots'):
                html += '                    <div class="case-screenshots">\n'
                for screenshot in case['screenshots']:
                    html += '                        <div class="screenshot">\n'
                    html += '                            <a href="' + screenshot + '" target="_blank">\n'
                    html += '                                <img src="' + screenshot + '" alt="截图">\n'
                    html += '                            </a>\n'
                    html += '                        </div>\n'
                html += '                    </div>\n'

            # 添加错误信息
            if case.get('error'):
                html += '                    <div class="error-message">\n'
                html += '                        <strong>错误信息：</strong>\n'
                html += '                        <pre>' + case['error'] + '</pre>\n'
                html += '                    </div>\n'

            html += '                </div>\n'
            html += '            </div>\n'

        # 添加尾部
        html += '        </div>\n'
        html += '    </div>\n'
        html += '    <script>\n'
        html += '        function filterCases(status) {\n'
        html += '            document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));\n'
        html += '            event.target.classList.add("active");\n'
        html += '            document.querySelectorAll(".test-case").forEach(case => {\n'
        html += '                case.style.display = (status === "all" || case.dataset.status === status) ? "block" : "none";\n'
        html += '            });\n'
        html += '        }\n'
        html += '    </script>\n'
        html += '</body>\n'
        html += '</html>\n'

        return html
