#!/usr/bin/env python3
"""
CSS Locator Optimizer for Playwright
Supports text locators as primary strategy with CSS fallback.
Extracts click selectors from Chrome recorder JSON, validates against HTML,
optimizes with text-first strategy, outputs {page_name: {element_name: locator}}.
"""

import json
import re
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

try:
    from bs4 import BeautifulSoup, NavigableString
except ImportError:
    print("Error: BeautifulSoup4 is required. Install with: pip install beautifulsoup4")
    sys.exit(1)


@dataclass
class ElementInfo:
    """Information about an element and its locator"""
    element_name: str
    original_selector: str
    final_locator: str
    locator_type: str  # 'text' or 'css'
    match_count: int = 0
    is_unique: bool = False
    is_clickable: bool = False
    text_content: str = ""
    validation_notes: List[str] = field(default_factory=list)


class CSSLocatorOptimizerPlaywright:
    """CSS locator optimizer with text-first strategy for Playwright"""

    MIN_CLICKABLE_AREA = 20

    CLICKABLE_TAGS = {
        'button', 'a', 'input', 'select', 'textarea',
        'option', 'label', 'menuitem', 'menu', 'summary'
    }

    CLICKABLE_ATTRIBUTES = {
        'onclick', 'onmousedown', 'onmouseup',
        'role="button"', 'role="link"', 'role="tab"',
        'data-clickable', 'data-testid', 'data-cy', 'data-automation'
    }

    def __init__(self, html_file, json_file, page_name: str = None):
        self.html_file = Path(html_file) if isinstance(html_file, str) else html_file
        self.json_file = Path(json_file) if json_file and isinstance(json_file, str) else json_file
        self.page_name = page_name or self.html_file.stem
        self.soup = None
        self.elements: List[ElementInfo] = []
        self.text_locator_cache: Dict[str, int] = {}

    def parse_html(self):
        with open(self.html_file, 'r', encoding='utf-8') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')

    def extract_selectors_from_json(self) -> List[Dict]:
        """Extract click selectors from Chrome recorder JSON (supports both steps and events)."""
        # 如果 json_file 为 None 或不存在，返回空列表
        if not self.json_file or not self.json_file.exists():
            return []

        with open(self.json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        selectors: List[Dict] = []

        # Support both 'steps' and 'events' key
        events = data.get('steps', data.get('events', []))
        if 'recording' in data and isinstance(data['recording'], dict):
            events = data['recording'].get('events', [])

        for event in events:
            if event.get('type') != 'click':
                continue

            # Handle nested selector structure: [[\"sel\"]] or [\"sel\"]
            selectors_field = event.get('selectors', [])
            if isinstance(selectors_field, list) and len(selectors_field) > 0:
                first = selectors_field[0]
                if isinstance(first, list):
                    selector = first[0] if first else ''
                else:
                    selector = first
            else:
                selector = event.get('selector', '')

            if selector and selector != '*':
                selectors.append({
                    'selector': selector,
                    'metadata': {
                        'target': event.get('target', ''),
                        'time': event.get('time', '')
                    }
                })

        return selectors

    def extract_clickable_elements_from_html(self) -> List[Dict]:
        """Extract all clickable elements from HTML directly."""
        selectors: List[Dict] = []

        # 查找所有可点击的元素
        for element in self.soup.find_all(True):
            if self.is_element_clickable(element):
                # 生成 CSS 选择器
                selector = self.generate_css_selector(element)
                if selector:
                    selectors.append({
                        'selector': selector,
                        'metadata': {
                            'tag': element.name,
                            'text': element.get_text(strip=True)[:50]
                        }
                    })

        return selectors

    def generate_css_selector(self, element) -> str:
        """Generate a CSS selector for the given element."""
        if element.get('id'):
            return f"#{element.get('id')}"

        # 尝试使用 class
        classes = element.get('class', [])
        stable_classes = [c for c in classes if not self.is_dynamic_class(c)]
        if stable_classes:
            return f"{element.name}.{'.'.join(stable_classes)}"

        # 使用标签名和属性
        attrs = []
        for attr, value in element.attrs.items():
            if attr not in ['class', 'id', 'style'] and not self.is_dynamic_attribute(attr, str(value)):
                attrs.append(f'[{attr}="{value}"]')

        if attrs:
            return f"{element.name}{''.join(attrs)}"

        # 使用标签名
        return element.name

    def is_dynamic_attribute(self, name: str, value: str) -> bool:
        if not isinstance(value, str):
            return False
        patterns = [
            r'^[a-f0-9]{8,}$', r'^\d{10,}$', r'.*-\d{4,}-.*',
            r'.*random.*', r'.*generated.*', r'^[a-z0-9]{20,}$',
        ]
        return any(re.match(p, value, re.IGNORECASE) for p in patterns)

    def is_dynamic_class(self, class_name: str) -> bool:
        patterns = [
            r'^css-[a-f0-9]+$', r'^_[a-f0-9]+$', r'^[a-z]{2}-[a-f0-9]+$',
            r'^style-[a-f0-9]+$', r'^sc-[a-f0-9]+$',
            r'^emotion-[a-f0-9]+$', r'^makeStyles-[a-f0-9]+$',
        ]
        return any(re.match(p, class_name, re.IGNORECASE) for p in patterns)

    def validate_selector(self, selector: str) -> Tuple[int, bool]:
        try:
            elements = self.soup.select(selector)
            return len(elements), len(elements) == 1
        except Exception:
            return 0, False

    def validate_text_locator(self, text: str) -> Tuple[int, bool]:
        try:
            matches = self.soup.find_all(string=text)
            actual = [m for m in matches if isinstance(m, NavigableString) and text in m.strip()]
            return len(actual), len(actual) == 1
        except Exception:
            return 0, False

    def is_element_clickable(self, element) -> bool:
        if element.name in self.CLICKABLE_TAGS:
            return True
        attrs_str = str(element.attrs).lower()
        if any(attr in attrs_str for attr in self.CLICKABLE_ATTRIBUTES):
            return True
        role = element.get('role', '').lower()
        if role in ['button', 'link', 'tab', 'menuitem', 'checkbox', 'radio']:
            return True
        style = element.get('style', '').lower()
        if 'cursor: pointer' in style or 'cursor:pointer' in style:
            return True
        parent = element.find_parent()
        while parent:
            if parent.name in self.CLICKABLE_TAGS:
                return True
            parent = parent.find_parent()
        if any(attr.startswith('data-') for attr in element.attrs):
            return True
        return False

    def estimate_element_size(self, element) -> Tuple[bool, int]:
        style = element.get('style', '')
        area = 1000
        w = re.search(r'width\s*:\s*(\d+)(px|%)', style, re.IGNORECASE)
        h = re.search(r'height\s*:\s*(\d+)(px|%)', style, re.IGNORECASE)
        if w and h:
            width = int(w.group(1)) if w.group(2) == 'px' else max(int(w.group(1)) * 5, 100)
            height = int(h.group(1)) if h.group(2) == 'px' else max(int(h.group(1)) * 5, 30)
            area = width * height
        elif w:
            width = int(w.group(1)) if w.group(2) == 'px' else max(int(w.group(1)) * 5, 100)
            area = width * 40
        elif h:
            height = int(h.group(1)) if h.group(2) == 'px' else max(int(h.group(1)) * 5, 30)
            area = 100 * height
        return area >= self.MIN_CLICKABLE_AREA, area

    def extract_element_features(self, element) -> Dict:
        return {
            'id': element.get('id', ''),
            'classes': element.get('class', []),
            'attributes': {k: v for k, v in element.attrs.items()
                          if k not in ['class', 'id', 'style']},
            'tag': element.name,
            'text': element.get_text(strip=True)[:50],
        }

    def generate_text_locator(self, element) -> Optional[str]:
        """Try to generate a text= locator. Returns None if not suitable."""
        text = element.get_text(strip=True)
        if not text or len(text) < 2 or len(text) > 50:
            return None
        if text.lower() in ['loading...', '...', '•', '—', '–']:
            return None
        _, is_unique = self.validate_text_locator(text)
        if not is_unique:
            return None
        if text in self.text_locator_cache:
            return None
        self.text_locator_cache[text] = 1
        return f"text={text}"

    def optimize_selector(self, selector: str, element) -> Tuple[str, str, List[str]]:
        """Optimize selector. Returns (final_locator, locator_type, notes)."""
        notes = []
        try:
            features = self.extract_element_features(element)

            # Priority 1: Text locator (most stable)
            text_loc = self.generate_text_locator(element)
            if text_loc:
                notes.append(f"Using text locator: {text_loc}")
                return text_loc, 'text', notes

            # Priority 2: Stable ID
            if features['id'] and not self.is_dynamic_attribute('id', features['id']):
                optimized = f"#{features['id']}"
                if optimized != selector:
                    notes.append("Optimized: Using stable ID selector")
                    return optimized, 'css', notes

            # Priority 3: Multiple stable classes
            stable_classes = [c for c in features['classes'] if not self.is_dynamic_class(c)]
            if len(stable_classes) >= 2:
                cs = f".{'.'.join(stable_classes)}"
                if len(self.soup.select(cs)) == 1 and cs != selector:
                    notes.append("Optimized: Using multiple stable classes")
                    return cs, 'css', notes

            # Priority 4: Data attributes
            custom_attrs = [(k, v) for k, v in features['attributes'].items()
                           if k.startswith('data-') and isinstance(v, str)
                           and not self.is_dynamic_attribute(k, v)]
            if custom_attrs:
                attr_sel = f"[{custom_attrs[0][0]}='{custom_attrs[0][1]}']"
                if len(self.soup.select(attr_sel)) == 1 and attr_sel != selector:
                    notes.append("Optimized: Using custom data attribute")
                    return attr_sel, 'css', notes

            # Priority 5: Tag + class + attribute combo
            if stable_classes:
                for attr_name, attr_value in features['attributes'].items():
                    if isinstance(attr_value, str) and not self.is_dynamic_attribute(attr_name, attr_value):
                        combo = f"{features['tag']}.{stable_classes[0]}[{attr_name}='{attr_value}']"
                        if len(self.soup.select(combo)) == 1 and combo != selector:
                            notes.append("Optimized: Using class + attribute combination")
                            return combo, 'css', notes

            # Priority 6: Simplified hierarchy
            if '>' in selector:
                parts = selector.split('>')
                if len(parts) > 2:
                    simplified = '>'.join(parts[-2:])
                    if len(self.soup.select(simplified)) == 1 and simplified != selector:
                        notes.append("Optimized: Simplified selector hierarchy")
                        return simplified, 'css', notes

            notes.append("Using original selector - no better optimization found")
            return selector, 'css', notes

        except Exception as e:
            return selector, 'css', [f"Optimization error: {str(e)}"]

    def generate_element_name(self, element, selector: str) -> str:
        text = element.get_text(strip=True)[:30]
        tag = element.name
        role = element.get('role', '')
        input_type = element.get('type', '')

        if text:
            name = re.sub(r'[^\w\s-]', '', text)
            name = re.sub(r'\s+', '_', name.strip()).lower()
            suffix_map = {'button': '_button', 'a': '_link',
                         'input': '_input', 'select': '_select', 'textarea': '_textarea'}
            return f"{name}{suffix_map.get(tag, '_element')}"
        elif role:
            return f"{role.replace('-', '_')}_{tag}"
        elif input_type:
            return f"{input_type}_{tag}"
        else:
            elem_id = element.get('id', '')
            if elem_id and not self.is_dynamic_attribute('id', elem_id):
                return f"{re.sub(r'[^w]', '_', elem_id)}_{tag}"
            stable_classes = [c for c in element.get('class', []) if not self.is_dynamic_class(c)]
            if stable_classes:
                return f"{stable_classes[0].replace('-', '_')}_{tag}"
            return f"{tag}_{hashlib.md5(selector.encode()).hexdigest()[:8]}"

    def process(self) -> Dict[str, Dict[str, str]]:
        """Main pipeline. Returns {page_name: {element_name: locator}}."""
        self.parse_html()

        # 如果 JSON 文件不存在或为 None，则从 HTML 中提取所有可点击元素
        if self.json_file and self.json_file.exists():
            selectors_data = self.extract_selectors_from_json()
            print(f"\nFound {len(selectors_data)} click selectors from JSON")
        else:
            selectors_data = self.extract_clickable_elements_from_html()
            print(f"\nFound {len(selectors_data)} clickable elements from HTML")

        print("=" * 60)

        result_dict = {self.page_name: {}}

        for selector_data in selectors_data:
            selector = selector_data['selector']
            match_count, is_unique = self.validate_selector(selector)

            if not is_unique:
                print(f"  ⚠️  Skip: {selector} (matches {match_count})")
                continue

            elements = self.soup.select(selector)
            if not elements:
                continue

            element = elements[0]
            is_clickable = self.is_element_clickable(element)
            has_min_size, area = self.estimate_element_size(element)
            element_name = self.generate_element_name(element, selector)
            final_locator, locator_type, opt_notes = self.optimize_selector(selector, element)

            validation_notes = opt_notes.copy()
            if not is_clickable:
                validation_notes.append("Warning: Element may not be clickable")
            if not has_min_size:
                validation_notes.append(f"Warning: Small area ({area}px²)")

            result_dict[self.page_name][element_name] = final_locator

            info = ElementInfo(
                element_name=element_name,
                original_selector=selector,
                final_locator=final_locator,
                locator_type=locator_type,
                match_count=match_count,
                is_unique=is_unique,
                is_clickable=is_clickable,
                text_content=element.get_text(strip=True)[:30],
                validation_notes=validation_notes
            )
            self.elements.append(info)

            emoji = '📝' if locator_type == 'text' else '🔧'
            status = '✅' if is_clickable else '⚠️'
            print(f"  {status} {emoji} {element_name} → {final_locator}")

        return result_dict

    def generate_report(self) -> str:
        lines = ["\n" + "=" * 60, "PLAYWRIGHT LOCATOR OPTIMIZATION REPORT", "=" * 60]
        lines.append(f"\nPage: {self.page_name}")
        lines.append(f"Total: {len(self.elements)} elements")
        text_n = sum(1 for e in self.elements if e.locator_type == 'text')
        css_n = sum(1 for e in self.elements if e.locator_type == 'css')
        lines.append(f"Text locators: {text_n}, CSS locators: {css_n}")
        lines.append("\n" + "-" * 60)

        for i, info in enumerate(self.elements, 1):
            emoji = '📝' if info.locator_type == 'text' else '🔧'
            lines.append(f"\n[{i}] {info.element_name} {emoji}")
            lines.append(f"    Original:  {info.original_selector}")
            lines.append(f"    Final:     {info.final_locator}")
            lines.append(f"    Type:      {info.locator_type}")
            lines.append(f"    Clickable: {'✅' if info.is_clickable else '❌'}")
            if info.text_content:
                lines.append(f"    Text:      {info.text_content}")
            for note in info.validation_notes:
                lines.append(f"    • {note}")

        lines.append("\n" + "=" * 60)
        lines.append("OUTPUT DICT")
        lines.append("=" * 60)
        result = {self.page_name: {e.element_name: e.final_locator for e in self.elements}}
        lines.append(json.dumps(result, indent=2, ensure_ascii=False))
        return '\n'.join(lines)


def find_matching_files(base_path) -> Tuple[Path, Path]:
    """Find matching HTML and JSON files with same prefix."""
    base = Path(base_path) if isinstance(base_path, str) else base_path
    base_name = base.stem

    html_file = None
    for ext in ['.html', '.htm']:
        p = base.parent / f"{base_name}{ext}"
        if p.exists():
            html_file = p
            break

    json_file = None
    for ext in ['.json', '_recording.json', '.recording.json']:
        p = base.parent / f"{base_name}{ext}"
        if p.exists():
            json_file = p
            break

    if not html_file or not json_file:
        raise FileNotFoundError(
            f"Could not find matching HTML/JSON pair for: {base}\n"
            f"Expected prefix: {base_name}\n"
            f"Found: HTML={html_file}, JSON={json_file}"
        )
    return html_file, json_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 css_locator_optimizer_playwright.py <base_file_path> [page_name]")
        sys.exit(1)

    base_path = Path(sys.argv[1])
    page_name = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        html_file, json_file = find_matching_files(base_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"HTML: {html_file}")
    print(f"JSON: {json_file}")

    optimizer = CSSLocatorOptimizerPlaywright(html_file, json_file, page_name)
    result = optimizer.process()
    report = optimizer.generate_report()
    print(report)

    out_json = base_path.parent / f"{base_path.stem}_locators.json"
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    out_report = base_path.parent / f"{base_path.stem}_optimizer_report.txt"
    with open(out_report, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 JSON: {out_json}")
    print(f"📄 Report: {out_report}")


if __name__ == "__main__":
    main()
