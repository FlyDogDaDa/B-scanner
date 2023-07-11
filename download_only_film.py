import requests
import re
import json
import time


def get_url(url: str) -> list[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "referer": "https://www.bilibili.com",
    }  # request所需的標頭檔
    resp = requests.get(url, headers=headers)  # 發送請求
    palyinfo = re.findall(r"<script>window.__playinfo__=(.*?)</script>", resp.text)[
        0
    ]  # 用正值表達找到影片資訊
    palyinfo_data = json.loads(palyinfo)  # 轉換文json格式
    video_url = palyinfo_data["data"]["dash"]["video"][-1]["base_url"]  # 取出畫面網址
    return video_url  # 回傳網址


def download(path: str, file_url: str, visible=True) -> None:
    chunk_size = 1024  # 每次寫入數據塊大小
    done_size = 0  # 完成大小
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        "referer": "https://www.bilibili.com",
    }  # request所需的標頭檔

    resp = requests.get(url=file_url, headers=headers)  # 發送請求
    file_size = int(resp.headers["content-length"])  # 取得文件大小
    file_size_MB = file_size / 1048576  # 將大小換成MB表示

    if visible:  # 如果需要顯示
        print(f"文件大小：{file_size_MB:0.2f} MB")  # 列印出文件大小

    start_time = time.time()  # 紀錄開始時間
    with open(path, mode="wb") as f:  # 以位元寫入開啟檔案
        for chunk in resp.iter_content(chunk_size=chunk_size):  # 迭代過每個區塊
            f.write(chunk)  # 寫入區塊
            done_size += len(chunk)  # 累計完成大小
            if visible:  # 如果需要顯示
                # 列印完成進度
                print(f"\r下載進度：{done_size/file_size*100:0.2f}%", end="")

    end_time = time.time()  # 紀錄結束時間
    cost_time = end_time - start_time  # 計算花費時間

    if visible:  # 如果需要顯示
        print(f"\t耗時：{cost_time:0.2f} 秒")  # 列印花費時間
        print(f"下载速度：{file_size_MB/cost_time:0.2f}M/s")  # 列印下載速度


if __name__ == "__main__":
    # 取得範例影片資訊
    url = get_url("https://www.bilibili.com/video/BV15x4y1L7Mc")
    download(f"video_storage\亂下載的影片.mp4", url)  # 下載範例影片
