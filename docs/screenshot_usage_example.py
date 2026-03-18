"""
截图功能使用示例

在测试中使用截图的几种方式：

1. 自动截图：测试失败时自动捕获失败截图
2. 手动截图：在测试中主动调用 screenshot_utils.take_screenshot()

示例代码：

import pytest
from utils.screenshot_utils import get_screenshot_utils

@pytest.mark.drama_home
class TestDramaHome:
    """首页测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, drama_home_page):
        self.page = drama_home_page
        self.screenshot = get_screenshot_utils()  # 获取截图工具

    def test_back_button(self):
        \"\"\"测试返回按钮 - 自动在失败时截图\"\"\"
        # 执行测试...
        assert self.drama_home.click_back_button()
        
        # 手动截图（可选）
        self.screenshot.take_screenshot(self.page, name="back_button_clicked")
        
    def test_complex_flow(self):
        \"\"\"测试复杂流程 - 多步骤截图\"\"\"
        # 步骤1截图
        self.screenshot.take_screenshot(self.page, name="step1_initial")
        
        # 执行操作...
        
        # 步骤2截图
        self.screenshot.take_screenshot(self.page, name="step2_after_click")
        
        # 更多操作...
        
        # 最终截图
        self.screenshot.take_screenshot(self.page, name="step3_final")

生成的报告特点：
- 全中文界面（标题、按钮、状态等）
- 每个测试用例显示截图缩略图
- 点击缩略图可以放大查看
- 失败测试自动标记为红色
- 支持筛选：全部/通过/失败/跳过
- 显示通过率进度条
- 截图以 base64 嵌入，方便分享
"""
