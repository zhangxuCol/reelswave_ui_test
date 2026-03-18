# 项目架构说明

## 目录结构

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

## 设计模式

### 1. 页面对象模式 (POM)

项目采用页面对象模式，将页面元素和操作封装在组件类中：

- **组件层** (`components/`): 封装页面元素和操作
- **测试层** (`page/`): 使用组件进行测试
- **工具层** (`utils/`): 提供通用功能

### 2. 装饰器模式

使用装饰器统一处理元素等待逻辑：

```python
@element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    element = self._get_element(locator, selector_type)
    return element if element else None
```

### 3. 工厂模式

使用 PageActions 类作为工厂，提供统一的页面操作方法：

```python
class PageActions:
    """页面基础操作类，封装常用的元素操作方法"""

    def find_element(self, locator, selector_type=None):
        """查找单个元素"""
        pass

    def click_element(self, locator, selector_type=None):
        """点击元素"""
        pass

    # ... 更多方法
```

## 核心组件

### 1. PageActions 类

位置：`utils/page_actions.py`

功能：
- 封装所有页面操作方法
- 提供统一的元素查找、点击、获取文本等操作
- 使用装饰器自动处理元素等待

关键方法：
- `find_element()`: 查找单个元素
- `find_elements()`: 查找多个元素
- `click_element()`: 点击元素
- `get_element_text()`: 获取元素文本
- `is_element_exists()`: 检查元素是否存在
- `wait_for_element()`: 等待元素出现

### 2. element_wait_decorator 装饰器

位置：`utils/decorators.py`

功能：
- 自动处理元素等待逻辑
- 支持 "clickable"（可点击）和 "exists"（存在）两种等待类型
- 可配置超时时间和错误处理方式

参数说明：
- `wait_type`: 等待类型，支持 "clickable"（可点击）和 "exists"（存在）
- `timeout`: 超时时间（秒），默认为 8 秒
- `raise_err`: 未找到元素时是否抛出异常，默认为 False

### 3. 组件类

位置：`components/`

功能：
- 封装特定页面的元素和操作
- 使用 PageActions 进行元素操作
- 提供高层级的页面操作方法

示例：ProfileComponent

```python
class ProfileComponent:
    """个人中心页面组件类"""

    def __init__(self, page):
        """初始化组件"""
        self.page = page
        self.page_actions = PageActions(page)
        self.logger = LoggerUtils.get_default_logger()
        self.locators = PROFILE_PAGE

    def get_top_up_button(self):
        """获取充值按钮"""
        locator = self.locators["top_up_button"]
        selector_type = None if locator.startswith("text=") else "css"
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element
```

### 4. 测试类

位置：`page/`

功能：
- 使用组件进行测试
- 使用 pytest 框架组织测试
- 使用装饰器标记测试类型

示例：TestProfile

```python
@pytest.mark.profile
class TestProfile:
    """个人中心测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """测试夹具，在每个测试方法前执行"""
        self.logger = LoggerUtils.get_default_logger()
        self.page = page
        self.profile = ProfileComponent(self.page)
        self.page.get(PROFILE_URL)
        self.profile.wait_for_page_load()

    @pytest.mark.smoke
    def test_top_up_button(self):
        """测试充值按钮"""
        top_up_button = self.profile.get_top_up_button()
        assert top_up_button is not None, "未找到充值按钮"
        top_up_button.click()
        self.page.wait(5)
        self.profile.click_back_button()
        self.page.wait(2)
```

## 数据流

1. **测试层** 调用 **组件层** 的方法
2. **组件层** 使用 **PageActions** 进行元素操作
3. **PageActions** 使用 **装饰器** 自动处理元素等待
4. **装饰器** 使用 DrissionPage 的等待机制等待元素
5. **PageActions** 返回元素对象给 **组件层**
6. **组件层** 返回元素对象给 **测试层**
7. **测试层** 进行断言和验证

## 扩展指南

### 添加新页面组件

1. 在 `components/` 目录下创建新的组件文件
2. 继承或使用 `PageActions` 类进行元素操作
3. 在 `config/locators.py` 中添加页面定位器
4. 在 `page/` 目录下创建对应的测试文件

### 添加新测试用例

1. 在对应的测试文件中添加测试方法
2. 使用 `@pytest.mark.xxx` 标记测试类型
3. 使用组件的方法进行元素操作
4. 使用 `assert` 进行断言
5. 使用 `self.logger` 记录日志

### 添加新工具方法

1. 在 `utils/` 目录下的相应文件中添加方法
2. 确保方法符合现有的代码风格
3. 添加适当的日志记录
4. 更新相关文档
