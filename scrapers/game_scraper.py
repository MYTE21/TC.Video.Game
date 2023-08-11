from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json

columns = []


def game_details():
    pass


def get_all_game():
    game_data = []
    driver = webdriver.Chrome()

    start_page, end_page = read_page_no()

    for page_id in range(start_page, end_page):
        url = f"https://www.metacritic.com/browse/games/score/metascore/all/all/?page={page_id}"
        driver.get(url)

        browser_list = driver.find_elements(By.CLASS_NAME, "browse_list_wrapper")
        print("Browser: ", len(browser_list))
        for browser in browser_list:
            anime_table = browser.find_element(By.CLASS_NAME, "clamp-list")
            anime_row = anime_table.find_elements(By.TAG_NAME, "tr")
            for i, ar in enumerate(anime_row):
                if i % 2 == 0:
                    anime_details = ar.find_elements(By.TAG_NAME, "td")[1].text.split("\n")
                    print(f"({i}): {anime_details}")

        break

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
