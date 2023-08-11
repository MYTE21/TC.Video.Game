from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json
from tqdm import tqdm

columns = ["Name", "Summary", "Link"]


def game_details():
    pass


def get_all_game():
    game_data = []
    total_games = 0
    driver = webdriver.Chrome()

    start_page, end_page = read_page_no()

    for page_id in tqdm(range(start_page, end_page)):
        print(f"\nPage No: {page_id + 1}")
        url = f"https://www.metacritic.com/browse/games/score/metascore/all/all/?page={page_id}"
        driver.get(url)

        browser_list = driver.find_elements(By.CLASS_NAME, "browse_list_wrapper")
        # print("Browser: ", len(browser_list))
        for browser in browser_list:
            game_table = browser.find_element(By.CLASS_NAME, "clamp-list")
            game_row = game_table.find_elements(By.TAG_NAME, "tr")
            for i, ar in enumerate(game_row):
                if i % 2 == 0:
                    table_list = browser.find_element(By.XPATH, "//tr").find_elements(By.XPATH, "//td")[i]
                    link = table_list.find_element(By.TAG_NAME, "a").get_attribute("href")
                    game_detail = ar.find_elements(By.TAG_NAME, "td")[1].text.split("\n")
                    total_games += 1
                    # print(f"({i}): {game_detail} \n link: {link}")

        write_page_no(start_page + 1, end_page)
        print("Total games: ", total_games)

    driver.close()


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
