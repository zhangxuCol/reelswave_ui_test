# ReelsWave Web 自动化测试框架

## 概述

这是一个基于 DrissionPage 的 Web 自动化测试框架，用于测试 ReelsWave 视频平台的各种页面功能。框架采用页面对象模式（POM）设计，提供了组件化、模块化的测试结构，支持移动端模拟、页面元素操作、HTML 解析等多种功能。

## 目录结构

```
reelswave_web_test/
├── components/             # 页面组件模块
│   ├── CarouselComponent.py    # 轮播图组件
│   ├── DramaHomeComponent.py   # 短剧首页组件
│   └── ProfileComponent.py     # 个人中心组件
├── config/                 # 配置文件
│   ├── locators.py            # 页面元素定位器配置
│   └── settings.py            # 应用配置（URL等）
├── html_files/             # 存储各个页面的HTML文件
├── page/                   # 页面测试模块
│   ├── base.py                # 基础页面类（包含浏览器操作）
│   ├── Home.py                # 首页测试
│   ├── drama_home_test.py     # 短剧首页测试
│   ├── player.py              # 播放器测试
│   ├── player_pytest.py       # 播放器 pytest 测试
│   └── profile_test.py        # 个人中心测试
├── recordjson/             # JSON录制回放模块
├── retest/                 # 重测试模块
└── utils/                  # 工具模块
    ├── decorators.py           # 装饰器（元素等待等）
    ├── html_parser.py          # HTML解析工具
    ├── json_transfer_driss.py  # JSON转换工具
    ├── logger_utils.py         # 日志工具
    └── page_actions.py         # 页面操作封装
```

## 使用步骤

### 1. 环境准备

确保已安装以下依赖：
- DrissionPage
- pytest
- BeautifulSoup4
- psutil

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

### 3. 运行测试

#### 运行单个测试文件

```bash
# 运行个人中心测试
pytest page/profile_test.py

# 运行播放器测试
pytest page/player_pytest.py
```

#### 运行所有测试

```bash
# 运行所有测试文件
pytest page/
```

### 4. 使用页面组件

框架提供了多个页面组件，可以直接使用：

```python
from page.base import open_mobile_browser
from components.ProfileComponent import ProfileComponent

# 打开浏览器
page = open_mobile_browser()

# 创建个人中心组件
profile = ProfileComponent(page)

# 执行操作
profile.click_user_avatar()
profile.click_settings()
```

### 5. 添加新的页面组件

1. 在 `components/` 目录下创建新的组件文件
2. 继承或使用 `PageActions` 类进行元素操作
3. 在 `config/locators.py` 中添加页面定位器
4. 在 `page/` 目录下创建对应的测试文件

## 工作流程

### 页面组件开发流程

1. **分析页面结构**：了解需要测试的页面元素和交互
2. **定义定位器**：在 `config/locators.py` 中添加页面元素的定位器
3. **创建组件**：在 `components/` 目录下创建页面组件类
4. **实现操作方法**：使用 `PageActions` 类实现页面元素的交互操作
5. **编写测试**：在 `page/` 目录下创建测试文件，使用组件进行测试

### HTML 解析流程

1. **保存页面HTML**：将需要测试的页面HTML保存到 `html_files/` 目录
2. **解析HTML**：使用 `HTMLParser` 类解析HTML文件
3. **提取元素**：从HTML中提取所有可交互元素的CSS路径
4. **生成定位器**：根据提取的元素信息生成定位器配置

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

### 4. 日志记录

使用 `LoggerUtils` 类进行统一的日志记录：

```python
from utils.logger_utils import LoggerUtils

logger = LoggerUtils.get_default_logger()
logger.info("这是一条信息日志")
logger.error("这是一条错误日志")
```

## 可交互元素的识别标准

HTML 解析器会识别以下类型的元素：

- 标签：`a`, `button`, `input`, `select`, `textarea`, `option`, `div`, `span`, `img`, `li`
- 类名包含：`button`, `btn`, `click`, `link`, `tab`, `menu`, `nav`, `icon`, `switch`, `toggle`, `select`, `dropdown`, `checkbox`, `radio`, `item`, `card`, `list`, `avatar`, `action`, `header`, `footer`, `toolbar`, `bar`, `control`, `panel`, `section`
- role属性：`button`, `link`, `tab`, `menuitem`, `checkbox`, `radio`
- 具有 `onclick` 属性的元素

## 注意事项

1. 确保HTML文件是最新的，反映当前页面的结构
2. 某些元素可能会导致页面跳转，需要在测试中处理这种情况
3. 如果某个元素无法点击或导致错误，框架会记录错误并继续测试
4. 建议在测试环境中运行，避免对生产环境造成影响
5. 使用移动端模拟时，注意响应式布局可能导致的元素定位问题

## 常见问题

### Q: 如何修改等待时间？

A: 可以在 `page_actions.py` 中修改 `element_wait_decorator` 的 `timeout` 参数，或者在具体方法中自定义等待时间。

### Q: 如何添加新的页面组件？

A: 参考 `ProfileComponent.py` 的实现，在 `components/` 目录下创建新的组件文件，使用 `PageActions` 类实现元素操作。

### Q: 如何调试元素定位问题？

A: 可以使用 `LoggerUtils` 记录详细的日志，或者使用浏览器的开发者工具检查元素定位器是否正确。
