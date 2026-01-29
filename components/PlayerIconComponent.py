import time
import DrissionPage

from utils.decorators import element_wait_decorator
from utils.logger_utils import LoggerUtils
from utils.page_actions import PageActions
from config.locators import VIDEO_PLAYER_PAGE


class IconComponent:
    def __init__(self, page):
        """
        初始化IconComponent类
        :param page: 页面对象，用于操作页面元素
        """
        self.page = page
        self.logger = LoggerUtils.get_default_logger()
        self.locators = VIDEO_PLAYER_PAGE
        self.page_actions = PageActions(page)

    def is_player_menu_open(self):
        """
        检查播放器菜单是否已打开，通过检查返回按钮、收藏按钮和菜单按钮是否可见
        :return: 布尔值，True表示菜单已打开，False表示菜单未打开
        """
        try:
            # 方法1：检查菜单按钮是否可点击
            menu_element = self.page_actions.find_element(self.locators["player_menu"], "css")
            if menu_element:
                try:
                    # 检查元素是否可点击
                    if menu_element.wait.clickable(timeout=3):
                        self.logger.debug("菜单按钮可点击")
                    else:
                        self.logger.debug("菜单按钮不可点击")
                except DrissionPage.errors.WaitTimeoutError:
                    self.logger.debug("等待菜单按钮可点击超时")

            # 方法2：检查关键元素是否可见（原is_player_menu_open逻辑）
            # 检查返回按钮是否可见
            back_button = self.page_actions.find_element(self.locators["player_back_button"], "css")
            if not back_button:
                self.logger.debug("返回按钮未找到，播放器菜单可能未打开")
                return False

            # 检查收藏按钮是否可见（检查两种状态）
            favorite_collected = self.page_actions.find_element(self.locators["favorite_collected"], "css")
            favorite_uncollected = self.page_actions.find_element(self.locators["favorite_uncollected"], "css")
            if not (favorite_collected or favorite_uncollected):
                self.logger.debug("收藏按钮未找到，播放器菜单可能未打开")
                return False

            # 检查菜单按钮是否可见
            menu_button = self.page_actions.find_element(self.locators["player_menu"], "css")
            if not menu_button:
                self.logger.debug("菜单按钮未找到，播放器菜单可能未打开")
                return False

            # 所有关键元素都可见，认为播放器菜单已打开
            self.logger.info("播放器菜单已打开（检测到返回按钮、收藏按钮和菜单按钮）")
            return True

        except Exception as e:
            self.logger.error(f"检查播放器菜单状态时出错: {str(e)}")
            return False



    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_icon(self):
        """播放图标"""
        return self.page_actions.find_element(self.locators["player_pause_button"], "css")

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_pause(self):
        """定位当前激活slide的播放器（修复wait语法+精准定位）"""
        try:
            # 旧版本修复：用 page.ele() 直接带超时，替代 page.wait.ele()
            # 精准定位：当前激活的slide → 里面的prism-player → 最终的video标签（播放/暂停核心元素）
            active_slide = self.page_actions.find_element(self.locators["active_slide"], "css")
            if not active_slide:
                raise DrissionPage.errors.ElementNotFoundError("无法定位当前激活的slide")

            # 先找播放器容器，再找视频核心元素（优先定位video标签，点击更精准）
            player_container = active_slide.ele(f'css:{self.locators["player_container"]}', timeout=5)
            if not player_container:
                raise DrissionPage.errors.ElementNotFoundError("无法定位播放器容器")

            video_player = player_container.ele(self.locators["video_element"], timeout=5)
            if not video_player:
                raise DrissionPage.errors.ElementNotFoundError("无法定位视频元素")

            self.logger.info("成功定位当前激活slide的播放器")
            return video_player  # 返回video标签，点击即可播放/暂停

        except Exception as e:
            # 处理定位播放器失败的情况
            self.logger.error(f"定位播放器失败：{str(e)}")
            raise  # 抛出异常，方便排查

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=False)
    def play_back(self):
        """返回按钮图标"""
        # 定位返回按钮图标元素
        back_icon = self.page_actions.find_element(self.locators["player_back_button"], "css")
        # 备选定位方式（已注释）
        # back_icon = self.page.ele('css:.flex.items-center.justify-start.gap-sm .icon-svg')
        return back_icon

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def favorite_icon(self, is_collected: bool = False):
        """收藏按钮"""
        # 已经收藏
        if is_collected:
            # 定位已收藏状态的收藏图标
            favoriteicon = self.page_actions.find_element(self.locators["favorite_collected"], "css")
        else:
            # 未收藏
            # 定位未收藏状态的收藏图标
            favoriteicon = self.page_actions.find_element(self.locators["favorite_uncollected"], "css")
        return favoriteicon

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def mute_icon(self, is_mute: bool = False):
        """静音图标"""
        try:
            if is_mute:
                # 静音状态
                # 定位静音状态的图标
                muteicon = self.page_actions.find_element(self.locators["mute_active"], "css")
            else:
                # 未静音状态
                # 定位未静音状态的图标
                muteicon = self.page_actions.find_element(self.locators["mute_inactive"], "css")
            return muteicon
        except Exception as e:
            # 处理静音图标定位异常
            self.logger.error(f"定位静音图标失败: {str(e)}")
            return None

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_menu(self):
        """播放器菜单"""
        # 定位播放器菜单元素并确保其可点击
        try:
            # 使用PageActions查找元素
            menu_element = self.page_actions.find_element(self.locators["player_menu"], "css")
            if menu_element:
                # 等待元素可点击
                clickable_menu = menu_element.wait.clickable(timeout=5)
                self.logger.info("成功定位播放器菜单元素")
                return clickable_menu
            else:
                self.logger.error("无法定位播放器菜单元素")
                raise DrissionPage.errors.ElementNotFoundError("播放器菜单元素未找到")
        except DrissionPage.errors.ElementNotFoundError:
            self.logger.error("播放器菜单元素未找到")
            raise
        except DrissionPage.errors.WaitTimeoutError:
            self.logger.error("等待播放器菜单元素可点击超时")
            raise
        except Exception as e:
            self.logger.error(f"定位播放器菜单时发生未知错误: {str(e)}")
            raise

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_menu_speed(self, speed):
        """视频播放速度"""
        try:
            speed_obj = self.page_actions.find_element(self.locators["menu_speed_container"], "css")
            if not speed_obj:
                self.logger.error("无法定位播放速度列表容器")
                raise DrissionPage.errors.ElementNotFoundError("播放速度列表容器未找到")

            speed_list = self.page_actions.find_elements('tag:div', "tag")
            if not speed_list:
                self.logger.error("播放速度列表为空")
                raise DrissionPage.errors.ElementNotFoundError("播放速度选项未找到")

            for speed_index in speed_list:
                if speed_index.text == speed:
                    self.logger.info(f"找到匹配的播放速度: {speed}")
                    return speed_index

            self.logger.error(f"未找到匹配的播放速度: {speed}")
            raise DrissionPage.errors.ElementNotFoundError(f"未找到播放速度: {speed}")
        except Exception as e:
            self.logger.error(f"定位播放速度时出错: {str(e)}")
            raise

    def get_play_speed_text(self):
        """获取所有播放速度文本"""
        try:
            speed_list = self.page_actions.find_elements(self.locators["menu_speed_container"], "css")
            if not speed_list:
                self.logger.warning("播放速度列表为空")
                return []

            speed_text_list = [speed.text for speed in speed_list]
            self.logger.info(f"找到 {len(speed_text_list)} 个播放速度选项: {speed_text_list}")
            return speed_text_list
        except Exception as e:
            self.logger.error(f"获取播放速度列表时出错: {str(e)}")
            return []

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_menu_quality(self, quality):
        """视频播放质量"""
        try:
            quality_obj = self.page_actions.find_element(self.locators["menu_quality_container"], "css")
            if not quality_obj:
                self.logger.error("无法定位播放质量列表容器")
                raise DrissionPage.errors.ElementNotFoundError("播放质量列表容器未找到")

            quality_list = self.page_actions.find_elements('tag:div', "tag")
            if not quality_list:
                self.logger.error("播放质量列表为空")
                raise DrissionPage.errors.ElementNotFoundError("播放质量选项未找到")

            for quality_index in quality_list:
                if quality_index.text == quality:
                    self.logger.info(f"找到匹配的播放质量: {quality}")
                    return quality_index

            self.logger.error(f"未找到匹配的播放质量: {quality}")
            raise DrissionPage.errors.ElementNotFoundError(f"未找到播放质量: {quality}")
        except Exception as e:
            self.logger.error(f"定位播放质量时出错: {str(e)}")
            raise

    def get_play_quality_text(self):
        """视频播放质量"""
        try:
            quality_list = self.page_actions.find_elements(self.locators["menu_quality_container"], "css")
            if not quality_list:
                self.logger.warning("播放质量列表为空")
                return []

            quality_text_list = [quality.text for quality in quality_list]
            self.logger.info(f"找到 {len(quality_text_list)} 个播放质量选项: {quality_text_list}")
            return quality_text_list
        except Exception as e:
            self.logger.error(f"获取播放质量列表时出错: {str(e)}")
            return []

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_title(self):
        """播放器-菜单-标题"""
        playtitle = self.page_actions.find_element(self.locators["player_title"], "css")
        return playtitle

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_introduction(self):
        """播放器-菜单-简介"""
        playintroduction = self.page_actions.find_element(self.locators["player_introduction"], "css")
        return playintroduction

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)
    def play_catalog(self):
        """播放器-菜单-目录"""
        playcatalog = self.page_actions.find_element(self.locators["player_catalog"], "css")
        return playcatalog

    def get_catalogtab_text(self):
        """播放器-菜单-目录-分组text"""
        catalogtab = self.page_actions.find_element(self.locators["catalog_tab"], "css")
        if not catalogtab:
            self.logger.warning("无法定位目录标签容器")
            return []

        catalogtab_list = self.page_actions.find_elements('tag:div', "tag")
        catalog_text_list = [catalog.text for catalog in catalogtab_list]
        return catalog_text_list


    def get_catalog_text(self):
        """播放器-菜单-目录-分组中的剧集列表"""
        catalogtab = self.page_actions.find_element(self.locators["catalog_grid"], "css")
        if not catalogtab:
            self.logger.warning("无法定位目录网格容器")
            return []

        catalogtab_list = self.page_actions.find_elements('tag:div', "tag")
        catalog_text_list = [catalog.text for catalog in catalogtab_list]
        return catalog_text_list

    @element_wait_decorator(wait_type="clickable", timeout=25, raise_err=True)  # 使用装饰器等待元素可点击，设置超时时间为25秒，如果元素不可点击则抛出异常
    def play_introduction_catalog_title(self):  # 定义一个方法，用于获取聚合页的标题
        """聚合页的标题"""  # 方法的文档字符串，说明此方法的作用是获取聚合页的标题
        inca_obj = self.page_actions.find_element(self.locators["player_introduction_catalog_title"], "css")  # 使用PageActions查找元素，获取聚合页的标题元素
        return inca_obj  # 返回获取到的标题元素




