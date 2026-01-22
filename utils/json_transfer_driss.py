import json
import os


def recorder_json_to_drissionpage(json_path, output_path='drissionpage_script.py'):

    # 获取当前脚本所在目录的上一级目录的绝对路径
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(current_dir)
    # 构建完整的文件路径
    json_full_path = os.path.join(current_dir, json_path)
    output_full_path = os.path.join(current_dir, output_path)

    # 读取Recorder导出的JSON
    with open(json_full_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 初始化DrissionPage代码模板
    code = [
        'from DrissionPage import ChromiumPage\n',
        'page = ChromiumPage()\n\n'
    ]

    # 解析每个步骤并转换为DrissionPage语法
    for step in data.get('steps', []):
        step_type = step.get('type')
        selectors = step.get('selectors', [])
        # 提取CSS选择器（优先用CSS，无则用XPath）
        selector = ''
        if selectors:
            for sel in selectors:
                if isinstance(sel, list) and len(sel) > 0:
                    sel_value = sel[0]
                    if sel_value.startswith('css='):
                        selector = f'css:{sel_value[4:]}'
                        break
                    elif sel_value.startswith('xpath='):
                        selector = f'xpath:{sel_value[6:]}'
                        break
                    # 默认当作CSS选择器处理
                    selector = f'css:{sel_value}'
                    break

        # 按操作类型生成代码
        if step_type == 'navigate':
            url = step.get('url')
            code.append(f'page.get("{url}")\n')

        elif step_type == 'click':
            if selector:
                code.append(f'page.ele("{selector}").click()\n')

        elif step_type == 'type':
            text = step.get('text', '')
            if selector and text:
                code.append(f'page.ele("{selector}").input("{text}")\n')

        elif step_type == 'keyDown':
            key = step.get('key', '')
            if selector and key:
                code.append(f'page.ele("{selector}").key_down("{key}")\n')

        # 可扩展：添加等待、滚动等操作的转换
        elif step_type == 'waitForElement':
            code.append(f'page.ele("{selector}", timeout=10)\n')

        # 换行分隔步骤，提升可读性
        code.append('\n')

    # 添加关闭浏览器代码
    code.append('page.wait(2)\n')
    code.append('page.quit()\n')

    # 保存生成的代码
    with open(output_full_path, 'w', encoding='utf-8') as f:
        f.writelines(code)

    print(f'✅ DrissionPage代码已生成：{output_full_path}')


# 调用函数（替换为你的JSON文件路径）
recorder_json_to_drissionpage('recordjson/record_play.json', 'recordjson/drissionpage_script.py')