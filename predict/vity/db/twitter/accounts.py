#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""VITY Twitter Accounts Database Table
Outlines interaction with the Twitter Accounts table
"""

import sys
import json
sys.path.append('../../')
from vity.logs import logging
from vity.names import VityNames
from vity.geolocation import Address

logger = logging.getLogger(__name__)

class Accounts:

    db = False

    def __init__(self, db):
        """Init
        Parameters
        ----------
        db : MySQLdb.connections.Connection
            The platform_user_id value
        """
        self.db = db

    def updateNameDemoData(self, name: VityNames):
        """Updates the demographic data for the name data
        Parameters
        ----------
        name : VityNames
            The Names object
        return : boolean
        """
        sql = """
            UPDATE
            exp_vity_twitter_accounts SET
            gender=%s,
            generation_name=%s,
            last_name=%s,
            first_name=%s,
            is_company=%s,
            ethnicity=%s,
            ethnicity_primary_region=%s,
            ethnicity_secondary_region=%s
            WHERE name=%s
        """
        data = (name.gender,
                name.generation_name,
                name.last_name,
                name.first_name,
                name.is_company,
                name.race['name'],
                name.race['primary_region'],
                name.race['secondary_region'],
                name.name, )

        cursor = self.db.cursor()
        try:
            cursor.execute(sql, data)
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error('Can\'t Execute Update!', sql % save_data)
            return False

    def updateLocationGeoData(self, location, address_data: Address):
        sql = """
            UPDATE
            exp_vity_twitter_accounts SET
            city=%s,
            state=%s,
            country=%s,
            country_code=%s,
            postcode=%s,
            latitude=%s,
            longitude=%s,
            boundingbox=%s,
            place_id=%s,
            display_name=%s
            WHERE location=%s
            """
        save_data = (address_data.city,
                    address_data.state,
                    address_data.country,
                    address_data.country_code,
                    address_data.postcode,
                    address_data.latitude,
                    address_data.longitude,
                    json.dumps(address_data.boundingbox),
                    address_data.place_id,
                    address_data.display_name,
                    location, )
        cursor = self.db.cursor()
        try:
            cursor.execute(sql, save_data)
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error('Can\'t Execute Update!', sql % save_data)
            return False

    def getAddressByLocation(self, location):
        sql = """SELECT city, state, country, country_code,
                postcode, longitude, latitude, display_name,
                boundingbox, place_id, location
                FROM exp_vity_twitter_accounts
                WHERE location = %s AND country IS NOT NULL
                LIMIT 1
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (location, ))
        results = cursor.fetchall()
        if cursor.rowcount != 0:
            address_data = Address()
            for row in results:
                row['boundingbox'] = json.loads(row['boundingbox'])
                return address_data.set({'address': row})

    def getAudiencePendingDemo(self, account_id):
        follower_ids = self.getFollowerIds(account_id)
        if follower_ids is not None:
            format_strings = ','.join(['%s'] * len(follower_ids))
            sql = """SELECT DISTINCT(name) FROM exp_vity_twitter_accounts
                    WHERE twitter_id IN(%s) and gender IS NULL
                    LIMIT 500
            """
            cursor = self.db.cursor()
            cursor.execute(sql % format_strings, tuple(follower_ids))
            results = cursor.fetchall()
            if cursor.rowcount == 0:
                return
            else:
                return results

    def getFollowerIds(self, account_id):
        sql = """SELECT follower_id
                FROM `exp_vity_twitter_followers`
                WHERE twitter_id = %s
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (str(account_id), ))
        results = cursor.fetchall()
        if cursor.rowcount == 0:
            return
        else:
            return_data = list()
            for follower in results:
                return_data.append(follower['follower_id'])

            return return_data

    def getAudiencePendingGeo(self, account_id):
        follower_ids = self.getFollowerIds(account_id)
        if follower_ids is not None:
            format_strings = ','.join(['%s'] * len(follower_ids))
            sql = """SELECT DISTINCT(location), twitter_id
                    FROM exp_vity_twitter_accounts WHERE location != ''
                    AND country IS NULL AND twitter_id IN(%s)
                    LIMIT 500
            """
            cursor = self.db.cursor()
            cursor.execute(sql % format_strings, tuple(follower_ids))
            results = cursor.fetchall()
            if cursor.rowcount == 0:
                return
            else:
                return results
