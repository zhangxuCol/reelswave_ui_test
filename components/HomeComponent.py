from utils.logger_utils import LoggerUtils
from utils.page_actions import PageActions

class HomeComponent:
    def __init__(self, page):
        """初始化，传入页面对象"""
        self.page = page
        self.page_actions = PageActions(page)
        self.logger = LoggerUtils.get_default_logger()

    def get_swiper_slides(self):
        """获取所有轮播图（标题和元素）"""
        slides = self.page_actions.find_elements('.swiper-slide', selector_type='css')
        result = []
        for slide in slides:
            # 在当前轮播图元素内查找标题
            title_ele = slide.ele('css:.text-lg', timeout=0.1)
            title = title_ele.text if title_ele else None
            result.append({'title': title, 'element': slide})
        return result

    def open_slide_by_title(self, title):
        """根据标题打开轮播图"""
        # 获取所有轮播图
        slides = self.get_swiper_slides()
        self.logger.info(f"当前页面共有 {len(slides)} 个轮播图")

        # 遍历轮播图，查找目标标题
        for index, slide in enumerate(slides):
            self.logger.debug(f"检查第 {index} 个轮播图，标题: {slide['title']}")
            if slide['title'] == title:
                self.logger.info(f"找到目标轮播图，索引: {index}，标题: {title}")

                # 使用 JavaScript 滚动到目标轮播图，避免触发轮播图动画
                self.page.run_js(f'arguments[0].scrollIntoView({{behavior: "instant", block: "center"}})', slide['element'])
                # 等待轮播图滚动到可见位置
                self.page.wait(1)

                # 再次确认轮播图标题是否正确（在目标轮播图元素内查找）
                title_ele = slide['element'].ele('css:.text-lg', timeout=0.1)
                current_title = title_ele.text if title_ele else None
                self.logger.info(f"滚动后轮播图标题: {current_title}")

                if current_title != title:
                    self.logger.warning(f"轮播图标题不匹配，期望: {title}，实际: {current_title}")
                    # 尝试重新获取轮播图
                    slides = self.get_swiper_slides()
                    for new_slide in slides:
                        if new_slide['title'] == title:
                            slide = new_slide
                            break

                # 等待轮播图完全停下
                self.page.wait(2)

                # 尝试点击轮播图内部的标题元素（在目标轮播图元素内查找）
                title_ele = slide['element'].ele('css:.text-lg', timeout=0.1)
                if title_ele:
                    title_ele.click()
                    self.logger.info(f"成功点击轮播图标题: {title}")
                    return True
                else:
                    # 如果没有找到标题元素，则点击整个轮播图
                    slide['element'].click()
                    self.logger.info(f"成功点击轮播图元素: {title}")
                    return True
        self.logger.warning(f"没有找到标题为 {title} 的轮播图")
        return False

    def list_titles(self):
        """列出所有轮播图的标题"""
        slides = self.get_swiper_slides()
        return [slide['title'] for slide in slides]

    def wait_for_slide_to_load(self, index=0):
        """等待指定索引的轮播图加载（防止异步问题）"""
        self.logger.debug(f"等待轮播图加载，目标索引: {index}")

        # 等待轮播图容器出现
        max_retries = 10
        retry_count = 0

        while retry_count < max_retries:
            # 使用 CSS 选择器查找轮播图元素
            slides = self.page_actions.find_elements('.swiper-slide', selector_type='css')

            if slides and len(slides) > index:
                self.logger.debug(f"找到 {len(slides)} 个轮播图，滚动到第 {index} 个")
                self.page.scroll.to_see(slides[index])
                self.page.wait(1)
                return

            self.logger.debug(f"第 {retry_count + 1} 次尝试：未找到足够的轮播图，当前找到 {len(slides) if slides else 0} 个")
            self.page.wait(1)
            retry_count += 1

        self.logger.warning(f"等待轮播图加载超时，当前找到 {len(slides) if slides else 0} 个")
