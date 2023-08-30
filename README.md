# TC Video Game
A text classification model from data collection, model training, and deployment.
The model can classify 20 different types of game genres
The keys of `encrypted/kaggle/genre_types_encoded_kaggle.json` show the game genres.

*🔴Notice🔴*
>  `original` sub folder of all the folder contains codes for the scraped dataset.
> 
> `kaggle` sub folder of all the folder contains codes for the collected dataset from the Kaggle platform.

# Data Collection
Data was collected from a Game Website:[Metacritic Game](https://www.metacritic.com/browse/games/score/metascore/all/all).
The data collection process is divided into 2 steps:
1. `Game URL Scraping`: The game urls were scraped with `scraper\game_url_scraper.py` and the urls are stored along with game title.
2. `Game Details Scraping`: Using the urls, the game description and genres are scraped with `scraper\game_details_scraper.py`
   and they are stored in `data/raw_data/game_detils.csv`.

In total, I scraped `20,406` game details.

# Data Preprocessing
Initially, there were 33 different genres in the dataset. 
After some analysis, I found out 12 of them are rare (probably custom genres by users). 
So, I removed those genres and then I have 21 genres. 
After that, I removed the description without any genres resulting in `73,551` samples.

# Model Training
Fine-tuned a distilrobera-base model from HuggingFace Transformers using Fastai and Blurr. 
The model training notebook can be viewed [here](notebooks)

# Model Compression and ONNX Inference
The trained model has a memory of `900+MB`.
I compressed this model using ONNX quantization and brought it under `78.7MB`.

# Model Deployment
The compressed model is deployed to HuggingFace Spaces Gradio App. The implementation can be found in 
the [deployment](development) folder or [here](https://huggingface.co/spaces/myte/tc-video-game/tree/main)

# Web Deployment
Deployed a Flask App built to take description and show the genres as output. 
Check `dev` branch. 
The website is live [here](https://tc-video-game.onrender.com/)
