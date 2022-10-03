#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""VITY Oauth Keys Database Table
Outlines interaction with the Oauth Keys table
"""
import sys
sys.path.append('../../')
from vity.logs import logging

logger = logging.getLogger(__name__)

class Keys:

    db = False

    def __init__(self, db):
        """Init
        Parameters
        ----------
        db : MySQLdb.connections.Connection
            The platform_user_id value
        """
        self.db = db

    def lockDemoKey(self, account_id, platform):
        """Updates the demo_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        account_id : string
            The platform_user_id value
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET demo_predict_start_date = NOW()
                WHERE platform_user_id = %s AND platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (str(account_id), platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (str(account_id), platform, ))
            return False


    def unlockDemoKey(self, account_id, platform):
        """Updates the demo_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        account_id : string
            The platform_user_id value
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET demo_last_predicted = NOW(), demo_predict_start_date = NULL
                WHERE platform_user_id = %s AND platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (str(account_id), platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (str(account_id), platform, ))
            return False

    def getNextDemoQueueAccountId(self, platform):
        """Returns the platform_user_id to use for next
        demographic predictions
        Parameters
        ----------
        platform : string
            Which platform the account_id belongs to
        return : tuple
        """
        sql = """SELECT platform_user_id
                FROM exp_vity_oauth_keys
                WHERE platform = %s AND audience_last_synced IS NOT NULL
                AND demo_predict_start_date IS NULL
                AND audience_sync_start_date IS NULL
                AND geo_predict_start_date IS NULL
                ORDER BY demo_last_predicted ASC
                LIMIT 1
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (platform, ))
        results = cursor.fetchall()
        if cursor.rowcount != 1:
            return

        for row in results:
            return row['platform_user_id']

    def lockGeoKey(self, account_id, platform):
        """Updates the geo_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        account_id : string
            The platform_user_id value
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET geo_predict_start_date = NOW()
                WHERE platform_user_id = %s AND platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (str(account_id), platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (str(account_id), platform, ))
            return False


    def unlockGeoKey(self, account_id, platform):
        """Updates the geo_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        account_id : string
            The platform_user_id value
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET geo_last_predicted = NOW(), geo_predict_start_date = NULL
                WHERE platform_user_id = %s AND platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (str(account_id), platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (str(account_id), platform, ))
            return False

    def getNextGeoQueueAccountId(self, platform):
        """Returns the platform_user_id to use for next
        geolocation predictions
        Parameters
        ----------
        platform : string
            Which platform the account_id belongs to
        return : string
        """
        sql = """SELECT platform_user_id
                FROM exp_vity_oauth_keys
                WHERE platform = %s AND audience_last_synced IS NOT NULL
                AND demo_predict_start_date IS NULL
                AND audience_sync_start_date IS NULL
                AND geo_predict_start_date IS NULL
                ORDER BY geo_last_predicted ASC
                LIMIT 1
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (platform, ))
        results = cursor.fetchall()
        if cursor.rowcount != 1:
            return

        for row in results:
            return row['platform_user_id']

    def getNextPredictQueueAccountId(self, platform):
        """Returns the platform_user_id to use for next
        content predictions
        Parameters
        ----------
        platform : string
            Which platform the account_id belongs to
        return : string
        """
        sql = """SELECT platform_user_id
                FROM exp_vity_oauth_keys
                WHERE platform = %s AND audience_last_synced IS NOT NULL
                AND audience_predict_start_date IS NULL
                AND demo_predict_start_date IS NULL
                AND geo_predict_start_date IS NULL
                ORDER BY audience_last_predicted ASC
                LIMIT 1
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (platform, ))
        results = cursor.fetchall()

        if cursor.rowcount != 1:
            return

        for row in results:
            return row['platform_user_id']

    def lockPredictKey(self, account_id, platform):
        """Updates the audience_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        account_id : string
            The platform_user_id value
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET audience_predict_start_date = NOW()
                WHERE platform_user_id = %s AND platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (str(account_id), platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (str(account_id), platform, ))
            return False

    def unlockPredictKey(self, account_id, platform):
        """Updates the audience_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        account_id : string
            The platform_user_id value
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET audience_last_predicted = NOW(), audience_predict_start_date = NULL
                WHERE platform_user_id = %s AND platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (str(account_id), platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (str(account_id), platform, ))
            return False

    def unlockPredictKeys(self, platform):
        """Updates the audience_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET audience_predict_start_date = NULL
                WHERE platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (platform, ))
            return False

    def unlockGeoKeys(self, platform):
        """Updates the geo_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET geo_predict_start_date = NULL
                WHERE platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (platform, ))
            return False

    def unlockDemoKeys(self, platform):
        """Updates the demo_predict_start_date column with the
        current datetime to remove from queue
        Parameters
        ----------
        platform : string
            Which platform the account_id belongs to
        return : boolean
        """
        sql = """UPDATE exp_vity_oauth_keys
                SET demo_predict_start_date = NULL
                WHERE platform = %s
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, (platform, ))
            self.db.commit()
            return True
        except self.db.Error as e:
            logger.exception("%d : %s" % (e.args[0], e.args[1]))
            logger.error(sql % (platform, ))
            return False
