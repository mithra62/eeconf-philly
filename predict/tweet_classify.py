#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""VITY Twitter Content Prediction
Iterates through Twitter Content and predicts the sentiment
and categorization for it
Example:
    $ python tweet_predict.py
"""
from vity.logs import logging
from vity.db.connect import db_obj
from vity.db.oauth.keys import Keys as OauthKeys
from vity.db.twitter.tweets import Tweets
from categorizer.data_helper import DataHelper
from sentiment.sentiment import Sentiment
from categorizer.predict import Predictor
from time import sleep

logger = logging.getLogger('tweet_classify')

def main():
    db = db_obj()
    keys = OauthKeys(db)
    keys.unlockPredictKeys('twitter')
    twitter_id = keys.getNextPredictQueueAccountId('twitter')
    logger.info('Starting Tweet Classify for User: %s', str(twitter_id))
    if twitter_id == None:
        db.close() # nothing to queue
        logger.warning('Nothing to do...')
        return

    if keys.lockPredictKey(twitter_id, 'twitter'):
        tweets = Tweets(db)
        predict_content = tweets.getAudiencePendingPrediction(twitter_id)
        if predict_content != None and len(predict_content) >= 1:
            logger.info('Processing %i Tweets', len(predict_content))
            pred = Predictor()
            sentiment = Sentiment()
            data_helper = DataHelper()
            for tweet in predict_content:
                text = data_helper.cleanTweet(tweet['tweet_text'])
                # determine if we should proceed
                sentiment_data = sentiment.analyze(tweet['tweet_text'])
                category = pred.predictSingle(text)
                tweets.updateTweetPredictData(tweet['tweet_id'], sentiment_data, category)

        keys.unlockPredictKey(twitter_id, 'twitter')
        logger.info('Completed Tweet Classify for User: %s', str(twitter_id))
    db.close()

if __name__ == "__main__":
    while(True):
        main()
        sleep(30)
