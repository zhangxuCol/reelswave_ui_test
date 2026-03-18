
"""
邮件通知工具类
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from utils.logger_utils import LoggerUtils
from config.settings import EMAIL_CONFIG


class EmailNotifier:
    """邮件通知器，负责发送测试报告邮件"""

    def __init__(self):
        """初始化邮件通知器"""
        self.logger = LoggerUtils.get_default_logger()
        self.smtp_server = EMAIL_CONFIG.get('smtp_server')
        self.smtp_port = EMAIL_CONFIG.get('smtp_port')
        self.smtp_username = EMAIL_CONFIG.get('smtp_username')
        self.smtp_password = EMAIL_CONFIG.get('smtp_password')
        self.from_email = EMAIL_CONFIG.get('from_email')
        self.to_email = EMAIL_CONFIG.get('to_email', 'zhangxu@col.com')

    def send_test_report(self, test_date, total_cases, passed, failed, 
                      report_path, screenshots_zip_path=None, 
                      total_duration=None):
        """
        发送测试报告邮件
        :param test_date: 测试日期
        :param total_cases: 总用例数
        :param passed: 通过用例数
        :param failed: 失败用例数
        :param report_path: 测试报告文件路径
        :param screenshots_zip_path: 截图压缩包路径（可选）
        :param total_duration: 总耗时（秒）
        :return: 是否发送成功
        """
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = f'【网页自动化测试报告】{test_date} - 总用例数：{total_cases}，通过：{passed}，失败：{failed}'

            # 构建邮件正文
            body = self._build_email_body(
                test_date, total_cases, passed, failed, 
                total_duration, report_path
            )
            msg.attach(MIMEText(body, 'html', 'utf-8'))

            # 附加测试报告
            if report_path and Path(report_path).exists():
                with open(report_path, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=Path(report_path).name)
                part['Content-Disposition'] = f'attachment; filename="{Path(report_path).name}"'
                msg.attach(part)

            # 附加截图压缩包（如果提供）
            if screenshots_zip_path and Path(screenshots_zip_path).exists():
                with open(screenshots_zip_path, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=Path(screenshots_zip_path).name)
                part['Content-Disposition'] = f'attachment; filename="{Path(screenshots_zip_path).name}"'
                msg.attach(part)

            # 发送邮件
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            self.logger.info("测试报告邮件发送成功")
            return True

        except Exception as e:
            self.logger.error(f"发送测试报告邮件失败: {e}")
            return False

    def _build_email_body(self, test_date, total_cases, passed, failed, 
                        total_duration, report_path):
        """
        构建邮件正文
        :param test_date: 测试日期
        :param total_cases: 总用例数
        :param passed: 通过用例数
        :param failed: 失败用例数
        :param total_duration: 总耗时
        :param report_path: 报告路径
        :return: HTML格式的邮件正文
        """
        pass_rate = (passed / total_cases * 100) if total_cases > 0 else 0
        duration_str = f"{total_duration:.2f}秒" if total_duration else "未知"

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .stat-box {{ 
                    display: inline-block; 
                    margin: 10px; 
                    padding: 15px; 
                    border: 1px solid #ddd; 
                    border-radius: 5px; 
                    width: 150px;
                }}
                .stat-label {{ font-size: 14px; color: #666; }}
                .stat-value {{ font-size: 24px; font-weight: bold; margin-top: 5px; }}
                .pass {{ color: #4CAF50; }}
                .fail {{ color: #f44336; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>网页自动化测试报告</h2>
                <p>测试日期: {test_date}</p>
            </div>
            <div class="content">
                <h3>测试统计</h3>
                <div class="stat-box">
                    <div class="stat-label">总用例数</div>
                    <div class="stat-value">{total_cases}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">通过</div>
                    <div class="stat-value pass">{passed}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">失败</div>
                    <div class="stat-value fail">{failed}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">通过率</div>
                    <div class="stat-value">{pass_rate:.1f}%</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">总耗时</div>
                    <div class="stat-value">{duration_str}</div>
                </div>

                <h3>测试报告</h3>
                <p>详细的测试报告请查看附件中的HTML文件。</p>
            </div>
        </body>
        </html>
        """
        return html

    def send_error_notification(self, error_message, test_date):
        """
        发送错误通知邮件
        :param error_message: 错误信息
        :param test_date: 测试日期
        :return: 是否发送成功
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = f'【测试执行失败】{test_date}'

            body = f"""
            <html>
            <body>
                <h2>测试执行失败通知</h2>
                <p><strong>测试日期:</strong> {test_date}</p>
                <p><strong>错误信息:</strong></p>
                <pre style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">{error_message}</pre>
            </body>
            </html>
            """
            msg.attach(MIMEText(body, 'html', 'utf-8'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            self.logger.info("错误通知邮件发送成功")
            return True

        except Exception as e:
            self.logger.error(f"发送错误通知邮件失败: {e}")
            return False
