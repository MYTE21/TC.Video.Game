from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json
from tqdm import tqdm
import os

columns = ["Name", "Summary", "Link"]


def get_all_game():
    game_data = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(options=chrome_options)

    start_page, end_page = read_page_no()

    for page_id in tqdm(range(start_page, end_page)):
        url = f"https://www.metacritic.com/browse/games/score/metascore/all/all/?page={page_id}"
        driver.get(url)

        browser_list = driver.find_elements(By.CLASS_NAME, "browse_list_wrapper")
        for browser in browser_list:
            game_table = browser.find_element(By.CLASS_NAME, "clamp-list")
            game_row = game_table.find_elements(By.TAG_NAME, "tr")
            for i, ar in enumerate(game_row):
                if i % 2 == 0:
                    game_detail = ar.find_elements(By.TAG_NAME, "td")[1].text.split("\n")
                    table_list = browser.find_element(By.XPATH, "//tr").find_elements(By.XPATH, "//td")[i]
                    link = table_list.find_element(By.TAG_NAME, "a").get_attribute("href")

                    try:
                        summary = game_detail[5]
                    except Exception:
                        summary = None

                    game_info = {
                        "Name": game_detail[2],
                        "Summary": summary,
                        "Link": link
                    }
                    game_data.append(game_info)

        write_page_no(page_id + 1, end_page)

        game_data_save(game_data)
        game_data.clear()

    driver.close()


def game_data_save(game_data):
    path = os.path.join("../data/raw_data", "game_data.csv")

    if not os.path.isfile(path):
        df = pd.DataFrame(data=game_data, columns=columns)
        df.to_csv(path, index=False)
        return df.shape[0]
    else:
        new_df = pd.DataFrame(data=game_data, columns=columns)
        ex_df = pd.read_csv(path)
        combine_df = pd.concat([ex_df, new_df], ignore_index=True)
        combine_df.to_csv(path, index=False)
        return combine_df.shape[0]


def read_page_no():
    with open("page_pointer.json", "r") as file:
        data = json.load(file)

    return data["start"], data["end"]


def write_page_no(start, end):
    with open("page_pointer.json", "w") as file:
        data = {"start": start, "end": end}
        json.dump(data, file)


if __name__ == "__main__":
    get_all_game()
