import time
from components.PlayerIconComponent import IconComponent
from utils.logger_utils import LoggerUtils


class PlayerTest:
    """播放器测试类"""

    def __init__(self, page):
        """
        初始化播放器测试类
        :param page: 页面对象
        """
        self.page = page
        self.logger = LoggerUtils.get_default_logger()
        # 播放十秒后播放器实例化
        self.page.wait(10)
        self.player_control = IconComponent(page)
        self.logger.info("初始化播放器测试类")

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

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 打开聚合页-简介
        if self.player_control.is_player_menu_open():
            player_introduction = self.player_control.play_introduction()
            player_introduction.click()
            self.logger.info("播放器聚合页打开成功")

            float_layer = self.page.ele('css:.flex.justify-start.absolute.flex-col.items-stretch.box-border')
            if float_layer:
                float_layer.click()
            else:
                self.logger.warning("没有找到浮层")

        self.page.wait(30)

        # 定位播放器-关闭聚合页
        introduction_catalog = self.player_control.play_introduction_catalog_title()
        self.page.wait(2)
        video_player.click()

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

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 静音---恢复静音
        if self.player_control.is_player_menu_open():
            # 静音操作
            mute_icon = self.player_control.mute_icon(is_mute=False)
            mute_icon.click()
            self.logger.info("静音成功")
            self.page.wait(10)
            mute_icon = self.player_control.mute_icon(is_mute=True)
            mute_icon.click()
            self.logger.info("取消静音")

    def test_favorite_function(self):
        """测试收藏和取消收藏功能"""
        self.logger.info("测试收藏和取消收藏功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 收藏-取消收藏
        if self.player_control.is_player_menu_open():
            # 收藏夹
            favorite_icon = self.player_control.favorite_icon(is_collected=False)
            self.page.wait(1)
            favorite_icon.click()
            self.logger.info("收藏成功")
            self.page.wait(3)
            favorite_icon = self.player_control.favorite_icon(is_collected=True)
            self.page.wait(1)
            favorite_icon.click()
            self.logger.info("取消收藏")
            self.page.wait(1)

    def test_quality_and_speed(self):
        """测试视频质量和播放速度切换功能"""
        self.logger.info("测试视频质量和播放速度切换功能")

        # 定位播放器（调用正确的 play_pause 方法）
        video_player = self.player_control.play_pause()
        video_player.click()

        # 打开播分辨率、倍速菜单
        if self.player_control.is_player_menu_open():
            menu = self.player_control.play_menu()
            menu.click()
            self.logger.info("打开菜单")
            self.page.wait(5)
        else:
            video_player.click()
            self.page.wait(1)
            menu = self.player_control.play_menu()
            menu.click()
            self.logger.info("打开菜单")

        # 获取质量列表-->关闭菜单
        quality_list = self.player_control.get_play_quality_text()
        speed_list = self.player_control.get_play_speed_text()
        video_player.click()

        for quality in quality_list:
            # 定位播放器--->唤起播放器菜单
            video_player = self.player_control.play_pause()
            video_player.click()
            self.page.wait(1)

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

        # 退出播放器
        player_back_icon = self.player_control.play_back()
        player_back_icon.click()
        self.logger.info("执行退出播放器成功")

    def run_all_tests(self):
        """运行所有测试方法"""
        self.logger.info("开始运行所有播放器测试")

        self.test_pause_play()
        self.test_home_page()
        self.test_introduction_page()
        self.test_catalog_page()
        self.test_pause_play()  # 再次测试暂停和播放
        self.test_mute_function()
        self.test_favorite_function()
        self.test_quality_and_speed()
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
    # 此处需要传入页面对象，实际使用时由调用方提供
    pass