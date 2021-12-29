from flask import Flask, request, render_template
from st.data import get_searched_title, get_reviews, generate_charts
from st.analyzer import wordcloud_generator, sample_analyze_sentiment

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/games', methods=['POST'])
def games():
    """
    Get the Steam game based on the given search
    """
    if request.method == 'POST':
        req = request.json
        game = request.form['searchQueryInput']
        reviews = get_reviews(game)
        full_name = get_searched_title(game)
        wordcloud_generator(full_name, reviews['review_text'])

        sentiment = []
        for review in reviews['review_text'].to_list():
            sentiment.append(sample_analyze_sentiment(review))

        for i in range(len(sentiment)):
            sentiment[i]['rating'] = reviews['review_score'].iloc[i]

        doughnut, stacked = generate_charts(sentiment)

    return render_template(
        'games_result.html', 
        game=full_name, 
        doughnut=doughnut, 
        stacked=stacked, 
        sentiment=sentiment
    )
