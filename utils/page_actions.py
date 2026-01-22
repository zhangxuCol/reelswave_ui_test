from DrissionPage import ChromiumPage
from utils.decorators import element_wait_decorator
from utils.logger_utils import LoggerUtils

class PageActions:
    """页面基础操作类，封装常用的元素操作方法"""

    # 这是一个页面基础操作类，主要用于封装常用的页面元素操作方法
    def __init__(self, page: ChromiumPage):
        """
        初始化页面操作对象
        :param page: ChromiumPage对象
        """
        # 初始化页面操作对象，传入ChromiumPage实例
        self.page = page
        # 获取当前模块的日志记录器
        self.logger = LoggerUtils.get_default_logger()
    
    def _format_locator(self, locator, selector_type=None):
        """
        根据选择器类型格式化定位器
        :param locator: 定位器
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :return: 格式化后的定位器
        """
        if selector_type:
            # 根据选择器类型拼接定位器
            if selector_type.lower() == "css" and not locator.startswith("css:"):
                return f"css:{locator}"
            elif selector_type.lower() == "xpath" and not locator.startswith("xpath:"):
                return f"xpath:{locator}"
            elif selector_type.lower() == "tag" and not locator.startswith("tag:"):
                return f"tag:{locator}"
        return locator

    @element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
    def find_element(self, locator, selector_type=None):
        """
        查找单个元素
        :param locator: 定位器，可以是字符串或列表
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :return: 元素对象或None
        """
        try:
            # 判断定位器是否为列表类型
            if isinstance(locator, list):
                # 如果是列表，尝试每个定位器直到找到元素
                for loc in locator:
                    element = self._get_element(loc, selector_type)
                    if element:
                        return element
                return None
            else:
                # 单个定位器，直接查找元素
                return self._get_element(locator, selector_type)
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"查找元素失败: {e}")
            return None
    
    def _get_element(self, locator, selector_type=None):
        """
        根据选择器类型获取元素
        :param locator: 定位器
        :param selector_type: 选择器类型
        :return: 元素对象或None
        """
        # 使用 _format_locator 方法格式化定位器
        locator = self._format_locator(locator, selector_type)
            
        try:
            element = self.page.ele(locator, timeout=0.1)  # 使用极短超时，由装饰器控制等待
            return element if element else None
        except Exception as e:
            self.logger.debug(f"元素查找失败: {e}")
            return None

    @element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
    def find_elements(self, locator, selector_type=None):
        """
        查找多个元素
        :param locator: 定位器
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :return: 元素列表
        """
        try:
            # 使用 _format_locator 方法格式化定位器
            locator = self._format_locator(locator, selector_type)
            
            # 查找多个元素并返回列表
            return self.page.eles(locator, timeout=0.1)  # 使用极短超时，由装饰器控制等待
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"查找元素列表失败: {e}")
            return []

    @element_wait_decorator(wait_type="clickable", timeout=20, raise_err=False)
    def click_element(self, locator, selector_type=None):
        """
        点击元素
        :param locator: 定位器，可以是字符串或列表
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :return: 是否成功点击
        """
        # 装饰器会等待元素可点击，这里我们只需要查找元素
        element = self.find_element(locator, selector_type)
        
        try:
            # 点击元素（装饰器已确保元素可点击）
            element.click()
            # 记录成功日志
            self.logger.info(f"成功点击元素: {locator}")
            return True
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"点击元素失败: {e}")
            return False

    @element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
    def get_element_text(self, locator, selector_type=None):
        """
        获取元素文本
        :param locator: 定位器，可以是字符串或列表
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :return: 元素文本或None
        """
        # 装饰器会等待元素存在，这里我们只需要查找元素
        element = self.find_element(locator, selector_type)
        
        try:
            # 获取元素文本（装饰器已确保元素存在）
            text = element.text
            # 记录成功日志
            self.logger.info(f"获取元素文本: {text}")
            return text
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"获取元素文本失败: {e}")
            return None

    def is_element_exists(self, locator, selector_type=None, timeout=3):
        """
        检查元素是否存在
        :param locator: 定位器，可以是字符串或列表
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :param timeout: 超时时间
        :return: 是否存在
        """
        try:
            # 查找元素并返回是否存在
            element = self.find_element(locator, selector_type)
            return element is not None
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"检查元素是否存在失败: {e}")
            return False

    @element_wait_decorator(wait_type="exists", timeout=20, raise_err=False)
    def wait_for_element(self, locator, selector_type=None):
        """
        等待元素出现
        :param locator: 定位器，可以是字符串或列表
        :param selector_type: 选择器类型，如 "css", "xpath", "tag" 等，默认为 None
        :return: 是否成功等到元素
        """
        # 装饰器会等待元素存在，这里我们只需要查找元素
        element = self.find_element(locator, selector_type)
        
        try:
            # 检查元素是否存在（装饰器已确保元素存在）
            if element:
                # 如果元素存在，记录成功日志
                self.logger.info(f"成功等待元素出现: {locator}")
                return True
            else:
                # 如果元素不存在，记录错误日志
                self.logger.error(f"等待元素超时: {locator}")
                return False
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"等待元素失败: {e}")
            return False

    def click_at_position(self, x, y):
        """
        点击指定坐标
        :param x: X坐标
        :param y: Y坐标
        :return: 是否成功点击
        """
        try:
            # 使用 JavaScript 在指定坐标执行点击
            self.page.run_js(f"document.elementFromPoint({x}, {y}).click();")
            self.logger.info(f"成功点击坐标({x}, {y})")
            return True
        except Exception as e:
            # 记录错误日志
            self.logger.error(f"点击坐标({x}, {y})失败: {e}")
            return False

    def close_float_layer(self, element, offset_y=40, fallback=True):
        """
        关闭浮层，点击元素顶部向上偏移指定像素的位置
        :param element: 浮层元素对象
        :param offset_y: 向上偏移的像素数，默认为40
        :param fallback: 是否使用备用方案，默认为True
        :return: 是否成功关闭浮层
        """
        try:
            # 使用 JavaScript 获取元素位置
            js_code = f"""
            var element = arguments[0];
            var rect = element.getBoundingClientRect();
            return {{
                x: rect.left + rect.width / 2,
                y: rect.top - {offset_y}
            }};
            """
            position = self.page.run_js(js_code, element)
            click_x = position['x']
            click_y = position['y']

            # 点击计算出的位置
            self.click_at_position(click_x, click_y)
            self.logger.info(f"点击浮层顶部向上{offset_y}像素位置({click_x}, {click_y})关闭浮层")
            return True
        except Exception as e:
            self.logger.error(f"点击浮层顶部位置失败: {str(e)}")
            if fallback:
                try:
                    # 使用默认点击方式作为备用方案
                    element.click()
                    self.logger.info("使用默认点击方式关闭浮层成功")
                    return True
                except Exception as inner_e:
                    self.logger.error(f"备用方案也失败: {str(inner_e)}")
                    return False
            return False
