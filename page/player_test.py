"""
播放器测试模块
"""
import pytest
from components.PlayerIconComponent import IconComponent
from utils.logger_utils import LoggerUtils
from page.base import get_current_url
from config.locators import VIDEO_PLAYER_PAGE
from utils.page_actions import PageActions
from utils.screenshot_utils import get_screenshot_utils


class TestPlayer:
    """播放器测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, player_page):
        """
        测试夹具，在每个测试方法前执行
        此夹具用于初始化测试环境，包括设置日志记录器、页面实例、播放器组件，
        并导航到播放器页面，确保播放器加载完成
        """
        self.logger = LoggerUtils.get_default_logger()
        self.page = player_page
        self.player_control = IconComponent(self.page)

        # 先通过剧首页打开播放器
        from components.DramaHomeComponent import DramaHomeComponent
        from config.settings import TEST_HOME_URL

        # 导航到剧首页
        self.page.get(TEST_HOME_URL)
        self.logger.info(f"导航到剧首页: {TEST_HOME_URL}")

        # 创建剧首页组件并点击"去看剧"按钮打开播放器
        drama_home = DramaHomeComponent(self.page)
        drama_home.wait_for_elements_loaded()
        self.logger.info("剧首页元素加载完成")

        # 点击"去看剧"按钮打开播放器
        assert drama_home.click_watch_button(), "点击'去看剧'按钮失败"
        self.logger.info("成功点击'去看剧'按钮，打开播放器")

        # 等待播放器加载
        self.page.wait(5)
        self.logger.info("播放器加载完成")

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_loaded")

        # 初始化播放器组件
        self.player_control = IconComponent(self.page)
        self.currenturl = get_current_url(self.page)



    def _wait_for_condition(self, condition_func, timeout=10, interval=0.5, error_msg="等待条件超时"):
        """
        等待条件满足
        :param condition_func: 条件函数，返回 True 表示条件满足
        :param timeout: 超时时间（秒）
        :param interval: 检查间隔（秒）
        :param error_msg: 超时错误信息
        :return: 是否成功等待
        """
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        self.logger.error(error_msg)
        return False

    def _ensure_player_menu_open(self):
        """
        确保播放器菜单已打开，如果未打开则尝试打开
        :return: 是否成功打开菜单
        :raises Exception: 如果无法打开播放器菜单
        """
        if self.player_control.is_player_menu_open():
            self.logger.debug("播放器菜单已打开")
            return True

        self.logger.info("播放器菜单未打开，尝试打开菜单")
        try:
            video_player = self.player_control.play_pause()
            video_player.click()
            self.logger.info("播放器菜单打开成功")
            return True
        except Exception as e:
            error_msg = f"无法打开播放器菜单: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)

    def _close_player_menu(self):
        """
        关闭播放器菜单/聚合页/浮层
        :return: 是否成功关闭菜单
        """
        try:
            # 使用 PageActions 的方法关闭聚合页/浮层
            page_actions = PageActions(self.page)

            # 尝试找到浮层元素
            float_layer = page_actions.find_element(VIDEO_PLAYER_PAGE["float_layer"], "css")

            if float_layer:
                self.logger.info("发现浮层，尝试使用 close_float_layer 方法关闭")
                if page_actions.close_float_layer(float_layer):
                    self.logger.info("使用 close_float_layer 方法关闭浮层成功")
                    return True
                else:
                    self.logger.warning("使用 close_float_layer 方法关闭浮层失败，尝试备用方案")

            # 备用方案：点击播放器关闭菜单
            self.logger.info("尝试点击播放器关闭菜单")
            video_player = self.player_control.play_pause()
            if video_player:
                video_player.click()

            # 使用条件等待，最多等待1秒，等待菜单关闭
            if self._wait_for_condition(
                lambda: not self.player_control.is_player_menu_open(),
                timeout=1,
                error_msg="等待播放器菜单关闭超时"
            ):
                self.logger.info("播放器菜单关闭成功")
                return True
            else:
                self.logger.warning("播放器菜单关闭超时")
                return False
        except Exception as e:
            self.logger.error(f"关闭播放器菜单失败: {str(e)}")
            return False

    def _click_video_player(self, video_player, action_name="点击播放器"):
        """
        点击播放器，如果播放器菜单未打开就执行点击操作，如果已经打开就跳过

        :param video_player: 播放器元素
        :param action_name: 操作名称，用于日志记录
        :return: 播放器元素
        """
        if not self.player_control.is_player_menu_open():
            # 播放器菜单未打开，执行点击操作
            video_player.click()
            self.logger.info(f"{action_name}操作成功")
        else:
            # 播放器菜单已打开，跳过点击操作
            self.logger.info(f"播放器菜单已打开，跳过{action_name}操作")
        return video_player

    @pytest.mark.smoke
    def test_pause_play(self):
        """测试暂停和播放功能"""
        self.logger.info("测试暂停和播放功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"

        # 唤起播放器菜单-->暂停播放
        video_player = self._click_video_player(video_player, "唤起播放器菜单")

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        # 重新获取播放器元素，避免 ElementLostError
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"

        # 执行暂停操作
        video_player = self._click_video_player(video_player, "执行暂停操作")
        # 使用条件等待，最多等待5秒，等待菜单关闭
        self.page.wait(5)
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_paused")

        # 继续播放
        # 重新获取播放器元素，避免 ElementLostError
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"

        video_player = self._click_video_player(video_player, "继续播放操作")
        # 等待视频播放一段时间（10秒）
        self.page.wait(10)
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_playing")

        # 再次确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 执行暂停操作
        # 重新获取播放器元素，避免 ElementLostError
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"

        video_player = self._click_video_player(video_player, "再次执行暂停操作")
        # 使用条件等待，最多等待5秒，等待菜单关闭
        self.page.wait(5)
        
        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_paused_again")

    @pytest.mark.regression
    def test_home_page(self):
        """测试打开首页功能"""
        self.logger.info("测试打开首页功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"
        video_player.click()
        # 等待 3 秒确保菜单是打开的。
        self.page.wait(8)

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        # 打开首页
        play_title = self.player_control.play_title()
        assert play_title is not None, "未找到首页按钮"
        play_title.click()
        self.logger.info("打开首页成功")
        self.page.wait(3)

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="home_page_opened")

        # 使用条件等待，最多等待5秒，等待首页加载完成
        assert self._wait_for_condition(
            lambda: self.player_control.play_back() is not None,
            timeout=5,
            error_msg="等待首页加载超时"
        ), "等待首页加载超时"

        # 返回
        player_home_back = self.player_control.play_back()
        assert player_home_back is not None, "未找到返回按钮"
        player_home_back.click()
        # 使用条件等待，最多等待2秒，等待首页关闭
        assert self._wait_for_condition(
            lambda: self.player_control.play_back() is None,
            timeout=2,
            error_msg="等待首页关闭超时"
        ), "等待首页关闭超时"
        self.logger.info("退出首页成功")

    @pytest.mark.regression
    def test_introduction_page(self):
        """测试打开聚合页-简介功能"""
        self.logger.info("测试打开聚合页-简介功能")

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        # 打开聚合页-简介
        self.logger.info("尝试打开聚合页-简介")
        player_introduction = self.player_control.play_introduction()
        assert player_introduction is not None, "未找到简介按钮"
        player_introduction.click()

        self.page.wait(3)

        # 使用条件等待，最多等待30秒，等待聚合页打开和页面加载完成
        assert self._wait_for_condition(
            lambda: self.player_control.play_introduction_catalog_title() is not None,
            timeout=30,
            error_msg="等待聚合页打开或页面加载完成超时"
        ), "等待聚合页打开或页面加载完成超时"
        self.logger.info("播放器聚合页打开成功")

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="introduction_page_opened")

        # 确保菜单已打开（等待期间菜单可能已关闭）
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 关闭聚合页/浮层
        self.logger.info("定位标题并关闭聚合页/浮层")
        introduction_catalog = self.player_control.play_introduction_catalog_title()
        self.page.wait(2)

        # 使用 PageActions 的方法关闭聚合页/浮层
        page_actions = PageActions(self.page)

        # 尝试使用 close_float_layer 方法关闭聚合页/浮层
        if introduction_catalog:
            # 如果找到了标题元素，尝试关闭聚合页
            if page_actions.close_float_layer(introduction_catalog, offset_y=30):
                self.logger.info("使用 close_float_layer 方法关闭聚合页成功")
            else:
                self.logger.error("使用 close_float_layer 方法关闭聚合页失败，尝试备用方案")
                assert self._close_player_menu(), "关闭播放器菜单失败"
                self.logger.info("使用备用方案关闭聚合页成功")
        else:
            # 如果没有找到标题元素，尝试关闭浮层
            float_layer = page_actions.find_element(VIDEO_PLAYER_PAGE["float_layer"], "css")
            if float_layer:
                self.logger.info("发现浮层，尝试点击关闭")
                assert page_actions.close_float_layer(float_layer), "关闭浮层失败"
                self.logger.info("关闭浮层成功")
            else:
                self.logger.warning("未找到标题元素和浮层，使用默认点击方式关闭")
                assert self._close_player_menu(), "关闭播放器菜单失败"
                self.logger.info("使用默认方式关闭聚合页成功")

        # 使用条件等待，最多等待2秒，等待聚合页/浮层关闭
        assert self._wait_for_condition(
            lambda: self.player_control.play_introduction_catalog_title() is None,
            timeout=2,
            error_msg="等待聚合页/浮层关闭超时"
        ), "等待聚合页/浮层关闭超时"
        self.logger.info("聚合页/浮层关闭成功")

        self.logger.info("简介功能测试完成")

    @pytest.mark.regression
    def test_catalog_page(self):
        """测试打开聚合页-目录功能"""
        self.logger.info("测试打开聚合页-目录功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"
        video_player.click()

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        # 打开聚合页-目录
        player_catalog = self.player_control.play_catalog()
        assert player_catalog is not None, "未找到目录按钮"
        player_catalog.click()
        self.logger.info("目录打开成功")

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="catalog_page_opened")

        # 使用条件等待，最多等待2秒，等待目录加载
        assert self._wait_for_condition(
            lambda: self.player_control.get_catalogtab_text() is not None,
            timeout=2,
            error_msg="等待目录加载超时"
        ), "等待目录加载超时"

        player_tabs = self.player_control.get_catalogtab_text()
        play_catalog = self.player_control.get_catalog_text()
        self.logger.info(f"目录标签: {player_tabs}")
        self.logger.info(f"目录内容: {play_catalog}")

        # 关闭目录
        assert self._close_player_menu(), "关闭目录失败"
        self.page.wait(5)
        self.logger.info("目录关闭成功")

    @pytest.mark.regression
    def test_mute_function(self):
        """测试静音和恢复静音功能"""
        self.logger.info("测试静音和恢复静音功能")

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        #暂停播放,保持播放器菜单显示
        video_player = self.player_control.play_pause()
        video_player.click()

        # 检查当前静音状态
        self.logger.info("检查当前静音状态")
        is_muted = False

        # 尝试查找静音图标，判断当前是否已静音
        mute_icon = self.player_control.mute_icon(is_mute=False)  # 未静音图标
        unmute_icon = self.player_control.mute_icon(is_mute=True)  # 已静音图标

        assert mute_icon is not None or unmute_icon is not None, "未找到任何静音图标"

        if mute_icon:
            self.logger.info("当前为未静音状态，将先执行静音操作")
            is_muted = False
        elif unmute_icon:
            self.logger.info("当前为已静音状态，将先执行取消静音操作")
            is_muted = True

        # 根据当前状态执行相应的操作
        if is_muted:
            # 当前已静音，先取消静音
            self.logger.info("执行取消静音操作")
            unmute_icon.click()
            self.logger.info("取消静音成功，等待5秒")
            # 使用条件等待，最多等待5秒，等待取消静音完成
            assert self._wait_for_condition(
                lambda: self.player_control.mute_icon(is_mute=False) is not None,
                timeout=5,
                error_msg="等待取消静音完成超时"
            ), "等待取消静音完成超时"

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            assert self._ensure_player_menu_open(), "播放器菜单打开失败"

            # 然后执行静音操作
            self.logger.info("执行静音操作")
            mute_icon = self.player_control.mute_icon(is_mute=False)
            assert mute_icon is not None, "未找到静音按钮"
            mute_icon.click()
            self.logger.info("静音成功")
        else:
            # 当前未静音，先执行静音操作
            self.logger.info("执行静音操作")
            mute_icon.click()
            self.logger.info("静音成功，等待5秒")
            # 使用条件等待，最多等待5秒，等待静音完成
            assert self._wait_for_condition(
                lambda: self.player_control.mute_icon(is_mute=True) is not None,
                timeout=5,
                error_msg="等待静音完成超时"
            ), "等待静音完成超时"

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            assert self._ensure_player_menu_open(), "播放器菜单打开失败"

            # 然后执行取消静音操作
            self.logger.info("执行取消静音操作")
            # 添加5秒固定等待时间，以便观察静音状态
            self.page.wait(5)
            unmute_icon = self.player_control.mute_icon(is_mute=True)
            assert unmute_icon is not None, "未找到恢复静音按钮"
            unmute_icon.click()
            self.logger.info("取消静音成功")
            # 添加3秒固定等待时间，以便观察取消静音后的状态
            self.page.wait(3)

            # 捕获截图
            screenshot_utils = get_screenshot_utils()
            screenshot_utils.take_screenshot(self.page, name="unmuted")

        self.logger.info("静音功能测试完成")

    @pytest.mark.regression
    def test_favorite_function(self):
        """测试收藏和取消收藏功能"""
        self.logger.info("测试收藏和取消收藏功能")

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        #暂停播放,保持播放器菜单显示
        video_player = self.player_control.play_pause()
        video_player.click()

        # 检查当前收藏状态
        self.logger.info("检查当前收藏状态")
        is_collected = False

        # 尝试查找收藏图标，判断当前是否已收藏
        favorite_icon = self.player_control.favorite_icon(is_collected=False)  # 未收藏图标
        unfavorite_icon = self.player_control.favorite_icon(is_collected=True)  # 已收藏图标

        assert favorite_icon is not None or unfavorite_icon is not None, "未找到任何收藏图标"

        if favorite_icon:
            self.logger.info("当前为未收藏状态，将先执行收藏操作")
            is_collected = False
        elif unfavorite_icon:
            self.logger.info("当前为已收藏状态，将先执行取消收藏操作")
            is_collected = True

        # 根据当前状态执行相应的操作
        if is_collected:
            # 当前已收藏，先取消收藏
            self.logger.info("执行取消收藏操作")
            unfavorite_icon.click()
            self.logger.info("取消收藏成功，等待3秒")
            # 使用条件等待，最多等待3秒，等待取消收藏完成
            assert self._wait_for_condition(
                lambda: self.player_control.favorite_icon(is_collected=False) is not None,
                timeout=3,
                error_msg="等待取消收藏完成超时"
            ), "等待取消收藏完成超时"

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            assert self._ensure_player_menu_open(), "播放器菜单打开失败"

            # 然后执行收藏操作
            self.logger.info("执行收藏操作")
            favorite_icon = self.player_control.favorite_icon(is_collected=False)
            assert favorite_icon is not None, "未找到收藏按钮"
            favorite_icon.click()
            self.logger.info("收藏成功")
            # 添加5秒固定等待时间，以便观察收藏后的状态
            self.page.wait(5)
        else:
            # 当前未收藏，先执行收藏操作
            self.logger.info("执行收藏操作")
            favorite_icon.click()
            self.logger.info("收藏成功，等待3秒")
            # 使用条件等待，最多等待3秒，等待收藏完成
            assert self._wait_for_condition(
                lambda: self.player_control.favorite_icon(is_collected=True) is not None,
                timeout=3,
                error_msg="等待收藏完成超时"
            ), "等待收藏完成超时"

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            assert self._ensure_player_menu_open(), "播放器菜单打开失败"

            # 然后执行取消收藏操作
            self.logger.info("执行取消收藏操作")
            unfavorite_icon = self.player_control.favorite_icon(is_collected=True)
            assert unfavorite_icon is not None, "未找到取消收藏按钮"
            unfavorite_icon.click()
            self.logger.info("取消收藏成功")
            # 添加3秒固定等待时间，以便观察取消收藏后的状态
            self.page.wait(3)

            # 捕获截图
            screenshot_utils = get_screenshot_utils()
            screenshot_utils.take_screenshot(self.page, name="unfavorited")

        # 使用条件等待，最多等待3秒，等待取消收藏完成
        assert self._wait_for_condition(
            lambda: self.player_control.favorite_icon(is_collected=False) is not None,
            timeout=3,
            error_msg="等待取消收藏完成超时"
        ), "等待取消收藏完成超时"

        self.logger.info("收藏功能测试完成")

    @pytest.mark.regression
    def test_quality_and_speed(self):
        """测试视频质量和播放速度切换功能"""
        self.logger.info("测试视频质量和播放速度切换功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        assert video_player is not None, "未找到播放器元素"
        video_player.click()

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        # 打开播分辨率、倍速菜单
        menu = self.player_control.play_menu()
        assert menu is not None, "未找到菜单按钮"
        menu.click()
        self.logger.info("打开菜单")
        # 使用条件等待，最多等待1秒，等待质量菜单加载
        assert self._wait_for_condition(
            lambda: len(self.player_control.get_play_quality_text()) > 0,
            timeout=1,
            error_msg="等待质量菜单加载超时"
        ), "等待质量菜单加载超时"

        # 获取质量列表-->关闭菜单
        quality_list = self.player_control.get_play_quality_text()
        speed_list = self.player_control.get_play_speed_text()

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="quality_speed_menu_opened")
        video_player.click()

        for quality in quality_list:
            # 定位播放器--->唤起播放器菜单
            video_player = self.player_control.play_pause()
            assert video_player is not None, "未找到播放器元素"
            video_player.click()
            # 使用条件等待，最多等待1秒，等待菜单打开
            assert self._wait_for_condition(
                lambda: self.player_control.is_player_menu_open(),
                timeout=1,
                error_msg="等待播放器菜单打开超时"
            ), "等待播放器菜单打开超时"

            # 确保菜单已打开
            assert self._ensure_player_menu_open(), "播放器菜单打开失败"

            # 打开质量菜单
            menu = self.player_control.play_menu()
            assert menu is not None, "未找到菜单按钮"
            menu.click()
            # 使用条件等待，最多等待1秒，等待质量选项加载
            assert self._wait_for_condition(
                lambda: self.player_control.play_menu_quality(quality=quality) is not None,
                timeout=1,
                error_msg="等待质量选项加载超时"
            ), "等待质量选项加载超时"

            # 切换视频质量
            switch_quality = self.player_control.play_menu_quality(quality=quality)
            assert switch_quality is not None, f"未找到{quality}质量选项"
            switch_quality.click()
            self.logger.info(f"切换{quality}成功")
            # 添加3秒固定等待时间，以便观察切换质量后的状态
            self.page.wait(3)
            self.logger.info(f"切换{quality}成功等待20秒")
            # 等待视频播放一段时间（20秒）
            self.page.wait(20)

        for speed in speed_list:
            # 定位播放器--->唤起播放器菜单
            video_player = self.player_control.play_pause()
            assert video_player is not None, "未找到播放器元素"
            video_player.click()
            # 使用条件等待，最多等待1秒，等待菜单打开
            assert self._wait_for_condition(
                lambda: self.player_control.is_player_menu_open(),
                timeout=1,
                error_msg="等待播放器菜单打开超时"
            ), "等待播放器菜单打开超时"

            # 确保菜单已打开
            assert self._ensure_player_menu_open(), "播放器菜单打开失败"

            # 打开质量菜单
            menu = self.player_control.play_menu()
            assert menu is not None, "未找到菜单按钮"
            menu.click()
            # 使用条件等待，最多等待1秒
            assert self._wait_for_condition(
                lambda: self.player_control.play_menu_speed(speed=speed) is not None,
                timeout=1,
                error_msg="等待速度选项加载超时"
            ), "等待速度选项加载超时"

            # 切换播放速度
            switch_speed = self.player_control.play_menu_speed(speed=speed)
            assert switch_speed is not None, f"未找到{speed}速度选项"
            switch_speed.click()
            self.logger.info(f"切换{speed}成功")
            # 添加3秒固定等待时间，以便观察切换速度后的状态
            self.page.wait(3)
            self.logger.info(f"切换{speed}成功等待20秒")
            # 等待视频播放一段时间（20秒）
            self.page.wait(20)

    @pytest.mark.regression
    def test_exit_player(self):
        """测试退出播放器功能"""
        self.logger.info("测试退出播放器功能")

        # 确保菜单已打开
        assert self._ensure_player_menu_open(), "播放器菜单打开失败"

        # 捕获截图
        screenshot_utils = get_screenshot_utils()
        screenshot_utils.take_screenshot(self.page, name="player_menu_opened")

        # 执行退出操作
        self.logger.info("执行退出播放器")
        player_back_icon = self.player_control.play_back()
        assert player_back_icon is not None, "未找到返回按钮"
        player_back_icon.click()
        # 使用条件等待，最多等待2秒，等待播放器退出
        assert self._wait_for_condition(
            lambda: self.player_control.play_back() is None,
            timeout=2,
            error_msg="等待播放器退出超时"
        ), "等待播放器退出超时"
        self.logger.info("退出播放器成功")
