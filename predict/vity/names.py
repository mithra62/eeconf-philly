# coding: utf-8

"""VITY Name Parser
Can take a human name and run predictions to dtermine
various demographic details like gender and race
"""
from vity.logs import logging
logger = logging.getLogger(__name__)
logger.info('Loading Names Object')

from timeit import default_timer as timer
start_timer = timer()
from agefromname import AgeFromName, GenerationFromName
from nameparser import HumanName
import probablepeople as pp
import spacy
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from ethnicolr import census_ln, pred_census_ln, pred_wiki_ln, pred_wiki_name

nlp = spacy.load('en_core_web_sm')

logger.info('Names Object Loaded')
class VityNames:

	def __init__(self):
		self.gender = 'na'
		self.race = {'name': '', 'secondary_region': '', 'primary_region': ''}
		self.is_company = 'n'
		self.last_name = ''
		self.first_name = ''
		self.generation_name = ''
		self.ethnicity = ''
		self.name = ''

	def parse(self, name):
		"""Takes a human name and predicts the
		various demographic details Parameters
		----------
		name : string
			The human name to parse up
		return : VityNames
		"""
		logger.info('Checking if %s is a company', name)
		if self.is_person(name) == False:
			logger.info('%s is a company so bouncing out', name)
			self.is_company = 'y'
			return self

		self.name = name
		name = HumanName(name)
		self.last_name = name.last
		self.first_name = name.first
		if name.first != '':
			logger.info('Determine the gender for %s', name)
			self.gender = self.get_gender(name.first)
			logger.info('Determine the generation for %s', name)
			self.generation_name = self.get_generation(name.first, self.gender)

		if name.last != '':
			logger.info('Determine the race for %s', name)
			race = self.get_race(name.last)
			if race:
				self.race = race

		logger.info('Complete parse for %s', name)
		return self

	def get_race(self, last_name):
		"""Takes a human LAST name and returns the Race for it Parameters
		----------
		last_name : string
			The human last name to parse up
		return : dictionary
		"""
		race_name = [{'name': last_name}]
		df = pd.DataFrame(race_name)
		mydata = pred_wiki_ln(df, 'name')
		pd_race = mydata['race'].max(axis=0)
		parts = [x.strip() for x in pd_race.split(',')]

		race = {}
		race['name'] = parts[-1]
		race['secondary_region'] = ''
		if parts[1] and parts[1] != race['name']:
			race['secondary_region'] = parts[1]

		race['primary_region'] = ''
		if parts[0]:
			race['primary_region'] = parts[0]

		return race

	def get_generation(self, first_name, gender):
		"""Takes a human FIRST name and gender and
			returns the Generation Label for them
		Parameters
		----------
		last_name : string
			The human last name to parse up
		gender : string
			The short label for the Gender to use
		return : string
		"""
		generation_from_name = GenerationFromName()
		generation = generation_from_name.argmax(first_name, gender)
		return generation

	def get_gender(self, first_name):
		"""Takes a human FIRST name and returns the gender code Parameters
		----------
		first_name : string
			The human first name to parse up
		return : string
		"""
		gender = 'm'
		age_from_name = AgeFromName()
		is_female = age_from_name.prob_female(first_name)
		if is_female*2 >= 1:
			gender = 'f'

		return gender

	def is_person(self, name):
		"""Takes a human name and determines if it's a person Parameters
		----------
		name : string
			The to parse up
		return : boolean
		"""
		doc = nlp(name)
		for ent in doc.ents:
			if ent.label_ == 'ORG':
				return False

		#print(pp.tag(name))
		return True
