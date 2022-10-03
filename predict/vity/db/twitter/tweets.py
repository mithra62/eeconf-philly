#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""VITY Twitter Tweets Database Table
Outlines interaction with the Twitter Tweets table
"""
import sys
sys.path.append('../../')
from vity.logs import logging
from vity.db.twitter.accounts import Accounts as TwitterAccounts

logger = logging.getLogger(__name__)

class Tweets:
    db = False
    def __init__(self, db):
        self.db = db

    def updateTweetPredictData(self, tweet_id, sentiment_data, category):
        sql = """
            UPDATE
            exp_vity_twitter_tweets SET
            sentiment_score=%s,
            sentiment=%s,
            category_id=%s
            WHERE tweet_id=%s
            """
        save_data = (sentiment_data['score'],
                    sentiment_data['sentiment'],
                    category,
                    str(tweet_id), )

        cursor = self.db.cursor()
        try:
            cursor.execute(sql, save_data)
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error('Can\'t Execute Update!', sql % save_data)
            return False

    def getAudiencePendingPrediction(self, account_id, max_total = 50000):
        account = TwitterAccounts(self.db)
        follower_ids = account.getFollowerIds(account_id)
        if follower_ids is not None:
            return_data = []
            for follower_id in follower_ids:
                # format_strings = ','.join(['%s'] * len(follower_ids))
                sql = """SELECT tweet_text, tweet_id
                FROM exp_vity_twitter_tweets
                WHERE
                user_id = %s
                AND sentiment IS NULL ORDER BY tweet_id DESC
                LIMIT 1000
                """
                cursor = self.db.cursor()
                cursor.execute(sql, (follower_id, ))
                results = cursor.fetchall()
                if cursor.rowcount >= 1:
                    logger.info('Found %i tweets for follower %s', len(results), follower_id)
                    for tweet in results:
                        return_data.append(tweet)

                if len(return_data) >= max_total:
                    break

            return return_data
