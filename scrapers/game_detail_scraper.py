from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import json
from tqdm import tqdm
import os


columns = ["Name", "Summary", "Genres"]


def get_game_details():
    df_game = pd.read_csv("../data/raw_data/game_data.csv")
    total_game = df_game.shape[0]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(options=chrome_options)

    game_data = []

    start = read_count()

    for idx in tqdm(range(start, total_game)):
        name, summary, link = get_game_info(df_game.loc[idx])
        driver.get(link)

        details = driver.find_elements(By.CLASS_NAME, "summary_details")[2].text.split("\n")[1]
        genre_list = details.split(":")[1].split(",")
        genres = []
        for genre in genre_list:
            genres.append(genre.strip())

        game_details = {
            "Name": name,
            "Summary": summary,
            "Genres": genres
        }
        game_data.append(game_details)
        if (idx + 1) % 100 == 0:
            game_data_save(game_data)
            game_data.clear()
            write_count(idx)

    game_data_save(game_data)
    game_data.clear()
    driver.close()


def get_game_info(row):
    name = row["Name"]
    summary = row["Summary"]
    link = row["Link"]
    return name, summary, link


def game_data_save(game_data):
    path = os.path.join("../data/raw_data", "game_details.csv")

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
    with open("counter.json", "r") as file:
        data = json.load(file)

    return data["count"]


def write_count(count):
    with open("counter.json", "w") as file:
        data = {"count": count}
        json.dump(data, file)


if __name__ == "__main__":
    get_game_details()
