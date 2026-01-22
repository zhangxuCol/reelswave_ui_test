import time
from components.PlayerIconComponent import IconComponent
from utils.logger_utils import LoggerUtils
from page.base import get_current_url,navigate_to_url
from config.locators import VIDEO_PLAYER_PAGE


class PlayerTest:
    """播放器测试类"""

    def __init__(self, page=None):
        """
        初始化测试类
        :param page: 可选，传入已打开的页面对象
        """
        # 创建日志记录器实例
        self.logger = LoggerUtils.get_default_logger()
        # 初始化页面对象，如果未传入则创建新页面
        self.page = self._init_page(page)
        # 创建播放器组件实例
        self.player_control = IconComponent(self.page)
        # 记录初始化完成的日志信息
        self.logger.info("初始化播放器测试类")
        self.currenturl = get_current_url(self.page)

    def _init_page(self, page=None):
        """
        基础方法：如果没有传入页面对象，则打开新页面
        :param page: 可选，传入已打开的页面对象
        :return: 页面对象
        """
        # 如果没有传入页面对象，则打开新页面
        if page is None:
            page = open_mobile_browser()

        # 等待页面加载完成
        page.wait(10)  # 播放十秒后播放器实例化
        self.logger.info("页面加载完成")

        return page

    def test_pause_play(self):
        """测试暂停和播放功能"""
        self.logger.info("测试暂停和播放功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        # 唤起播放器菜单-->暂停播放
        video_player.click()
        self.logger.info("执行唤起播放器菜单操作成功")

        if self.player_control.is_player_menu_open():
            video_player.click()
            self.logger.info("执行暂停操作成功")
            self.page.wait(2)
        else:
            video_player.click()
            self.page.wait(1)
            video_player.click()
            self.logger.info("执行暂停操作成功")
            self.page.wait(5)

        # 继续播放
        video_player.click()
        self.logger.info("继续播放操作成功")
        self.page.wait(10)

        # 暂停播放
        if self.player_control.is_player_menu_open():
            video_player.click()
            self.logger.info("执行暂停操作成功")
            self.page.wait(5)
        else:
            video_player.click()
            self.page.wait(1)
            video_player.click()
            self.logger.info("执行暂停操作成功")
            self.page.wait(5)

    def test_home_page(self):
        """测试打开首页功能"""
        self.logger.info("测试打开首页功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 打开首页
        if self.player_control.is_player_menu_open():
            play_title = self.player_control.play_title()
            play_title.click()
            self.logger.info("打开首页成功")
            self.page.wait(5)
            # 返回
            player_home_back = self.player_control.play_back()
            player_home_back.click()
            self.logger.info("退出首页成功")
        else:
            self.logger.error("首页打开失败")

    def test_introduction_page(self):
        """测试打开聚合页-简介功能"""
        self.logger.info("测试打开聚合页-简介功能")

        # 确保菜单已打开
        if not self.player_control.is_player_menu_open():
            self.logger.info("播放器菜单未打开，先打开菜单")
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            if not self.player_control.is_player_menu_open():
                self.logger.error("无法打开播放器菜单，简介功能测试失败")
                raise Exception("无法打开播放器菜单")

        # 打开聚合页-简介
        self.logger.info("尝试打开聚合页-简介")
        player_introduction = self.player_control.play_introduction()
        if not player_introduction:
            self.logger.error("未找到简介按钮，简介功能测试失败")
            raise Exception("未找到简介按钮")

        player_introduction.click()
        self.logger.info("播放器聚合页打开成功")
        self.page.wait(2)

        # 处理可能出现的浮层
        self.logger.info("检查并处理可能的浮层")
        float_layer = self.page.ele(f'css:{VIDEO_PLAYER_PAGE["float_layer"]}')
        if float_layer:
            self.logger.info("发现浮层，尝试点击关闭")
            from utils.page_actions import PageActions
            page_actions = PageActions(self.page)
            page_actions.close_float_layer(float_layer)
            self.page.wait(1)
        else:
            self.logger.info("未发现浮层，继续测试")

        # 等待页面加载完成
        self.logger.info("等待页面加载完成")
        self.page.wait(30)

        # 确保菜单已打开（等待期间菜单可能已关闭）
        if not self.player_control.is_player_menu_open():
            self.logger.info("播放器菜单已关闭，重新打开菜单")
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            if not self.player_control.is_player_menu_open():
                self.logger.error("无法重新打开播放器菜单，关闭聚合页测试失败")
                raise Exception("无法重新打开播放器菜单")

        # 定位标题并关闭聚合页
        self.logger.info("定位标题并关闭聚合页")
        introduction_catalog = self.player_control.play_introduction_catalog_title()
        self.page.wait(2)

        if not introduction_catalog:
            self.logger.warning("未找到标题元素，使用默认点击方式关闭")
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(2)
            self.logger.info("使用默认方式关闭聚合页成功")
            return

        # 使用 PageActions 的方法关闭聚合页
        from utils.page_actions import PageActions
        page_actions = PageActions(self.page)

        # 尝试使用 close_float_layer 方法关闭聚合页，向上偏移30像素
        if not page_actions.close_float_layer(introduction_catalog, offset_y=30):
            self.logger.error("使用 close_float_layer 方法关闭聚合页失败，尝试备用方案")
            try:
                video_player = self.player_control.play_pause()
                video_player.click()
                self.page.wait(2)
                self.logger.info("使用备用方案关闭聚合页成功")
            except Exception as inner_e:
                self.logger.error(f"备用方案也失败: {str(inner_e)}")
                # 尝试直接点击页面空白处
                page_actions.click_at_position(100, 100)
                self.page.wait(2)
                self.logger.info("使用点击页面空白处方式关闭聚合页")
        else:
            self.page.wait(2)
            self.logger.info("聚合页关闭成功")

        self.logger.info("简介功能测试完成")

    def test_catalog_page(self):
        """测试打开聚合页-目录功能"""
        self.logger.info("测试打开聚合页-目录功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 打开聚合页-目录
        if self.player_control.is_player_menu_open():
            player_catalog = self.player_control.play_catalog()
            player_catalog.click()
            self.logger.info("目录打开成功")
        else:
            video_player.click()
            player_catalog = self.player_control.play_catalog()
            player_catalog.click()
            self.logger.info("目录打开成功")

        player_tabs = self.player_control.get_catalogtab_text()
        play_catalog = self.player_control.get_catalog_text()
        self.logger.info(f"目录标签: {player_tabs}")
        self.logger.info(f"目录内容: {play_catalog}")

    def test_mute_function(self):
        """测试静音和恢复静音功能"""
        self.logger.info("测试静音和恢复静音功能")

        # 确保菜单已打开
        if not self.player_control.is_player_menu_open():
            self.logger.info("打开播放器菜单")
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            if not self.player_control.is_player_menu_open():
                self.logger.error("无法打开播放器菜单，静音测试失败")
                raise Exception("无法打开播放器菜单")

        # 检查当前静音状态
        self.logger.info("检查当前静音状态")
        is_muted = False

        # 尝试查找静音图标，判断当前是否已静音
        mute_icon = self.player_control.mute_icon(is_mute=False)  # 未静音图标
        unmute_icon = self.player_control.mute_icon(is_mute=True)  # 已静音图标

        if mute_icon:
            self.logger.info("当前为未静音状态，将先执行静音操作")
            is_muted = False
        elif unmute_icon:
            self.logger.info("当前为已静音状态，将先执行取消静音操作")
            is_muted = True
        else:
            self.logger.error("未找到任何静音图标，静音测试失败")
            raise Exception("未找到静音图标")

        # 根据当前状态执行相应的操作
        if is_muted:
            # 当前已静音，先取消静音
            self.logger.info("执行取消静音操作")
            unmute_icon.click()
            self.logger.info("取消静音成功，等待5秒")
            self.page.wait(5)

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            if not self.player_control.is_player_menu_open():
                self.logger.info("重新打开播放器菜单")
                video_player = self.player_control.play_pause()
                video_player.click()
                self.page.wait(1)

                if not self.player_control.is_player_menu_open():
                    self.logger.error("无法重新打开播放器菜单，静音测试失败")
                    raise Exception("无法重新打开播放器菜单")

            # 然后执行静音操作
            self.logger.info("执行静音操作")
            mute_icon = self.player_control.mute_icon(is_mute=False)
            if not mute_icon:
                self.logger.error("未找到静音按钮，静音操作失败")
                raise Exception("未找到静音按钮")

            mute_icon.click()
            self.logger.info("静音成功")
        else:
            # 当前未静音，先执行静音操作
            self.logger.info("执行静音操作")
            mute_icon.click()
            self.logger.info("静音成功，等待5秒")
            self.page.wait(5)

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            if not self.player_control.is_player_menu_open():
                self.logger.info("重新打开播放器菜单")
                video_player = self.player_control.play_pause()
                video_player.click()
                self.page.wait(1)

                if not self.player_control.is_player_menu_open():
                    self.logger.error("无法重新打开播放器菜单，恢复静音测试失败")
                    raise Exception("无法重新打开播放器菜单")

            # 然后执行取消静音操作
            self.logger.info("执行取消静音操作")
            unmute_icon = self.player_control.mute_icon(is_mute=True)
            if not unmute_icon:
                self.logger.error("未找到恢复静音按钮，恢复静音操作失败")
                raise Exception("未找到恢复静音按钮")

            unmute_icon.click()
            self.logger.info("取消静音成功")

        self.logger.info("静音功能测试完成")

    def test_favorite_function(self):
        """测试收藏和取消收藏功能"""
        self.logger.info("测试收藏和取消收藏功能")

        # 确保菜单已打开
        if not self.player_control.is_player_menu_open():
            self.logger.info("打开播放器菜单")
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            if not self.player_control.is_player_menu_open():
                self.logger.error("无法打开播放器菜单，收藏测试失败")
                raise Exception("无法打开播放器菜单")

        # 检查当前收藏状态
        self.logger.info("检查当前收藏状态")
        is_collected = False

        # 尝试查找收藏图标，判断当前是否已收藏
        favorite_icon = self.player_control.favorite_icon(is_collected=False)  # 未收藏图标
        unfavorite_icon = self.player_control.favorite_icon(is_collected=True)  # 已收藏图标

        if favorite_icon:
            self.logger.info("当前为未收藏状态，将先执行收藏操作")
            is_collected = False
        elif unfavorite_icon:
            self.logger.info("当前为已收藏状态，将先执行取消收藏操作")
            is_collected = True
        else:
            self.logger.error("未找到任何收藏图标，收藏测试失败")
            raise Exception("未找到收藏图标")

        # 根据当前状态执行相应的操作
        if is_collected:
            # 当前已收藏，先取消收藏
            self.logger.info("执行取消收藏操作")
            unfavorite_icon.click()
            self.logger.info("取消收藏成功，等待3秒")
            self.page.wait(3)

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            if not self.player_control.is_player_menu_open():
                self.logger.info("重新打开播放器菜单")
                video_player = self.player_control.play_pause()
                video_player.click()
                self.page.wait(1)

                if not self.player_control.is_player_menu_open():
                    self.logger.error("无法重新打开播放器菜单，收藏测试失败")
                    raise Exception("无法重新打开播放器菜单")

            # 然后执行收藏操作
            self.logger.info("执行收藏操作")
            favorite_icon = self.player_control.favorite_icon(is_collected=False)
            if not favorite_icon:
                self.logger.error("未找到收藏按钮，收藏操作失败")
                raise Exception("未找到收藏按钮")

            favorite_icon.click()
            self.logger.info("收藏成功")
        else:
            # 当前未收藏，先执行收藏操作
            self.logger.info("执行收藏操作")
            favorite_icon.click()
            self.logger.info("收藏成功，等待3秒")
            self.page.wait(3)

            # 再次确保菜单已打开（等待期间菜单可能已关闭）
            if not self.player_control.is_player_menu_open():
                self.logger.info("重新打开播放器菜单")
                video_player = self.player_control.play_pause()
                video_player.click()
                self.page.wait(1)

                if not self.player_control.is_player_menu_open():
                    self.logger.error("无法重新打开播放器菜单，取消收藏测试失败")
                    raise Exception("无法重新打开播放器菜单")

            # 然后执行取消收藏操作
            self.logger.info("执行取消收藏操作")
            unfavorite_icon = self.player_control.favorite_icon(is_collected=True)
            if not unfavorite_icon:
                self.logger.error("未找到取消收藏按钮，取消收藏操作失败")
                raise Exception("未找到取消收藏按钮")

            unfavorite_icon.click()
            self.logger.info("取消收藏成功")
        self.page.wait(3)

        self.logger.info("收藏功能测试完成")

    def test_quality_and_speed(self):
        """测试视频质量和播放速度切换功能"""
        self.logger.info("测试视频质量和播放速度切换功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 打开播分辨率、倍速菜单
        if not self.player_control.is_player_menu_open():
            self.logger.info("播放器菜单未打开，先打开菜单")
            video_player.click()
            self.page.wait(1)

            if not self.player_control.is_player_menu_open():
                self.logger.error("无法打开播放器菜单，测试失败")
                raise Exception("无法打开播放器菜单")

        menu = self.player_control.play_menu()
        menu.click()
        self.logger.info("打开菜单")
        self.page.wait(1)

        # 获取质量列表-->关闭菜单
        quality_list = self.player_control.get_play_quality_text()
        speed_list = self.player_control.get_play_speed_text()
        video_player.click()

        for quality in quality_list:
            # 定位播放器--->唤起播放器菜单
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            # 确保菜单已打开
            if not self.player_control.is_player_menu_open():
                self.logger.info("播放器菜单未打开，先打开菜单")
                video_player.click()
                self.page.wait(1)

                if not self.player_control.is_player_menu_open():
                    self.logger.error("无法打开播放器菜单，质量切换测试失败")
                    raise Exception("无法打开播放器菜单")

            # 打开质量菜单
            menu = self.player_control.play_menu()
            menu.click()
            self.page.wait(1)

            # 切换视频质量
            switch_quality = self.player_control.play_menu_quality(quality=quality)
            switch_quality.click()
            self.logger.info(f"切换{quality}成功等待20秒")
            self.page.wait(20)

        for speed in speed_list:
            # 定位播放器--->唤起播放器菜单
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            # 确保菜单已打开
            if not self.player_control.is_player_menu_open():
                self.logger.info("播放器菜单未打开，先打开菜单")
                video_player.click()
                self.page.wait(1)

                if not self.player_control.is_player_menu_open():
                    self.logger.error("无法打开播放器菜单，速度切换测试失败")
                    raise Exception("无法打开播放器菜单")

            # 打开质量菜单
            menu = self.player_control.play_menu()
            menu.click()
            self.page.wait(1)

            # 切换播放速度
            switch_speed = self.player_control.play_menu_speed(speed=speed)
            switch_speed.click()
            self.logger.info(f"切换{speed}成功等待20秒")
            self.page.wait(20)

    def test_exit_player(self):
        """测试退出播放器功能"""
        self.logger.info("测试退出播放器功能")

        # 如果菜单未打开，先打开菜单
        if not self.player_control.is_player_menu_open():
            self.logger.info("播放器菜单未打开，先打开菜单")
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

            # 验证菜单是否已成功打开
            if not self.player_control.is_player_menu_open():
                self.logger.error("无法打开播放器菜单，退出操作失败")
                raise Exception("无法打开播放器菜单")

        # 执行退出操作
        self.logger.info("执行退出播放器")
        player_back_icon = self.player_control.play_back()
        player_back_icon.click()
        self.logger.info("执行退出播放器成功")

    def run_all_tests(self):
        """运行所有测试方法"""
        self.logger.info("开始运行所有播放器测试")

        # self.test_pause_play()
        # self.test_mute_function()
        # self.test_favorite_function()
        # self.test_quality_and_speed()
        self.test_introduction_page()
        # self.test_home_page()

        # self.test_catalog_page()
        # self.test_pause_play()  # 再次测试暂停和播放

        self.test_exit_player()

        self.logger.info("播放器所有测试完成")

def player_verify(page):
    """
    播放器内部操作（兼容旧接口）
    :param page: 页面对象
    :return: 页面对象
    """
    player_test = PlayerTest(page)
    player_test.run_all_tests()
    return page


if __name__ == "__main__":
    # 这里可以添加测试代码，例如：
    from page.base import open_mobile_browser
    page = open_mobile_browser()
    player_verify(page)
