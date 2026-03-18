# 测试编写指南

本文档详细说明如何编写和维护测试用例。

## 测试类结构

### 基本结构

```python
import pytest
from components.XXXComponent import XXXComponent
from utils.logger_utils import LoggerUtils
from config.settings import XXX_URL


@pytest.mark.xxx
class TestXXX:
    """XXX测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """
        测试夹具，在每个测试方法前执行
        此夹具用于初始化测试环境，包括设置日志记录器、页面实例、XXX组件，
        并导航到XXX页面，确保页面加载完成
        """
        self.logger = LoggerUtils.get_default_logger()
        self.page = page
        self.xxx = XXXComponent(self.page)

        # 导航到XXX页面
        self.page.get(XXX_URL)
        self.logger.info(f"导航到XXX页面: {XXX_URL}")

        # 等待页面加载完成
        try:
            self.xxx.wait_for_page_load()
            self.logger.info("XXX页面加载完成")
        except Exception as e:
            self.logger.error(f"等待XXX页面加载时出错: {str(e)}")
            raise
```

### 必需的初始化

每个测试类必须初始化以下属性：

```python
self.logger = LoggerUtils.get_default_logger() # 日志记录器
self.page = page                              # 页面对象
self.xxx = XXXComponent(self.page)            # 组件对象
```

## 测试方法规范

### 基本结构

```python
@pytest.mark.smoke
def test_xxx(self):
    """测试XXX"""
    self.logger.info("测试XXX")
    xxx = self.xxx.get_xxx()
    assert xxx is not None, "未找到XXX"
    self.logger.info("XXX存在")
    xxx.click()
    self.logger.info("成功点击XXX")
    self.page.wait(5)
    # 返回上一页
    self.xxx.click_back_button()
    self.logger.info("返回上一页")
    self.page.wait(2)
```

### 测试方法步骤

1. 记录测试开始日志
2. 获取元素
3. 断言元素存在
4. 记录元素存在日志
5. 执行操作（如点击）
6. 记录操作成功日志
7. 等待页面响应
8. 返回上一页（如需要）
9. 记录返回日志
10. 等待页面加载

## 测试标记

### smoke（冒烟测试）

```python
@pytest.mark.smoke
def test_xxx(self):
    """测试XXX"""
    pass
```

### regression（回归测试）

```python
@pytest.mark.regression
def test_xxx(self):
    """测试XXX"""
    pass
```

### 自定义标记

```python
@pytest.mark.xxx
class TestXXX:
    """XXX测试类"""
    pass
```

## 断言规范

### 元素存在断言

```python
xxx = self.xxx.get_xxx()
assert xxx is not None, "未找到XXX"
```

### 文本匹配断言

```python
text = self.xxx.get_xxx_text()
assert text == "预期文本", "文本不匹配"
```

### 元素可见断言

```python
xxx = self.xxx.get_xxx()
assert xxx.states.is_displayed, "XXX不可见"
```

### 元素可点击断言

```python
xxx = self.xxx.get_xxx()
assert xxx.states.is_enabled, "XXX不可点击"
```

## 日志记录规范

### 信息日志

```python
self.logger.info("测试XXX")
self.logger.info("XXX存在")
self.logger.info("成功点击XXX")
self.logger.info("返回上一页")
```

### 错误日志

```python
self.logger.error(f"等待XXX页面加载时出错: {str(e)}")
```

### 调试日志

```python
self.logger.debug(f"当前页面URL: {self.page.url}")
```

## 测试用例示例

### 测试按钮点击

```python
@pytest.mark.smoke
def test_top_up_button(self):
    """测试充值按钮"""
    self.logger.info("测试充值按钮")
    top_up_button = self.profile.get_top_up_button()
    assert top_up_button is not None, "未找到充值按钮"
    self.logger.info("充值按钮存在")
    top_up_button.click()
    self.logger.info("成功点击充值按钮")
    self.page.wait(5)
    # 返回上一页
    self.profile.click_back_button()
    self.logger.info("返回上一页")
    self.page.wait(2)
```

### 测试链接点击

```python
@pytest.mark.smoke
def test_transaction_history_link(self):
    """测试交易历史链接"""
    self.logger.info("测试交易历史链接")
    transaction_history = self.profile.get_transaction_history_link()
    assert transaction_history is not None, "未找到交易历史链接"
    self.logger.info("交易历史链接存在")
    transaction_history.click()
    self.logger.info("成功点击交易历史链接")
    self.page.wait(5)
    # 返回上一页
    self.profile.click_back_button()
    self.logger.info("返回上一页")
    self.page.wait(2)
```

### 测试VIP状态

```python
@pytest.mark.smoke
def test_vip_status(self):
    """测试VIP状态"""
    self.logger.info("测试VIP状态")
    vip_avatar = self.profile.get_vip_avatar()
    assert vip_avatar is not None, "未找到VIP头像"
    self.logger.info("VIP头像存在")
    vip_avatar.click()
    self.logger.info("成功点击VIP头像")
    self.page.wait(5)
    # 返回上一页
    self.profile.click_back_button()
    self.logger.info("返回上一页")
    self.page.wait(2)
```

## 测试夹具（Fixtures）

### page 夹具

```python
@pytest.fixture(autouse=True)
def setup(self, page):
    """
    测试夹具，在每个测试方法前执行
    """
    self.logger = LoggerUtils.get_default_logger()
    self.page = page
    self.xxx = XXXComponent(self.page)
    self.page.get(XXX_URL)
    self.xxx.wait_for_page_load()
```

### 自定义夹具

```python
@pytest.fixture
def custom_data(self):
    """自定义数据夹具"""
    return {
        "username": "test",
        "password": "test123"
    }
```

## 测试最佳实践

### 1. 测试独立性

每个测试用例应该独立运行，不依赖其他测试用例：

```python
# ✅ 正确做法
def test_xxx(self):
    """测试XXX"""
    self.page.get(XXX_URL)
    xxx = self.xxx.get_xxx()
    assert xxx is not None

# ❌ 错误做法
def test_xxx(self):
    """测试XXX"""
    # 依赖上一个测试用例的页面状态
    xxx = self.xxx.get_xxx()
    assert xxx is not None
```

### 2. 测试清理

每个测试用例应该清理测试环境：

```python
# ✅ 正确做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    xxx.click()
    self.page.wait(5)
    self.xxx.click_back_button()
    self.page.wait(2)

# ❌ 错误做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    xxx.click()
    # 没有返回上一页
```

### 3. 测试断言

每个测试用例应该有明确的断言：

```python
# ✅ 正确做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    assert xxx is not None, "未找到XXX"

# ❌ 错误做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    # 没有断言
```

### 4. 测试日志

每个测试用例应该有详细的日志记录：

```python
# ✅ 正确做法
def test_xxx(self):
    """测试XXX"""
    self.logger.info("测试XXX")
    xxx = self.xxx.get_xxx()
    assert xxx is not None, "未找到XXX"
    self.logger.info("XXX存在")
    xxx.click()
    self.logger.info("成功点击XXX")

# ❌ 错误做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    assert xxx is not None
    xxx.click()
    # 没有日志记录
```

### 5. 测试等待

使用合理的等待时间：

```python
# ✅ 正确做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    xxx.click()
    self.page.wait(5)  # 等待页面加载

# ❌ 错误做法
def test_xxx(self):
    """测试XXX"""
    xxx = self.xxx.get_xxx()
    xxx.click()
    self.page.wait(30)  # 等待时间过长
```

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest page/xxx_test.py
```

### 运行特定测试类

```bash
pytest page/xxx_test.py::TestXXX
```

### 运行特定测试方法

```bash
pytest page/xxx_test.py::TestXXX::test_xxx
```

### 使用标记运行测试

```bash
# 运行冒烟测试
pytest -m smoke

# 运行回归测试
pytest -m regression

# 运行特定页面测试
pytest -m xxx
```

### 并行运行测试

```bash
# 使用 4 个进程并行运行测试
pytest -n 4
```

### 生成测试报告

```bash
# 生成 HTML 测试报告
pytest --html=reports/report.html --self-contained-html

# 生成 XML 测试报告（用于 CI/CD）
pytest --junitxml=reports/report.xml
```

## 常见问题

### Q: 如何跳过某个测试？

A: 使用 `@pytest.mark.skip` 装饰器：

```python
@pytest.mark.skip(reason="功能尚未实现")
def test_xxx(self):
    pass
```

### Q: 如何预期测试失败？

A: 使用 `@pytest.mark.xfail` 装饰器：

```python
@pytest.mark.xfail(reason="已知问题，待修复")
def test_xxx(self):
    assert False
```

### Q: 如何参数化测试？

A: 使用 `@pytest.mark.parametrize` 装饰器：

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])
def test_xxx(self, input, expected):
    assert input * 2 == expected
```
