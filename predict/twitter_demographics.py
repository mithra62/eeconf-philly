#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""VITY Twitter Demographic Extraction
This module iterates through stored Twitter Accounts and
extracts various demographic insights from it.
Example:
    $ python twitter_demographics.py
"""
from vity.logs import logging
from vity.db.connect import db_obj
from vity.db.oauth.keys import Keys as OauthKeys
from vity.db.twitter.accounts import Accounts as TwitterAccounts
import vity.names as vity_names
from time import sleep

logger = logging.getLogger('twitter_demographics')

def main():
    db = db_obj()
    keys = OauthKeys(db)
    keys.unlockDemoKeys('twitter')
    twitter_id = keys.getNextDemoQueueAccountId('twitter')
    logger.info('Starting Twitter Follower Demographics for User: %s', str(twitter_id))
    if twitter_id == None:
        db.close() # nothing to queue
        logger.info('Nothing to do...')
        sleep(30)
        return

    if keys.lockDemoKey(twitter_id, 'twitter'):
        accounts = TwitterAccounts(db)
        demo_audience = accounts.getAudiencePendingDemo(twitter_id)
        if demo_audience is not None:
            logger.info('Processing %i Follower Demographics', len(demo_audience))
            for follower in demo_audience:
                nameparser = vity_names.VityNames()
                name = nameparser.parse( follower['name'] )
                if name:
                    accounts.updateNameDemoData(name)

        keys.unlockDemoKey(twitter_id, 'twitter')
        logger.info('Completed Twitter Follower Demographics for User: %s', str(twitter_id))
    db.close()

if __name__ == "__main__":
    while(True):
        main()
        sleep(30)
