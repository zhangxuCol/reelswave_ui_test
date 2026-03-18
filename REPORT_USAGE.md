# 中文测试报告使用说明

## 功能特性

1. **中文报告界面** - 完全中文化的测试报告，包含统计信息和测试结果
2. **截图支持** - 每个测试用例都会自动捕获关键步骤的截图
3. **失败自动截图** - 测试失败时会自动捕获失败截图
4. **交互式界面** - 支持筛选（全部/通过/失败/跳过）和点击查看大图

## 使用方法

### 1. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定标记的测试
pytest -m smoke

# 运行单个测试文件
pytest page/drama_home_test.py

# 并发运行
pytest -n 4
```

### 2. 查看报告

测试完成后，报告会自动生成在 `reports/` 目录下，文件名为 `report_YYYYMMDD_HHMMSS.html`。

报告包含：
- 📊 统计概览（总用例数、通过、失败、跳过、通过率、总耗时）
- 🔍 筛选功能（按状态筛选测试用例）
- 📝 详细测试列表（每个用例的名称、描述、状态、耗时）
- 📸 测试截图（每个用例的截图，点击可放大）
- ❌ 错误信息（失败的用例显示详细错误信息）

### 3. 在测试中添加截图

测试类继承 `ScreenshotMixin` 类，然后使用 `take_screenshot()` 方法：

```python
from utils.screenshot_mixin import ScreenshotMixin

class TestDramaHome(ScreenshotMixin):
    def test_back_button(self):
        """测试点击返回按钮"""
        result = self.drama_home.click_back_button()
        # 操作完成后截图
        self.take_screenshot(name="after_click_back")
        assert result, "点击返回按钮失败"
```

### 4. 自动截图

- **页面加载完成后**：自动截图
- **关键操作后**：手动调用 `take_screenshot()`
- **测试失败时**：自动捕获失败截图

## 配置文件

### pytest.ini

```ini
[pytest]
addopts =
    -v
    -s
    --strict-markers
    --tb=short
    --disable-warnings
    --color=yes
    -p utils.pytest_html_plugin  # 加载中文报告插件
```

### config/settings.py

```python
REPORT_CONFIG = {
    "base_dir": "reports",
    "screenshot_dir": "reports/screenshots",
    "enable_screenshots": True
}
```

## 目录结构

```
reports/
├── report_YYYYMMDD_HHMMSS.html  # 测试报告
├── screenshots/                  # 截图目录
│   ├── YYYYMMDD_HHMMSS_xxx.png
│   └── ...
└── html/                         # pytest-html 生成的报告（保留）
```

## 注意事项

1. 截图文件会自动保存到 `reports/screenshots/` 目录
2. 报告中的截图使用 base64 编码嵌入，可以直接在浏览器中打开查看
3. 测试失败后会自动捕获当前页面状态
4. 可以使用 `screenshot_utils.clean_old_screenshots(days=7)` 清理旧截图
