# 页面元素定位配置文件

# 短剧首页元素定位器
DRAMA_HOME_PAGE = {
    "back_button": "div.gap-sm > svg",
    "home_button": "svg.filter-drop-shadow-\\[0_0_1px_\\#000c\\] > path",
    "profile_button": "div.gap-sm path:nth-of-type(2)",
    "watch_button": "div.button-primary",
    "add_to_list_button": "div.button",
    "remove_from_list_button": "div.button",
    "description": "span",
    "description_toggle_button": "span.float-right.text-primary.clear-both",
    "episodes_tab": ".color-placeholder.mb-xl.text-lg",
    "episodes_list": ".gap-md.grid.grid-cols-6",
    "locked_episodes_list": ".gap-md.grid.grid-cols-6 > div >svg > path[d^=m307]",
    "unlocked_episodes_list": ".gap-md.grid.grid-cols-6 > div >svg > path[d^=M870]",
    "free_episodes": ".gap-md.grid.grid-cols-6 > div:not(:has(svg)) > div"
}

# 视频播放页面元素定位器
VIDEO_PLAYER_PAGE = {
    # 播放器控制元素
    "player_menu": ".flex-1.text-xxl svg.icon-svg.icon[fill]",
    "player_pause_button": "svg.icon-svg.text-xxl",
    "player_back_button": ".flex.items-center.justify-start.gap-sm >.icon-svg",
    "player_title": ".line-clamp-1.flex-1.text-xxl",
    "player_introduction": ".flex.text-md .flex-1",
    "player_catalog": ".px-xl.flex.justify-between.items-center.line-height-3em.gap-sm.rounded-md.text-lg",
    "player_introduction_catalog_title": ".line-clamp-1.flex-1.text-xl",

    # 播放器质量和速度元素
    "menu_speed_container": ".bg-bgpage:not(.mt-xl) .text-md > div",
    "menu_quality_container": ".mt-xl .text-md > div",

    # 收藏按钮
    "favorite_collected": ".flex-1.text-xxl svg.icon-svg.color-primary:not(.icon)[fill]",
    "favorite_uncollected": ".flex-1.text-xxl svg.icon-svg:not(.icon)[fill]",

    # 静音按钮
    "mute_active": ".flex-1.text-xxl .icon-svg.color-danger",
    "mute_inactive": ".flex-1.text-xxl .icon-svg.text-xxl",

    # 播放器容器和视频元素
    "active_slide": ".swiper-slide-active",
    "player_container": ".prism-player",
    "video_element": "tag:video",

    # 目录相关
    "catalog_tab": ".color-placeholder.mb-xl.text-lg",
    "catalog_grid": ".gap-md.grid.grid-cols-6",

    # 播放器聚合页元素
    "float_layer": ".flex.justify-start.absolute.flex-col.items-stretch.box-border"
}

# 个人中心页面元素定位器
PROFILE_PAGE = {
    "back_button": "div.h-50 > svg",
    "user_avatar": "svg.text-112",
    "top_up_button": "div.button-primary:contains('Top UP')",
    "transaction_history_link": "div.p-xl:contains('Transaction History')",
    "my_list_and_history_link": "div.p-xl:contains('My List & History')",
    "contact_us_link": "div.p-xl:contains('Contact Us')",
    "settings_link": "div.p-xl:contains('Setting')"
}

# 可以继续添加其他页面的定位器...
