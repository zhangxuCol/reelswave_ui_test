# utils/decorators.py
from functools import wraps
from utils.logger_utils import LoggerUtils

def element_wait_decorator(
    wait_type: str = "clickable",  # 等待类型：clickable/exists（你的版本支持的核心类型）
    timeout: int = 8,              # 超时时间
    raise_err: bool = False        # 未找到是否报错
):
    """
    适配「元素链式等待」的装饰器（完全贴合你的原生写法）
    核心：用 element.wait.clickable() / element.wait.exists()，和你手动写的一致
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 获取日志记录器
            logger = getattr(self, 'logger', LoggerUtils.get_default_logger())

            try:
                # 1. 特殊处理 click_element、get_element_text 和 wait_for_element 方法
                if func.__name__ == "click_element":
                    # 对于 click_element，我们需要先获取参数，然后查找并等待元素
                    locator = args[0]  # 第一个参数是定位器
                    selector_type = args[1] if len(args) > 1 else kwargs.get('selector_type')
                    
                    # 查找元素
                    element = self.find_element(locator, selector_type)
                    
                    # 如果元素不存在，则尝试等待
                    if not element:
                        # 使用 DrissionPage 的等待机制
                        try:
                            # 使用 _format_locator 方法格式化定位器
                            locator = self._format_locator(locator, selector_type)
                            
                            # 等待元素出现并可点击
                            element = self.page.ele(locator, timeout=timeout)
                            if element:
                                element.wait.clickable(timeout=timeout)
                        except Exception as e:
                            logger.error(f"等待元素可点击失败: {e}")
                            return None
                    
                    # 执行原始方法，传入已找到的元素
                    return func(self, locator, selector_type)
                
                # 特殊处理需要等待元素的方法（get_element_text 和 wait_for_element）
                if func.__name__ in ["get_element_text", "wait_for_element"]:
                    # 获取参数
                    locator = args[0]  # 第一个参数是定位器
                    selector_type = args[1] if len(args) > 1 else kwargs.get('selector_type')
                    
                    # 查找元素
                    element = self.find_element(locator, selector_type)
                    
                    # 如果元素不存在，则尝试等待
                    if not element:
                        # 使用 DrissionPage 的等待机制
                        try:
                            # 使用 _format_locator 方法格式化定位器
                            locator = self._format_locator(locator, selector_type)
                            
                            # 等待元素出现
                            element = self.page.ele(locator, timeout=timeout)
                        except Exception as e:
                            logger.error(f"等待元素存在失败: {e}")
                            return None
                    
                    # 执行原始方法，传入已找到的元素
                    return func(self, locator, selector_type)
                
                # 对于其他方法（如 find_element），需要特殊处理
                # 获取定位器和选择器类型参数
                locator = args[0] if len(args) > 0 else kwargs.get('locator')
                selector_type = args[1] if len(args) > 1 else kwargs.get('selector_type')

                # 如果是 find_element 方法，需要等待元素出现
                if func.__name__ == "find_element":
                    # 格式化定位器
                    locator = self._format_locator(locator, selector_type)

                    # 使用 DrissionPage 的等待机制，等待元素出现
                    try:
                        logger.debug(f"开始等待元素出现：{locator}，超时：{timeout}秒")
                        element = self.page.ele(locator, timeout=timeout)
                        if element:
                            logger.debug(f"元素等待成功：{locator}")
                            return element
                        else:
                            logger.warning(f"元素等待超时：{locator}")
                            return None
                    except Exception as e:
                        logger.error(f"等待元素出现失败: {e}")
                        return None

                # 对于其他方法，执行原方法并获取返回值
                result = func(self, *args, **kwargs)
                element = result

                # 处理元素为 None 或 False 的情况
                if element is None or element is False:
                    logger.warning("方法未找到元素，返回 None")
                    return None
                    
                # 2.5 检查元素是否为布尔值或其他非元素对象
                if isinstance(element, bool):
                    logger.debug(f"返回的是布尔值而不是元素对象: {element}")
                    return element  # 直接返回布尔值
                    
                # 确保元素对象有 wait 属性
                if not hasattr(element, 'wait'):
                    logger.debug(f"元素对象没有 wait 属性: {type(element)}")
                    return element  # 直接返回元素对象

                # 3. 提取元素信息（用于日志）
                try:
                    if hasattr(element, 'locator'):
                        locator = element.locator
                    elif hasattr(element, 'tag'):
                        locator = f"元素对象（标签：{element.tag}）"
                    else:
                        locator = "未知元素"
                except Exception as e:
                    # 记录调试信息
                    logger.debug(f"获取元素信息失败: {e}")
                    locator = "未知元素"
                logger.debug(f"开始等待元素（{wait_type}）：{locator}，超时：{timeout}秒")

                # 4. 核心：用你的原生链式等待写法（和你手动写的完全一致）
                try:
                    if wait_type == "clickable":
                        # 等同于你写的：element.wait.clickable()
                        element.wait.clickable(timeout=timeout)
                    elif wait_type == "exists":
                        # 对于 exists 类型，等待元素显示
                        element.wait.displayed(timeout=timeout)
                except Exception as wait_error:
                    logger.error(f"元素等待异常: {wait_error}")
                    return None

                # 5. 等待成功，返回元素对象
                logger.debug(f"元素等待成功：{locator}")
                return element

            except Exception as e:
                err_msg = f"元素等待失败：{str(e)}"
                logger.error(err_msg)
                if raise_err:
                    raise  # 要求报错时抛出异常
                return None
        return wrapper
    return decorator