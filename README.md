# ReelsWave Web 自动化测试框架

## 项目简介

这是一个基于 DrissionPage 和 pytest 的 Web 自动化测试项目，用于测试 ReelsWave 网站的各项功能。框架采用页面对象模式（POM）设计，提供了组件化、模块化的测试结构，支持移动端模拟、页面元素操作、HTML 解析等多种功能。

## 项目结构

```
reelswave_web_test/
├── components/             # 页面组件模块
│   ├── CarouselComponent.py    # 轮播图组件
│   ├── DramaHomeComponent.py   # 短剧首页组件
│   ├── PlayerIconComponent.py  # 播放器图标组件
│   └── ProfileComponent.py     # 个人中心组件
├── config/                 # 配置文件
│   ├── locators.py            # 页面元素定位器配置
│   └── settings.py            # 应用配置（URL等）
├── html_files/             # 存储各个页面的HTML文件
├── page/                   # 页面测试模块
│   ├── base.py                # 基础页面类和测试基类
│   ├── drama_home_test.py     # 短剧首页测试
│   ├── player_test.py       # 播放器测试
│   └── profile_test.py        # 个人中心测试
├── utils/                  # 工具模块
│   ├── decorators.py           # 装饰器（元素等待等）
│   ├── logger_utils.py         # 日志工具
│   └── page_actions.py         # 页面操作封装
├── conftest.py            # pytest 配置文件
├── pytest.ini              # pytest 配置文件
└── requirements.txt         # 依赖包列表
```

## 环境准备

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 配置测试环境

在 `config/settings.py` 中配置测试环境：

```python
# 基础地址
BASE_URL = "https://video.reelswave.net/"

# 测试首页地址
TEST_HOME_URL = "https://video.reelswave.net/content/286606456962772992?chapterIndex=1"

# 个人中心页面地址
PROFILE_URL = "https://video.reelswave.net/profile"
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest page/drama_home_test.py
pytest page/player_test.py
pytest page/profile_test.py
```

### 运行特定测试类

```bash
pytest page/drama_home_test.py::TestDramaHome
pytest page/player_test.py::TestPlayer
pytest page/profile_test.py::TestProfile
```

### 运行特定测试方法

```bash
pytest page/drama_home_test.py::TestDramaHome::test_back_button
pytest page/player_test.py::TestPlayer::test_pause_play
pytest page/profile_test.py::TestProfile::test_top_up_button
pytest page/profile_test.py::TestProfile::test_vip_status
```

### 使用标记运行测试

```bash
# 运行冒烟测试
pytest -m smoke

# 运行回归测试
pytest -m regression

# 运行短剧首页测试
pytest -m drama_home

# 运行播放器测试
pytest -m player

# 运行个人中心测试
pytest -m profile
```

### 并行运行测试

```bash
# 使用 4 个进程并行运行测试
python run_test.py concurrent

# 使用 8 个进程并行运行测试
python run_test.py concurrent -n 8

# 使用 2 个进程运行单个测试文件
python run_test.py concurrent -n 2 page/drama_home_test.py
```

注意：并行运行测试时，每个浏览器会固定执行一个测试类中的所有测试方法，测试类执行完毕后才关闭浏览器。

### 生成测试报告

```bash
# 生成中文 HTML 测试报告（单文件测试）
python run_test.py single page/drama_home_test.py

# 生成中文 HTML 测试报告（并发测试）
python run_test.py concurrent

# 生成 XML 测试报告（用于 CI/CD）
pytest --junitxml=reports/report.xml
```

测试报告特点：
- 中文界面，易于阅读
- 包含测试结果统计（总数、通过、失败、通过率）
- 显示每个测试用例的执行耗时
- 支持按状态筛选（全部、通过、失败）
- 关联测试截图，可点击查看
- 报告文件名包含时间戳，避免覆盖

## 测试标记说明

- `smoke`: 冒烟测试，验证核心功能是否正常
- `regression`: 回归测试，验证功能是否正常工作
- `drama_home`: 短剧首页相关测试
- `player`: 播放器相关测试
- `profile`: 个人中心相关测试
- `carousel`: 轮播图相关测试

## 个人中心测试用例

个人中心测试包含以下测试用例：

1. `test_top_up_button` - 测试充值按钮
   - 验证充值按钮是否存在
   - 点击充值按钮
   - 返回上一页

2. `test_transaction_history_link` - 测试交易历史链接
   - 验证交易历史链接是否存在
   - 点击交易历史链接
   - 返回上一页

3. `test_my_list_and_history_link` - 测试我的列表和历史记录链接
   - 验证我的列表和历史记录链接是否存在
   - 点击我的列表和历史记录链接
   - 返回上一页

4. `test_contact_us_link` - 测试联系我们链接
   - 验证联系我们链接是否存在
   - 点击联系我们链接
   - 返回上一页

5. `test_settings_link` - 测试设置链接
   - 验证设置链接是否存在
   - 点击设置链接
   - 返回上一页

6. `test_vip_status` - 测试VIP状态
   - 验证VIP头像是否存在
   - 点击VIP头像
   - 返回上一页

## 测试夹具（Fixtures）

### page
类级别的夹具，为每个测试类提供一个页面对象。在并发模式下，每个浏览器固定执行一个测试类中的所有测试方法，测试类执行完毕后才关闭浏览器。

### drama_home_page
类级别的夹具，提供短剧首页的页面对象。在并发模式下，每个浏览器固定执行短剧首页测试类中的所有测试方法，测试类执行完毕后才关闭浏览器。

### player_page
类级别的夹具，提供播放器页面的页面对象。在并发模式下，每个浏览器固定执行播放器测试类中的所有测试方法，测试类执行完毕后才关闭浏览器。

### profile_page
类级别的夹具，提供个人中心页面的页面对象。在并发模式下，每个浏览器固定执行个人中心测试类中的所有测试方法，测试类执行完毕后才关闭浏览器。

## 编写测试

### 测试类结构

```python
import pytest
from page.base import BaseTest

@pytest.mark.drama_home
class TestDramaHome(BaseTest):
    """测试类描述"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """测试夹具，在每个测试方法前执行"""
        self.logger = LoggerUtils.get_default_logger()
        self.page = page
        # 其他初始化代码...

    @pytest.mark.smoke
    def test_example(self):
        """测试方法描述"""
        # 测试代码
        assert True, "断言失败时的错误信息"
```

### 测试方法命名规范

- 测试方法必须以 `test_` 开头
- 测试类必须以 `Test` 开头
- 测试文件必须以 `test_` 开头或以 `_test.py` 结尾

## 核心功能

### 1. 移动端模拟

框架支持移动端浏览器模拟，使用 iPhone Safari UA：

```python
from page.base import open_mobile_browser

# 打开移动端浏览器
page = open_mobile_browser()
```

### 2. 页面操作封装

`PageActions` 类提供了丰富的页面操作方法：

- `find_element`: 查找单个元素
- `find_elements`: 查找多个元素
- `click_element`: 点击元素
- `get_element_text`: 获取元素文本
- `is_element_exists`: 检查元素是否存在
- `wait_for_element`: 等待元素出现

### 3. 元素等待装饰器

使用 `element_wait_decorator` 装饰器可以自动等待元素：

```python
from utils.decorators import element_wait_decorator

class MyComponent:
    @element_wait_decorator(wait_type="clickable", timeout=10)
    def click_button(self, locator):
        # 装饰器会自动等待元素可点击
        element = self.find_element(locator)
        element.click()
```

装饰器参数说明：
- `wait_type`: 等待类型，支持 "clickable"（可点击）和 "exists"（存在）
- `timeout`: 超时时间（秒），默认为 8 秒
- `raise_err`: 未找到元素时是否抛出异常，默认为 False

装饰器会自动处理元素等待逻辑，无需在方法中手动调用 `element.wait.clickable()` 或 `element.wait.displayed()`。

### 4. 日志记录

使用 `LoggerUtils` 类进行统一的日志记录：

```python
from utils.logger_utils import LoggerUtils

logger = LoggerUtils.get_default_logger()
logger.info("这是一条信息日志")
logger.error("这是一条错误日志")
```

## 添加新的页面组件

1. 在 `components/` 目录下创建新的组件文件
2. 继承或使用 `PageActions` 类进行元素操作
3. 在 `config/locators.py` 中添加页面定位器
4. 在 `page/` 目录下创建对应的测试文件

## 注意事项

1. 所有测试方法都应该使用 `assert` 语句进行断言
2. 使用装饰器 `@pytest.mark.xxx` 来标记测试
3. 使用夹具（fixture）来管理测试资源
4. 避免使用 `page.wait()` 固定等待，优先使用条件等待
5. 测试失败时会自动截图（如果配置了截图功能）
6. 确保HTML文件是最新的，反映当前页面的结构
7. 建议在测试环境中运行，避免对生产环境造成影响
8. 使用移动端模拟时，注意响应式布局可能导致的元素定位问题

## 代码规范

### 减少重复代码

在编写测试代码时，应遵循 DRY（Don't Repeat Yourself）原则，避免重复代码。当发现代码中有重复的逻辑时，应该将其提取为辅助方法或工具函数。

#### 示例

**不推荐的做法（重复代码）：**

```python
def test_pause_play(self):
    # 第一次点击
    max_attempts = 3
    for attempt in range(max_attempts):
        if not self.player_control.is_player_menu_open():
            video_player.click()
            self.logger.info("操作成功")
            break
        else:
            self.logger.warning(f"播放器菜单已打开，等待 3 秒后再次检查 (尝试 {attempt + 1}/{max_attempts})")
            self.page.wait(3)
            video_player = self.player_control.play_pause()
            assert video_player is not None, "未找到播放器元素"
    else:
        self.logger.error(f"等待 {max_attempts * 3} 秒后，播放器菜单仍然打开")
        raise AssertionError("播放器菜单仍然打开，无法执行点击操作")

    # 第二次点击（完全相同的代码）
    max_attempts = 3
    for attempt in range(max_attempts):
        if not self.player_control.is_player_menu_open():
            video_player.click()
            self.logger.info("操作成功")
            break
        else:
            self.logger.warning(f"播放器菜单已打开，等待 3 秒后再次检查 (尝试 {attempt + 1}/{max_attempts})")
            self.page.wait(3)
            video_player = self.player_control.play_pause()
            assert video_player is not None, "未找到播放器元素"
    else:
        self.logger.error(f"等待 {max_attempts * 3} 秒后，播放器菜单仍然打开")
        raise AssertionError("播放器菜单仍然打开，无法执行点击操作")
```

**推荐的做法（提取辅助方法）：**

```python
def _click_video_player(self, video_player, action_name="点击播放器"):
    """
    点击播放器，如果播放器菜单已打开则等待后重试

    :param video_player: 播放器元素
    :param action_name: 操作名称，用于日志记录
    :raises AssertionError: 如果所有尝试都失败
    """
    max_attempts = 3
    for attempt in range(max_attempts):
        if not self.player_control.is_player_menu_open():
            video_player.click()
            self.logger.info(f"{action_name}操作成功")
            break
        else:
            self.logger.warning(f"播放器菜单已打开，等待 3 秒后再次检查 (尝试 {attempt + 1}/{max_attempts})")
            self.page.wait(3)
            video_player = self.player_control.play_pause()
            assert video_player is not None, "未找到播放器元素"
    else:
        self.logger.error(f"等待 {max_attempts * 3} 秒后，播放器菜单仍然打开")
        raise AssertionError("播放器菜单仍然打开，无法执行点击操作")

    return video_player

def test_pause_play(self):
    # 第一次点击
    video_player = self._click_video_player(video_player, "唤起播放器菜单")

    # 第二次点击
    video_player = self._click_video_player(video_player, "执行暂停操作")
```

#### 优势

1. **减少重复代码**：将相同的逻辑封装到一个方法中，避免了代码重复。
2. **提高可维护性**：如果需要修改逻辑，只需要修改一个地方。
3. **提高可读性**：代码更加简洁，易于理解。
4. **统一错误处理**：所有操作都使用相同的错误处理机制。

#### 应用场景

当以下情况出现时，应该考虑提取辅助方法：

1. 相同或相似的代码块在多个地方出现
2. 代码块长度超过 10 行，且在多个地方重复使用
3. 需要对多个元素执行相同的操作序列
4. 需要统一处理某种错误或异常情况

#### 命名规范

辅助方法的命名应该清晰表达其功能，通常使用 `_` 前缀表示这是内部方法：

- `_click_video_player`: 点击播放器
- `_ensure_player_menu_open`: 确保播放器菜单打开
- `_wait_for_element_visible`: 等待元素可见

## 常见问题

### Q: 如何修改等待时间？

A: 可以在 `page_actions.py` 中修改 `element_wait_decorator` 的 `timeout` 参数，或者在具体方法中自定义等待时间。

### Q: 如何添加新的页面组件？

A: 参考 `ProfileComponent.py` 的实现，在 `components/` 目录下创建新的组件文件，使用 `PageActions` 类实现元素操作。

### Q: 如何跳过某个测试？

A: 使用 `@pytest.mark.skip` 装饰器：

```python
@pytest.mark.skip(reason="功能尚未实现")
def test_example(self):
    pass
```

### Q: 如何预期测试失败？

A: 使用 `@pytest.mark.xfail` 装饰器：

```python
@pytest.mark.xfail(reason="已知问题，待修复")
def test_example(self):
    assert False
```

### Q: 如何参数化测试？

A: 使用 `@pytest.mark.parametrize` 装饰器：

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])
def test_example(self, input, expected):
    assert input * 2 == expected
```

## 可交互元素的识别标准

HTML 解析器会识别以下类型的元素：

- 标签：`a`, `button`, `input`, `select`, `textarea`, `option`, `div`, `span`, `img`, `li`
- 类名包含：`button`, `btn`, `click`, `link`, `tab`, `menu`, `nav`, `icon`, `switch`, `toggle`, `select`, `dropdown`, `checkbox`, `radio`, `item`, `card`, `list`, `avatar`, `action`, `header`, `footer`, `toolbar`, `bar`, `control`, `panel`, `section`
- role属性：`button`, `link`, `tab`, `menuitem`, `checkbox`, `radio`
- 具有 `onclick` 属性的元素

### Q: 如何调试元素定位问题？

A: 可以使用 `LoggerUtils` 记录详细的日志，或者使用浏览器的开发者工具检查元素定位器是否正确。

## 技术栈限定
测试报告：基于 pytest-html（基础 HTML 报告）+ pytest-metadata（补充自定义维度：耗时、截图），或 allure-pytest（更强大的筛选 / 截图关联）；
定时执行：使用 schedule 库（简单 cron 表达式）或 APScheduler（工业级定时任务）；
邮件发送：使用 smtplib + email 标准库；
工具存放路径：/Users/zhangxu/work/script-test/reelswave_web_test/utils


## 截图功能
① 每个测试用例（case）每一步操作生成截图（如打开网页、点击按钮、输入内容等）；
② 截图命名规则：{用例名}_{步骤序号}_{操作描述}.png（如 test_login_01_打开登录页.png）；
③ 截图存储路径：reports/screenshots/{测试日期}/{用例名}/（按日期 + 用例名分层）。
4 单条用例执行耗时统计精准到毫秒，截图生成不阻塞测试流程；
5 步骤截图：通过 Playwright 的 page.screenshot() 在每个操作后调用，而非用例结束才截图；
6 截图关联：在 pytest 报告的每个用例条目后添加截图链接（HTML 报告中可点击查看）。

## 测试报告
使用：allure-pytest（更强大的筛选 / 截图关联）
① 核心维度：用例名称、执行状态（通过 / 失败）、执行耗时（精确到毫秒）、截图关联；
② 筛选能力：报告支持按「通过 / 失败」筛选，筛选后仅展示对应状态的用例名 + 截图（可点击查看 / 下载）；
③ 报告格式：HTML 格式（可视化）+ 可选 JSON 格式（便于二次处理）；
④ 报告存储：reports/html/{测试日期}_test_report.html。
5 用例执行失败时，除截图外，记录详细报错信息（堆栈、报错行）到报告；
6 定时任务执行失败时，触发邮件通知并记录错误日志；
7 截图 / 报告生成失败时，不中断整体测试流程，仅记录警告日志。

## 定时功能
① 配置化：config 中配置定时规则（支持 cron 表达式 / 固定时间）；
② 定时触发：按配置自动执行全套测试，无需手动触发；
③ 定时日志：记录定时任务的启动 / 结束时间、执行结果。

## 邮件通知
① 触发时机：测试执行完成后（无论成功 / 失败）立即发送；
② 收件人：固定为 zhangxu@col.com；
③ 邮件内容：
- 标题：【网页自动化测试报告】{测试日期} - 总用例数：X，通过：X，失败：X；
- 正文：核心统计（总耗时、通过 / 失败数）+ 测试报告下载链接 / 附件；
- 附件：HTML 测试报告（必带）、可选压缩后的截图包；
④ 邮件配置：SMTP 信息（服务器、端口、发件人账号 / 密码）统一配置在 config 中。

## 并发执行

### 并发测试特点

框架支持并发测试，可以同时打开多个浏览器执行不同测试类中的测试用例：

1. **测试类级别并发**：每个浏览器固定执行一个测试类中的所有测试方法
2. **浏览器复用**：测试类中的所有测试方法共享同一个浏览器实例，测试类执行完毕后才关闭浏览器
3. **独立端口**：每个浏览器使用不同的端口号（9223, 9224, 9225, 9226 等），避免端口冲突
4. **中文报告**：生成中文测试报告，包含测试结果、耗时和截图
5. **时间戳**：报告文件名包含时间戳，避免报告被覆盖

### 运行并发测试

```bash
# 运行所有测试，使用 4 个进程
python run_test.py concurrent

# 运行所有测试，指定进程数
python run_test.py concurrent -n 8

# 运行单个测试文件，使用 2 个进程
python run_test.py concurrent -n 2 page/drama_home_test.py
```

### 并发测试配置

并发测试的配置位于 `pytest.ini` 和 `conftest.py` 中：

1. **pytest.ini**：配置 `--dist=loadscope` 选项，使每个测试类被分发到不同的 worker
2. **conftest.py**：
   - `page` fixture：类级别的夹具，为每个测试类提供浏览器实例
   - `player_page` fixture：类级别的夹具，为播放器测试提供浏览器实例
   - `drama_home_page` fixture：类级别的夹具，为短剧首页测试提供浏览器实例

### 并发测试示例

假设有 4 个测试类：
- `TestDramaHome`：短剧首页测试
- `TestPlayer`：播放器测试
- `TestProfile`：个人中心测试
- `TestSearch`：搜索页面测试

使用 4 个进程并发执行时：
- 浏览器 1（端口 9223）：执行 `TestDramaHome` 中的所有测试方法
- 浏览器 2（端口 9224）：执行 `TestPlayer` 中的所有测试方法
- 浏览器 3（端口 9225）：执行 `TestProfile` 中的所有测试方法
- 浏览器 4（端口 9226）：执行 `TestSearch` 中的所有测试方法

每个浏览器在执行完对应测试类的所有测试方法后才会关闭。



