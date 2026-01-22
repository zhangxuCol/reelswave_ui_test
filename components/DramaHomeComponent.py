import time

from DrissionPage import ChromiumPage
from utils.page_actions import PageActions
from config.locators import DRAMA_HOME_PAGE
from utils.logger_utils import LoggerUtils


class DramaHomeComponent:
    """短剧首页组件类，包含短剧首页的各种操作方法"""

    def __init__(self, page: ChromiumPage):
        """
        初始化短剧首页组件对象
        :param page: ChromiumPage对象
        """
        self.page = page  # 保存传入的页面对象
        self.actions = PageActions(page)  # 初始化基础操作类
        self.logger = LoggerUtils.get_default_logger()  # 获取日志记录器

    def click_back_button(self):
        """点击剧首页-返回按钮"""
        return self.actions.click_element(DRAMA_HOME_PAGE["back_button"], selector_type="css")

    def click_home_button(self):
        """点击剧首页-home按钮"""
        return self.actions.click_element(DRAMA_HOME_PAGE["home_button"], selector_type="css")

    def click_profile_button(self):
        """点击剧首页-个人中心按钮"""
        return self.actions.click_element(DRAMA_HOME_PAGE["profile_button"], selector_type="css")

    def click_watch_button(self):
        """点击剧首页-去看剧按钮"""
        return self.actions.click_element(DRAMA_HOME_PAGE["watch_button"], selector_type="css")

    def click_add_to_list(self):
        """点击剧首页-添加收藏按钮（页面文案：Add to List）"""
        return self.actions.click_element(DRAMA_HOME_PAGE["add_to_list_button"], selector_type="css")

    def click_remove_from_list(self):
        """点击剧首页-取消收藏按钮（页面文案：In my List）"""
        return self.actions.click_element(DRAMA_HOME_PAGE["remove_from_list_button"], selector_type="css")

    def click_free_episode(self):
        """点击剧首页-任意一个免费剧集"""
        try:
            # 查找所有免费剧集
            free_episodes = self.actions.find_elements(DRAMA_HOME_PAGE["free_episodes"], selector_type="css")
            if not free_episodes:
                self.logger.error("未找到任何免费剧集！")
                return False

            # 点击第一个免费剧集
            for free_episode in range(0, len(free_episodes)):
                print(free_episode, len(free_episodes))
                free_episodes[free_episode].click()
                self.logger.info("成功点击免费剧集")
                return True
        except Exception as e:
            self.logger.error(f"点击免费剧集失败: {e}")
            return False

    def toggle_description(self):
        """展开或收起短剧简介"""
        try:
            # 查找简介元素
            description = self.actions.find_element(DRAMA_HOME_PAGE["description"], selector_type="css")
            if not description:
                self.logger.error("未找到短剧简介元素")
                return False

            # 点击简介元素
            description.click()
            self.logger.info("成功点击短剧简介，切换展开/收起状态")
            return True
        except Exception as e:
            self.logger.error(f"切换短剧简介状态失败: {e}")
            return False

    def is_description_expanded(self):
        """检查短剧简介是否处于展开状态"""
        try:
            # Fold 是已经展开了，More 是已经收起了
            button_text = self.actions.get_element_text(DRAMA_HOME_PAGE["description"], selector_type="css")
            if not button_text:
                self.logger.error("未找到简介展开/收起按钮或无法获取按钮文本")
                return False
                
            # 如果按钮文本是"Fold"，表示简介已展开
            # 如果按钮文本是"More"，表示简介已收起
            return button_text
        except Exception as e:
            self.logger.error(f"检查短剧简介状态失败: {e}")
            return False

    def navigate_to_drama_home(self):
        """从其它页面回到剧首页"""
        try:
            # 尝试多种方式回到剧首页

            # 方法1：点击返回按钮
            if self.actions.is_element_exists(DRAMA_HOME_PAGE["back_button"], selector_type="css", timeout=3):
                self.click_back_button()
                if self.is_drama_home_page():
                    self.logger.info("通过返回按钮成功回到剧首页")
                    return True

            # 方法2：点击Home按钮
            if self.actions.is_element_exists(DRAMA_HOME_PAGE["home_button"], selector_type="css", timeout=3):
                self.click_home_button()
                if self.is_drama_home_page():
                    self.logger.info("通过Home按钮成功回到剧首页")
                    return True

            # 方法3：直接访问剧首页URL
            drama_home_url = "https://video.reelswave.net"
            self.page.get(drama_home_url)
            if self.is_drama_home_page():
                self.logger.info("通过直接访问URL成功回到剧首页")
                return True

            self.logger.error("无法回到剧首页")
            return False
        except Exception as e:
            self.logger.error(f"回到剧首页失败: {e}")
            return False

    def is_drama_home_page(self):
        """检查当前是否在剧首页"""
        try:
            # 获取当前 URL
            current_url = self.page.url
            self.logger.debug(f"当前 URL: {current_url}")
            
            # 检查 URL 格式是否符合剧首页模式
            # 格式: https://video.reelswave.net/content/数字字符串?chapterIndex=1
            import re
            pattern = r"https://video\.reelswave\.net/content/\d+\?chapterIndex=1"
            
            if re.match(pattern, current_url):
                self.logger.debug("URL 匹配剧首页模式")
                return True
            else:
                self.logger.debug("URL 不匹配剧首页模式")
                return False

        except Exception as e:
            self.logger.error(f"检查是否在剧首页时出错: {e}")
            return False

    def wait_for_elements_loaded(self):
        """等待剧首页关键元素加载完成"""
        try:
            # 等待页面加载完成 - DrissionPage 使用 wait 方法
            self.page.wait(2)  # 等待2秒让页面加载

            # 检查并等待关键元素加载
            key_elements = [
                DRAMA_HOME_PAGE["back_button"],
                DRAMA_HOME_PAGE["home_button"],
                DRAMA_HOME_PAGE["profile_button"],
                DRAMA_HOME_PAGE["watch_button"]
            ]

            all_loaded = True
            for element_selector in key_elements:
                if not self.actions.is_element_exists(element_selector, selector_type="css", timeout=5):
                    self.logger.warning(f"关键元素未加载: {element_selector}")
                    all_loaded = False
                else:
                    self.logger.debug(f"关键元素已加载: {element_selector}")

            if all_loaded:
                self.logger.info("所有关键元素加载完成")
                self.page.wait(1)  # 使用 DrissionPage 的 wait 方法
            else:
                self.logger.warning("部分关键元素未加载，但继续执行")

            return True
        except Exception as e:
            self.logger.error(f"等待元素加载时出错: {str(e)}")
            return False
