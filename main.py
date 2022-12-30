import configparser
import time
import tweepy
import alpaca_trade_api as tradeapi
from transformers import pipeline

config = configparser.RawConfigParser()
config.read("config.ini")
print(config)
#Alpaca Credentials
bearer_token = config['twitter']['bearer_token']
endpoint= config['twitter']['endpoint']
api_key_id= config['twitter']['api_key_id']
secret_key= config['twitter']['secret_key']

#Twitter credentials
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
client_id = config['twitter']['client_id']
client_secret = config['twitter']['client_secret']

#alpaca authentication
api = tradeapi.REST(api_key_id,
                    secret_key,
                    endpoint, api_version='v2')

#Twitter authentication
auth = tweepy.OAuth2BearerHandler(bearer_token)
api = tweepy.API(auth)

def checkTwitter():
    client = tweepy.Client(bearer_token)
    response = client.search_recent_tweets("TSLA", max_results=100)

    print(response.meta)

    tweets = response.data
    tweet_ids = []

    for i, tweet in enumerate(tweets):
        print(i)
        tweet_ids.append(tweet.id)
        print(tweet.text)
        print("\n**********************\n\n")

        res = performSentimentAnalysis(tweet)
        print("result: ", res)
    
    viabilityScores = {"AAPL":100,
        "GOOGL": 91,
        "AMZN": 45,
        "TSLA": -80,
        "META": 20}
    return viabilityScores

def performSentimentAnalysis(tweet):
    sentiment_analysis = pipeline('sentiment-analysis')

    result = sentiment_analysis(tweet)[0]
    if result['score'] < .80:
        return
    else:
        if result['label'] == "NEGATIVE":
            print("NEGATIVE")
            return "NEGATIVE"
        else:
            return "POSITIVE"

def tradeStocks(viabilityScores):
    
    print(viabilityScores.items())
    for stock in viabilityScores.items():      
    # Submit a market order to buy 1 share of Apple at market price
        
        print(stock[1])
        
        if stock[1] >= 50:
            api.submit_order(
                symbol=stock[0],
                qty=1,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print("BUY: ", stock)
        elif stock[1] <-50:
            api.submit_order(
                symbol=stock[0],
                qty=1,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            print("SELL: ", stock)
    return "Success"


if __name__=="__main__":
    #print("test")
    viabilityScores = checkTwitter()
    tradeStocks(viabilityScores)