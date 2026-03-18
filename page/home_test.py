"""
首页测试模块
"""
import pytest
from components.HomeComponent import HomeComponent
from components.PlayerIconComponent import IconComponent
from scripts.css_locator_optimizer_playwright import CSSLocatorOptimizerPlaywright
from utils.logger_utils import LoggerUtils
from config.settings import BASE_URL
from config.locators import VIDEO_PLAYER_PAGE, DRAMA_HOME_PAGE, HOME_PAGE, HOME_MORE_PAGE
from utils.page_actions import PageActions
from utils.screenshot_utils import get_screenshot_utils
from pathlib import Path
import sys


@pytest.mark.carousel
class TestHome:
    """首页测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page):
        """测试夹具，在每个测试方法前执行"""
        self.logger = LoggerUtils.get_default_logger()
        self.page = page
        self.home_component = HomeComponent(self.page)
        self.page_actions = PageActions(self.page)
        self.player_control = IconComponent(self.page)

        # 导航到首页
        self.page.get(BASE_URL)
        self.logger.info(f"导航到首页: {BASE_URL}")

        # 等待页面加载完成
        try:
            self.home_component.wait_for_slide_to_load()
            self.logger.info("首页轮播图加载完成")
            
            # 捕获截图
            screenshot_utils = get_screenshot_utils()
            screenshot_utils.take_screenshot(self.page, name="home_page_loaded")
            
        except Exception as e:
            self.logger.error(f"等待首页轮播图加载时出错: {str(e)}")
            raise

    def _test_more_page_elements(self, section_name):
        """测试 MORE 页面中的所有元素 - 从当前页面动态提取"""
        self.logger.info(f"开始测试 MORE 页面元素: {section_name}")
        
        # 使用 page_actions.find_elements 查找剧集条目
        try:
            # 从配置中获取定位器
            drama_items = self.page_actions.find_elements(
                HOME_MORE_PAGE["drama_item"],
                selector_type='css'
            )
            self.logger.info(f"找到 {len(drama_items)} 个剧集条目")
            
            # 逐个点击测试
            for index, item in enumerate(drama_items):
                try:
                    # 尝试查找可点击的图片元素
                    img_elem = item.ele('css:img')
                    if img_elem:
                        elem_name = f"drama_item_{index + 1}"
                        self.logger.info(f"测试剧集 {index + 1}")
                        
                        # 点击元素
                        img_elem.click()
                        self.logger.info(f"成功点击剧集 {index + 1}")
                        
                        # 等待页面加载
                        self.page.wait(3)
                        
                        # 检查是否进入播放器页面
                        video_player = self.player_control.play_pause()
                        if video_player:
                            self.logger.info(f"成功进入播放器页面 (点击剧集 {index + 1} 后)")
                            self.page.wait(3)
                            
                            # 点击播放器，确保播放器处于活动状态
                            video_player.click()
                            
                            # 点击返回按钮
                            back_button_locator = VIDEO_PLAYER_PAGE["player_back_button"]
                            if self.page_actions.click_element(back_button_locator, selector_type='css'):
                                self.logger.info(f"从播放器返回到 MORE 页面")
                                self.page.wait(2)
                            else:
                                self.logger.warning(f"未找到播放器返回按钮，后退")
                                self.page.back()
                                self.page.wait(2)
                        else:
                            self.logger.warning(f"点击剧集 {index + 1} 后未进入播放器页面")
                            self.page.back()
                            self.page.wait(2)
                    else:
                        self.logger.debug(f"剧集 {index + 1} 没有图片元素，跳过")
                except Exception as e:
                    self.logger.warning(f"测试剧集 {index + 1} 时出错: {str(e)}")
                    try:
                        self.page.back()
                        self.page.wait(2)
                    except:
                        pass
                        
        except Exception as e:
            self.logger.error(f"提取 MORE 页面元素失败: {str(e)}")
        
        self.logger.info(f"MORE 页面元素测试完成: {section_name}")

    def _return_to_home_from_more(self):
        """从 MORE 页面返回到首页"""
        self.logger.info("从 MORE 页面返回首页")
        
        # 尝试点击返回按钮
        back_button_locator = DRAMA_HOME_PAGE["back_button"]
        if self.page_actions.click_element(back_button_locator, selector_type='css'):
            self.logger.info("成功通过返回按钮返回首页")
            self.home_component.wait_for_slide_to_load()
            return True
        else:
            self.logger.warning("未找到返回按钮，重新加载首页")
            self.page.get(BASE_URL)
            self.home_component.wait_for_slide_to_load()
            return True

    @pytest.mark.smoke
    def test_banner_carousel(self):
        """测试首页 banner 轮播图"""
        self.logger.info("测试首页 banner 轮播图")

        titles = self.home_component.list_titles()
        assert len(titles) > 0, "未找到任何轮播图"
        self.logger.info(f"轮播图标题: {titles}")

        for index, title in enumerate(titles):
            self.logger.info(f"当前轮播图标题: {title}")

            assert self.home_component.open_slide_by_title(title), f"点击标题为 {title} 的轮播图失败"
            self.logger.info(f"成功点击轮播图: {title}")

            self.page.wait(5)
            
            # 捕获截图
            screenshot_utils = get_screenshot_utils()
            screenshot_utils.take_screenshot(self.page, name=f"banner_carousel_{index}")

            video_player = self.player_control.play_pause()
            if video_player:
                self.logger.info("成功进入播放器页面")
                self.page.wait(3)
            else:
                self.logger.warning(f"点击轮播图 {title} 后未进入播放器页面")

            if index < len(titles) - 1:
                video_player = self.player_control.play_pause()

                if video_player:
                    video_player.click()

                    back_button_locator = VIDEO_PLAYER_PAGE["player_back_button"]
                    if self.page_actions.click_element(back_button_locator, selector_type='css'):
                        self.logger.info(f"通过后退按钮返回首页")
                        self.home_component.wait_for_slide_to_load()
                    else:
                        self.logger.warning(f"未找到后退按钮，重新加载首页")
                        self.page.get(BASE_URL)
                        self.home_component.wait_for_slide_to_load()
                else:
                    self.logger.warning(f"播放器不存在，重新加载首页")
                    self.page.get(BASE_URL)
                    self.home_component.wait_for_slide_to_load()

        self.logger.info("首页 banner 轮播图测试完成")

    @pytest.mark.smoke
    def test_home_page_locators(self):
        """测试首页所有定位器"""
        self.logger.info("开始测试首页所有定位器")

        # 添加 scripts 目录到路径
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir))

        # 遍历 HOME_PAGE 中的所有定位器
        for locator_name, locator_value in HOME_PAGE.items():
            self.logger.info(f"测试定位器: {locator_name}, 值: {locator_value}")

            # 判断是否是 more 入口
            is_more_entry = locator_name.endswith('_more')

            # 如果不是 more 入口，跳过
            if not is_more_entry:
                self.logger.info(f"定位器 {locator_name} 不是 more 入口，跳过")
                continue

            # 点击定位器
            if self.page_actions.click_element(locator_value, selector_type='css'):
                self.logger.info(f"成功点击定位器: {locator_name}")

                # 等待页面加载
                self.page.wait(3)
                
                # 捕获截图
                screenshot_utils = get_screenshot_utils()
                screenshot_utils.take_screenshot(self.page, name=f"home_locator_{locator_name}")

                if is_more_entry:
                    # 如果是 more 入口，等待页面完全打开
                    self.logger.info(f"等待 {locator_name} 页面完全打开")
                    self.page.wait(2)

                    # 提取栏目名
                    section_name = locator_name.replace('_more', '')

                    # 保存 HTML 文件
                    html_dir = Path(__file__).parent.parent / "html_files"
                    html_dir.mkdir(exist_ok=True)
                    html_file = html_dir / f"{section_name}.html"

                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(self.page.html)
                    self.logger.info(f"已保存 HTML 文件: {html_file}")

                    # 动态测试 MORE 页面元素
                    self._test_more_page_elements(section_name)

                    # 测试完成后返回首页
                    self._return_to_home_from_more()
                else:
                    # 如果不是 more 入口，验证是否打开播放器
                    try:
                        video_player = self.player_control.play_pause()
                        if video_player:
                            self.logger.info(f"成功进入播放器页面")
                            self.page.wait(3)

                            video_player.click()

                            back_button_locator = VIDEO_PLAYER_PAGE["player_back_button"]
                            if self.page_actions.click_element(back_button_locator, selector_type='css'):
                                self.logger.info(f"通过后退按钮返回首页")
                                self.home_component.wait_for_slide_to_load()
                            else:
                                self.logger.warning(f"未找到后退按钮，重新加载首页")
                                self.page.get(BASE_URL)
                                self.home_component.wait_for_slide_to_load()
                        else:
                            self.logger.warning(f"点击 {locator_name} 后未进入播放器页面")
                            self.page.get(BASE_URL)
                            self.home_component.wait_for_slide_to_load()
                    except Exception as e:
                        self.logger.warning(f"点击 {locator_name} 后发生异常: {str(e)}")
                        self.page.get(BASE_URL)
                        self.home_component.wait_for_slide_to_load()
            else:
                # 定位器失败时截图
                screenshot_dir = Path(__file__).parent.parent / "screenshots"
                screenshot_dir.mkdir(exist_ok=True)
                screenshot_file = screenshot_dir / f"locator_failed_{locator_name}.png"
                self.page.get_screenshot(path=str(screenshot_file))
                self.logger.error(f"点击定位器 {locator_name} 失败，已截图: {screenshot_file}")

                # 断言失败，使测试失败
                pytest.fail(f"点击定位器 {locator_name} 失败")

        self.logger.info("首页所有定位器测试完成")
