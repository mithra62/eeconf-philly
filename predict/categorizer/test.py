import time
import pickle
from data_helper import DataHelper

pickle_file_path = 'yahoo-nb-classifier.pickle'
with open (pickle_file_path, 'rb') as fp:
    classifier = pickle.load(fp)

pickle_file_path = 'yahoo-nb-vectorizer.pickle'
with open (pickle_file_path, 'rb') as fp:
    vectorizer = pickle.load(fp)

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

Now think about that for a moment, and the difference it makes - a this is a branch of the russian military and it mounted an attack on US systems at Trump's request.""",
"""1. If its getting cold and you have tomatoes still ripening on the vine — save your tomatoes! Pull the plants up and bring them inside to a warm dry place. Hang them up, and the tomatoes will ripen on the vine.

2. Companion planting is an excellent way to improve your garden. Some plants replenish nutrients lost by another one, and some combinations effectively keep pests away.

3. Paint the handles of your gardens tools a bright, color other than green to help you find them amongst your plants. You can also keep a mailbox in your garden for easy tool storage.

4. Compost needs time to integrate and stabilize in the soil. Apply two to three weeks prior to planting.

5. There is an easy way to mix compost into your soil without a lot of back breaking work: Spread the compost over your garden in the late fall, after all the harvesting is done. Cover with a winter mulch such as hay or chopped leaves and let nature take its course. By spring, the melting snow and soil organisms will have worked the compost in for you.

If you’re looking for the fastest ticket to a lush garden, start at ground level. Planet Natural offers a large selection of soils and amendments to help you produce healthy, productive plants year after year. Now, let’s grow!

6. Like vining vegetables, but don’t have the room? Train your melons, squash, and cucumbers onto a vertical trellis or fence. Saves space and looks pretty too.

7. Garden vegetables that become over-ripe are an easy target for some pests. Remove them as soon as possible to avoid detection.

8. Onions are ready to harvest when the tops have fallen over. Let the soil dry out, harvest, and store in a warm, dry, dark place until the tops dry. Cut off the foliage down to an inch, then store in a cool, dry area.

9. Keep dirt off lettuce and cabbage leaves when growing by spreading a 1-2 inch layer of mulch (untreated by pesticides or fertilizers) around each plant. This also helps keep the weeds down.

10. When planting a flower or vegetable transplant, deposit a handful of compost into each hole. Compost will provide transplants with an extra boost that lasts throughout the growing season.

11. Insects can’t stand plants such as garlic, onions, chives and chrysanthemums. Grow these plants around the garden to help repel insects.

12. Milk jugs, soda bottles and other plastic containers make great mini-covers to place over your plants and protect them from frost.

13. For easy peas, start them indoors. The germination rate is far better, and the seedlings will be healthier and better able to fight off pests and disease.

14. Healthy soil means healthy plants that are better able to resist pests and disease, reducing the need for harmful pesticides.""",
" On this mountain he will destroy the shroud that enfolds all peoples, the sheet that covers all nations; 8 he will swallow up death forever. The Sovereign LORD will wipe away the tears from all faces; he will remove his people’s disgrace from all the earth. The LORD has spoken. "]

pickle_file_path = 'yahoo-nb-tfidf.pickle'
with open (pickle_file_path, 'rb') as fp:
    tfidf_transformer = pickle.load(fp)

X_input_termcounts = vectorizer.transform(input_data)
X_input_tfidf = tfidf_transformer.transform(X_input_termcounts)

# Predict the output categories
predicted_categories = classifier.predict(X_input_tfidf)

# Print the outputs
data_obj = DataHelper()
for sentence, category in zip(input_data, predicted_categories):
    print('\nInput:', sentence, category, '\nPredicted category:', data_obj.convertCategoryId(category))
