
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
from utils.logger_utils import LoggerUtils

class HTMLParser:
    """HTML解析器，用于从HTML文件中提取可交互元素的CSS路径"""

    # 可交互元素的标签名
    INTERACTIVE_TAGS = ['a', 'button', 'input', 'select', 'textarea', 'option', 'div', 'span', 'img', 'li']

    # 常见的可交互类名模式
    INTERACTIVE_CLASS_PATTERNS = [
        r'button',
        r'btn',
        r'click',
        r'link',
        r'tab',
        r'menu',
        r'nav',
        r'icon',
        r'switch',
        r'toggle',
        r'select',
        r'dropdown',
        r'checkbox',
        r'radio',
        r'item',
        r'card',
        r'list',
        r'avatar',
        r'action',
        r'header',
        r'footer',
        r'toolbar',
        r'bar',
        r'control',
        r'panel',
        r'section'
    ]

    @staticmethod
    def parse_html_file(html_file_path: str) -> List[Dict[str, str]]:
        """
        解析HTML文件，提取所有可交互元素的CSS路径

        :param html_file_path: HTML文件路径
        :return: 包含元素信息的字典列表，每个字典包含元素名称和CSS路径
        """
        logger = LoggerUtils.get_default_logger()
        logger.info(f"开始解析HTML文件: {html_file_path}")

        try:
            with open(html_file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            return HTMLParser.parse_html_content(html_content)
        except Exception as e:
            logger.error(f"解析HTML文件时出错: {e}")
            return []

    @staticmethod
    def parse_html_content(html_content: str) -> List[Dict[str, str]]:
        """
        解析HTML内容，提取所有可交互元素的CSS路径

        :param html_content: HTML内容字符串
        :return: 包含元素信息的字典列表，每个字典包含元素名称和CSS路径
        """
        logger = LoggerUtils.get_default_logger()
        logger.info(f"开始解析HTML内容，长度: {len(html_content)} 字符")

        soup = BeautifulSoup(html_content, 'html.parser')
        interactive_elements = []

        # 查找所有元素
        all_elements = soup.find_all(True)
        logger.info(f"HTML中共有 {len(all_elements)} 个元素")

        # 查找所有可交互元素
        for element in all_elements:
            if HTMLParser._is_interactive(element):
                element_info = HTMLParser._extract_element_info(element)
                if element_info:
                    interactive_elements.append(element_info)

        logger.info(f"共找到 {len(interactive_elements)} 个可交互元素")
        return interactive_elements

    @staticmethod
    def _is_interactive(element) -> bool:
        """
        判断元素是否为可交互元素

        :param element: BeautifulSoup元素对象
        :return: 是否为可交互元素
        """
        # 检查标签名
        if element.name in HTMLParser.INTERACTIVE_TAGS:
            return True

        # 检查class属性
        if element.get('class'):
            class_list = ' '.join(element.get('class')).lower()
            for pattern in HTMLParser.INTERACTIVE_CLASS_PATTERNS:
                if re.search(pattern, class_list):
                    return True

        # 检查role属性
        role = element.get('role', '').lower()
        if role in ['button', 'link', 'tab', 'menuitem', 'checkbox', 'radio']:
            return True

        # 检查onclick属性
        if element.get('onclick'):
            return True

        # 检查其他常见交互属性
        if element.get('href') or element.get('data-href'):
            return True

        # 检查data-action或data-click属性
        if element.get('data-action') or element.get('data-click'):
            return True

        # 检查是否是可点击的SVG图标
        if element.name == 'svg' and element.parent:
            parent_class = ' '.join(element.parent.get('class', [])).lower()
            if any(pattern in parent_class for pattern in HTMLParser.INTERACTIVE_CLASS_PATTERNS):
                return True

        return False

    @staticmethod
    def _extract_element_info(element) -> Optional[Dict[str, str]]:
        """
        提取元素的信息，包括名称和CSS路径

        :param element: BeautifulSoup元素对象
        :return: 包含元素信息的字典，或None
        """
        try:
            # 生成CSS路径
            css_path = HTMLParser._generate_css_path(element)

            # 提取元素名称
            element_name = HTMLParser._extract_element_name(element)

            return {
                'name': element_name,
                'css_path': css_path
            }
        except Exception as e:
            return None

    @staticmethod
    def _generate_css_path(element) -> str:
        """
        生成元素的CSS路径

        :param element: BeautifulSoup元素对象
        :return: CSS路径字符串
        """
        path_parts = []
        current = element

        while current and current.name:
            # 获取标签名
            tag = current.name

            # 如果有id，直接使用id
            element_id = current.get('id')
            if element_id:
                path_parts.insert(0, f"#{element_id}")
                break

            # 如果有class，使用class
            classes = current.get('class', [])
            if classes:
                # 使用第一个class作为主要选择器，避免class过长
                class_selector = classes[0]

                # 添加属性选择器以提高唯一性
                attributes = []

                # 添加alt属性（如果有）
                alt = current.get('alt')
                if alt:
                    attributes.append(f'[alt="{alt}"]')

                # 添加data-*属性（如果有）
                for attr in element.attrs:
                    if attr.startswith('data-') and attr not in ['data-v-app']:
                        value = element.get(attr)
                        if value:
                            attributes.append(f'[{attr}="{value}"]')
                            break  # 只添加一个data-*属性

                # 添加role属性（如果有）
                role = element.get('role')
                if role:
                    attributes.append(f'[role="{role}"]')

                # 组合选择器
                selector = f"{tag}.{class_selector}"
                if attributes:
                    selector += ''.join(attributes)

                # 如果没有属性，尝试使用文本内容
                if not attributes and current == element:
                    text = element.get_text(strip=True)
                    if text and len(text) <= 20:
                        # 转义特殊字符
                        escaped_text = text.replace('"', '\"')
                        selector = f"{tag}.{class_selector}:contains('{escaped_text}')"

                # 添加:nth-child伪类以提高唯一性
                if current.parent and current == element:
                    siblings = [sib for sib in current.parent.children if hasattr(sib, 'name') and sib.name == tag]
                    if len(siblings) > 1:
                        index = siblings.index(current) + 1
                        selector += f':nth-child({index})'

                path_parts.insert(0, selector)
            else:
                # 对于没有class的元素，添加:nth-child伪类
                if current.parent:
                    siblings = [sib for sib in current.parent.children if hasattr(sib, 'name') and sib.name == tag]
                    if len(siblings) > 1:
                        index = siblings.index(current) + 1
                        path_parts.insert(0, f"{tag}:nth-child({index})")
                    else:
                        path_parts.insert(0, tag)
                else:
                    path_parts.insert(0, tag)

            current = current.parent

        return ' > '.join(path_parts)

    @staticmethod
    def _extract_element_name(element) -> str:
        """
        提取元素的名称

        :param element: BeautifulSoup元素对象
        :return: 元素名称
        """
        # 优先使用文本内容
        text = element.get_text(strip=True)
        if text and len(text) <= 50:
            return text

        # 使用title属性
        title = element.get('title', '')
        if title:
            return title

        # 使用aria-label属性
        aria_label = element.get('aria-label', '')
        if aria_label:
            return aria_label

        # 使用alt属性（针对图片）
        alt = element.get('alt', '')
        if alt:
            return alt

        # 使用标签名和class的组合
        tag = element.name
        classes = element.get('class', [])
        if classes:
            return f"{tag}_{'_'.join(classes)}"

        return tag
