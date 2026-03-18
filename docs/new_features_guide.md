
# 新功能使用指南

## 概述

本文档介绍项目中新增的功能，包括截图功能、测试报告、定时任务、邮件通知和并发执行。

## 功能列表

### 1. 截图功能

#### 功能说明
- 每个测试用例的每一步操作可以生成截图
- 截图命名规则：{用例名}_{步骤序号}_{操作描述}.png
- 截图存储路径：reports/screenshots/{测试日期}/{用例名}/
- 支持在测试报告中查看和下载截图

#### 使用方法

在测试用例中使用 `TestHelper` 类：

```python
from utils.test_helper import TestHelper

def test_example(page):
    # 初始化测试辅助类
    helper = TestHelper("test_example")

    # 执行操作并截图
    helper.take_screenshot(page, "打开首页")
    page.get("https://video.reelswave.net/")

    helper.take_screenshot(page, "点击搜索按钮")
    search_icon = page.ele('css:svg.text-xxl')
    search_icon.click()
```

#### 配置说明

在 `config/settings.py` 中配置：

```python
REPORT_CONFIG = {
    "base_dir": "reports",
    "screenshot_dir": "reports/screenshots",
    "enable_screenshots": True  # 是否启用截图
}
```

### 2. 测试报告功能

#### 功能说明
- 生成 HTML 格式的可视化测试报告
- 生成 JSON 格式的测试报告（便于二次处理）
- 支持按通过/失败状态筛选用例
- 显示测试统计信息（总用例数、通过率、总耗时等）
- 关联截图到测试用例

#### 使用方法

使用 `SimpleReportGenerator` 生成报告：

```python
from utils.simple_report import SimpleReportGenerator

# 准备测试结果数据
test_results = [
    {
        'name': 'test_example',
        'status': 'passed',
        'duration': 5.234,
        'screenshots': ['reports/screenshots/2024-01-01/test_example_01_打开首页.png'],
        'error': None
    }
]

# 生成报告
generator = SimpleReportGenerator()
report_path = generator.generate_report(test_results)
print(f"报告已生成: {report_path}")
```

#### 报告查看

生成的报告位于：`reports/html/{日期}_test_report.html`

在浏览器中打开报告文件即可查看。

### 3. 定时任务功能

#### 功能说明
- 支持 cron 表达式配置定时规则
- 支持固定时间执行
- 自动记录定时任务的启动/结束时间和执行结果
- 执行失败时发送错误通知

#### 使用方法

##### 方式一：使用定时任务模式

```bash
python run_scheduled_tests.py --schedule
```

##### 方式二：立即执行测试

```bash
python run_scheduled_tests.py
```

#### 配置说明

在 `config/settings.py` 中配置定时规则：

```python
# 定时任务配置
SCHEDULE_CONFIG = {
    "type": "cron",  # 定时类型: "cron" 或 "fixed_time"
    "cron_expression": "0 2 * * *",  # cron表达式: 分 时 日 月 周
    "fixed_time": None  # 固定时间: "2024-01-01 02:00:00"
}
```

#### Cron 表达式说明

格式：`分 时 日 月 周`

示例：
- `0 2 * * *`：每天凌晨2点执行
- `0 */6 * * *`：每6小时执行一次
- `0 9 * * 1-5`：周一到周五早上9点执行

### 4. 邮件通知功能

#### 功能说明
- 测试执行完成后自动发送邮件通知
- 邮件包含测试统计信息
- 附件包含 HTML 测试报告
- 可选附加截图压缩包
- 执行失败时发送错误通知

#### 使用方法

邮件通知会在测试执行完成后自动发送，无需手动触发。

#### 配置说明

在 `config/settings.py` 中配置邮件信息：

```python
EMAIL_CONFIG = {
    "smtp_server": "smtp.example.com",  # SMTP服务器地址
    "smtp_port": 587,  # SMTP端口
    "smtp_username": "your_email@example.com",  # 发件人账号
    "smtp_password": "your_password",  # 发件人密码
    "from_email": "your_email@example.com",  # 发件人邮箱
    "to_email": "zhangxu@col.com"  # 收件人邮箱
}
```

#### 邮件内容

邮件包含以下信息：
- 标题：【网页自动化测试报告】{测试日期} - 总用例数：X，通过：X，失败：X
- 正文：核心统计（总耗时、通过/失败数）
- 附件：HTML 测试报告、可选的截图压缩包

### 5. 并发执行功能

#### 功能说明
- 支持同时打开多个浏览器标签页执行测试
- 可配置最大并发数
- 每个测试在独立的浏览器实例中执行
- 自动收集所有测试结果并生成报告

#### 使用方法

使用 `ConcurrentTestRunner` 执行并发测试：

```bash
python run_concurrent_tests.py
```

#### 配置说明

在 `run_concurrent_tests.py` 中配置：

```python
# 创建并发测试执行器
runner = ConcurrentTestRunner(max_workers=4)  # 设置最大并发数
```

#### 示例

项目提供了并发测试示例，包括：
- 测试首页
- 测试播放器页面
- 测试个人中心页面
- 测试搜索页面

每个测试在独立的浏览器实例中执行，互不影响。

## 注意事项

1. **配置文件**
   - 使用前请先配置 `config/settings.py` 中的邮件和定时任务参数
   - 确保邮件服务器信息正确

2. **截图功能**
   - 截图会占用磁盘空间，定期清理旧截图
   - 可通过 `enable_screenshots` 配置项控制是否启用截图

3. **并发执行**
   - 并发数不宜过高，建议 2-4 个
   - 确保系统资源充足

4. **定时任务**
   - 使用定时模式时，程序会一直运行
   - 按 Ctrl+C 可停止定时任务

5. **邮件发送**
   - 确保网络连接正常
   - 检查邮件服务器是否需要特殊配置（如 SSL/TLS）

## 故障排查

### 问题：截图未生成
- 检查 `enable_screenshots` 是否为 True
- 检查截图目录是否有写入权限

### 问题：邮件未发送
- 检查邮件配置是否正确
- 查看日志中的错误信息
- 确认邮件服务器是否允许发送

### 问题：定时任务未执行
- 检查 cron 表达式是否正确
- 查看日志中的定时任务启动信息
- 确认程序是否在运行

### 问题：并发测试失败
- 降低并发数
- 检查系统资源使用情况
- 查看日志中的错误信息
