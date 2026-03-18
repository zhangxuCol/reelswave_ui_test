# 中文测试报告与截图功能

## 功能概述

本次更新为你的测试项目添加了以下功能：

1. **中文 HTML 测试报告** - 美观的中文界面，包含：
   - 测试统计（总数/通过/失败/跳过）
   - 通过率进度条
   - 状态筛选（全部/通过/失败/跳过）
   - 可展开的测试详情
   - 响应式设计

2. **自动截图功能** - 支持：
   - 测试失败时自动截图
   - 手动在测试中截图
   - 每个测试用例显示截图缩略图
   - 点击缩略图放大查看

## 文件变更

### 新增文件

- `utils/screenshot_utils.py` - 截图工具类
- `utils/pytest_html_plugin.py` - 中文 HTML 报告插件
- `docs/screenshot_usage_example.py` - 使用示例文档

### 修改文件

- `conftest.py` - 添加截图钩子，自动捕获失败截图
- `pytest.ini` - 配置 pytest 选项

## 使用方法

### 方式1：使用 ScreenshotMixin（推荐）

测试类继承 `ScreenshotMixin`，然后调用 `take_screenshot()` 方法：

```python
from utils.screenshot_mixin import ScreenshotMixin

class TestDramaHome(ScreenshotMixin):
    def test_example(self):
        # 执行操作...
        
        # 手动截图
        self.take_screenshot(name="after_action")
        
        # 断言
        assert result
```

### 方式2：使用 screenshot_utils 夹具

在测试函数中使用 `screenshot_utils` 夹具：

```python
def test_example(self, page, screenshot_utils):
    # 执行操作...
    
    # 手动截图
    screenshot_utils.take_screenshot(page, name="step1")
    
    # 更多操作...
    screenshot_utils.take_screenshot(page, name="step2")
```

### 方式3：自动截图

测试失败时会自动截图，无需任何额外代码。

## 运行测试

```bash
# 运行单个测试文件
pytest page/drama_home_test.py -v

# 运行所有测试
pytest -v

# 运行带标记的测试
pytest -v -m smoke

# 并发运行
pytest -v -n 4
```

## 查看报告

测试完成后，报告会生成在 `reports/` 目录下：

- `report_YYYYMMDD_HHMMSS.html` - 中文 HTML 报告

打开报告可以看到：
- 测试统计概览
- 每个测试用例的结果
- 截图缩略图（如果有）
- 错误详情（失败时）

## 截图文件位置

截图保存在 `reports/screenshots/` 目录下，文件命名格式：
- `YYYYMMDD_HHMMSS_name.png` - 手动截图
- `YYYYMMDD_HHMMSS_failure_test_name.png` - 失败自动截图

## 注意事项

1. 截图功能依赖 DrissionPage 的 `get_screenshot()` 方法
2. 报告以 base64 格式嵌入截图，方便分享
3. 失败截图会自动附加到测试报告中
4. 每个测试用例的截图是独立的

## 示例截图

报告中每个测试用例会显示：
- 测试名称和描述
- 执行结果（通过/失败/跳过）
- 执行耗时
- 截图缩略图（可点击放大）
- 错误信息（失败时）
