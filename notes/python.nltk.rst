================================================================================
Python Natural Language Toolkit
================================================================================

--------------------------------------------------------------------------------
Preface
--------------------------------------------------------------------------------

What follows is a quick summary of the tools available in the `nltk` library:

* **Accessing Corpora** : `corpus`
  Provides standardized interfaces to corpora and lexicons.

* **String processing** : `tokenize`, `stem`
  Provivdes tokenizers, sentence tokenizers, stemmers

* **Collocation Discovery** : `collocations`
  Provides t-test, chi-squared, point-wise mutual information

* **Part-of-Speech Tagging** : `tag`
  Provides n-gram, backoff, Brill, HMM, TnT

* **Machine Learning** : `classify`, `cluster`, `tbl`
  Provides decision tree, maximum entropy, naive Bayes, EM, k-means

* **Chunking** : `chunk`
  Provides regular expression, n-gram, named-entity

* **Parsing** : `parse`, `ccg`
  Provides chart, feature-based, unification, probabilistic, dependency

* **Semantic Interpretation** : `sem`, `inference`
  Provides lambda calculus, first-order logic, model checking

* **Evaluation Metrics** : `metrics`
  Provides precision, recall, agreement coefficients

* **Probability and Estimation** : `probability`
  Provides frequency distributions, smoothed probability distributions

* **Applications** : `app`, `chat`
  Provides graphical concordancer, parsers, WordNet browser, chatbots

* **Linguistic Fieldwork** : `toolbox`
  Provides manipulate data in SIL Toolbox format

--------------------------------------------------------------------------------
Chapter 1: Language Processing and Python
--------------------------------------------------------------------------------

Most of the first chapter is a quick ramp up on python by using some sample
datasets from the nltk package. What follows is a summary of some useful
utilities:

.. code-block:: python

    from nltk.book import *    # import the book examples
    from __future__ import division # use float division
    from __future__ import print # use the print function

    text = text6               # monty python and the holy grail
    text.concordance('taunt')  # find every mention of a work with some context
    text.similar('swallow')    # find words used in a similar context
    text.common_contexts(['swallow', 'plover']) # find a common context for the given words
    text.dispersion_plot(['swallow']) # shows locations of words in the text
    text.generate()            # generate random text in the style of the text sample

    len(text)                  # length of types in the text
    len(set(text))a            # length of unique types (words, punctuation, spelling)
    len(set(text)) / len(text) # richness of the text
    text.count('and')          # number of times that word is used in the text
    100 * text.count('a') / len(text) # percent of the text that is that word

    dist = FreqDist(text6)     # frequency distribution of MPATHG
    dist.most_common(10)       # the 10 most common words
    dist.plot(50, cumulative=True) # plot a cumulative frequeny of the 50 most common types
    dist.hapaxes()             # words that only occur once in the text

    words = set(text)
    longs = [w for w in words if len(w) > 12] # print all the long words in a text
    goods = [w for w in words if len(2) > 7 and dist[w] > 7]

    grams = bigrams(sent6)      # produce all the bigrams in sent6
    text.collocations()         # produce all the common bigrams in the text

    lens = FreqDist(len(w) for w in text) # distribution of word lengths
    lens.freq(13)               # the frequency of long words
    lens.N()                    # the total number of samples

    words = { w for w in text if w.isalpha() } # remove numbers and punctuation

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Common Natural Language Problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What follows are a collection of problems in natural language processing:

* **word sense disambiguation**
  Attempt to understand which sense of a word was intended in a given context.

* **pronoun resolution**
  Answer the questions "who did what to whom." More concretely, what are the
  subjects and objects of verbs. Techniques for doing this include: anaphora
  resolution (identifying which noun a pronoun refers to) and semantic role labeling
  (identifying how a noun phrase refers to a verb).

* **generating language output**
  Being able to answer questions and perform machine translation.

* **machine translation**
  Automatic translation of text to and from other languages.

* **spoken dialog systems**
  Automated systems that can answer simple or complex questions using speech as the
  input and output.

.. image:: http://www.nltk.org/images/dialogue.png
   :target: http://www.nltk.org/images/dialogue.png
   :align: center

* **textual entailment**
  Can we merge various pieces of text to create expert or knowlege systems?

--------------------------------------------------------------------------------
Chapter 2: Accessing Text Corpora
--------------------------------------------------------------------------------

To assist in testing natural language systems, `nltk` includes a number of text
corpora that is easily usable. What follows is only a quick survey of some of
the datasets, but there are many more:

.. code-block:: python

    from nltk.corpus import gutenberg

    gutenberg.fileids()         # a collection of the available files
    emma = gutenberg.words('austen-emma.txt') # get the words from emma
    emma.concordance('suprise') # performing some common operations

    from nltk.corpus import webtext   # a collection of web extracted text
    from nltk.corpus import nps_chat  # age based chat room conversation
    from nltk.corpus import brown     # brown collection of english by genre
    from nltk.corpus import reuters   # test / train set of 90 genres of news
    from nltk.corpus import inaugural # many years of inaugural addresses
    from nltk.corpus import indian    # nltk includes a number of languages as well
    from nltk.corpus import cmudict   # pronunciation guide for synthesizers
    from nltk.corpus import swadesh   # 200 common words in a number of languages
    from nltk.corpus import toolbox   # a massive textual resource
    from nltk.corpus import wordnet   # a hierarchical word mapping
    from nltk.corpus import verbnet   # the same but for verbs

    brown.categories()               # the list of categories
    brown.sents(categories="news")   # the sentences of the news category
    brown.words(categories=["news", "lore"])

Here are some quick examples of using the corpus for quick examination:

.. code-block:: python

    # look at word distributions of various news generes
    dist  = FreqDist(w.lower() for w in brown.words(categories="news"))
    words = ["who", "what", "where", "when", "why"]
    for word in words:
        print "{}\t{}".format(word, dist[word])

    # a quick way to do this for all the brown categories
    dist = nltk.ConditionalFreqDist((category, word)
      for category in brown.categories()
      for word in brown.words(categories=category))
    genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
    modals = ['can', 'could', 'may', 'might', 'must', 'will']
    dist.tabulate(conditions=genres, samples=modals)

    # plot word use over time with the inaugural corpus
    dist = nltk.ConditionalFreqDist((target, fileid[:4]) # year
        for fileid in inaugural.fileids()
        for word in inaugural.words(fileid)
        for target in ['america', 'citizen']
        if word.lower().startswith(target))
    dist.plot()
    dist.tabulate()

What follows is a quick example to print out the average word length, average
sentence length and lexical diversity of each file in the gutenberg set:

.. code-block:: python

    from nltk.corpus import gutenberg

    for fileid in gutenberg.fileids():
        num_chars = len(gutenberg.raw(fileid))
        num_words = len(gutenberg.words(fileid))
        num_sents = len(gutenberg.sents(fileid))
        num_vocab = len(set(w.lower()) for w in gutenberg.words(fileid))
        print(round(num_chars / num_words), round(num_words / num_sents), rount(num_words / num_vocab), fileid)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Common Corpus Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most corpus expose their functionality through the following common methods.
More information can be found by `help(nltk.corpus.reader)`:

.. code-block:: python

    fileids()                  # the files of the corpus
    fileids([categories])      # the files of the corpus corresponding to these categories
    categories()               # the categories of the corpus
    categories([fileids])      # the categories of the corpus corresponding to these files
    raw()                      # the raw content of the corpus
    raw(fileids=[f1,f2,f3])    # the raw content of the specified files
    raw(categories=[c1,c2])    # the raw content of the specified categories
    words()                    # the words of the whole corpus
    words(fileids=[f1,f2,f3])  # the words of the specified fileids
    words(categories=[c1,c2])  # the words of the specified categories
    sents()                    # the sentences of the whole corpus
    sents(fileids=[f1,f2,f3])  # the sentences of the specified fileids
    sents(categories=[c1,c2])  # the sentences of the specified categories
    abspath(fileid)            # the location of the given file on disk
    encoding(fileid)           # the encoding of the file (if known)
    open(fileid)               # open a stream for reading the given corpus file
    root                       # if the path to the root of locally installed corpus
    readme()                   # the contents of the README file of the corpus

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Writing Your Own Corpus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create your own corpus of text files, use the provided `PlainTextCorpusReader`:

.. code-block:: python

    from nltk.corpus import PlaintextCorpusReader

    path_root = "/usr/share/dict"
    reader = PlainTextCorpusReader(path_root, '.*')
    reader.fileids()      # all the available files
    reader.words('words') # read an available file

The `BracketParseCorpusReader` can be used to read parenthesis delimited parse
trees, for example the `Penn Treebank` collection.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Text Generation with Bigrams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can build a frequency distribution that can be used to predict the best
next word given the previous:

.. code-block:: python

    def generate_sentence(model, word, size=15):
        for i in range(10):
            yield word
            word = model[word].max()

    text = nltk.corpus.genesis.words('english-kjv.txt')
    bigrams = nltk.bigrams(text)
    model = nltk.ConditionalFreqDist(bigrams)
    print ' '.join(generate_sentence(model, 'living'))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Wordlist Corpora
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`nltk` includes some resources that are just wordlists. These can be used for
example to find unusual or misspelled words:

.. code-block:: python

    def unusual_words(text):
        ''' Find potentially mis-spelt words or unique words from
        a given piece of text.

        :param text: The text to examine the words in
        :returns: A sorted list of unusual words
        '''
        words   = set(w.lower() for w in text if w.isalpha())
        checks  = set(w.lower() for w in nltk.corpus.words.words())
        unusual = words - checks
        return sorted(unusual)

    unusual_words(nltk.corpus.nps_chat.words())

Another helpful collection is of stopwords for a number of languages:

.. code-block:: python

    def content_fraction(text):
        ''' Computes the percentage of actual content in a piece of
        text after removing the stopwords.

        :param text: The text to examine
        :returns: The percentage of content
        '''
        stopwords = nltk.corpus.stopwords.words('english')
        content   = [w for w in text if not in stopwords]
        return len(content) / len(text)

    content_fraction(nltk.corpus.reuters.words())

Here is an example of using the wordlist to solve a simple puzzle game:

.. code-block:: python

    puzzle_letters = nltk.FreqDist('egivrvonl')
    required = 'r'
    wordlist = nltk.corpus.words.words()
    results  = [w for w in wordlist if len(w) >= 4
      and required in w
      and nltk.FreqDict(w) <= puzzle_letters]

Here is an example of finding common male and female names from the names corpus:

.. code-block:: python

    names = nltk.corpus.names
    male_names   = set(names.words('male.txt'))
    female_names = set(names.words('female.txt'))
    common_names = male_names.intersection(female_names)

Here is an example of plotting names based on the last letter of the name:

.. code-block:: python

    dist = nltk.ConditionFreqDist((fileid, name[-1])
        for fileid in nltk.corpus.names.fileids()
        for name in nltk.corpus.names.words(fileid))
    dist.plot()
    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pronunciation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can use the `cmudict` dataset to work with english pronuncitation for tasks
like finding rhyming words:

.. code-block:: python

    entries  = nltk.corpus.cmudict.entries()
    syllable = ['N', 'IH0', 'K', 'S']
    rhymes   = [word for word, pron in entries if pron[-4:] == syllable]

We can also use it to find interesting ways in which the English language
manipulates its various letters (this format is discussed more at
http://en.wikipedia.org/wiki/Arpabet):

.. code-block:: python

    [w for w, pron in entries if pron[-1] == 'M' and w[-1] == 'n'] # slient n
    [w for w, pron in entries if pron[0]  == 'N' and w[0]  != 'n'] # slient fist letter

    def stress(pron):
        return [char for phone in pron for char in phone if char.isdigit()]

    def match_stress(source, match):
        return [word for word, pron in source if stress(pron) == match]

    match_stress(entries, ['0', '1', '0', '2', '0'])
    match_stress(entries, ['0', '2', '0', '1', '0'])

We can extend this to find all kinds of similar sounding words. The following
finds all words starting with `p` that have three syllables:

.. code-block:: python

    p_words = [("%s-%s" % (pron[0], pron[2]), word)
        for word, pron in entries
        if len(pron) == 3 and pron[0] == 'P']
    dist = nltk.ConditionalFreqDist(p_words)

    for template in sorted(dist.conditions()):
        if len(dist[template]) > 10:
            words = sorted(dist[template])
            all_words = ' '.join(words)
            print "{}\t{}...".format(template, all_words[:70])
            print 

Finally here is an example of a system that would be fed into a text to speech
program:

.. code-block:: python

    def text_to_speech(words):
        ''' Given a collection of words, return the list of phonemes
        that must be uttered by a text to speech program.

        :param words: The words to convert to phonemes
        :returns: The list of phonemes for the words
        '''
        sayings = nltk.corpus.cmudict.dict()
        return [ph for w in words for ph in sayings[word][0]]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Comparitive Wordlists
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can use the `swadesh` wordlist to compare common words in different langauges
and even make simple translation systems:

.. code-block::

    french_to_english = nltk.corpus.swadesa.entriesh(('fr', 'en'))
    translate = dict(french_to_english)
    print translate['chien']

    languages = ['en', 'de', 'nl', 'es', 'fr', 'pt', 'la']
    for i in [139, 140, 141, 142]:
        print(swadesh.entries(languages)[i])

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Wordnet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The wordnet database gives us a rich collection of synonyms and word senses:

.. code-block:: python

    from nltk.corpus import wordnet as wn

    wn.synsets('motocar')   # [Synset('car.n.01')] noun sense of car
    wn.synset('car.n.01').lemma_names  # all the lemma names
    wn.synset('car.n.01').definition   # the defintion of this sense
    wn.synset('car.n.01').examples     # a common example for all lemmas
    wn.synset('car.n.01').lemmas       # all the matching lemmas to this set

    for synset in wn.synsets('car'):
        print synset.lemma_names       # all the sense of the word car

We can also explore the hierarchy of more specific hyponyms:

.. code-block:: python

    motorcar = wn.synset('car.n.01')
    types_of_motorcar = motorcar.hyponyms() # down the hierarchy
    trees_of_motorcar = motocar.hypernyms() # up the hierarchy
    roots_of_motorcar = motocar.root_hypernyms() # the root of the hierarchy
    sorted(lemma.name for synset in types_of_motorcar for lemma in synset.lemmas)
    paths_of_motorcar = motocar.hypernym_paths() # up the hierarchy

    [synset.name() for synset in paths[0]] # walk the path one way
    [synset.name() for synset in paths[1]] # walk the path another way

Hypernyms and hyponyms are called lexical relations because they relate one synset
to another. These two relations navigate up and down the "is-a" hierarchy. Another
important way to navigate the network is from items to their components (meronyms)
or to the things they are contained in (holonyms). For example, the parts of a tree
are its trunk, crown, and so on; the `part_meronyms`. The substance a tree is made
of includes heartwood and sapwood; the `substance_meronyms`. A collection of trees
forms a forest; the `member_holonyms`:

.. code-block:: python

    wn.synset('tree.n.01').part_meronyms()
    wn.synset('tree.n.01').substance_meronyms()
    wn.synset('tree.n.01').member_holonyms()

There are also relationships between verbs. For example, the act of walking involves
the act of stepping, so walking entails stepping:

.. code-block:: python

    wn.synset('walk.v.01').entailments()
    wn.synset('eat.v.01').entailments()
    wn.synset('tease.v.03').entailments()

    wn.lemma('supply.n.02.supply').antonyms()  # see the antonym lemmas of a word
    dir(wn.synset('harmony.n.02'))             # see all the lexical relations of a word


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Semantic Similarity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can ues the wordnet hierarchy to find words that have a similar meaning. The
deaper down the graph words match, the tigher they are related:

.. code-block:: python

    right    = wn.synset('right_whale.n.01')
    orca     = wn.synset('orca.n.01')
    minke    = wn.synset('minke_whale.n.01')
    tortoise = wn.synset('tortoise.n.01')
    novel    = wn.synset('novel.n.01')

    right.lowest_common_hypernyms(minke)[0].min_depth()    # both same genus whales
    right.lowest_common_hypernyms(orca)[0].min_depth()     # both whales
    right.lowest_common_hypernyms(tortoise)[0].min_depth() # both animals
    right.lowest_common_hypernyms(novel)[0].min_depth()    # both objects

    right.path_similarity(orca)  # score between 0..1 of how similar
    right.path_similarity(right) # comparison with oneself is always 1

--------------------------------------------------------------------------------
Chapter 3: Processing Raw Text
--------------------------------------------------------------------------------

If we need to use our own text sources, we can use the tools offered by `nltk`
to work with them directly. It should be noted that a number of texts include
headers, line numbers, or other artifacts that we would like to remove. Although
there is no automatic way to remove all of these elements, a little manual work
or simple python should make this a quick task:

.. code-block:: python

    from nltk import word_tokenize
    from urllib import request

    url = "http://www.gutenberg.org/files/2554/2554.txt"
    response = request.urlopen(url)
    raw_text = response.read().decode('utf8')
    tokens = word_tokenize(raw_text)
    text = nltk.Text(tokens)

If you are pulling data from a web page, you can remove some of the HTML with
`BeautifulSoup`:

.. code-block:: python

    from bs4 import BeautifulSoup

    url      = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    html     = request.urlopen(url).read().decode('utf8')
    # there is also nltk.clean_html(html)
    raw_text = BeautifulSoup(html).get_text()
    tokens   = word_tokenize(raw_text[start:end])
    text     = nltk.Text(tokens)
    text.concordance('gene')

We can also parse rss or atom feeds using the universal feed parser:

.. code-block:: python

    # -*- coding: utf8 -*-
    import feedparser

    feed = feedparser.parse("http://languagelog.ldc.upenn.edu/nll/?feed=atom")
    feed['feed']['title']

`nltk` includes a regex engine that makes it easy to tokenize text using the `<match>`
operator:

.. code-block:: python

    from nltk.corpus import gutenberg, nps_chat
    moby = nltk.Text(gutenberg.words('melville-moby_dick.txt'))
    moby.findall(r"<a> (<.*>) <man>")

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Normalizing Text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If we want to be able to search for text in a well defined way, a good processing
step for text is to stem it (use the porter stemmer for a general search system):

.. code-block:: python

    import nltk

    raw_text = nltk.corpus.gutenberg.raw('melville-moby_dick.txt')
    tokens   = nltk.word_tokenize(raw_text)

    porter    = nltk.PorterStemmer()
    lancaster = nltk.LancasterStemmer()

    [(token, lancaster.stem(token)) in tokens]
    [(token, porter.stem(token)) in tokens]

What follows is a simple text indexer that can be used to search a corpus:

.. code-block:: python

    import ntlk

    class Indexer(object):

        def __init__(self, text, stemmer=None):
            self.text = text
            self.stemmer = stemmer or nltk.PorterStemmer()
            self.index = nltk.Index((self.stemmer.stem(word), index)
                for index, word in enumerate(text))

        def search(self, word, width=40):
            token = self.stemmer.stem(word)
            count = int(width / 4.0)
            for index in self.index[token]:
                lcontext = ' '.join(self.text[index-count:index])
                rcontext = ' '.join(self.text[index:index+count])
                ldisplay = '{:>{width}}'.format(lcontext[-width:], width=width)
                rdisplay = '{:{width}}'.format(rcontext[:width], width=width)
                print (ldisplay, rdisplay)

       tokens = nltk.corpus.webtext.words('grail.txt')
       index  = IndexedText(tokens)
       index.search('lie')

The wordnet lemmatizer only removes affixes if the word is in its dictionary, as
such it is a bit slower, but more precise. It is a good choice if you want to 
build a vocabulary of a given text:

.. code-block:: python

    import nltk

    lemma = nltk.WordNetLemmatizer()
    [lemma.lemmatize(token) for token in tokens]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tokenizing Text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nltk proivdes a regular expression tokenizer that be be plugged with various
regular expressions:

.. code-block:: python

    import re

    re.split(r'[ \t\n]+', raw_text)   # split on whitespace
    re.split(r'\W+', raw_text)        # split on all whitespace
    re.findall('\w+|\S\w*', raw_text) # split by finding all words

    pattern = r'''(?x)    # set flag to allow verbose regexps
        ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
      | \w+(-\w+)*        # words with optional internal hyphens
      | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
      | \.\.\.            # ellipsis
      | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
    '''
    nltk.regexp_tokenize(raw_text, pattern)

However, creating a custom tokenizer is complicated and hard to get perfect. The
best method is to train on a raw text that has already been tokenized. nltk provides
the treebank dataset that can help with this purpose. Another thing to think about is
normalizing contractions (either by spliting into common tokens like "did" "n't" or
by replacing the words with a lookup table into "did" "not"):

.. code-block:: python

    import nltk

    nltk.corpus.treebank_raw.raw() # the original raw text
    nltk.corpus.treebank.words()   # the tokenized set of words


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Segmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generally before we tokenize a text into words, we would first tokenize it into
sentences. The nltk toolkit supplies the *Punkt* sentence segmenter for this
purpose (this is generally hard because periods are used for abbreviations and
other uses):

.. code-block:: python

    import nltk

    raw_text = nltk.corpus.gutenberg.raw('chesterton-thursday.txt')
    nltk.sent_tokenize(raw_text)

Say we have a stream of letters and need to represent segmentation of sentences
and words, here is a simple technique:

.. code-block:: python

    text = "doyouseethekittyseethedoggydoyoulikethekittylikethedoggy" # run on letters
    seg1 = "0000000000000001000000000010000000000000000100000000000"  # sentences
    seg2 = "0100100100100001001001000010100100010010000100010010000"  # words

    def segment(text, segments):
        ''' Given a piece of run on text and a segmentation list
        where a '0' indicates a letter in a word and '1' represents
        the last letter in a word, return the words in the sentence.

        :param text: The run on text
        :param segments: The segments to split on
        '''
        index = 0
        words = []
        for i in range(len(segments)):
            if segments[i] == '1':
                words.append(text[index:i + 1])
                index = i + 1
        words.append(text[index:])
        return words

    segment(text, seg1)
    segment(text, seg2)

    def evaluate(text, segments):
        ''' evaluates an objective function on the supplied
        segmentation of the given text. Smaller scores are better.

        :param text: The raw text to segment
        :param segments: A possible segmentation
        :returns: The resulting score for this segmentation
        '''
        words = segment(text, segments)
        text_size = len(words)
        lexicon_size = sum(len(word) + 1 for word in set(words))
        return text_size + lexicon_size

    evaluate(text, seg1)
    evaluate(text, seg2)

We can use these utilities and a quick simulated annealing implementation to search
for trivial segmentations:

.. code-block:: python

    from random import randint

    def flip(segments, pos):
        return segments[:pos] + str(1 - int(segments[pos])) + segments[pos+1:]

    def flip_n(segments, n):
        for i in range(n):
            segments = flip(segments, randint(0, len(segments) - 1))
        return segments

    def simulated_annealing(text, segments, iterations=5000, cooling_rate=1.5):
        temperature = float(len(segments))
        while temperature > 0.5:
            best_segments, best = segments, evaluate(text, segments)
            for i in range(iterations):
                guess = flip_n(segments, int(temperature + 0.5))
                score = evaluate(text, guess)
                if score < best:
                    best, best_segments = score, guess
            score, segments = best, best_segments
            temperature = temperature / cooling_rate
            print "%d:\t%s" % (evaluate(text, segments), segment(text, segments))
        return segments

The rest of the chapter focuses on text formatting, but it also mentions this handy utility:

.. code-block:: python

    from textwrap import fill

    text = ' '.join(str(n) for n in range(500))
    wrapped = fill(text, width=80)
    print(wrapped)

--------------------------------------------------------------------------------
Chapter 4: Python Review
--------------------------------------------------------------------------------

This chapter is mostly a python review, although it also includes a few summaries
of programming techniques and python libraries:

.. code-block:: python
    
    import networkx as nx
    import matplotlib
    from nltk.corpus import wordnet as wn
    
    def traverse(graph, start, node):
        graph.depth[node.name] = node.shortest_path_distance(start)
        for child in node.hyponyms():
            graph.add_edge(node.name, child.name) [1]
            traverse(graph, start, child) [2]
    
    def hyponym_graph(start):
        G = nx.Graph() [3]
        G.depth = {}
        traverse(G, start, start)
        return G
    
    def graph_draw(graph):
        nx.draw_graphviz(graph,
             node_size = [16 * graph.degree(n) for n in graph],
             node_color = [graph.depth[n] for n in graph],
             with_labels = False)
        matplotlib.pyplot.show()
        
    dog = wn.synset('dog.n.01')
    graph = hyponym_graph(dog)
    graph_draw(graph)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gematria Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    letter_values = {
        'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':80, 'g':3, 'h':8,
        'i':10, 'j':10, 'k':20, 'l':30, 'm':40, 'n':50, 'o':70, 'p':80, 'q':100,
        'r':200, 's':300, 't':400, 'u':6, 'v':6, 'w':800, 'x':60, 'y':10, 'z':7
    }

    def gematria(word, values=letter_values):
        return sum(values.get(char, 0) for char in  word.lower())

    def gematria_words(words):
        return [gematria(word) for word in words]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Soundex Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python

    def soundex(word):
        '''
        http://en.wikipedia.org/wiki/Soundex

        :param word: The word to get the soundex encoding for
        :returns: The soundex encoding for that word
        '''
        vowels = set('aeiouy')
        ignore = set('aeiouyhw')
        lookup = {
            'b': '1', 'f': '1', 'p': '1', 'v': '1',
            'c': '2', 'g': '2', 'j': '2', 'k': '2', 'q': '2', 's': '2', 'x': '2', 'z': '2',
            'd': '3', 't': '3',
            'l': '4',
            'm': '5', 'n': '5',
            'r': '6',
        }
        prev = None
        result = word[0].upper()
        for char in word.lower()[1:]:
            if char not in ignore:
                value = lookup.get(char, None)
                if not value: continue # we don't know these characters
                if result[-1] != value or prev in vowels:
                    result = result + value
            prev = char
        result = result[:4] + ('0' * (4 - len(result)))
        return result

    def soundex_words(words):
        return [soundex(word) for word in words]

    def build_soundex_dictionary(words):
        ''' Create a dictionary of how english words sound and
        can be used as a spelling checker.

        :param words: The words to build a dictionary for
        :returns: A lookup dictionary of matching words
        '''
        lookup = {}
        for word in words:
            value = soundex(word)
            lookup.setdefault(value, []).append(word)
        return lookup

    class SoundexSpellCheck(object):

        def __init__(self, words):
            self.lookup = build_soundex_dictionary(words)

        def correct(self, word):
            return self.lookup.get(soundex(word), [])

.. todo:: http://en.wikipedia.org/wiki/Metaphone

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Statistically Improbable Phrase
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: http://en.wikipedia.org/wiki/Statistically_Improbable_Phrases


--------------------------------------------------------------------------------
Chapter 5: Categorizing and Tagging Words
--------------------------------------------------------------------------------

.. todo:: http://www.nltk.org/book/ch05.html
