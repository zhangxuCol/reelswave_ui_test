from utils.logger_utils import LoggerUtils
from utils.page_actions import PageActions
from config.locators import SEARCH_PAGE, HOME_MORE_PAGE, VIDEO_PLAYER_PAGE

class SearchComponent:
    """搜索页面组件类"""

    def __init__(self, page):
        """初始化，传入页面对象"""
        self.page = page
        self.logger = LoggerUtils.get_default_logger()
        self.page_actions = PageActions(self.page)

    def open_search_page(self):
        """打开搜索页面"""
        self.logger.info("打开搜索页面")

        # 点击搜索图标
        if self.page_actions.click_element(SEARCH_PAGE["search_icon"], selector_type='css'):
            self.logger.info("成功点击搜索图标")
            self.page.wait(2)
            return True
        else:
            self.logger.error("点击搜索图标失败")
            return False

    def close_search_page(self, home_component):
        """关闭搜索页面，返回首页"""
        self.logger.info("关闭搜索页面")

        # 点击取消按钮
        if self.page_actions.click_element(SEARCH_PAGE["cancel_button"], selector_type='css'):
            self.logger.info("成功点击取消按钮")
            self.page.wait(2)
            home_component.wait_for_slide_to_load()
            return True
        else:
            self.logger.error("点击取消按钮失败")
            return False

    def search_keyword(self, keyword):
        """搜索关键词"""
        self.logger.info(f"搜索关键词: {keyword}")

        # 点击搜索输入框
        if self.page_actions.click_element(SEARCH_PAGE["search_input"], selector_type='css'):
            self.logger.info("成功点击搜索输入框")

            # 重新获取输入框元素并输入关键词
            search_input = self.page_actions.find_element(SEARCH_PAGE["search_input"], selector_type='css')
            if search_input:
                # 先清空输入框
                search_input.clear()

                # 输入关键词
                search_input.input(keyword)
                self.logger.info(f"已输入关键词并搜索: {keyword}")

                # 等待搜索结果
                self.page.wait(3)

                # 检查是否真的有搜索结果（检查 URL 或页面内容变化）
                current_url = self.page.url
                self.logger.info(f"当前 URL: {current_url}")

                return True
            else:
                self.logger.error("无法找到搜索输入框")
                return False
        else:
            self.logger.error("点击搜索输入框失败")
            return False

    def clear_search(self):
        """清空搜索内容"""
        self.logger.info("清空搜索内容")

        # 点击清空按钮
        if self.page_actions.click_element(SEARCH_PAGE["clear_button"], selector_type='css'):
            self.logger.info("成功点击清空按钮")
            self.page.wait(1)
            return True
        else:
            self.logger.warning("点击清空按钮失败，可能没有内容需要清空")
            return False

    def test_hot_search_elements(self, player_control):
        """测试热门搜索视频元素"""
        self.logger.info("开始测试热门搜索视频元素")

        # 使用 page_actions.find_elements 查找视频元素
        try:
            # 查找热门搜索区域的视频条目
            drama_items = self.page_actions.find_elements(
                HOME_MORE_PAGE["drama_item"],
                selector_type='css'
            )
            self.logger.info(f"找到 {len(drama_items)} 个热门搜索视频条目")

            # 逐个点击测试（只测试前2个，避免测试时间过长）
            for index, item in enumerate(drama_items[:2]):
                try:
                    # 尝试查找可点击的图片元素
                    img_elem = item.ele('css:img')
                    if img_elem:
                        elem_name = f"hot_search_item_{index + 1}"
                        self.logger.info(f"测试热门搜索视频 {index + 1}")

                        # 点击元素
                        img_elem.click()
                        self.logger.info(f"成功点击热门搜索视频 {index + 1}")

                        # 等待页面加载
                        self.page.wait(3)

                        # 检查是否进入播放器页面
                        video_player = player_control.play_pause()
                        if video_player:
                            self.logger.info(f"成功进入播放器页面 (点击热门搜索视频 {index + 1} 后)")
                            self.page.wait(3)

                            # 点击播放器，确保播放器处于活动状态
                            video_player.click()

                            # 点击返回按钮
                            back_button_locator = VIDEO_PLAYER_PAGE["player_back_button"]
                            if self.page_actions.click_element(back_button_locator, selector_type='css'):
                                self.logger.info(f"从播放器返回到搜索页面")
                                self.page.wait(2)
                            else:
                                self.logger.warning(f"未找到播放器返回按钮，后退")
                                self.page.back()
                                self.page.wait(2)
                        else:
                            self.logger.warning(f"点击热门搜索视频 {index + 1} 后未进入播放器页面")
                            self.page.back()
                            self.page.wait(2)
                    else:
                        self.logger.debug(f"热门搜索视频 {index + 1} 没有图片元素，跳过")
                except Exception as e:
                    self.logger.warning(f"测试热门搜索视频 {index + 1} 时出错: {str(e)}")
                    try:
                        self.page.back()
                        self.page.wait(2)
                    except:
                        pass

        except Exception as e:
            self.logger.error(f"提取热门搜索视频元素失败: {str(e)}")

        self.logger.info("热门搜索视频元素测试完成")
