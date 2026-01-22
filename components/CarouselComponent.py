from utils.logger_utils import LoggerUtils

class CarouselComponent:
    def __init__(self, page):
        """初始化，传入页面对象"""
        self.page = page
        self.logger = LoggerUtils.get_default_logger()

    def get_swiper_slides(self):
        """获取所有轮播图（标题和元素）"""
        slides = self.page.eles('css:.swiper-slide')
        result = []
        for slide in slides:
            title_ele = slide.ele('css:.text-lg')
            title = title_ele.text if title_ele else None
            result.append({'title': title, 'element': slide})
        return result

    def open_slide_by_title(self, title):
        """根据标题打开轮播图"""
        slides = self.get_swiper_slides()
        for slide in slides:
            if slide['title'] == title:
                slide['element'].click()
                return True
        self.logger.warning(f"没有找到标题为 {title} 的轮播图")
        return False

    def list_titles(self):
        """列出所有轮播图的标题"""
        slides = self.get_swiper_slides()
        return [slide['title'] for slide in slides]

    def wait_for_slide_to_load(self, index=0):
        """等待指定索引的轮播图加载（防止异步问题）"""
        self.page.wait(1)
        self.page.scroll.to_ele(self.page.ele(f'xpath://div[@data-swiper-slide-index="{index}"]'))
        self.page.wait(1)
