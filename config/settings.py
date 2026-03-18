# 应用配置文件

# 基础地址
BASE_URL = "https://video.reelswave.net/"

# 测试首页地址
TEST_HOME_URL = "https://video.reelswave.net/content/286606456962772992?chapterIndex=1"

# 个人中心页面地址
PROFILE_URL = "https://video.reelswave.net/profile"

# 邮件配置
EMAIL_CONFIG = {
    "smtp_server": "smtp.exmail.qq.com",
    "smtp_port": 465,
    "smtp_username": "zhangxu@col.com",
    "smtp_password": "wKmail2025",
    "from_email": "zhangxu@col.com",
    "to_email": "zhangxu@col.com"
}

# 定时任务配置
SCHEDULE_CONFIG = {
    "type": "cron",
    "cron_expression": "0 2 * * *",
    "fixed_time": None
}

# 测试报告配置
REPORT_CONFIG = {
    "base_dir": "reports",
    "screenshot_dir": "reports/screenshots",
    "enable_screenshots": True
}
