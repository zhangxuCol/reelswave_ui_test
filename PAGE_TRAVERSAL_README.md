# 页面遍历测试框架使用指南

## 概述

这个框架用于自动化测试网页中的所有可交互元素。它会自动遍历页面中的所有可交互元素，点击每个元素，然后返回到主页面，继续测试下一个元素。

## 目录结构

```
reelswave_web_test/
├── html_files/              # 存储各个页面的HTML文件
├── config/
│   └── locators.py         # 页面元素定位器配置
├── page/
│   ├── base.py             # 基础页面类
│   └── page_traversal.py   # 页面遍历测试类
└── utils/
    ├── html_parser.py      # HTML解析工具
    └── page_traversal_generator.py  # 页面遍历测试生成工具
```

## 使用步骤

### 1. 准备HTML文件

将需要测试的页面HTML文件保存到 `html_files/` 目录中，文件名为 `{页面名称}.html`。

例如：
- `dramahome.html` - 短剧首页
- `player.html` - 视频播放页面
- `profile.html` - 个人中心页面

### 2. 生成元素定位器

使用 `PageTraversalGenerator` 从HTML文件中提取可交互元素的CSS路径：

```python
from utils.page_traversal_generator import PageTraversalGenerator

# 生成所有需要的代码
result = PageTraversalGenerator.generate_all(
    page_name="DramaHome",
    html_file_path="html_files/dramahome.html",
    main_page_url="/drama"
)

# 获取生成的代码
locators = result['locators']
locators_code = result['locators_code']
traversal_class_code = result['traversal_class_code']

# 将定位器代码添加到 config/locators.py
print(locators_code)

# 将遍历测试类代码添加到 page/page_traversal.py
print(traversal_class_code)
```

### 3. 添加定位器到配置文件

将生成的定位器代码添加到 `config/locators.py` 文件中：

```python
# 短剧首页元素定位器
DRAMA_HOME_PAGE = {
    "back_button": "div.gap-sm > svg",
    "home_button": "svg.filter-drop-shadow-\[0_0_1px_\#000c\] > path",
    # ... 更多定位器
}
```

### 4. 创建页面遍历测试类

在 `page/page_traversal.py` 中添加新的页面遍历测试类：

```python
class DramaHomeTraversal(PageTraversal):
    """短剧首页遍历测试"""

    def __init__(self, page: ChromiumPage):
        super().__init__(
            page=page,
            page_name="DramaHome",
            main_page_url="/drama",
            locators=DRAMA_HOME_PAGE
        )
```

### 5. 运行页面遍历测试

```python
from page.base import open_mobile_browser
from page.page_traversal import DramaHomeTraversal

# 打开浏览器
page = open_mobile_browser()

# 创建遍历测试实例
traversal = DramaHomeTraversal(page)

# 运行遍历测试
traversal.traverse_page_elements()
```

## 工作流程

1. **保存页面HTML**：将当前页面的HTML保存到文件
2. **解析HTML**：从HTML中提取所有可交互元素
3. **遍历元素**：依次点击每个可交互元素
4. **返回主页**：每次点击后返回到主页面
5. **继续测试**：继续测试下一个元素

## 可交互元素的识别标准

框架会识别以下类型的元素：

- 标签：`a`, `button`, `input`, `select`, `textarea`, `option`
- 类名包含：`button`, `btn`, `click`, `link`, `tab`, `menu`, `nav`, `icon`, `switch`, `toggle`, `select`, `dropdown`, `checkbox`, `radio`
- role属性：`button`, `link`, `tab`, `menuitem`, `checkbox`, `radio`
- 具有 `onclick` 属性的元素

## 自定义配置

### 修改等待时间

在 `page_traversal.py` 中修改 `time.sleep()` 的值：

```python
time.sleep(2)  # 修改这个值来调整等待时间
```

### 添加新的可交互元素类型

在 `html_parser.py` 的 `HTMLParser` 类中修改 `INTERACTIVE_TAGS` 和 `INTERACTIVE_CLASS_PATTERNS`：

```python
INTERACTIVE_TAGS = ['a', 'button', 'input', 'select', 'textarea', 'option', 'div']  # 添加新的标签

INTERACTIVE_CLASS_PATTERNS = [
    r'button',
    r'btn',
    # ... 添加新的模式
]
```

## 注意事项

1. 确保HTML文件是最新的，反映当前页面的结构
2. 某些元素可能会导致页面跳转，框架会自动返回主页面
3. 如果某个元素无法点击或导致错误，框架会记录错误并继续测试下一个元素
4. 建议在测试环境中运行，避免对生产环境造成影响
