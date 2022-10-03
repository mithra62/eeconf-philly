# coding: utf-8

"""VITY Categorization Prediction Object

Example:
    predict = Predictor()
    print(predict.predict('string to categorize'))
"""
import pickle

class Predictor:

    classifier = ''
    vectorizer = ''
    tfidf_transformer = ''

    """The ExpressionEngine mapping to
    the DataHelper categories
    """
    EE_CATEGORY_MAP = {1:5, #Arts
                    3:15, #Beauty
                    4:61, #Business
                    5:52, #Automotive
                    6:62, #Computers
                    7:21, #Electronics
                    8:63, #Education
                    9:7, #Music
                    10:6, #Food
                    11:18, #Gaming
                    12:16, #Health
                    13:20, #Gardening
                    14:64, #Pets
                    15:28, #Parenting
                    16:10, #SocialScience / Humanities
                    17:66, #SocietyAndCulture
                    18:2, #Sports
                    19:11, #Religion
                    20:8} #Politics

    def getEECategoryIdFromInternalid(self, id):
        return self.EE_CATEGORY_MAP[id]

    def getClassifier(self):
        if self.classifier == '':
            pickle_file_path = 'categorizer/yahoo-nb-classifier.pickle'
            with open (pickle_file_path, 'rb') as fp:
                self.classifier = pickle.load(fp)

        return self.classifier

    def getVectorizer(self):
        if self.vectorizer == '':
            pickle_file_path = 'categorizer/yahoo-nb-vectorizer.pickle'
            with open (pickle_file_path, 'rb') as fp:
                self.vectorizer = pickle.load(fp)

        return self.vectorizer

    def getTfidfTransformer(self):
        if self.tfidf_transformer == '':
            pickle_file_path = 'categorizer/yahoo-nb-tfidf.pickle'
            with open (pickle_file_path, 'rb') as fp:
                self.tfidf_transformer = pickle.load(fp)

        return self.tfidf_transformer

    def predictSingle(self, content):
        input_data = [content]
        classifier = self.getClassifier()
        vectorizer = self.getVectorizer()
        tfidf_transformer = self.getTfidfTransformer()

        X_input_termcounts = vectorizer.transform(input_data)
        X_input_tfidf = tfidf_transformer.transform(X_input_termcounts)

        # Predict the output categories
        predicted_categories = classifier.predict(X_input_tfidf)
        return self.getEECategoryIdFromInternalid(predicted_categories[0])
