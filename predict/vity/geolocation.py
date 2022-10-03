# coding: utf-8

"""VITY Gelocation Translation
Handles geocoding of address data
Example:
    $ python twitter_geolo.py
"""

from vity.nominatim import Nominatim
from time import sleep
import re
from unidecode import unidecode

class Address:
    city = 'n/a'
    state = 'n/a'
    country = 'n/a'
    country_code = 'n/a'
    county = ''
    postcode = ''
    latitude = ''
    longitude = ''
    display_name = ''
    boundingbox = []
    place_id = ''
    data = []

    def set(self, data):
        self.data = data
        address = data['address']
        if 'city' in address:
            self.city = unidecode(address['city'])
        if 'state' in address:
            self.state = address['state']
        if 'country' in address:
            self.country = address['country']
        if 'country_code' in address:
            self.country_code = address['country_code']
        if 'county' in address:
            self.county = address['county']
        if 'postcode' in address:
            self.postcode = address['postcode']
        if 'lat' in data:
            self.latitude = data['lat']
        if 'lon' in data:
            self.longitude = data['lon']
        if 'display_name' in data:
            self.display_name = data['display_name']
        if 'boundingbox' in data:
            self.boundingbox = data['boundingbox']
        if 'place_id' in data:
            self.place_id = data['place_id']
        return self

class Geolo:

    def geocode(self, query, limit=1):
        sleep(2) #we can only do 1 query a second 'cause $ reasons
        nom = Nominatim()
        data = nom.query(unidecode(query), 'en', limit)
        if data != None and len(data) >= 1:
            address_data = Address()
            return address_data.set(data[0])
