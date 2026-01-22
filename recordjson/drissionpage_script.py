from DrissionPage import ChromiumPage
page = ChromiumPage()


page.get("https://reelswave.net/content/286563649187311616?chapterIndex=1")

page.ele("css:div.gap-sm > svg").click()

page.get("https://reelswave.net/player/286563649187311616?chapterId=286564749932007424&from=home-module_1x3&chapterIndex=1&free=1&pay=0")

page.wait(2)
page.quit()
