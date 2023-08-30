from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json
from tqdm import tqdm
import os


# Columns of the DataFrame
columns = ["Name", "Summary", "Genres"]


# Headless Webdriver
def create_headless_webdriver() :
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    return webdriver.Chrome(options=chrome_options)


# Get Game Name, Summary and Link
def get_game_info(row):
    name = row["Name"]
    summary = row["Summary"]
    link = row["Link"]
    return name, summary, link


def get_game_details():
    df_game = pd.read_csv("../data/raw_data/game_url_data.csv")
    start, end = read_count(), df_game.shape[0]
    game_data = []

    driver = create_headless_webdriver()

    for idx in tqdm(range(start, end)):
        name, summary, link = get_game_info(df_game.loc[idx])
        driver.get(link)

        try:
            details = driver.find_elements(By.CLASS_NAME, "summary_details")[2].text.split("\n")[1]
            genre_list = details.split(":")[1].split(",")
            genres = []
            for genre in genre_list:
                genres.append(genre.strip())
        except Exception:
            genres = []

        game_details = {
            columns[0]: name,
            columns[1]: summary,
            columns[2]: genres
        }
        game_data.append(game_details)
        if (idx + 1) % 100 == 0:
            game_data_save(game_data)
            game_data.clear()
            write_count(idx)

    game_data_save(game_data)
    game_data.clear()
    driver.close()


# Save Game Data To CSV File
def game_data_save(game_data):
    path = os.path.join("../data/raw_data", "game_details_data.csv")

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


def read_count():
    with open("pointer/count_pointer.json", "r") as file:
        data = json.load(file)

    return data["count"]


def write_count(count):
    with open("pointer/count_pointer.json", "w") as file:
        data = {"count": count}
        json.dump(data, file)


if __name__ == "__main__":
    get_game_details()
