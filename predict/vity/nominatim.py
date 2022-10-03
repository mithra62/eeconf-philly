import json
import logging
import sys
import urllib.parse
import urllib.request
from unidecode import unidecode

class Nominatim(object):
    """Class for querying text adress

http://wiki.openstreetmap.org/wiki/Nominatim#Search"""
    def __init__(self):
        self.url = 'http://nominatim.openstreetmap.org/search?format=json&addressdetails=1'
        self.logger = logging.getLogger(__name__)

    def query(self, query, acceptlanguage='', limit=None):
        """Method takes query string, acceptlanguage string (rfc2616 language
code), limit integer (limits number of results)."""
        query = query.replace(' ', '+')
        query = query.strip()
        query = query.replace("\n", "")
        query = query.replace("\r","")

        url = self.url
        url += '&q=' + unidecode(query)
        if acceptlanguage:
            url += '&accept-language=' + acceptlanguage
        if limit:
            url += '&limit=' + str(limit)
        self.logger.info('url:\n' + url)
        try:
            headers = {'User-Agent' : 'VITY.co Geocoder <eric@vity.co>'}
            req = urllib.request.Request(url, headers = headers)
            response = urllib.request.urlopen(req)
            if response.code == 200:
                result = json.loads(response.read().decode('utf-8'))
                return result
            else:
                return None
        except urllib.URLError:
            self.logger.info('Server connection problem')
            return None
            pass


class NominatimReverse(object):
    """Class for querying gps coordinates
        http://wiki.openstreetmap.org/wiki/Nominatim#Reverse_Geocoding_.2F_Address_lookup
    """
    def __init__(self):
        self.url = 'http://nominatim.openstreetmap.org/reverse?format=json'
        self.logger = logging.getLogger(__name__)

    def query(self, lat=None, lon=None, acceptlanguage='', zoom=18):
        """Method takes lat and lon for GPS coordinates, acceptlanguage string,
            zoom integer (between from 0 to 18).
        """
        url = self.url
        if lat and lon:
            url += '&lat=' + str(lat) + '&lon=' + str(lon)
        if acceptlanguage:
            url += '&accept-language=' + acceptlanguage
        if zoom < 0 or zoom > 18:
            raise Exception('zoom must be betwen 0 and 18')
        url +='&zoom=' + str(zoom)
        self.logger.info('url:\n' + url)
        try:
            headers = {'User-Agent' : 'VITY.co Geocoder <eric@vity.co>'}
            req = urllib.request.Request(url, headers = headers)
            response = urllib.request.urlopen(req)
            if response.code == 200:
                result = json.loads(response.read().decode('utf-8'))
                return result
            else:
                return None
        except urllib2.URLError:
            self.logger.info('Server connection problem')
            return None
            pass
