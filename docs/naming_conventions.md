# 命名规范

本文档定义了项目中各种元素的命名规范。

## 文件命名

### 测试文件

- 格式：`test_*.py` 或 `*_test.py`
- 示例：
  - ✅ `test_profile.py`
  - ✅ `profile_test.py`
  - ❌ `ProfileTest.py`
  - ❌ `profiletest.py`

### 组件文件

- 格式：`*Component.py`
- 使用驼峰命名法
- 示例：
  - ✅ `ProfileComponent.py`
  - ✅ `DramaHomeComponent.py`
  - ❌ `profilecomponent.py`
  - ❌ `profile_component.py`

### 工具文件

- 格式：`*.py`
- 使用小写字母和下划线
- 示例：
  - ✅ `page_actions.py`
  - ✅ `logger_utils.py`
  - ❌ `PageActions.py`
  - ❌ `pageActions.py`

### 配置文件

- 格式：`*.py`
- 使用小写字母和下划线
- 示例：
  - ✅ `settings.py`
  - ✅ `locators.py`
  - ❌ `Settings.py`
  - ❌ `Locators.py`

## 类命名

### 测试类

- 格式：`Test*`
- 使用驼峰命名法
- 示例：
  - ✅ `class TestProfile:`
  - ✅ `class TestDramaHome:`
  - ❌ `class profile_test:`
  - ❌ `class ProfileTest:`

### 组件类

- 格式：`*Component`
- 使用驼峰命名法
- 示例：
  - ✅ `class ProfileComponent:`
  - ✅ `class DramaHomeComponent:`
  - ❌ `class profilecomponent:`
  - ❌ `class Profile_Component:`

### 工具类

- 格式：`*`
- 使用驼峰命名法
- 示例：
  - ✅ `class PageActions:`
  - ✅ `class LoggerUtils:`
  - ❌ `class page_actions:`
  - ❌ `class Page_Actions:`

## 方法命名

### 测试方法

- 格式：`test_*`
- 使用小写字母和下划线
- 示例：
  - ✅ `def test_top_up_button(self):`
  - ✅ `def test_vip_status(self):`
  - ❌ `def TestTopUpButton(self):`
  - ❌ `def testTopUpButton(self):`

### 组件方法

- 格式：`动词_名词`
- 使用小写字母和下划线
- 示例：
  - ✅ `def get_top_up_button(self):`
  - ✅ `def click_back_button(self):`
  - ❌ `def GetTopUpButton(self):`
  - ❌ `def getTopUpButton(self):`

### 工具方法

- 格式：`动词_名词`
- 使用小写字母和下划线
- 示例：
  - ✅ `def find_element(self, locator):`
  - ✅ `def click_element(self, locator):`
  - ❌ `def FindElement(self, locator):`
  - ❌ `def findElement(self, locator):`

## 变量命名

### 局部变量

- 使用小写字母和下划线
- 示例：
  - ✅ `top_up_button`
  - ✅ `transaction_history`
  - ❌ `topUpButton`
  - ❌ `transactionHistory`

### 实例变量

- 使用小写字母和下划线
- 示例：
  - ✅ `self.page`
  - ✅ `self.logger`
  - ❌ `self.Page`
  - ❌ `self.Logger`

### 类变量

- 使用大写字母和下划线
- 示例：
  - ✅ `BASE_URL`
  - ✅ `PROFILE_URL`
  - ❌ `baseUrl`
  - ❌ `profileUrl`

## 常量命名

### 配置常量

- 使用大写字母和下划线
- 示例：
  - ✅ `BASE_URL = "https://video.reelswave.net/"`
  - ✅ `PROFILE_URL = "https://video.reelswave.net/profile"`
  - ❌ `baseUrl = "https://video.reelswave.net/"`
  - ❌ `profileUrl = "https://video.reelswave.net/profile"`

### 定位器常量

- 使用小写字母和下划线
- 示例：
  - ✅ `"top_up_button": "text=Top UP"`
  - ✅ `"transaction_history": "text=Transaction History"`
  - ❌ `"topUpButton": "text=Top UP"`
  - ❌ `"transactionHistory": "text=Transaction History"`

## 函数命名

### 普通函数

- 格式：`动词_名词`
- 使用小写字母和下划线
- 示例：
  - ✅ `def get_element(locator):`
  - ✅ `def click_element(locator):`
  - ❌ `def GetElement(locator):`
  - ❌ `def getElement(locator):`

### 工厂函数

- 格式：`create_*` 或 `get_*`
- 使用小写字母和下划线
- 示例：
  - ✅ `def get_default_logger():`
  - ✅ `def create_page():`
  - ❌ `def GetDefaultLogger():`
  - ❌ `def getDefaultLogger():`

## 参数命名

### 普通参数

- 使用小写字母和下划线
- 示例：
  - ✅ `def find_element(self, locator, selector_type=None):`
  - ✅ `def click_element(self, locator, selector_type=None):`
  - ❌ `def find_element(self, Locator, SelectorType=None):`
  - ❌ `def find_element(self, locator, selectorType=None):`

### 可变参数

- 使用小写字母和下划线
- 示例：
  - ✅ `def func(*args, **kwargs):`
  - ❌ `def func(*Args, **Kwargs):`

## 返回值命名

### 布尔值

- 使用 `is_` 或 `has_` 前缀
- 示例：
  - ✅ `def is_element_exists(self, locator):`
  - ✅ `def has_vip_status(self):`
  - ❌ `def element_exists(self, locator):`
  - ❌ `def vip_status(self):`

### 元素对象

- 使用名词
- 示例：
  - ✅ `def get_top_up_button(self):`
  - ✅ `def get_vip_avatar(self):`
  - ❌ `def top_up_button(self):`
  - ❌ `def vip_avatar(self):`

### 文本内容

- 使用 `get_*_text` 格式
- 示例：
  - ✅ `def get_element_text(self, locator):`
  - ✅ `def get_button_text(self):`
  - ❌ `def element_text(self, locator):`
  - ❌ `def button_text(self):`

## 特殊命名

### 私有方法

- 使用 `_` 前缀
- 示例：
  - ✅ `def _get_element(self, locator):`
  - ✅ `def _format_locator(self, locator):`
  - ❌ `def get_element(self, locator):`
  - ❌ `def format_locator(self, locator):`

### 魔术方法

- 使用双下划线
- 示例：
  - ✅ `def __init__(self, page):`
  - ✅ `def __str__(self):`
  - ❌ `def init(self, page):`
  - ❌ `def str(self):`

### 回调函数

- 使用 `on_*` 格式
- 示例：
  - ✅ `def on_page_load(self):`
  - ✅ `def on_element_click(self):`
  - ❌ `def page_load(self):`
  - ❌ `def element_click(self):`

## 命名最佳实践

### 1. 使用描述性名称

```python
# ✅ 正确做法
def get_top_up_button(self):
    """获取充值按钮"""
    pass

# ❌ 错误做法
def get_btn(self):
    """获取按钮"""
    pass
```

### 2. 避免缩写

```python
# ✅ 正确做法
def get_transaction_history(self):
    """获取交易历史"""
    pass

# ❌ 错误做法
def get_tx_hist(self):
    """获取交易历史"""
    pass
```

### 3. 使用动词开头

```python
# ✅ 正确做法
def get_top_up_button(self):
    """获取充值按钮"""
    pass

def click_top_up_button(self):
    """点击充值按钮"""
    pass

# ❌ 错误做法
def top_up_button(self):
    """充值按钮"""
    pass
```

### 4. 保持一致性

```python
# ✅ 正确做法
def get_top_up_button(self):
    """获取充值按钮"""
    pass

def get_transaction_history(self):
    """获取交易历史"""
    pass

def get_vip_avatar(self):
    """获取VIP头像"""
    pass

# ❌ 错误做法
def get_top_up_button(self):
    """获取充值按钮"""
    pass

def transaction_history(self):
    """获取交易历史"""
    pass

def vip_avatar(self):
    """获取VIP头像"""
    pass
```

### 5. 避免使用保留字

```python
# ✅ 正确做法
def get_element(self, locator):
    """获取元素"""
    pass

# ❌ 错误做法
def class(self, locator):
    """获取元素"""
    pass

def return(self, locator):
    """获取元素"""
    pass
```
