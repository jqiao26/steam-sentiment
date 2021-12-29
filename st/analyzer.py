import matplotlib.pyplot as plt
import os
from google.cloud import language_v1
from google.oauth2 import service_account
from collections import Counter
from wordcloud import WordCloud 


def get_analysis(game, data):
    wordcloud_generator(game, data)


def wordcloud_generator(game, data, title=None):
    most_freq = Counter(data).most_common(1000) 
    text = ' '.join([x[0] for x in most_freq])
    
    wordcloud = WordCloud(width = 1200, height = 1200,
                          background_color ='white',
                          min_font_size = 10,
                          collocations=False
                         ).generate(text)

    # plot the Word Cloud                      
    plt.figure(figsize = (9, 9), facecolor = None) 
    plt.imshow(wordcloud, interpolation='bilinear') 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.title(title,fontsize=25)

    dev_dir = os.environ['DEV_DIR']
    plt.savefig(f'{dev_dir}\\steam-sentiment\\static\\{game}.png')


def sample_analyze_sentiment(text_content):
    analysis = {}

    google_cred_path = os.environ['GOOGLE_CREDS']
    creds = service_account.Credentials.from_service_account_file(google_cred_path)
    client = language_v1.LanguageServiceClient(credentials=creds,)
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    analysis['score'] = response.document_sentiment.score
    analysis['magnitude'] = response.document_sentiment.magnitude
    analysis['sentences'] = []
    
    for sentence in response.sentences:
        analysis['sentences'].append((sentence.text.content, sentence.sentiment.score))
    
    return analysis
