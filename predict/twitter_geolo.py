#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""VITY Twitter Gelocation Mining
This module iterates through stored Twitter Accounts and translates colloquial
location names into usable location data
Example:
    $ python twitter_geolo.py
"""
from vity.logs import logging
from vity.geolocation import Geolo, Address
from vity.db.connect import db_obj
from vity.db.oauth.keys import Keys as OauthKeys
from vity.db.twitter.accounts import Accounts as TwitterAccounts
from time import sleep

logger = logging.getLogger('twitter_geolo')

def main():
    db = db_obj()
    keys = OauthKeys(db)
    keys.unlockGeoKeys('twitter')
    twitter_id = keys.getNextGeoQueueAccountId('twitter')
    if twitter_id == None:
        db.close() # nothing to queue
        logger.warning('Nothing to do...')
        sleep(30)
        return

    if keys.lockGeoKey(twitter_id, 'twitter'):
        accounts = TwitterAccounts(db)
        geo_audience = accounts.getAudiencePendingGeo(twitter_id)
        if geo_audience is not None:
            logger.info('Processing %i Follower Geolocation', len(geo_audience))
            for follower in geo_audience:
                # check local store
                address_data = accounts.getAddressByLocation(follower['location'])
                if isinstance(address_data, Address) == False:
                    # pull from remote
                    geo = Geolo()
                    address_data = geo.geocode(follower['location'])
                    if isinstance(address_data, Address) == False:
                        address_data = Address

                accounts.updateLocationGeoData(follower['location'], address_data)

        keys.unlockGeoKey(twitter_id, 'twitter')
        logger.info('Completed Twitter Follower Geolocation for User: %s', str(twitter_id))
    db.close()

if __name__ == "__main__":
    while(True):
        #main()
        sleep(30)
