from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def get_driver() -> webdriver.Edge:
    options = webdriver.EdgeOptions()
    options.binary_location = (
        r"C:\\Program Files (x86)\\Microsoft\\Edge\Application\\msedge.exe"
    )
    options.add_argument("--headless")

    service = Service(executable_path=r"msedgedriver.exe")
    driver = webdriver.Edge(
        options=options, service=service, keep_alive=True
    )  # 取用網頁驅動器
    return driver


def keyword_crawler(keyword: str, quantity_limit: int) -> list[tuple[str, str]]:
    video_list: list[tuple[str, str]] = []

    driver = get_driver()  # 取得網頁驅動
    driver.get(
        f"https://search.bilibili.com/video?keyword={keyword}&order=pubdate"
    )  # 前往B站搜尋頁面

    for _ in range(10):  # 限制迴圈最大只能跑10遍
        driver.refresh()  # 重新整理畫面跳過防爬蟲
        title_objects: list[WebElement] = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "bili-video-card__info--tit")
            ),
            "找不到指定的元素",
        )  # 明確等待所有標題
        titles = [
            obj.text for obj in title_objects if obj.is_displayed()
        ]  # 僅保留有顯示物件並取出文字

        url_objects = driver.find_elements(By.CLASS_NAME, "bili-video-card")
        urls = [
            obj.find_element(By.TAG_NAME, "a").get_attribute("href")
            for obj in url_objects
            if obj.is_displayed()
        ]  # 僅保留有顯示物件並取出連結

        for video_info in zip(titles, urls):  # 跑過每個標題和連結
            video_list.append(video_info)
            if len(video_list) >= quantity_limit:  # 影片數量到達上限
                driver.close()  # 關閉瀏覽器視窗
                return video_list  # 回傳
        # 未達上限則繼續執行

        try:
            page_buttons = driver.find_element(
                By.CLASS_NAME, "vui_pagenation--btns"
            ).find_elements(By.TAG_NAME, "button")[-1]
            if page_buttons.is_enabled():  # 下一頁按鈕有啟用
                page_buttons.click()  # 點按鈕
            else:
                raise (IndexError("找不到可點擊物件"))
        except:  # 找尋不到按鈕
            driver.close()  # 關閉瀏覽器視窗
            return video_list  # 回傳


if __name__ == "__main__":
    videos = keyword_crawler("Vtuber", 40)
    print(f"【獲取 {len(videos)} 部影片】\n")
    for i in videos:
        print(*i, sep="\n", end="\n\n")
