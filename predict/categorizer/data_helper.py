import re
import string
import glob
import os
from bs4 import BeautifulSoup
import ntpath
from random import shuffle
from nltk.corpus import stopwords
import pickle
import json
import numpy as np
from sklearn.utils import shuffle
from textblob import TextBlob
import preprocessor as p
from sklearn.datasets import fetch_20newsgroups

class DataHelper:

    """The working space cat models
        Each category maps to an internal
        ExpressionEngine Channel Entry category
    """
    CATEGORY_MAP = {'Arts': 1,
                    'BeautyAndStyle': 3,
                    'BusinessAndFinance': 4,
                    'CarsAndTransportation': 5,
                    'ComputersAndInternet': 6,
                    'ConsumerElectronics': 7,
                    'EducationAndReference': 8,
                    'EntertainmnentAndMusic': 9,
                    'FoodAndDrink': 10,
                    'GamesAndRecreation': 11,
                    'Health': 12,
                    'HomeAndGarden': 13,
                    'Pets': 14,
                    'PregnancyAndParenting': 15,
                    'SocialScience': 16,
                    'SocietyAndCulture': 17,
                    'Sports': 18,
                    'Religion': 19,
                    'Politics': 20}

    def convertCategoryId(self, cat_id):
        for key, value in self.CATEGORY_MAP.items():
            if value == cat_id:
                return key

    def getCategoryIdFromName(self, name):
        return self.CATEGORY_MAP[name]

    def makeReturn(self, data, randomize=True):
        """Takes the dataset from the filesystem and prpares it for use
        Parameters
        ----------
        data : list
            A list container of values to use
        """
        return_data = {'target': [], 'data': [], 'target_names': [], 'description': 'Yahoo Answers dataset using 20newgroup format'}
        if randomize:
            data = shuffle(data, random_state=42)

        for value in data:
            return_data['target'].append(value['cat_id'])
            return_data['data'].append(value['data'])
            return_data['target_names'].append(value['cat_name'])

        return return_data

    def parseCategoryFromName(self, name):
        """Parses the stored filename for a useful canonical name

        Parameters
        ----------
        name : string
            The value to parse for the Category name
        """
        name = ntpath.basename(name)
        # return name

        return_value = name.split('.')
        return_name = return_value[0]
        #hack for ArtsAndHumanities
        if return_name == 'ArtsAndHumanities':
            return_name = 'Arts'

        return return_name

    def getTrainData(self):
        print('')

    def loadTrainData(self):
        """Returns the Yahoo Answeres dataset
        We want the data to come back in a similar format as 20newsgroups dataset
        Here, we just load the data from disc
        """
        data = []
        file_path = '../../datasets/yahoo.answers/Yahoo/Yahoo.ESA'
        soup = BeautifulSoup
        cachedStopWords = stopwords.words("english")
        for filename in glob.glob(os.path.join(file_path, '*')):
            with open(filename, 'r', encoding='utf-8') as fd:
                parse_data = soup(fd.read(), 'html.parser')
                for node_data in parse_data.findAll('text'):
                    cat_name = self.parseCategoryFromName(filename)
                    cat_id = self.getCategoryIdFromName(cat_name)
                    text = self.parseDataSet(node_data.string)
                    if text:
                        data.append({'data': text, 'cat_name': cat_name, 'cat_id': cat_id})

        # #append the 20newsgroups data we want for CarsAndTransportation
        category_map = {'rec.autos': 'CarsAndTransportation', 'rec.motorcycles': 'CarsAndTransportation'}
        newsgroup_data = fetch_20newsgroups(categories=category_map.keys(), shuffle=True, random_state=7)
        for text in newsgroup_data.data:
            data.append({'data': text, 'cat_name': 'CarsAndTransportation', 'cat_id': 5})

        # #append the 20newsgroups data we want for CarsAndTransportation
        category_map = {'rec.sport.baseball': 'Sports', 'rec.sport.hockey': 'Sports'}
        newsgroup_data = fetch_20newsgroups(categories=category_map.keys(), shuffle=True, random_state=7)
        for text in newsgroup_data.data:
            data.append({'data': text, 'cat_name': 'Sports', 'cat_id': 18})

        # #append the 20newsgroups data we want for ConsumerElectronics
        category_map = {'comp.sys.ibm.pc.hardware': 'ConsumerElectronics', 'comp.sys.mac.hardware': 'ConsumerElectronics', 'sci.electronics': 'ConsumerElectronics'}
        newsgroup_data = fetch_20newsgroups(categories=category_map.keys(), shuffle=True, random_state=7)
        for text in newsgroup_data.data:
            data.append({'data': text, 'cat_name': 'ConsumerElectronics', 'cat_id': 7})

        # #append the 20newsgroups data we want for Religion
        category_map = {'soc.religion.christian': 'Religion', 'talk.religion.misc': 'Religion', 'alt.atheism': 'Religion'}
        newsgroup_data = fetch_20newsgroups(categories=category_map.keys(), shuffle=True, random_state=7)
        for text in newsgroup_data.data:
            data.append({'data': text, 'cat_name': 'Religion', 'cat_id': 19})

        # #append the 20newsgroups data we want for Politics
        category_map = {'talk.politics.guns': 'Politics', 'talk.politics.mideast': 'Politics', 'talk.politics.misc': 'Politics'}
        newsgroup_data = fetch_20newsgroups(categories=category_map.keys(), shuffle=True, random_state=7)
        for text in newsgroup_data.data:
            data.append({'data': text, 'cat_name': 'Politics', 'cat_id': 20})

        data = self.makeReturn(data)
        return data

    def parseDataSet(self, data_string):
        #data_string = ' '.join([word for word in data_string.split() if word not in cachedStopWords])
        return data_string

    def cleanTweet(self, tweet):
        tweet = re.sub(r"http\S+", "$LINK$", tweet)
        tweet = p.tokenize(tweet)
        return p.clean(tweet)
