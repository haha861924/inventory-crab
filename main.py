import requests
from bs4 import BeautifulSoup
import os
import json


def download_image(url, folder_path, filename):
    file_path = os.path.join(folder_path, filename)

    if os.path.exists(file_path):
        print(f"檔案已存在，無需下載：{file_path}")
    else:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"圖片已下載至 {file_path}")
        else:
            print("無法下載圖片")


if __name__ == '__main__':
    url = "https://valheim.fandom.com/zh-tw/wiki/%E9%A3%9F%E7%89%A9"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    food_table = soup.find("table", class_="wikitable")
    food_list = []

    if food_table:
        rows = food_table.find_all("tr")[1:]  # Skip the header row
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 3:
                food_list.append({
                    "食物": columns[0].text.strip(),
                    "圖標": columns[1].a["href"],
                    "生命": columns[2].text.strip(),
                    "耐力": columns[3].text.strip(),
                    "巨蛇之毒": columns[4].text.strip(),
                    "總計": columns[5].text.strip(),
                    "類型": columns[6].text.strip(),
                    "治療": columns[7].text.strip(),
                    "持續時間": columns[8].text.strip(),
                    "重量": columns[9].text.strip(),
                    "堆疊數量": columns[10].text.strip(),
                    "生物群落進度": columns[11].text.strip(),
                    "取得處": columns[12].text.strip(),
                    "製作材料": columns[13].text.strip()
                })

                # 下載圖片 記得修改名稱
                download_image(columns[1].a["href"], "images", columns[0].text.strip() + ".png")
    if os.path.exists('food_data.json'):
        with open('food_data.json', 'r', encoding='utf-8') as existing_json_file:
            existing_data = json.load(existing_json_file)
            food_list.extend(existing_data)

        # Save data as JSON
    with open('food_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(food_list, json_file, ensure_ascii=False, indent=4)

    for food in food_list:
        print("食物:", food["食物"])
        print("圖標:", food["圖標"])
        print("生命:", food["生命"])
        print("耐力:", food["耐力"])
        print("巨蛇之毒:", food["巨蛇之毒"])
        print("總計:", food["總計"])
        print("類型:", food["類型"])
        print("治療:", food["治療"])
        print("持續時間:", food["持續時間"])
        print("重量:", food["重量"])
        print("堆疊數量:", food["堆疊數量"])
        print("生物群落進度:", food["生物群落進度"])
        print("取得處:", food["取得處"])
        print("製作材料:", food["製作材料"])
        print("-" * 30)
