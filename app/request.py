import urllib.request,json
from .models import News,Articles

# Getting api key
api_key = None
# Getting the base urls
base_url = None
articles_base_url = None

def configure_request(app):
    global api_key,base_url,articles_base_url
    api_key = app.config['NEWS_API_KEY']
    base_url = app.config["NEWS_API_BASE_URL"]
    articles_base_url = app.config["ARTICLE_API_BASE_URL"]

def get_news(category):
    '''
    Function that gets the json response to our url request
    '''
    get_news_url = 'https://newsapi.org/v2/sources?language=en&category=general&apiKey=25c1ea6f9cbe4912b8e959433eba1c33'

    with urllib.request.urlopen(get_news_url) as url:
        get_news_data = url.read()
        get_news_response = json.loads(get_news_data)
    

        news_results = None

        if get_news_response['sources']:
            news_results_list = get_news_response['sources']
            news_results = process_results(news_results_list)


    return news_results

def process_results(news_list):
    '''
    Function  that processes the news result and transform them to a list of Objects

    Args:
        news_list: A list of dictionaries that contain news details

    Returns :
        news_results: A list of news objects
    '''
    news_results = []
    for news_item in news_list:
        id = news_item.get('id')
        name = news_item.get('name')
        description = news_item.get('description')
        url = news_item.get('url_path')
        category = news_item.get('category')
        language =news_item.get('language')
        country = news_item.get('country')

        
        news_object = News(id,name,description,url,category,language,country)
        news_results.append(news_object)

    return news_results

def get_articles(id):
    '''Function thet gets the json response to our url request'''
    get_articles_url = 'https://newsapi.org/v1/articles?source={}&apiKey={}'.format(id,api_key)

    with urllib.request.urlopen(get_articles_url) as url:
        get_articles_data = url.read()
        get_articles_response = json.loads(get_articles_data)

        article_results = None

        if get_articles_response['articles']:
            article_results_list = get_articles_response['articles']
            article_results = process_articles(article_results_list)

    return article_results

def process_articles(article_list):
    '''
    Function that processes the airticle result and transforms them to a list of objects
    Args:
        article_list: a list of dictionaries that contain articles
    Returns:
        article_results: a list of article objects
    '''
    article_results = []
    for article_item in article_list:
        id = article_item.get('id')
        title = article_item.get('title')
        description = article_item.get('description')
        author = article_item.get('author')
        urlToImage = article_item.get('urlToImage')
        publishedAt = article_item.get('publishedAt')
        url = article_item.get('url')
        if urlToImage:
            article_object = Articles(id,title,description,author,urlToImage,publishedAt,url)
            article_results.append(article_object)

    return article_results

