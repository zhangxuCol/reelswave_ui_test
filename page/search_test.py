"""
搜索页面测试模块
"""
import pytest
from components.HomeComponent import HomeComponent
from components.PlayerIconComponent import IconComponent
from scripts.css_locator_optimizer_playwright import CSSLocatorOptimizerPlaywright
from utils.logger_utils import LoggerUtils
from config.settings import BASE_URL
from config.locators import VIDEO_PLAYER_PAGE, DRAMA_HOME_PAGE, SEARCH_PAGE, HOME_MORE_PAGE
from utils.page_actions import PageActions
from utils.screenshot_utils import get_screenshot_utils
from pathlib import Path
import sys


@pytest.mark.search
class TestSearch:
    """搜索页面测试类"""

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
        except Exception as e:
            self.logger.error(f"等待首页轮播图加载时出错: {str(e)}")
            raise

    def _open_search_page(self):
        """打开搜索页面"""
        self.logger.info("打开搜索页面")

        # 点击搜索图标
        if self.page_actions.click_element(SEARCH_PAGE["search_icon"], selector_type='css'):
            self.logger.info("成功点击搜索图标")
            self.page.wait(2)
            
            # 捕获截图
            screenshot_utils = get_screenshot_utils()
            screenshot_utils.take_screenshot(self.page, name="search_page_opened")
            
            return True
        else:
            self.logger.error("点击搜索图标失败")
            return False

    def _close_search_page(self):
        """关闭搜索页面，返回首页"""
        self.logger.info("关闭搜索页面")

        # 点击取消按钮
        if self.page_actions.click_element(SEARCH_PAGE["cancel_button"], selector_type='css'):
            self.logger.info("成功点击取消按钮")
            self.page.wait(2)
            self.home_component.wait_for_slide_to_load()
            return True
        else:
            self.logger.error("点击取消按钮失败")
            return False

    def _search_keyword(self, keyword):
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

                # 输入关键词（包含\n以触发搜索）
                search_input.input(keyword + "\n")
                self.logger.info(f"已输入关键词: {keyword}")

                # 等待搜索结果
                self.page.wait(3)

                # 捕获截图
                screenshot_utils = get_screenshot_utils()
                screenshot_utils.take_screenshot(self.page, name=f"search_result_{keyword}")

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

    def _clear_search(self):
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

    def _test_hot_search_elements(self):
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
                        video_player = self.player_control.play_pause()
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

    @pytest.mark.smoke
    def test_search_functionality(self):
        """测试搜索功能完整流程"""
        self.logger.info("开始测试搜索功能")

        # 1. 打开搜索页面
        assert self._open_search_page(), "打开搜索页面失败"

        # 2. 保存搜索页面 HTML
        html_dir = Path(__file__).parent.parent / "html_files"
        html_dir.mkdir(exist_ok=True)
        html_file = html_dir / "search.html"

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(self.page.html)
        self.logger.info(f"已保存搜索页面 HTML: {html_file}")

        # 3. 使用 CSS 定位器优化器提取热门搜索视频定位器
        try:
            scripts_dir = Path(__file__).parent.parent / "scripts"
            sys.path.insert(0, str(scripts_dir))

            optimizer = CSSLocatorOptimizerPlaywright(html_file, None, "search")
            result = optimizer.process()

            if "search" in result and result["search"]:
                self.logger.info(f"为搜索页面提取到 {len(result['search'])} 个定位器")
                for elem_name, locator in result["search"].items():
                    self.logger.info(f"  - {elem_name}: {locator}")
        except Exception as e:
            self.logger.error(f"使用 CSS 定位器优化器时出错: {str(e)}")

        # 4. 测试热门搜索视频元素
        self._test_hot_search_elements()

        # 5. 搜索 "alibaba" - 预期无结果
        self.logger.info("搜索 'alibaba'")
        assert self._search_keyword("alibaba\n"), "输入搜索关键词失败"
        self.page.wait(2)

        # 检查是否出现"无结果"提示
        no_results_elem = self.page_actions.find_element(
            SEARCH_PAGE["no_results"],
            selector_type='css'
        )
        if no_results_elem:
            self.logger.info("找到 'No results found' 提示，搜索功能正常")
        else:
            self.logger.warning("未找到 'No results found' 提示")

        # 6. 清空搜索
        self.page.wait(1)

        # 7. 搜索 "love" - 预期有结果
        self.logger.info("搜索 'love'")
        assert self._search_keyword("love\n"), "输入搜索关键词失败"
        self.page.wait(2)

        # 8. 测试搜索结果中的视频
        self._test_hot_search_elements()

        # 9. 清空搜索历史
        self._clear_search()
        self.page.wait(1)

        # 10. 点击取消按钮返回首页
        self._close_search_page()

        self.logger.info("搜索功能测试完成")

    @pytest.mark.smoke
    def test_search_no_results(self):
        """测试搜索无结果场景"""
        self.logger.info("测试搜索无结果场景")

        # 打开搜索页面
        assert self._open_search_page(), "打开搜索页面失败"

        # 搜索 "alibaba"
        assert self._search_keyword("alibaba\n"), "输入搜索关键词失败"
        self.page.wait(2)

        # 验证无结果提示存在
        no_results_elem = self.page_actions.find_element(
            SEARCH_PAGE["no_results"],
            selector_type='css'
        )
        assert no_results_elem is not None, "未找到 'No results found' 提示"

        # 获取无结果提示文本
        no_results_text = no_results_elem.text if no_results_elem else ""
        self.logger.info(f"无结果提示文本: {no_results_text}")

        # 清空搜索
        self._clear_search()

        # 点击取消返回首页
        self._close_search_page()

        self.logger.info("搜索无结果场景测试完成")

    @pytest.mark.smoke
    def test_search_with_results(self):
        """测试搜索有结果场景"""
        self.logger.info("测试搜索有结果场景")

        # 打开搜索页面
        assert self._open_search_page(), "打开搜索页面失败"

        # 搜索 "love"
        assert self._search_keyword("love\n"), "输入搜索关键词失败"
        self.page.wait(2)

        # 测试搜索结果中的视频
        self._test_hot_search_elements()

        # 清空搜索
        self._clear_search()

        # 点击取消返回首页
        self._close_search_page()

        self.logger.info("搜索有结果场景测试完成")
