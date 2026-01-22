import time

from components.CarouselComponent import CarouselComponent
from page.base import open_mobile_browser
from page.player_pytest import player_verify
from page.drama_home_test import test_drama_home
from utils.logger_utils import LoggerUtils

def home_banner():
    logger = LoggerUtils.get_default_logger()
    page = open_mobile_browser()

    # 创建 CarouselComponent 实例
    carousel = CarouselComponent(page)

    # 查看所有轮播图标题
    titles = carousel.list_titles()
    logger.info(f"轮播图标题: {titles}")

    for videotitle in titles:

        logger.info(f"当前轮播图标题: {videotitle}")
        # 根据标题点击某一张图
        carousel.open_slide_by_title(videotitle)

        #播放器验证
        player_verify(page)
        time.sleep(5)

    # 执行剧首页测试
    # logger.info("开始执行剧首页测试")
    # test_drama_home(page)



if __name__ == "__main__":
    # open_mobile_browser()
    home_banner()
