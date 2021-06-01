import re
import urllib.request as urllib2
from lxml import html
import requests
from django.shortcuts import render
# our home page view
def home(request):
    return render(request, 'index.html')

# custom method for generating predictions
def getPredictions(pclass):

    #https://en.wikipedia.org/wiki/Virat_kohli
    page = requests.get(pclass)
    tree = html.fromstring(page.content)

    words = (tree[1].text_content()).lower().split()
    #I have not removed stopwords from the string
    #With NLTK it is not much difficult task and we can use it for this purpose

    #words
    uniques = []
    for word in words:
      if word not in uniques:
        uniques.append(word)

    # Make a list of (count, unique) tuples.
    counts = []
    for unique in uniques:
      count = 0              # Initialize the count to zero.
      for word in words:     # Iterate over the words.
        if word == unique:   # Coomparing with already existing word
          count += 1         # If so, increment the count
      counts.append((count, unique))

    counts.sort()            # Sorting the list.
    counts.reverse()         # Reverse it, putting the highest counts first.
    # Printing the ten words with the highest counts.
    k = {}
# Printing the ten words with the highest counts.
    for i in range(min(10, len(counts))):
      count, word = counts[i]
      #print('%s %d' % (word, count))
      k[word] = count

    return k
# our result page view

def result(request):

    pclass = request.GET['pclass']
    regex = ("^https?\:\/\/([\w\.]+)wikipedia.org\/wiki\/([\w]+\_?)+")
    # Compile the ReGex
    p = re.compile(regex)

    #https://en.wikipedia.org/wiki/Virat_kohli
    if(re.search(p, pclass)):
        result = getPredictions(pclass)
        return render(request, 'result.html', {'result': result})
    else:
        return render(request, 'index.html', {'newerror': "Please enter valid URL"})

