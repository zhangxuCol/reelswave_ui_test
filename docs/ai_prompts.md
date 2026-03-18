# AI 指令模板

本文档提供了使用 AI 辅助开发时的标准指令模板，确保 AI 生成的代码符合项目规范。

## 通用指令模板

### 添加新功能

```
任务：添加XXX功能

请严格按照以下步骤实现：

1. 在 config/locators.py 中添加定位器：
   - 优先使用 text= 定位器
   - 或使用 CSS 选择器

2. 在 components/XXXComponent.py 中添加方法：
   - 使用 self.page_actions.find_element() 查找元素
   - 使用 self.locators["xxx"] 获取定位器
   - 使用 selector_type = None if locator.startswith("text=") else "css" 判断选择器类型
   - 使用 self.logger 记录日志
   - 如果元素不存在，抛出异常

3. 在 page/xxx_test.py 中添加测试用例：
   - 使用 @pytest.mark.smoke 标记
   - 使用 self.xxx_component.get_xxx() 获取元素
   - 使用 assert 断言元素存在
   - 点击元素
   - 使用 self.page.wait() 等待
   - 使用 self.profile.click_back_button() 返回
   - 使用 self.logger 记录日志

4. 在 README.md 中更新文档

注意事项：
- 不要手动调用 element.wait.clickable() 或 element.wait.displayed()
- 不要直接使用 self.page.ele() 查找元素
- 必须使用 self.logger 记录日志
- 必须使用 assert 进行断言
- 必须遵循 docs/coding_standards.md 中的代码规范
```

## 个人中心测试指令模板

### 添加新的个人中心测试

```
请按照以下规范添加新的个人中心测试：

1. 在 ProfileComponent.py 中添加 get_xxx() 方法：
   - 使用 self.page_actions.find_element() 查找元素
   - 使用 self.locators["xxx"] 获取定位器
   - 使用 selector_type = None if locator.startswith("text=") else "css" 判断选择器类型
   - 使用 self.logger 记录日志
   - 如果元素不存在，抛出异常

2. 在 profile_test.py 中添加 test_xxx() 测试用例：
   - 使用 @pytest.mark.smoke 标记
   - 使用 self.profile.get_xxx() 获取元素
   - 使用 assert 断言元素存在
   - 点击元素
   - 使用 self.page.wait(5) 等待5秒
   - 使用 self.profile.click_back_button() 返回
   - 使用 self.page.wait(2) 等待页面加载
   - 使用 self.logger 记录日志

3. 在 locators.py 中添加定位器：
   - 使用 text= 定位器优先
   - 或使用 CSS 选择器

4. 在 README.md 中更新文档

注意事项：
- 不要手动调用 element.wait.clickable() 或 element.wait.displayed()
- 不要直接使用 self.page.ele() 查找元素
- 必须使用 self.logger 记录日志
- 必须使用 assert 进行断言
- 必须遵循 docs/coding_standards.md 中的代码规范
```

## 短剧首页测试指令模板

### 添加新的短剧首页测试

```
请按照以下规范添加新的短剧首页测试：

1. 在 DramaHomeComponent.py 中添加 get_xxx() 方法：
   - 使用 self.page_actions.find_element() 查找元素
   - 使用 self.locators["xxx"] 获取定位器
   - 使用 selector_type = None if locator.startswith("text=") else "css" 判断选择器类型
   - 使用 self.logger 记录日志
   - 如果元素不存在，抛出异常

2. 在 drama_home_test.py 中添加 test_xxx() 测试用例：
   - 使用 @pytest.mark.smoke 标记
   - 使用 self.drama_home.get_xxx() 获取元素
   - 使用 assert 断言元素存在
   - 点击元素
   - 使用 self.page.wait() 等待
   - 使用 self.logger 记录日志

3. 在 locators.py 中添加定位器：
   - 使用 text= 定位器优先
   - 或使用 CSS 选择器

4. 在 README.md 中更新文档

注意事项：
- 不要手动调用 element.wait.clickable() 或 element.wait.displayed()
- 不要直接使用 self.page.ele() 查找元素
- 必须使用 self.logger 记录日志
- 必须使用 assert 进行断言
- 必须遵循 docs/coding_standards.md 中的代码规范
```

## 播放器测试指令模板

### 添加新的播放器测试

```
请按照以下规范添加新的播放器测试：

1. 在 PlayerIconComponent.py 中添加 get_xxx() 方法：
   - 使用 self.page_actions.find_element() 查找元素
   - 使用 self.locators["xxx"] 获取定位器
   - 使用 selector_type = None if locator.startswith("text=") else "css" 判断选择器类型
   - 使用 self.logger 记录日志
   - 如果元素不存在，抛出异常

2. 在 player_test.py 中添加 test_xxx() 测试用例：
   - 使用 @pytest.mark.smoke 标记
   - 使用 self.player.get_xxx() 获取元素
   - 使用 assert 断言元素存在
   - 点击元素
   - 使用 self.page.wait() 等待
   - 使用 self.logger 记录日志

3. 在 locators.py 中添加定位器：
   - 使用 text= 定位器优先
   - 或使用 CSS 选择器

4. 在 README.md 中更新文档

注意事项：
- 不要手动调用 element.wait.clickable() 或 element.wait.displayed()
- 不要直接使用 self.page.ele() 查找元素
- 必须使用 self.logger 记录日志
- 必须使用 assert 进行断言
- 必须遵循 docs/coding_standards.md 中的代码规范
```

## 代码审查指令模板

### 审查 AI 生成的代码

```
请审查以下代码，确保它符合项目规范：

1. 检查代码是否遵循 docs/coding_standards.md 中的代码规范
2. 检查是否使用了正确的元素查找方法
3. 检查是否正确使用了装饰器
4. 检查是否正确使用了日志记录
5. 检查是否正确使用了断言
6. 检查是否正确使用了定位器
7. 检查是否有重复代码
8. 检查是否有不必要的等待
9. 检查是否有硬编码的值
10. 检查是否有未使用的导入

如果发现任何问题，请指出并提供修复建议。
```

## 代码重构指令模板

### 重构现有代码

```
请重构以下代码，使其符合项目规范：

1. 确保代码遵循 docs/coding_standards.md 中的代码规范
2. 使用 PageActions 的方法进行元素操作
3. 使用装饰器自动处理元素等待
4. 使用 LoggerUtils 记录日志
5. 使用 locators 中的定位器
6. 移除重复代码
7. 移除不必要的等待
8. 移除硬编码的值
9. 移除未使用的导入

请保持代码的功能不变，只改变代码的结构和风格。
```

## 调试指令模板

### 调试测试失败

```
请帮我调试以下测试失败的问题：

1. 检查定位器是否正确
2. 检查元素等待时间是否足够
3. 检查元素是否在正确的页面上
4. 检查元素是否被其他元素遮挡
5. 检查元素是否需要滚动到可见区域
6. 检查元素是否存在动态加载的情况
7. 检查元素是否存在多个匹配的情况
8. 检查元素是否存在时序问题

请提供详细的调试步骤和修复建议。
```

## 多模型协作指令模板

### 使用多个 AI 模型协作开发

```
任务：使用多个 AI 模型协作开发 XXX 功能

请按照以下步骤进行：

1. 模型 A：分析需求，设计组件方法
2. 模型 B：实现组件方法
3. 模型 C：编写测试用例
4. 模型 D：审查代码
5. 模型 E：优化代码

每个模型都应该：
- 遵循 docs/coding_standards.md 中的代码规范
- 使用 PageActions 的方法进行元素操作
- 使用装饰器自动处理元素等待
- 使用 LoggerUtils 记录日志
- 使用 locators 中的定位器

请确保所有模型生成的代码风格一致，符合项目规范。
```

## 最佳实践

### 使用 AI 开发时的建议

1. **明确指令**：提供清晰、详细的指令，避免歧义
2. **参考规范**：始终参考 docs/coding_standards.md 中的代码规范
3. **分步实施**：将大任务分解为小步骤，逐步实施
4. **代码审查**：让 AI 审查自己生成的代码，或者让另一个 AI 模型审查
5. **测试验证**：确保生成的代码能够通过测试
6. **文档更新**：及时更新相关文档
7. **版本控制**：使用 Git 管理代码变更
8. **持续改进**：根据实际情况调整指令模板

### 避免常见问题

1. **避免模糊指令**：不要使用"优化代码"这样模糊的指令
2. **避免忽略规范**：不要忽略 docs/coding_standards.md 中的代码规范
3. **避免跳过步骤**：不要跳过指令模板中的任何步骤
4. **避免过度依赖**：不要完全依赖 AI，人工审查是必要的
5. **避免重复代码**：避免生成重复的代码
6. **避免硬编码**：避免使用硬编码的值
7. **避免不必要的等待**：避免使用不必要的等待时间
8. **避免未使用的导入**：避免生成未使用的导入

## 示例

### 添加 VIP 头像测试的完整指令

```
任务：添加 VIP 头像测试

请按照以下规范添加 VIP 头像测试：

1. 在 ProfileComponent.py 中添加 get_vip_avatar() 方法：
   - 使用 self.page_actions.find_element() 查找元素
   - 使用 self.locators["vip_avatar"] 获取定位器
   - 使用 selector_type = None if locator.startswith("text=") else "css" 判断选择器类型
   - 使用 self.logger 记录日志
   - 如果元素不存在，抛出异常

2. 在 profile_test.py 中添加 test_vip_status() 测试用例：
   - 使用 @pytest.mark.smoke 标记
   - 使用 self.profile.get_vip_avatar() 获取元素
   - 使用 assert 断言元素存在
   - 点击元素
   - 使用 self.page.wait(5) 等待5秒
   - 使用 self.profile.click_back_button() 返回
   - 使用 self.page.wait(2) 等待页面加载
   - 使用 self.logger 记录日志

3. 在 locators.py 中添加定位器：
   - 使用 text= 定位器优先
   - 或使用 CSS 选择器

4. 在 README.md 中更新文档

注意事项：
- 不要手动调用 element.wait.clickable() 或 element.wait.displayed()
- 不要直接使用 self.page.ele() 查找元素
- 必须使用 self.logger 记录日志
- 必须使用 assert 进行断言
- 必须遵循 docs/coding_standards.md 中的代码规范
```

## 更新日志

- 2024-01-XX: 初始版本，添加基础指令模板
