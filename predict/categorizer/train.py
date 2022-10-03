
from sklearn.datasets import fetch_20newsgroups
from data_helper import DataHelper
import pickle
from timeit import default_timer as timer

start_timer = timer()
# category_map = {'misc.forsale': 'Sales', 'rec.motorcycles': 'Motorcycles'}
# training_data = fetch_20newsgroups(subset='train',
#         categories=category_map.keys(), shuffle=True, random_state=7)

data_obj = DataHelper()
training_data = data_obj.loadTrainData()
end_timer = timer()
print('Data Loaded:,', end_timer - start_timer)

# for key in training_data:
#     print(key)
#
# print(*data_obj._CATEGORY_MAP)
# exit()

# Feature extraction
start_timer = timer()
from sklearn.feature_extraction.text import CountVectorizer

# vectorizer = CountVectorizer(analyzer='word', max_features=5000, stop_words='english', min_df=0.2)
vectorizer = CountVectorizer(min_df=5, max_df=.81)
X_train_termcounts = vectorizer.fit_transform(training_data['data'])
print("Dimensions of training data:", X_train_termcounts.shape)
end_timer = timer()
print('Vectorizing Finished:,', end_timer - start_timer)

# Training a classifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer

input_data = [
    "The curveballs of right handed pitchers tend to curve to the left for batters at the plate",
    "Caesar cipher is an ancient form of encryption",
    "This two-wheeler is really good on slippery roads",
    "I wanna know about computers and mobile phones more than anything",
    "Tacos burgers dessert and cake",
    "The Kentucky product has been showing off new tricks in Vegas, and those skills align completely with David Fizdale’s vision for the team. If any of them carry into the regular season, the Knicks might have just found their second star.",
    "Vincent Willem van Gogh (Dutch: [ˈvɪnsɛnt ˈʋɪləm vɑŋ ˈɣɔx] (About this sound listen);[note 1] 30 March 1853 – 29 July 1890) was a Dutch Post-Impressionist painter who is among the most famous and influential figures in the history of Western art. In just over a decade he created about 2,100 artworks, including around 860 oil paintings, most of them in the last two years of his life. They include landscapes, still lifes, portraits and self-portraits, and are characterised by bold colours and dramatic, impulsive and expressive brushwork that contributed to the foundations of modern art. His suicide at 37 followed years of mental illness and poverty. ",
    "DENVER TOMORROW FOR 4/20. PULL UP TO THE CIVIC CENTER PARK AT 130PM. FREE CONCERT ALL DAY EVENT https://t.co/6pdmlnkVBM",
    "I'm just a soul who's intentions are good, oh lord, please don't let me be misunderstood",
    "Ugh. Can summer just hurry up and be over? It feels like it’s taking forever.",
    """Not OP but I tried one last week that was simple and gave me four weeks of frozen dough. 1kg strong white bread flour 1 tsp fine salt 2x 7g sachets of yeast 1Tbs sugar

Add yeast and sugar to warm water and let sit for few minutes.
(The next part is weird and almost ruined me so need to play with it) Pile the flour and salt onto a clean surface and make a well. In centre of well pour yeasty water. Stir in little bit of flour at a time with fork until all liquid is absorbed then knead for around 10 minutes. Fin. I cut mine into 8 balls (half the half again etc) I also made mistake of thinking I could make a nice base WITHOUT a rolling pin. I could not.

Edit: Literally forgot to write the most important part - after it comes together in the ball pop it in a warm spot for an hour covered with a towel. Pound it down after that and, I've been told, a second rise makes all the difference but I didn't do that.""",
"""Why call them 'russian hackers' after today's indictments? I say phrase it correctly:

The day after Trump asked them to, Russian military intelligence launched unprecedented attacks against Hillary.

Now think about that for a moment, and the difference it makes - a this is a branch of the russian military and it mounted an attack on US systems at Trump's request."""]

start_timer = timer()
# tf-idf transformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_termcounts)
end_timer = timer()
print('Transform Finished:,', end_timer - start_timer)

# Multinomial Naive Bayes classifier
start_timer = timer()
classifier = MultinomialNB(alpha=0).fit(X_train_tfidf, training_data['target'])
print('Accuracy in cv set: %f' % classifier.score(X_train_tfidf, training_data['target']))
pickle_file_path = 'yahoo-nb-classifier.pickle'
with open(pickle_file_path, 'wb') as f:
	pickle.dump(classifier, f)

end_timer = timer()
print('Classification Finished:,', end_timer - start_timer)

pickle_file_path = 'yahoo-nb-vectorizer.pickle'
with open(pickle_file_path, 'wb') as f:
	pickle.dump(vectorizer, f)

pickle_file_path = 'yahoo-nb-tfidf.pickle'
with open(pickle_file_path, 'wb') as f:
	pickle.dump(tfidf_transformer, f)

X_input_termcounts = vectorizer.transform(input_data)
X_input_tfidf = tfidf_transformer.transform(X_input_termcounts)

# Predict the output categories
predicted_categories = classifier.predict(X_input_tfidf)

# Print the outputs
for sentence, category in zip(input_data, predicted_categories):
    print('\nInput:', sentence, '\nPredicted category:', data_obj.convertCategoryId(category))
