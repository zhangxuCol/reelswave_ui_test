
# 测试运行使用指南

## 概述

本指南说明如何运行项目的测试并生成中文测试报告。

## 运行单个测试文件

### 方法一：使用pytest直接运行

```bash
# 运行个人中心测试
pytest page/profile_test.py -v -s

# 运行首页测试
pytest page/home_test.py -v -s

# 运行播放器测试
pytest page/player_test.py -v -s

# 运行搜索测试
pytest page/search_test.py -v -s

# 运行短剧首页测试
pytest page/drama_home_test.py -v -s
```

### 方法二：运行特定测试方法

```bash
# 运行单个测试方法
pytest page/profile_test.py::TestProfile::test_top_up_button -v -s
```

### 方法三：使用标记运行

```bash
# 运行冒烟测试
pytest -m smoke -v -s

# 运行回归测试
pytest -m regression -v -s

# 运行个人中心测试
pytest -m profile -v -s
```

## 查看测试报告

测试报告会自动生成到 `reports/html/` 目录下，文件名格式为 `{日期}_test_report.html`。

### 在浏览器中打开报告

```bash
# macOS
open reports/html/2026-03-12_test_report.html

# Linux
xdg-open reports/html/2026-03-12_test_report.html

# Windows
start reports/html/2026-03-12_test_report.html
```

## 报告功能说明

生成的中文测试报告包含以下功能：

1. **统计信息**
   - 总用例数
   - 通过数量
   - 失败数量
   - 通过率
   - 总耗时

2. **筛选功能**
   - 点击"全部"按钮显示所有用例
   - 点击"通过"按钮仅显示通过的用例
   - 点击"失败"按钮仅显示失败的用例

3. **用例详情**
   - 用例名称
   - 执行状态（通过/失败）
   - 执行耗时
   - 截图链接（如果有）
   - 错误信息（如果失败）

## 注意事项

1. **报告目录**
   - 确保reports/html目录存在
   - 如果不存在，脚本会自动创建

2. **测试结果**
   - 报告会显示所有测试用例的结果
   - 如果测试结果为0，可能是测试未执行或解析失败

3. **日期显示**
   - 报告显示的是生成报告时的日期
   - 不是测试执行的日期

## 常见问题

### 问题：报告显示0个用例

可能原因：
- pytest输出格式不匹配
- 测试未实际执行

解决方法：
- 确保使用正确的pytest命令
- 查看控制台输出确认测试是否执行

### 问题：报告样式异常

可能原因：
- 浏览器不支持某些CSS特性
- HTML文件编码问题

解决方法：
- 使用现代浏览器（Chrome、Firefox、Safari）
- 确保HTML文件使用UTF-8编码

## 示例

### 示例1：运行个人中心所有测试

```bash
pytest page/profile_test.py -v -s
```

### 示例2：运行单个测试方法

```bash
pytest page/profile_test.py::TestProfile::test_top_up_button -v -s
```

### 示例3：运行所有冒烟测试

```bash
pytest -m smoke -v -s
```

## 下一步

运行测试后，查看生成的中文测试报告，了解测试结果。如果需要进一步分析，可以：
1. 查看失败的用例详情
2. 检查错误信息
3. 查看相关截图（如果有）
