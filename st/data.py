import pandas as pd
import sqlite3

from pandas.core.reshape.reshape import stack


def get_reviews(game_name) -> pd.DataFrame:
    con = sqlite3.connect(database='C:\\Users\\Lenovo IdeaPad JQ\\Dev\\steam-sentiment\\data\\steam-data\\steam.db')
    title = get_searched_title(game_name)
    query = """
            SELECT review_text, review_score from steam
            WHERE app_name=='{title}'
            """.format(title=title)
    
    reviews = pd.read_sql_query(query, con=con)
    return reviews[['review_text', 'review_score']]


def get_searched_title(game_name) -> str:
    """
    Returns the full name of searched game
    """
    con = sqlite3.connect(database='C:\\Users\\Lenovo IdeaPad JQ\\Dev\\steam-sentiment\\data\\steam-data\\steam.db')
    query = """
            SELECT * from steam
            WHERE app_name LIKE '%{game_name}%'
            """.format(game_name=game_name)
    
    reviews = pd.read_sql_query(query, con=con)
    return reviews['app_name'].iloc[0]


def generate_charts(analysis) -> dict:
    doughnut = { 'pos': 0, 'neg': 0, 'neu': 0 }
    stacked = { 'pos_rec': 0, 'pos_norec': 0, 'neu_rec': 0, 'neu_norec': 0, 'neg_rec': 0, 'neg_norec': 0 }
    for review in analysis:
        if review['score'] >= -1 and review['score'] < -0.25:
            doughnut['neg'] += 1
            if review['rating'] == 1:
                stacked['neg_rec'] += 1
            else:
                stacked['neg_norec'] += 1
        elif review['score'] >= 0.25 and review['score'] <= 1:
            doughnut['pos'] += 1
            if review['rating'] == 1:
                stacked['pos_rec'] += 1
            else:
                stacked['pos_norec'] += 1
        else:
            doughnut['neu'] += 1
            if review['rating'] == 1:
                stacked['neu_rec'] += 1
            else:
                stacked['neu_norec'] += 1
    return doughnut, stacked


def get_data() -> pd.DataFrame:
    return pd.read_pickle('C:\\Users\\Lenovo IdeaPad JQ\\Dev\\steam-sentiment\\data\\steam-data\\steam.pkl')
