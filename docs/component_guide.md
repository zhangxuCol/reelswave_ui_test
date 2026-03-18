# 组件开发指南

本文档详细说明如何开发和维护页面组件。

## 组件类结构

### 基本结构

```python
from utils.page_actions import PageActions
from utils.logger_utils import LoggerUtils
from config.locators import XXX_PAGE
from utils.decorators import element_wait_decorator


class XXXComponent:
    """XXX页面组件类"""

    def __init__(self, page):
        """
        初始化XXX页面组件
        :param page: 页面对象
        """
        self.page = page
        self.page_actions = PageActions(page)
        self.logger = LoggerUtils.get_default_logger()
        self.locators = XXX_PAGE
        self.logger.info("初始化XXX页面组件")
```

### 必需的初始化

每个组件类必须初始化以下属性：

```python
self.page = page                      # 页面对象
self.page_actions = PageActions(page) # 页面操作对象
self.logger = LoggerUtils.get_default_logger() # 日志记录器
self.locators = XXX_PAGE              # 定位器字典
```

## 组件方法规范

### 获取元素方法

```python
def get_xxx(self):
    """获取XXX元素"""
    self.logger.info("获取XXX")
    locator = self.locators["xxx"]
    # 根据定位器类型选择正确的选择器类型
    selector_type = None if locator.startswith("text=") else "css"
    # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception(f"Element not found for locator: {locator}")
    return element
```

### 点击元素方法

```python
def click_xxx(self):
    """点击XXX元素"""
    self.logger.info("点击XXX")
    xxx = self.get_xxx()
    xxx.click()
    self.logger.info("成功点击XXX")
```

### 等待页面加载方法

```python
def wait_for_page_load(self, timeout=20):
    """等待XXX页面加载完成"""
    self.logger.info("等待XXX页面加载完成...")
    locator = self.locators["xxx"]
    # 根据定位器类型选择正确的选择器类型
    selector_type = None if locator.startswith("text=") else "css"
    # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception("XXX页面加载超时或'XXX'元素未找到")
    self.logger.info("XXX页面加载完成")
```

### 返回上一页方法

```python
def back(self):
    """返回上一页"""
    self.page.back()
    self.logger.info("执行浏览器后退操作")

def click_back_button(self):
    """点击返回按钮"""
    self.logger.info("点击返回按钮")
    back_button = self.get_back_button()
    back_button.click()
    self.logger.info("成功点击返回按钮")
```

## 元素查找规范

### 单个元素查找

```python
def get_xxx(self):
    """获取XXX元素"""
    locator = self.locators["xxx"]
    selector_type = None if locator.startswith("text=") else "css"
    element = self.page_actions.find_element(locator, selector_type)
    return element
```

### 多个元素查找

```python
def get_xxx_list(self):
    """获取XXX元素列表"""
    locator = self.locators["xxx"]
    selector_type = None if locator.startswith("text=") else "css"
    elements = self.page_actions.find_elements(locator, selector_type)
    return elements
```

### 使用多个定位器

```python
def get_xxx(self):
    """获取XXX元素"""
    # 尝试多个定位器
    locators = [
        self.locators["xxx_1"],
        self.locators["xxx_2"],
        self.locators["xxx_3"]
    ]

    for locator in locators:
        selector_type = None if locator.startswith("text=") else "css"
        element = self.page_actions.find_element(locator, selector_type)
        if element:
            self.logger.info(f"成功找到元素，使用定位器: {locator}")
            return element

    raise Exception(f"未找到XXX元素，尝试了以下定位器: {locators}")
```

## 日志记录规范

### 信息日志

```python
self.logger.info("获取XXX")
self.logger.info("成功点击XXX")
self.logger.info("XXX页面加载完成")
```

### 错误日志

```python
self.logger.error(f"未找到XXX元素: {locator}")
self.logger.error(f"XXX页面加载超时")
```

### 调试日志

```python
self.logger.debug(f"当前页面URL: {self.page.url}")
self.logger.debug(f"元素定位器: {locator}")
```

## 异常处理规范

### 元素不存在

```python
def get_xxx(self):
    """获取XXX元素"""
    locator = self.locators["xxx"]
    selector_type = None if locator.startswith("text=") else "css"
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception(f"Element not found for locator: {locator}")
    return element
```

### 页面加载超时

```python
def wait_for_page_load(self, timeout=20):
    """等待XXX页面加载完成"""
    locator = self.locators["xxx"]
    selector_type = None if locator.startswith("text=") else "css"
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception("XXX页面加载超时或'XXX'元素未找到")
    self.logger.info("XXX页面加载完成")
```

## 定位器使用规范

### 获取定位器

```python
locator = self.locators["xxx"]
```

### 判断选择器类型

```python
selector_type = None if locator.startswith("text=") else "css"
```

### 使用定位器

```python
element = self.page_actions.find_element(locator, selector_type)
```

## 完整示例

### ProfileComponent 完整示例

```python
from utils.page_actions import PageActions
from utils.logger_utils import LoggerUtils
from config.locators import PROFILE_PAGE
from utils.decorators import element_wait_decorator


class ProfileComponent:
    """个人中心页面组件类"""

    def __init__(self, page):
        """
        初始化个人中心页面组件
        :param page: 页面对象
        """
        self.page = page
        self.page_actions = PageActions(page)
        self.logger = LoggerUtils.get_default_logger()
        self.locators = PROFILE_PAGE
        self.logger.info("初始化个人中心页面组件")

    def wait_for_page_load(self, timeout=20):
        """等待个人中心页面加载完成"""
        self.logger.info("等待个人中心页面加载完成...")
        locator = self.locators["top_up_button"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception("个人中心页面加载超时或'Top UP'按钮未找到")
        self.logger.info("个人中心页面加载完成")

    def back(self):
        """返回上一页"""
        self.page.back()
        self.logger.info("执行浏览器后退操作")

    def get_back_button(self):
        """获取返回按钮"""
        self.logger.info("获取返回按钮")
        self.logger.info(f"当前页面URL: {self.page.url}")

        # 尝试多个定位器
        locator = self.locators["profile_back_button"]

        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if element:
            self.logger.info(f"成功找到元素，使用定位器: {locator}")
            return element

        if not element:
            raise Exception(f"未找到返回按钮，尝试了以下定位器: {locator}")

    def click_back_button(self):
        """点击返回按钮"""
        self.logger.info("点击返回按钮")
        back_button = self.get_back_button()
        back_button.click()
        self.logger.info("成功点击返回按钮")

    def get_top_up_button(self):
        """获取充值按钮"""
        self.logger.info("获取充值按钮")
        locator = self.locators["top_up_button"]
        # 根据定位器类型选择正确的选择器类型
        selector_type = None if locator.startswith("text=") else "css"
        # 使用 PageActions 的 find_element 方法，装饰器会自动处理等待
        element = self.page_actions.find_element(locator, selector_type)
        if not element:
            raise Exception(f"Element not found for locator: {locator}")
        return element
```

## 最佳实践

### 1. 方法命名

- 获取元素：`get_xxx()`
- 点击元素：`click_xxx()`
- 获取文本：`get_xxx_text()`
- 检查存在：`is_xxx_exists()`

### 2. 日志记录

- 每个方法开始时记录日志
- 关键操作后记录日志
- 错误时记录错误日志

### 3. 异常处理

- 元素不存在时抛出异常
- 提供清晰的错误信息
- 包含定位器信息

### 4. 代码复用

- 避免重复代码
- 提取公共方法
- 使用 PageActions 的通用方法

### 5. 文档字符串

- 每个方法都应有文档字符串
- 简洁描述方法功能
- 说明参数和返回值
