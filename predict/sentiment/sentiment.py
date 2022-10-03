# coding: utf-8

"""VITY Sentiment Extraction
"""
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
from sentiment.emoji_map import EmojiMap

"""VITY Sentiment
Extracts sentiment from a piece of text
Example:
    > sentiment = Sentiment()
    > value = sentiment.analyze('Is this a positive string?')
"""
class Sentiment:

    emoji_map = False
    analyzer = False

    def __init__(self):
        """Init
        We setup the emoji map list on instantiation
        @todo look into caching map
        """
        emoji_map = EmojiMap()
        self.analyzer = SentimentIntensityAnalyzer()
        self.emoji_map = emoji_map.buildEmojiMap()

    def extractEmojis(self, content):
        """Returns a string of all emojicons found
        within the string
        Parameters
        ----------
        content : string
            The data we want emojis from
        return : string
        """
        return ''.join(c for c in content if c in emoji.UNICODE_EMOJI)

    def removeEmojis(self, content):
        """Removes any emoji icons from
        within the string
        Parameters
        ----------
        content : string
            The string we want to remove emojis from
        return : string
        """
        return ''.join(c for c in content if c not in emoji.UNICODE_EMOJI)

    def getTextSentiment(self, content):
        """Returns a dictionary detailing the sentiment
        Parameters
        ----------
        content : string
            The string we want to parse
        return : dictionary
        """
        return self.analyzer.polarity_scores(content)

    def getEmojiSentiment(self, content):
        """Returns the sentiment for emojis
        Parameters
        ----------
        content : string
            The string we want to parse
        return : float
        """
        emoji_list = list(content)
        sentiment = []
        for emoji in emoji_list:
            for emoji_map in self.emoji_map:
                if emoji_map['unicode'].encode('utf-8') == emoji.encode('unicode_escape'):
                    sentiment.append(emoji_map['sentiment'])

        return sentiment

    def mergeSentiments(self, emoji_sentiment, content_sentiment):
        """Combines the sentiment from our sources into a unified value
        Parameters
        ----------
        content : string
            The string we want to parse
        return : dictionary
        """
        total = len(emoji_sentiment)
        emojis_sentiment = 0
        for emoji in emoji_sentiment:
            if emoji != '':
                emoji = float(emoji)
                emojis_sentiment += emoji

        content_sentiment['compound'] = (content_sentiment['compound']+emojis_sentiment) / 2
        return content_sentiment

    def analyze(self, content):
        emojis = self.extractEmojis(content)
        sentiment = self.getTextSentiment(content)
        content = self.removeEmojis(content)
        emoji_sentiment = False
        if emojis != '':
            emoji_sentiment = self.getEmojiSentiment(emojis)

        if emoji_sentiment:
            sentiment = self.mergeSentiments(emoji_sentiment, sentiment)

        if sentiment['compound'] >= 0.5:
            named_value = 'positive'
        elif sentiment['compound'] > -0.5 and sentiment['compound'] < 0.5:
            named_value = 'neutral'
        else:
            named_value = 'negative'

        return_data = {'sentiment': named_value, 'score':sentiment['compound']}
        return return_data
