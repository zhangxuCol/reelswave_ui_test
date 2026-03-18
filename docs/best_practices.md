# 最佳实践

本文档总结了项目开发中的最佳实践，帮助团队保持代码质量和一致性。

## 代码组织

### 1. 遵循项目架构

- 严格按照项目架构组织代码
- 组件放在 `components/` 目录
- 测试放在 `page/` 目录
- 工具放在 `utils/` 目录
- 配置放在 `config/` 目录

### 2. 使用页面对象模式

- 将页面元素和操作封装在组件类中
- 测试使用组件进行操作
- 避免在测试中直接操作页面元素

```python
# ✅ 正确做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.profile.get_top_up_button()
    top_up_button.click()

# ❌ 错误做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.page.ele("text=Top UP")
    top_up_button.click()
```

### 3. 使用装饰器统一处理等待

- 使用 `element_wait_decorator` 装饰器
- 不要手动调用 `element.wait.clickable()` 或 `element.wait.displayed()`

```python
# ✅ 正确做法
@element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    element = self._get_element(locator, selector_type)
    return element if element else None

# ❌ 错误做法
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    element = self._get_element(locator, selector_type)
    element.wait.displayed(timeout=20)
    return element
```

## 元素定位

### 1. 优先使用文本定位器

- 优先使用 `text=` 定位器
- 其次使用 CSS 选择器
- 最后使用 XPath

```python
# ✅ 正确做法
PROFILE_PAGE = {
    "top_up_button": "text=Top UP",
    "transaction_history": "text=Transaction History",
}

# ❌ 错误做法
PROFILE_PAGE = {
    "top_up_button": "div.button-primary",
    "transaction_history": "div.link",
}
```

### 2. 使用稳定的定位器

- 避免使用动态生成的 ID
- 避免使用容易变化的类名
- 使用稳定的属性和结构

```python
# ✅ 正确做法
PROFILE_PAGE = {
    "top_up_button": "text=Top UP",
    "transaction_history": "text=Transaction History",
}

# ❌ 错误做法
PROFILE_PAGE = {
    "top_up_button": "#btn-12345",
    "transaction_history": ".link-67890",
}
```

### 3. 使用 PageActions 查找元素

- 使用 `self.page_actions.find_element()` 查找元素
- 不要直接使用 `self.page.ele()` 查找元素

```python
# ✅ 正确做法
def get_top_up_button(self):
    """获取充值按钮"""
    locator = self.locators["top_up_button"]
    selector_type = None if locator.startswith("text=") else "css"
    element = self.page_actions.find_element(locator, selector_type)
    return element

# ❌ 错误做法
def get_top_up_button(self):
    """获取充值按钮"""
    locator = self.locators["top_up_button"]
    element = self.page.ele(locator)
    return element
```

## 测试编写

### 1. 保持测试独立性

- 每个测试用例应该独立运行
- 不依赖其他测试用例的状态
- 在测试前初始化环境
- 在测试后清理环境

```python
# ✅ 正确做法
@pytest.fixture(autouse=True)
def setup(self, page):
    """测试夹具，在每个测试方法前执行"""
    self.logger = LoggerUtils.get_default_logger()
    self.page = page
    self.profile = ProfileComponent(self.page)
    self.page.get(PROFILE_URL)
    self.profile.wait_for_page_load()

# ❌ 错误做法
def test_xxx(self):
    """测试XXX"""
    # 依赖上一个测试用例的页面状态
    xxx = self.profile.get_xxx()
```

### 2. 使用断言验证结果

- 使用 `assert` 进行断言
- 提供清晰的错误信息
- 验证关键结果

```python
# ✅ 正确做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.profile.get_top_up_button()
    assert top_up_button is not None, "未找到充值按钮"
    top_up_button.click()

# ❌ 错误做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.profile.get_top_up_button()
    top_up_button.click()
    # 没有断言
```

### 3. 使用日志记录测试过程

- 记录测试开始和结束
- 记录关键操作
- 记录错误信息

```python
# ✅ 正确做法
def test_top_up_button(self):
    """测试充值按钮"""
    self.logger.info("测试充值按钮")
    top_up_button = self.profile.get_top_up_button()
    assert top_up_button is not None, "未找到充值按钮"
    self.logger.info("充值按钮存在")
    top_up_button.click()
    self.logger.info("成功点击充值按钮")

# ❌ 错误做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.profile.get_top_up_button()
    top_up_button.click()
    # 没有日志记录
```

### 4. 使用合理的等待时间

- 使用必要的等待时间
- 避免过长的等待时间
- 优先使用条件等待

```python
# ✅ 正确做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.profile.get_top_up_button()
    top_up_button.click()
    self.page.wait(5)  # 等待页面加载

# ❌ 错误做法
def test_top_up_button(self):
    """测试充值按钮"""
    top_up_button = self.profile.get_top_up_button()
    top_up_button.click()
    self.page.wait(30)  # 等待时间过长
```

## 错误处理

### 1. 使用异常处理

- 使用 try-except 捕获异常
- 记录详细的错误信息
- 提供清晰的错误消息

```python
# ✅ 正确做法
def wait_for_page_load(self, timeout=20):
    """等待个人中心页面加载完成"""
    try:
        self.profile.wait_for_page_load()
        self.logger.info("个人中心页面加载完成")
    except Exception as e:
        self.logger.error(f"等待个人中心页面加载时出错: {str(e)}")
        raise

# ❌ 错误做法
def wait_for_page_load(self, timeout=20):
    """等待个人中心页面加载完成"""
    self.profile.wait_for_page_load()
    # 没有异常处理
```

### 2. 抛出有意义的异常

- 抛出有意义的异常
- 包含足够的上下文信息
- 帮助快速定位问题

```python
# ✅ 正确做法
def get_top_up_button(self):
    """获取充值按钮"""
    locator = self.locators["top_up_button"]
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception(f"Element not found for locator: {locator}")
    return element

# ❌ 错误做法
def get_top_up_button(self):
    """获取充值按钮"""
    locator = self.locators["top_up_button"]
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception("Element not found")
    return element
```

## 代码复用

### 1. 提取公共方法

- 避免重复代码
- 提取公共方法
- 提高代码复用性

```python
# ✅ 正确做法
def get_element(self, locator_name):
    """获取元素"""
    self.logger.info(f"获取{locator_name}")
    locator = self.locators[locator_name]
    selector_type = None if locator.startswith("text=") else "css"
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception(f"Element not found for locator: {locator}")
    return element

def get_top_up_button(self):
    """获取充值按钮"""
    return self.get_element("top_up_button")

# ❌ 错误做法
def get_top_up_button(self):
    """获取充值按钮"""
    locator = self.locators["top_up_button"]
    selector_type = None if locator.startswith("text=") else "css"
    element = self.page_actions.find_element(locator, selector_type)
    if not element:
        raise Exception(f"Element not found for locator: {locator}")
    return element
```

### 2. 使用 PageActions 的通用方法

- 使用 PageActions 提供的通用方法
- 避免重复实现相同功能

```python
# ✅ 正确做法
def click_top_up_button(self):
    """点击充值按钮"""
    locator = self.locators["top_up_button"]
    selector_type = None if locator.startswith("text=") else "css"
    self.page_actions.click_element(locator, selector_type)

# ❌ 错误做法
def click_top_up_button(self):
    """点击充值按钮"""
    element = self.get_top_up_button()
    element.click()
```

## 文档编写

### 1. 编写清晰的文档字符串

- 为每个类编写文档字符串
- 为每个方法编写文档字符串
- 描述方法的功能、参数和返回值

```python
# ✅ 正确做法
class ProfileComponent:
    """个人中心页面组件类"""

    def get_top_up_button(self):
        """
        获取充值按钮
        :return: 充值按钮元素对象
        """
        pass

# ❌ 错误做法
class ProfileComponent:
    """个人中心"""

    def get_top_up_button(self):
        pass
```

### 2. 保持文档更新

- 及时更新文档
- 反映最新的代码变更
- 删除过时的内容

## 性能优化

### 1. 避免不必要的等待

- 使用条件等待
- 避免固定等待时间
- 使用装饰器自动处理等待

```python
# ✅ 正确做法
@element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    element = self._get_element(locator, selector_type)
    return element if element else None

# ❌ 错误做法
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    self.page.wait(5)
    element = self._get_element(locator, selector_type)
    return element
```

### 2. 优化元素查找

- 使用高效的定位器
- 避免复杂的 XPath
- 优先使用文本定位器

```python
# ✅ 正确做法
PROFILE_PAGE = {
    "top_up_button": "text=Top UP",
}

# ❌ 错误做法
PROFILE_PAGE = {
    "top_up_button": "//div[@class='button']/span[text()='Top UP']",
}
```

## 安全性

### 1. 避免硬编码

- 使用配置文件
- 使用常量
- 避免在代码中硬编码值

```python
# ✅ 正确做法
from config.settings import PROFILE_URL

self.page.get(PROFILE_URL)

# ❌ 错误做法
self.page.get("https://video.reelswave.net/profile")
```

### 2. 验证输入参数

- 验证输入参数的有效性
- 提供清晰的错误信息
- 避免无效操作

```python
# ✅ 正确做法
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    if not locator:
        raise ValueError("Locator cannot be empty")
    element = self._get_element(locator, selector_type)
    return element if element else None

# ❌ 错误做法
def find_element(self, locator, selector_type=None):
    """查找单个元素"""
    element = self._get_element(locator, selector_type)
    return element if element else None
```

## 团队协作

### 1. 遵循代码规范

- 遵循项目代码规范
- 保持代码风格一致
- 使用统一的命名规范

### 2. 编写可读的代码

- 使用有意义的变量名
- 编写清晰的注释
- 保持代码简洁

### 3. 进行代码审查

- 审查他人的代码
- 接受他人的审查
- 持续改进代码质量

### 4. 使用版本控制

- 使用 Git 管理代码
- 编写清晰的提交信息
- 定期合并代码

## 工具使用

### 1. 使用 AI 辅助开发

- 参考 docs/ai_prompts.md 中的指令模板
- 确保 AI 生成的代码符合规范
- 审查 AI 生成的代码

### 2. 使用 IDE 功能

- 使用代码补全
- 使用代码格式化
- 使用代码检查

### 3. 使用测试框架

- 使用 pytest 框架
- 使用测试标记
- 生成测试报告

## 持续改进

### 1. 定期审查代码

- 定期审查现有代码
- 识别改进机会
- 实施改进措施

### 2. 学习新技术

- 学习新的测试技术
- 学习新的工具
- 分享学习成果

### 3. 收集反馈

- 收集用户反馈
- 收集团队反馈
- 持续改进项目
