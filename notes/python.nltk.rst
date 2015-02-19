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

    import warnings
    warnings.filterwarnings("ignore")

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

.. image:: images/nltk-pipeline.png
   :target: http://www.nltk.org/book/ch01.html
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

`nltk` makes it easy to computer the parts of speech of a given block of text:

.. code-block:: python

    text  = "And now for something completely different"
    words = nltk.word_tokenize(text)
    parts = nltk.pos_tag(words)

    nltk.help.upenn_tagset('RB')   # get documentation for a part of speech
    nltk.help.upenn_tagset('NN.*') # get documentation for a regex part of speech

To find words that are used similar to the supplied word, do the following(
this finds the supplied word, all its contexts, and finds words that are used
in similar contexts):

.. code-block:: python

    text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
    text.similar('woman')

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Representing Tagged Corpora
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`nltk` represents a tagged token as a tuple of the word and the part of speech.
There are utility functions that can make this easier to work with:

.. code-block:: python

   tagged_token = nltk.tag.str2tuple('fly/NN') # (fly, NN)
   sentence = '''
   The/AT grand/JJ jury/NN commented/VBD on/IN a/AT number/NN of/IN
   other/AP topics/NNS ,/, AMONG/IN them/PPO the/AT Atlanta/NP and/CC
   Fulton/NP-tl County/NN-tl purchasing/VBG departments/NNS which/WDT it/PPS
   said/VBD ``/`` ARE/BER well/QL operated/VBN and/CC follow/VB generally/RB
   accepted/VBN practices/NNS which/WDT inure/VB to/IN the/AT best/JJT
   interest/NN of/IN both/ABX governments/NNS ''/'' ./.
   '''
   [nltk.tag.str2tuple(token) for token in sentence.split()]

There are also helper functions for working with already token tagged corpora:

.. code-block:: python

    nltk.corpus.brown.tagged_words()                   # read the text as tagged words
    nltk.corpus.brown.tagged_words(tagset='universal') # use the universal POS token

    nltk.corpus.sinica_treebank.tagged_words()         # Chinese
    nltk.corpus.indian.tagged_words()                  # Hindi
    nltk.corpus.mac_morpho.tagged_words()              # Dutch
    nltk.corpus.conll2002.tagged_words()               # Portuguese
    nltk.corpus.cess_cat.tagged_words()                # Spanish

We can check a text to see which parts of speech are the most common:

.. code-block:: python

    from nltk.corpus import brown
    brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
    tag_dist = nltk.FreqDist(tag for (word, tag) in brown_news_tagged)
    tag_dist.most_common()

    nltk.app.concordance() # can be used to explore a text

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parts of Speech
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here are some ways to see how a given text uses various parts of speech. First,
which parts of speech occur the most before nouns:

.. code-block:: python

    brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
    word_tag_pairs = nltk.bigrams(brown_news_tagged)
    noun_preceders = [a[1] for (a, b) in word_tag_pairs if b[1] == 'NOUN']
    dist = nltk.FreqDist(noun_preceders)
    [tag for (tag, _) in dist.most_common()]

What about the most common verbs in a given piece of text:

.. code-block:: python

    brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
    dist  = nltk.FreqDist(brown_news_tagged)
    verbs = [token[0] for (token, _) in dist.most_common() if token[1] == "VERB"]

    # or conditionally based on the part of speech
    dist = nltk.ConditionalFreqDist(brown_news_tagged)
    dist['cut'].most_common()

    # or see the most common word given a part of speech
    words = ((tag, word) for (word, tag) in brown_news_tagged)
    dist  = nltk.ConditionalFreqDist(words)
    verbs = list(dist['VBN'])

    # to find words that can be used in multiple parts of speech
    verbs = [word for word in dist.conditions() if 'VBD' in dist[w] and 'VBN' in dist[w]]
    index = brown_news_tagged.index(('kicked', 'VBD'))
    nears = brown_next_tagged[index - 4:index + 1]

If we have a collection of the most common verbs, what are the most common words before
each verb:

.. code-block:: python

    def get_words_before(tagged, words, pos='VB'):
        for index, (word, tag) in enumerate(tagged):
            if tag == pos and word in words:
                yield tagged[index-1]

    verbs = set(dist['VB'])
    words = nltk.FreqDist(get_words_before(brown_tagged_words, verbs, pos='VB'))
    #print words.most_common()

What about all verb pairs that meet the form "<verb> to <verb.":

.. code-block:: python

    import nltk

    def verb_to_verb(sentences):
        for (w1, t1), (w2, t2), (w3, t3) in nltk.trigrams(sentences):
            if t1.startswith('V') and t2 == 'TO' and t3.startswith('V'):
                yield w1, w2, w3

    verbs = verb_to_verb(nltk.corpus.brown.tagged_sents())

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A quick summary of python dictionaries and an example of how to parse a text and
limit it to a simple vocabulary (replace unknown words with UNK):

.. code-block:: python

    import nltk
    from collections import defaultdict

    alice  = nltk.corpus.gutenberg.words('carroll-alice.txt')
    vocab  = nltk.FreqDist(alice)
    common = { word: word for (word, _) in vocab.most_common(1000) }
    mapper = defaultdict(lambda: 'UNK', common)
    alice2 = [mapper[word] for word in alice]
    len(set(alice2))

It also shows a quick way to recreate the FreqDist utility:

.. code-block:: python

    import nltk
    from collections import defaultdict
    from operator import itemgetter

    counts = defaultdict(int)
    for word, tag in nltk.corpus.brown.tagged_words():
        counts[tag] += 1

    print counts['NOUN']
    print sorted(counts)
    print sorted(counts.items(), key=itemgetter(1), reverse=True)

Or index words by their last two letters:

.. code-block:: python

    import nltk
    from collections import defaultdict

    last_letters = defaultdict(list)
    for word in nltk.corpus.words.words('en'):
        last_letters[word[-2:]].append(word)

    print last_letters['ly']
    print last_letters['zy']

Or an anagram dictionary:

.. code-block:: python

    import nltk
    from collections import defaultdict

    anagrams = defaultdict(list)
    for word in nltk.corpus.words.words('en'):
        key = ''.join(sorted(word))
        anagrams[key].append(word)

    # nltk acctually provides a utility for this common task
    anagrams = nltk.Index((''.join(sorted(word)), word) for word in words)
    print anagrams['dgo']

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Complex Keys and Values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say we wanted to create a lookup table so that given a word and the previous
part of speech, we can choose its part of speech:

.. code-block:: python

    parts_of_speech = defaultdict(lambda: defaultdict(int))
    brown_news_tagged = brown.tagged_words(categories='news', tagset='universal')
    for ((w1, t1), (w2, t2)) in nltk.bigrams(brown_news_tagged):
        parts_of_speech[(t1, w2)][t2] += 1
    parts_of_speech[('DET', 'right')] # then choose the POS with the most hits
    words_of_speech = nltk.Index((value, key) for (key, value) in parts_of_speech.items())

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parts of Speech Tagging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now we will make a system that will automatically tag the POS of a word given
its context within a sentence. What follows is the common setup for the remaining
exmaples:

.. code-block:: python

    import nltk
    from nltk.corpus import brown

    brown_tagged_sents = brown.tagged_sents(categories='news')
    brown_tagged_words = brown.tagged_words(categories='news')
    brown_sents = brown.sents(categories='news')

The default tagger is one that simply chooses the most common tag from a sample.
This is useful as a baseline for improving our tagger:

.. code-block:: python

    tags = [tag for word, tag in brown_tagged_words]
    base = nltk.FreqDist(tags).max() # 'NN'

    text   = 'I do not like green eggs and ham, I do not like them Sam I am!'
    tokens = nltk.word_tokenize(text)
    default_tagger = nltk.DefaultTagger(base)
    default_tagger.tag(tokens)
    default_tagger.evaluate(brown_tagged_sents) # performs rather poorly

The next tagger we can use is the regex tagger which assigns tags rather naively
to words matthing regex patterns:

.. code-block:: python

    patterns = [
        (r'.*ing$', 'VBG'),               # gerunds
        (r'.*ed$', 'VBD'),                # simple past
        (r'.*es$', 'VBZ'),                # 3rd singular present
        (r'.*ould$', 'MD'),               # modals
        (r'.*\'s$', 'NN$'),               # possessive nouns
        (r'.*s$', 'NNS'),                 # plural nouns
        (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
        (r'.*', 'NN')                     # nouns (default)
    ]
    regex_tagger = nltk.RegexpTagger(patterns)
    regex_tagger.tag(brown_sents[3])
    regex_tagger.evaluate(brown_tagged_sents)

If we have a high number of common words, we can simply make a lookup tagger which
may be all that we will need:

.. code-block:: python

    dist = nltk.FreqDist(brown.words(categories='news'))
    cond = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    most_freq_words = dist.most_common(100)
    likely_tags = dict((word, cond[word].max()) for word in most_freq_words)
    baseline_tagger = nltk.UnigramTagger(model=likely_tags)
    baseline_tagger.tag(brown_sents[3])
    baseline_tagger.evaluate(brown_tagged_sents)

    # if this tagger does not know the tag, it simply returns None, we can supply
    # a next stage tagger to continue with
    baseline_tagger = nltk.UnigramTagger(model=likely_tags, backoff=nltk.DefaultTagger('NN'))

We can see how well our lookup tagger is doing if we add more and more words. As
we add more words, we see that the returns get lower and lower:

.. code-block:: python

    import pylab
    
    def performance(cond, wordlist):
        lookup  = dict((word, cond[word].max()) for word in wordlist)
        default = nltk.DefaultTagger('NN')
        baseline_tagger = nltk.UnigramTagger(model=lookup, backoff=default)
        return baseline_tagger.evaluate(brown.tagged_sents(categories='news'))

    def display():
        words_by_freq = list(nltk.FreqDist(brown.words(categories='news')))
        cond = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
        sizes = 2 ** pylab.arange(15)
        perfs = [performance(cond, words_by_freq[:size]) for size in sizes]
        pylab.plot(sizes, perfs, '-bo')
        pylab.title('Lookup Tagger Performance with Varying Model Size')
        pylab.xlabel('Model Size')
        pylab.ylabel('Performance')
        pylab.show()

If we are allowed to train a unigram tagger with a good test set, we will receive
a decent evaluation score. The basic idea is that every word maps to the most
likely POS regardless of the context:

.. code-block:: python

    unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
    unigram_tagger.tag(brown_sents[3])
    unigram_tagger.evaluate(brown.tagged_sents)

    # split training and testing data 90% vs 10%
    size = int(len(brown_tagged_sents) * 0.9)
    train_sents = brown_tagged_sents[:size]
    test_sents  = brown_tagged_sents[size:]
    unigram_tagger = nltk.UnigramTagger(train_sents)
    unigram_tagger.evaluate(test_sents)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
General N-Gram Tagging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A 1-gram or unigram tagger only has the current word to use for deciding on the
POS of itself. We can make a much more robust tagger if we allow the word to be
indexed with 1 or more previous parts of speech:

.. code-block:: python

    bigram_tagger = nltk.BigramTagger(train_sents)
    bigram_tagger.tag(brown_sents[2007])
    unigram_tagger.evaluate(test_sents)

The problem with n-gram taggers is that as we increase the size of N, the tagger
gets more specific and thus may not have seen a word used in a particular context
before. If this happens, it will be unable to tag a word and will blow out the
rest of the markov chain (as the assignment will be `None`). This is known as 
the sparse data problem and basically involves trading off precision and recall.

Generally the highest model we will train is a trigram. Furthermore, n-gram models
should not train across sentences, therefore we train on sentence lists not word
lists.

In order to handle this error, we can simply chain less specific taggers to create
a hierarchy to fallback to. It is important to specify the fallback tagger during
construction as the training of the new tagger will take advantage of the previous
model's already learned data and not store the same knowledge twice. This can be
controlled via the `cutoff` parameter:

.. code-block:: python

    tagger_0 = nltk.DefaultTagger('NN')
    tagger_1 = nltk.UnigramTagger(train_sents, backoff=tagger_0)
    tagger_2 = nltk.BigramTagger(train_sents, backoff=tagger_1)
    tagger_3 = nltk.TrigramTagger(train_sents, backoff=tagger_2)
    tagger_2.evaluate(test_sents)

All of these taggers will still perform poorly on unknown words. One way to handle
this is to limit the vocabulary of the text (like we did with alice) and replace
unknown words with *UNK*. Then when we train the model, it will likely learn what
part of speech *UNK* should be given the context. For example *to UNK* will more
than likely be tagged as a verb.

We can also save our tagger models as follows:

.. code-block:: python

    import pickle # or cPickle

    def save_tagger(model, path):
        with open(path, 'wb') as handle:
            pickle.dump(model, handle, -1)

    def load_tagger(path):
        with open(path, 'bb') as handle:
            return pickle.load(handle)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Perfomance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How many ambiguous cases exist for our trigram tagger:

.. code-block:: python

    cond = nltk.ConditionalFreqDist(
               ((x[1], y[1], z[0]), z[1])
               for sent in brown_tagged_sents
               for x, y, z in nltk.trigrams(sent))
    ambiguous_contexts = [c for c in cond.conditions() if len(con[c]) > 1]
    sum(cond[c].N() for c in ambiguous_contexts) / con.N() # 5%

We can also look at a confusion matrix of the common errors against a gold
standard. Based on this we may be able to perform some pre or post processing
for special cases that may help our evaluation results:

.. code-block:: python

    test_tags = [tag for sent in brown.sents(categories='editorial')
                     for (word, tag) in tagger_2.tag(sent)]
    gold_tags = [tag for (word, tag) in brown.tagged_words(categories='editorial')]
    print(nltk.ConfusionMatrix(gold_tags, test_tags))    

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Transformation Based Tagging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes it doesn't make sense to store large sparse multilevel N-gram models.
For example on embedded or mobile devices. In these cases, we can use Brill
tagging which produces a model that is a fraction of the size of N-gram models.

Brill tagging is an inductive transformation based tagger with the basic idea
being: guess the tag of each word then go back and fix the mistakes. This is a 
supervised method as we need a tagged training set to learn with. Also, unlike
N-gram tagging, it does not count observations but compiles a list of
transformational correction rules.

After training, the tagger has a collection of rules of the form::

    replace T_1 with T_2 in the context C
    T_1 = incorrect tag
    T_2 = corrected tag
    C   = identity or tag of preceding or following word
    C  |= apperance of a tag within 2 to 3 words of the following word

These rules are candidate rules that are scored based on how many errors they
fix minus the number of errors they introduce. The best rules are then chosen.
A nice side effect of the Brill tagger is that the rules are linquisticly
understandable unlike the N-gram models.

One can play with the Brill tagger in `nltk` by simply calling the supplied
demo:  `nltk.tag.brill.demo()`.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Determining Word Categories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To determine the category of a word, NLP uses: morphilogical, semantic, and
syntactic clues:

**morphilogical**

  The internal structure of a word may give useful clues as to its category.
  For example, the '-ness' suffix combines with an adjective to form a noun:
  happiness. Another is the present participle of a verb ends in '-ing' to
  express ongoing or incomplete action. It also appears on nouns derived from
  verbs (gerunds)

**syntactic**

  Based on the context of a word, we can generally guess its category. For
  example adjectives generally appear right before nouns.

**semantic**

  The meaning of a word is also a clue as to its category. However, these
  are very hard to formalize.

New words also will enter the vocabulary, however they will only affect
certain classes like nouns which means they are an open class. Prepositions
on the other hand are a closed class and membership to this set changes
very slowly over time.

Morphology is generally captured in tagsets with morpho-syntactic information.
A balance must be struck with how fine the categories are as well as how to
work between two tagged sets that may use different levels of tagging. For
example, the brown corpus includes the following::

    ------------------------------------------------------------
    Form    Category               Tag
    ------------------------------------------------------------
    go      base                   VB
    goes    3rd singular present   VBZ
    gone    past participle        VBN
    going   gerund                 VBG
    went    simple past            VBD

.. todo:: http://www.nltk.org/book/ch05.html#Excercies

--------------------------------------------------------------------------------
Chapter 6: Learning to Classify Text
--------------------------------------------------------------------------------

The goal of this chapter is to answer the following questions:

* How can we identify particular features of language data that are salient for
  classifying it?
* How can we construct models of language that can be used to perform language
  processing tasks automatically?
* What can we learn about language from these models?

It should be noted that the pure python implementations are great for testing
examples quickly, but will not scale up to large datasets. As such, `nltk` is
able to use more scalable applications if they exist in its search path. How to
install these is documented here:

* https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Gender Name Classifier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What follows is an example of a classifier that predicts the sex of a name
given a training set. The first thing we need to worry about is to create a set
of features that can be used to describe the input values. It is important to
find the necessary features and not too many more to prevent overfitting:

.. code-block:: python

    # example features for gender based names for example, the last
    # letter of the name is highly predictive
    vowels = set('aeiouyAEIOUY')
    features = {
        'last-1-letter': name[-1:].lower(),
        'last-2-letter': name[-2:].lower(),
        'first-letter': name[0].lower(),
        'name-length': len(name),
        'vowel-count': sum(1 for l in name if l in vowels)
    }
    for letter in 'abcefghijklmnopqrstuvwxyz':
        features['count(%s)' % letter] = name.lower().count(letter)
        features['has(%s)' % letter]   = (letter in name.lower())

    # The following are the eager versions of computing the features
    features = [(gender_feature(name), gender) for name, gender in labeled_names]
    train_set, test_set = features[500:], features[:500]

Next, we can train our model (in this case a naive Bayes classifier) while making
sure to have a train, holdout, and test set of data:

.. code-block:: python

    import random
    from nltk.corpus import names
    from nltk.classify import apply_features

    def gender_features(name):
        return {
            'last-1-letter': name[-1:].lower(),
            'last-2-letter': name[-2:].lower(),
        }

    labeled_names = (
        [(name, 'male')   for name in names.words('male.txt')] +
        [(name, 'female') for name in names.words('female.txt')])
    random.shuffle(labeled_names)

    # These are the lazy versions that save on memory if our features are large
    train_set    = apply_features(gender_features, labeled_names[1500:])
    validate_set = apply_features(gender_features, labeled_names[500:1500])
    test_set     = apply_features(gender_features, labeled_names[:500])
    classifier   = nltk.NaiveBayesClassifier.train(train_set)

    classifier.classify(gender_feature("April"))
    classifier.classify(gender_feature("Mark"))
    print(nltk.classify.accuracy(classifier, validate_set))
    print(nltk.classify.accuracy(classifier, test_set)) # save this for the final test
    classifier.show_most_informative_features(5)

    # we can print the errors of our classification to find patterns to
    # adjust our features.
    errors = []
    validate_names = labeled_names[500:1500]
    for name, tag in validate_names:
        guess = classifier.classify(gender_features(name))
        if guess != tag: errors.append((tag, guess, name))
    print errors

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Document Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import random
    from nltk.corpus import movie_reviews

    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)

    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    word_features = all_words.keys()[:2000]

    def document_features(document):
        document_words = set(document)
        return { 'contains(%s)' % word : (word in document_words)
                 for word in word_features }

    print(document_features(movie_reviews.words('pos/cv957_8737.txt')))
        
    featuresets = [(document_features(d), c) for (d,c) in documents]
    train_set, test_set = featuresets[100:], featuresets[:100]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(5)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Part of Speech Tagging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of creating our regular expression part of speech tagger by hand, we can
learn the rules and create a decision tree based on the training data:

.. code-block:: python

    from nltk.corpus import brown

    suffix_dist = nltk.FreqDist()
    for word in brown.words():
        word = word.lower()
        suffix_dist[word[-1:]] += 1
        suffix_dist[word[-2:]] += 1
        suffix_dist[word[-3:]] += 1
    common_suffixes = [suffix for (suffix, count) in suffix_dist.most_common(100)]
    print(common_suffixes)

    def pos_features(word):
        features = {}
        for suffix in common_suffixes:
            features['endswith(%s)' % suffix] = word.lower().endswith(suffix)
        return features

    tagged_words = brown.tagged_words(categories='news')
    features     = [(pos_features(word), pos) for (word, pos) in tagged_words]
    
    size = int(len(features) * 0.1)
    train_set, test_set = features[size:], features[:size]
    
    classifier = nltk.DecisionTreeClassifier.train(train_set)
    nltk.classify.accuracy(classifier, test_set)
    classifier.classify(pos_features('cats'))
    print(classifier.pseudocode(depth=4)) # to see the actual tree

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Features with Context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The problem with our feature sets up to this point are that they are based on a
single word at a time without regards to the context of the word (what led up
to it). We can modify our feature generator to work on sentences so we can get
context dependent features:

.. code-block:: python

    def pos_features(sentence, index):
        features = {
            "suffix(1)": sentence[index][-1:],
            "suffix(2)": sentence[index][-2:],
            "suffix(3)": sentence[index][-3:],
        }
        features["prev-word"] = "<START>" if (index == 0) else sentence[i - 1]
        return features

    pos_features(brown.sents()[0], 8)

    tagged_sents = brown.tagged_sents(categories='news')
    featuresets  = []
    for tagged_sent in tagged_sents:
        untagged_sent = nltk.tag.untag(tagged_sent)
        for index, (word, tag) in enumerate(tagged_sent):
            featuresets.append((pos_features(untagged_sent, index), tag))

    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    nltk.classify.accuracy(classifier, test_set)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sequence Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to better work with sequences, we can use join classifiers, namely
consecutive classification or greedy sequence classification. These work by
finding the most likely label for the first value of the sequence and then uses
that as evidence for the remaining values in the sequence.

We can augment the previously used trainer to take in a history argument. During
training, we just supply the tags of the source text and during classification we
will pass in the current historical context:

.. code-block:: python

    def pos_features(sentence, index, history):
        '''
        :param sentence: The sequence to convert to features
        :param index: The current index in the sequence
        :param history: The current history of the classifier
        '''
        features = {
            "suffix(1)": sentence[index][-1:],
            "suffix(2)": sentence[index][-2:],
            "suffix(3)": sentence[index][-3:],
        }
    
        if index == 0:
            features["prev-word"] = "<START>"
            features["prev-tag"]  = "<START>"
        else:
            features["prev-word"] = sentence[index - 1]
            features["prev-tag"]  = history[index  - 1]
        return features

    class ConsecutivePosTagger(nltk.TaggerI):

        def __init__(self, train_sents):
            train_set = []
            for tagged_sent in train_sents:
                untagged_sent = nltk.tag.untag(tagged_sent)
                history = []
                for index, (word, tag) in enumerate(tagged_sent):
                    features = pos_features(untagged_sent, index, history)
                    train_set.append((features, tag))
                    history.append(tag)
            self.classifier = nltk.NaiveBayesClassifier.train(train_set)

        def tag(self, sentence):
            ''' Classify the parts of speech of a given sentence.

            :param sentence: The sentence to classify the parts of speech for
            :returns: The sentence with its associated tag pairs
            '''
            history = []
            for index, word in enumerate(sentence):
                features = pos_features(sentence, index, history)
                tag = self.classifier.classify(features)
                history.append(tag)
            return zip(sentence, history)

    tagged_sents = brown.tagged_sents(categories='news')
    size = int(len(tagged_sents) * 0.1)
    train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
    tagger = ConsecutivePosTagger(train_sents)
    print(tagger.evaluate(test_sents))

The problem with this approach is that if we make the wrong assignment of a
part of speech early in the classification, the remainder of the assignment
will be incorrect. Better models work by assigning a score to all possible
sequences through the classification and then choose the assignment with the
highest score. This is the approach taken by Hidden Markov Models (HMM). At
each value in the sequence, the HMM assigns a probability distribution of
the various labels which are combined at the end of the sequence.

A problem with this situation is that we cannot calculate all possible
classifications and compare the results. Instead the HMM will generally only
allow the feature extractor to look at the last 1 to N (small) values when
generating their features. It is then possible to use dynamic programming
to compute the most likely classification. This model is used by advanced
algorithms like Maximum Entropy Markov Models and Linear-Chain Conditional
Random Field Models; but different algorithms are used to find scores for
tag sequences.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sentence Segmentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sentence segmentation can be viewed as a classification task for punctuation:
whenever we encounter a symbol that could possibly end a sentence, we decide
if it indeed terminates the previous sentence.

.. code-block:: python

    def sents_to_punct(sents):
        ''' Given a collection of sentences, return a generator
        of punctuation.

        :param sents: A collection of sentences
        :returns: A generator of (token, index, is-sentence-boundary)
        '''
        index = 0
        punct = set('.?!')
        for sent in sents:
            for word in sent[:-1]:
                if word in punct:
                    yield (word, index, False) 
                index += 1
            yield (sent[-1], index, True) 
            index += 1

    def split_testset(values, ratio=0.1):
        size = int(len(values) * 0.1)
        return value[size:], values[:size]
        
    def punct_features(tokens, index):
        ''' Generate a collection of features about punctuation
        given its current context.

        :param tokens: The token stream to use for context
        :param index: The index of the punctuation in the tokens
        :returns: The generated features
        '''
        return {
            'next-word-capitalized': tokens[index + 1][0].isupper(),
            'prev-word': tokens[index - 1].lower(),
            'punct': tokens[index],
            'prev-word-is-one-char': len(tokens[index - 1]) == 1
        }

    sents    = nltk.corpus.treebank_raw.sents()
    tokens   = [word for sent in sents for word in sent]
    features = [(punct_features(tokens, index), boundary)
        for token, index, boundary in sents_to_punct(sents)]

    train_set, test_set = split_testset(features)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    nltk.classify.accuracy(classifier, test_set)
    
    def segment_sentences(words, classifier):
        ''' Given a sequence of words and a segmenting classifier,
        return a list of segmented sentences.

        :param words: a sequence of words to segment
        :param classifier: The classifer to split words with
        :returns: A list of segmented sentences
        '''
        start = 0
        sents = []
        punct = set('.?!')
        for index, word in enumerate(words):
            if  ((word in punct)
             and (classifier.classify(punct_features(words, index)) == True)):
                sents.append(words[start:index + 1])
                start = index + 1
        if start < len(words):
            sents.append(words[start:])
        return sents

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Identifying Dialog Acts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python 

    def dialogue_act_features(post):
        features = {}
        for word in nltk.word_tokenize(post):
            features['contains(%s)' % word.lower()] = True
        return features

    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    features = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    train_set, test_set = split_dataset(features)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recognizing Textual Entailment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given an example hypothesis, can we conclude that it is entangled in a supplied
text blurb::

    T: Parviz Davudi was representing Iran at a meeting of the Shanghai Co-operation
       Organisation (SCO), the fledgling association that binds Russia, China and
       four former Soviet republics of central Asia together to fight terrorism.

    H: China is a member of SCO.
    R: True

There is a utility in `nltk` that can assist in this problem (`nltk.classify.rte_classify`).
It mostly works with the following feature extractor:

.. code-block:: python

    def rte_features(rtepair):
        ''' The RTE extractor builds a bag of words for the hypothesis
        and the text after throwing away some stopwords and then calculates
        overlap and difference between the two.
        '''
        extractor = nltk.RTEFeatureExtractor(rtepair)
        features = {}
        features['word_overlap']   = len(extractor.overlap('word'))
        features['word_hyp_extra'] = len(extractor.hyp_extra('word'))
        features['ne_overlap']     = len(extractor.overlap('ne'))
        features['ne_hyp_extra']   = len(extractor.hyp_extra('ne'))
        return features

    rtepair   = nltk.corpus.rte.pairs(['rte3_dev.xml'])[33]
    extractor = nltk.RTEFeatureExtractor(rtepair)
    print(extractor.text_words)
    print(extractor.hyp_words)
    print(extractor.overlap('word'))
    print(extractor.overlap('ne'))
    print(extractor.hyp_extra('word'))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Model Evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A basic discussion about a number of ways to evaluate a model as well as advice
about how to split a training set into a seperate training set.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Decision Trees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decision trees work by creating a tree of decisions about splitting the data
until the value comes to a leaf which has a label ot assign that value. To create
a tree, first create a stump to split the data left or right based on the decrease
of entropy and information gain of creating the leaves. The learning continues if
another branch needs to be created (if the entropy of the leaf is too high).

.. code-block:: python

    import math

    def entropy(labels):
        freqs = nltk.FreqDist(labels)
        probs = [freqs.freq(label) for label in freqs]
        return -sum(prob * math.log(prob, 2) for prob in probs)

    print(entropy(['male', 'male', 'male', 'male'])) 
    print(entropy(['male', 'female', 'male', 'male']))

Some downsides of decision trees are:

* lower nodes tend to overfit the training data as they have less training data
* features that are independent of each other may not be able to be used well
* need to be cut off or pruned after training to prevent overfitting
* features need to be checked in a specific order failing to use weak features

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Maximum Entropy Models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Maximum Entropy classifier uses a model similar to a naive Bayes classifier.
But rather than using probabilities to set the model's parameters, it uses
search techniques to find a set of parameters that will maximize the performance
of the classifier. In particular, it looks for the set of parameters that maximizes
the total likelihood of the training corpus:

.. code-block:: text

    P(features) = \sum_{x : corpus} P(label(x)|features(x))
    P(label|features) = P(label, features) / \sum_label P(label, features)

Since these values cannot be directly calculated, iterative optimization methods
must be used.

When training entropy models, avoid Generalized Iterative Scaling (GIS) and
Improved Iterative Scaling (IIS). Instead use Conjugate Gradient (CG) and the
BFGS optimization methods.

.. todo:: Review this more


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generative vs Conditional Classifiers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The naive Bayes classifier is an example of a generative classifier, which
builds a model that predicts P(input, label), the joint probability of a
(input, label) pair. It can answer the following questions:

1. What is the most likely label for a given input?
2. How likely is a given label for a given input?
3. What is the most likely input value?
4. How likely is a given input value?
5. How likely is a given input value with a given label?
6. What is the most likely label for an input that might have one of two values?

The Maximum Entropy classifier, is a conditional classifier. Conditional
classifiers build models that predict P(label|input): the probability of a label
given the input value. Thus, they can answer questions 1 and 2, however not the
remaining questions.

In general, generative models are strictly more powerful than conditional models,
since they can calculate P(label|input) from P(input, label). However this comes
at a price: it has more free parameters which need to be learned. Thus with the
same amount of training data, generative models have less data to use for training
those free paramers then conditional models which can use all the available data
to focus on the first two questions.

.. todo:: Further Reading http://www.nltk.org/book/ch06.html
.. todo:: Exercise 8 http://www.nltk.org/book/ch06.html

--------------------------------------------------------------------------------
Chapter 7: Extracting Information From Text
--------------------------------------------------------------------------------

This chapter is used to answer the following questions:

* How can we build a system that extracts structured data from unstructured text?
* What are robust methods for identifying the entities and relationships in a text?
* Which corpora are appropriate for this work and how do we train a model with them?

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Information Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following is a general structure of a nltk information retrieval system. The
first three steps can be handled by the following code:

.. code-block:: python

    import nltk

    def ie_preprocess(document):
        sentences = nltk.sent_tokenize(document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences

.. image:: images/nltk-entity-pipeline.png
   :target: http://www.nltk.org/book/ch07.html
   :align: center

Next, we segment and label the entities that might have interesting relations to
each other. These will generally be definite noun phrases or proper names. Some
times indefinite nouns or noun chunks can be useful. Finally, we search for
specific patterns between pairs of entities that occur near to each other in the
text and use those patterns to build tuples of relationships.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Chunking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The basic technique for entity detection is chunking which segments and labels
multi-token sequences. This will produce a number of non overlapping chunks. The
first thing we will look at is Noun Phrase chunking (NP Chunking). We will start
with a simple regex parser:

.. code-block:: python

    import nltk

    sentence = [
        ("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
        ("dog", "NN"), ("barked", "VBD"), ("at", "IN"), ("the", "DT"), ("cat", "NN")
    ]
        
    grammar = r"""
      NP: {<DT|PP\$>?<JJ>*<NN>}   # chunk determiner/possessive, adjectives and noun
            {<NNP>+}              # chunk sequences of proper nouns
    """                           # if you add comments, they will show up in the trace
    grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}" # this will match any type of adjective or noun
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    parser  = nltk.RegexpParser(grammar)
    result  = parser.parse(sentence)
    print(result)
    result.draw()

The parser is driven by tag patterns which are used to describe a sequence of
tagged words. The grammars can be tested using `nltk.app.chunkparser()`. Chunking
makes it much easier to explore a text corpus:

.. code-block:: python

    import nltk

    def find_chunks(grammar, sents):
        parser = nltk.RegexpParser(grammar)
        for sent in sents:
            tree = parser.parse(sent)
            for subtree in tree.subtrees():
                if subtree.label() == 'CHUNK':
                    print(subtree)

    sents   = nltk.corpus.brown.tagged_sents() 
    grammar = 'CHUNK: {<V.*> <TO> <V.*>}' # VERB to VERB
    find_chunks(grammar, sents)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Chinking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chinking is the process of removing a sequence of tokens from a chunk. If the
matching tokens span an entire chunk, then that chunk is removed. If the chink
is in the middle of a chunk, the chunk is split into two. It the chink is at
the head or tail, it is simply removed from the chunk:

.. code-block:: python

    import nltk

    grammar = r"""
      NP:
          {<.*>+}          # Chunk everything
          }<VBD|IN>+{      # Chink sequences of VBD and IN
    """
    sentence = [
        ("the", "DT"), ("little", "JJ"), ("yellow", "JJ"),
        ("dog", "NN"), ("barked", "VBD"), ("at", "IN"),  ("the", "DT"), ("cat", "NN")
    ]
    parser = nltk.RegexpParser(grammar)
    print(parser.parse(sentence))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Chunks can be represented with tags or with trees. The most widespread usage in
files is IOB tags. This works by using three tags to represent the chunk:

* **I** : inside the chunk (so `I-JJ`)
* **B** : begin the chunk (so `B-NP`)
* **O** : outside of the chunk (the POS is usualy left out, so `O`)

While this is good for storing the structures in files, in memory trees are
generally used. This makes it easy to quickly manipulate and walk through the
structure of chunks. What follows is an example of converting IOB tags into a nltk
tree:

.. code-block:: python

    text = '''
    he PRP B-NP
    accepted VBD B-VP
    the DT B-NP
    position NN I-NP
    of IN B-PP
    vice NN B-NP
    chairman NN I-NP
    of IN B-PP
    Carlyle NNP B-NP
    Group NNP I-NP
    , , O
    a DT B-NP
    merchant NN I-NP
    banking NN I-NP
    concern NN I-NP
    . . O'''
    nltk.chunk.conllstr2tree(text, chunk_types=['NP']).draw()

Furthermore, nltk includes a large corpus of chunked text that can be used for
training and validation:

.. code-block:: python 

    # this is the conll2000 corpus which consists of 270k chunked words of the
    # wallstreet journal. It includes three chunk types: NP, VP, and PP
    from nltk.corpus import conll2000
    print(conll2000.chunked_sents('train.txt')[99]) # print the 100'th training chunk
    print(conll2000.chunked_sents('train.txt', chunk_types=['NP'])[99]) # print only the NP chunk

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We start our evaluation out with a simple baseline of a chunker that creates no
chunks:

.. code-block:: python

    from nltk.corpus import conll2000

    parser = nltk.RegexpParser("")
    test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    print(parser.evaluate(test_sents))

Now if we make a parser that checks for common noun phrase starters:

.. code-block:: python

    grammar = r"NP: {<[CDJNP].*>+}"
    parser = nltk.RegexpParser(grammar)
    print(parser.evaluate(test_sents))

We can do better with a simple data driven parser based on a unigram tagger:

.. code-block:: python

    import nltk

    class UnigramChunker(nltk.ChunkParserI):

        @classmethod
        def create_from_tree(klass, sents):
            train_sents = [
                [(tag, chunk) for word, tag, chunk in nltk.chunk.tree2conlltags(sent)]
                              for sent in sents]
            return klass(train_sents)

        def __init__(self, train_data):
            ''' Initializes a new unigram chunked 

            :param train_data: The sentence training data
            '''
            self.tagger = nltk.UnigramTagger(train_data)

        def parse(self, sentence):
            ''' Parses a sentence into chunks using the previously
            trained model.

            :param sentence: A sentence with pos tagged words
            :returns: The sentence chunks
            '''
            pos_tags = [pos for (word, pos) in sentence]
            tagged_pos_tags = self.tagger.tag(pos_tags)
            chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
            conlltags = [(word, pos, chunktag) for ((word, pos), chunktag)
                         in zip(sentence, chunktags)]
            return nltk.chunk.conlltags2tree(conlltags)

    test_sents  = conll2000.chunked_sents('test.txt', chunk_types=['NP'])
    train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
    chunker = UnigramChunker.create_from_tree(train_sents)
    print(chunker.evaluate(test_sents))

        
    pos_tags = sorted(set(pos for sent in train_sents
                              for (word,pos) in sent.leaves()))
    print(chunker.tagger.tag(pos_tags))

We can get a little better performance by using a bigram chunker which we can
create with just a little extra work:

.. code-block:: python

    class BigramChunker(UnigramChunker):

        def __init__(self, train_data):
            ''' Initializes a new unigram chunked 

            :param train_data: The sentence training data
            '''
            self.tagger = nltk.BigramTagger(train_data)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Classifier Based Chunkers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class ConsecutiveNPChunkTagger(nltk.TaggerI):

        def __init__(self, train_sents, features):
            train_set = []
            for tagged_sent in train_sents:
                untagged_sent = nltk.tag.untag(tagged_sent)
                history = []
                for index, (word, tag) in enumerate(tagged_sent):
                    featureset = features(untagged_sent, index, history)
                    train_set.append((featureset, tag))
                    history.append(tag)
            self.features = features
            self.classifier = nltk.MaxentClassifier.train
                train_set, algorithm='megam', trace=0)

        def tag(self, sentence):
            history = []
            for index, word in enumerate(sentence):
                featureset = self.features(sentence, index, history)
                tag = self.classifier.classify(featureset)
                history.append(tag)
            return zip(sentence, history)

    class ConsecutiveNPChunker(nltk.ChunkParserI):

        def __init__(self, train_sents):
            tagged_sents = [[((w,t),c) for (w,t,c) in
                             nltk.chunk.tree2conlltags(sent)]
                            for sent in train_sents]
            self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

        def parse(self, sentence):
            tagged_sents = self.tagger.tag(sentence)
            conlltags = [(word, tag, chunk) for ((word, tag),chunk) in tagged_sents]
            return nltk.chunk.conlltags2tree(conlltags)

    def pos_features(sentence, i, history):
        word, pos = sentence[i]
        return {"pos" : pos}

    chunker = ConsecutiveNPChunker(train_sents, npchunk_features)
    print(chunker.evaluate(test_sents))

We can plug in different feature extractors to see if they make the
classifier have better results:

.. code-block:: python    

    def two_pos_features(sentence, i, history):
        word, pos = sentence[i]
        if i == 0:
            prevword, prevpos = "<START>", "<START>"
        else: prevword, prevpos = sentence[i-1]

        return {"pos": pos, "prevpos": prevpos}

    def cur_word_features(sentence, i, history):
        word, pos = sentence[i]
        if i == 0:
            prevword, prevpos = "<START>", "<START>"
        else: prevword, prevpos = sentence[i-1]

        return {"pos": pos, "word": word, "prevpos": prevpos}
            
     def npchunk_features(sentence, i, history):
         word, pos = sentence[i]
         if i == 0:
             prevword, prevpos = "<START>", "<START>"
         else: prevword, prevpos = sentence[i-1]

         if i == len(sentence)-1:
             nextword, nextpos = "<END>", "<END>"
         else: nextword, nextpos = sentence[i+1]
         return {
             "pos": pos,
             "word": word,
             "prevpos": prevpos,
             "nextpos": nextpos,
             "prevpos+pos": "%s+%s" % (prevpos, pos),
             "pos+nextpos": "%s+%s" % (pos, nextpos),
             "tags-since-dt": tags_since_dt(sentence, i)
         }
           
     def tags_since_dt(sentence, index):
         tags = set()
         for word, pos in sentence[:index]:
             if pos == 'DT':
                 tags = set()
             else: tags.add(pos)
         return '+'.join(sorted(tags))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recursion in Linguistic Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can create recursive hierarchies in the chunks:

.. code-block:: pyhton

    grammar = r"""
        NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
        PP: {<IN><NP>}               # Chunk prepositions followed by NP
        VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
        CLAUSE: {<NP><VP>}           # Chunk NP, VP
    """
    parser   = nltk.RegexpParser(grammar, loop=2)
    sentence = [
        ("Mary", "NN"), ("saw", "VBD"), ("the", "DT"), ("cat", "NN"),
        ("sit", "VB"), ("on", "IN"), ("the", "DT"), ("mat", "NN")
    ]
    print(parser.parse(sentence))

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Trees
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trees are useful for representing hierarchical structures:

.. code-block:: python

    tree1 = nltk.Tree('NP', ['Alice'])
    tree2 = nltk.Tree('NP', ['the', 'rabbit'])
    tree3 = nltk.Tree('VP', ['chased', tree2])
    tree4 = nltk.Tree('S', [tree1, tree3])
    
    print(tree1) # (NP Alice)
    print(tree2) # (NP the rabbit)
    print(tree4) # (S (NP Alice) (VP chased (NP the rabbit)))
    
    print(tree4[1])  # (VP chased (NP the rabbit))
    tree4[1].label() # 'VP'
    tree4.leaves()   # ['Alice', 'chased', 'the', 'rabbit']
    tree4[1][1][1]   # 'rabbit'
    tree3.draw()

We can traverse the language trees using standard tree traversal:

.. code-block:: python

    def traverse(node):
        try:
            node.label()
        except AttributeError:
            print(node, end=" ")
        else:
            # Now we know that t.node is defined
            print('(', node.label(), end=" ")
            for child in node:
                traverse(child)
            print(')', end=" ")
    
     tree = nltk.Tree('(S (NP Alice) (VP chased (NP the rabbit)))')
     traverse(tree)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Named Entity Recognition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The goal of a named entity recognition (NER) system is to identify all textual
mentions of the named entities. This can be broken down into two sub-tasks:
identifying the boundaries of the NE, and identifying its type. This is useful
for other tasks as well such as question answering.

When the information retrieval system returns a hit for a question, we can use
a NER system to filter the result to a simple response to a question instead of
a page of text.

One approach to NER is to use a gazetteer or a geographical dictionary. The
problem with this is that there will be a number of false positives that must be
filtered out.

`nltk` has an already trained classifier for named entities:

.. code-block:: python

    sent = nltk.corpus.treebank.tagged_sents()[22]
    print(nltk.ne_chunk(sent))

We can extract relations using a simple regex parser for triples of (X, '...in...', Y):

.. code-block:: python

    import re, nltk

    pattern = re.compile(r'.*\bin\b(?!\b.+ing)')
    for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
        for rel in nltk.sem.extract_rels('ORG', 'LOC', doc, corpus='ieer', pattern = pattern):
            print(nltk.sem.rtuple(rel))

We can use the part of speech tags as well to generate these semantic tuples:

.. code-block:: python

    from nltk.corpus import conll2002
    vnv = """
        (
        is/V|    # 3rd sing present and
        was/V|   # past forms of the verb zijn ('be')
        werd/V|  # and also present
        wordt/V  # past of worden ('become)
        )
        .*       # followed by anything
        van/Prep # followed by van ('of')
    """
    pattern = re.compile(vnv, re.VERBOSE)
    for doc in conll2002.chunked_sents('ned.train'):
        for r in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='conll2002', pattern=pattern):
            print(nltk.sem.clause(r, relsym="VAN"))

--------------------------------------------------------------------------------
Chapter 8: Analyzing Sentence Structure
--------------------------------------------------------------------------------

The goal of this chapter is to answer the following questions:

* How can we use a formal grammar to describe the structure of an unlimited set of sentences?
* How do we represent the structure of sentences using syntax trees?
* How do parsers analyze a sentence and automatically build a syntax tree?

We can start by looking at an ambiguous sentence and writing a simple generative
parser to decode it:

.. code-block:: python

    groucho_grammar = nltk.CFG.fromstring("""
        S   -> NP VP
        PP  -> P NP
        NP  -> Det N | Det N PP | 'I'
        VP  -> V NP | VP PP
        Det -> 'an' | 'my'
        N   -> 'elephant' | 'pajamas'
        V   -> 'shot'
        P   -> 'in'
    """)
   
    // other sentences are:
    // * visiting relatives are timesome
    // * fighting animals could be dangerous

    sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
    parser = nltk.ChartParser(groucho_grammar)
    for tree in parser.parse(sent):
        print(tree)

A grammar specifies how a sentence can be subdivided into its immediate
constituents, and how these can be further subdivided until we reach the level
of individual words.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Grammatical Structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **noun**
* **adjective**
* **preposition**
* **determinter**

  Includes words like: the, an, a, some

* **prepositional phrase (PP)**

  A phrase making a prepostion statement; examples:

  - in the brook
  - behind your back

* **noun phrase (NP)**
* **adjective phrase (AP)**

* **coordinate structure**
  
  Where two phrases are joined with a coordinating conjunction such as and, but,
  or. More formally: If `v_1` and `v_2` are both phrases of grammatical category
  `X`, then `v_1` and `v_2` is also a phrase of category `X`. For example:

  - The book's ending was (NP the worst part and the best part) for me.
  - On land they are (AP slow and clumsy looking).

* **constituent structure**

  Constituent structure is based on the observation that words combine with other
  words to form units. These units can be replaced without making rending the
  sentence structure ill-formed. If we flip the smallest structure, we are left
  with a phrase tree where every node is a constituent and the children are the
  immediate consituents.

.. image:: images/nltk-constituent-structure.png
   :target: http://www.nltk.org/book/ch08.html
   :align: center

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Context Free Grammar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    grammar = nltk.CFG.fromstring("""
        S   -> NP VP
        VP  -> V NP | V NP PP
        PP  -> P NP
        V   -> "saw" | "ate" | "walked"
        NP  -> "John" | "Mary" | "Bob" | Det N | Det N PP
        Det -> "a" | "an" | "the" | "my"
        N   -> "man" | "dog" | "cat" | "telescope" | "park"
        P   -> "in" | "on" | "by" | "with"
    """)
        
    // explore this with the `nltk.app.rdparser()` demo
    sent = "Mary saw Bob".split()
    parser = nltk.RecursiveDescentParser(grammar)
    for tree in parser.parse(sent):
        print(tree)

.. code-block:: python

    def run_grammer(text, path):
        ''' A simply utility to run test data through an
        external grammar.

        :param text: The text to run the parser on
        :param path: The path to the parser grammar
        '''
        grammar = nltk.data.load('file:' + path)
        sent    = text.split()
        parser  = nltk.RecursiveDescentParser(grammar, trace=2)
        for tree in parser.parse(sent):
             print(tree)

    run_grammer("Mary saw Bob", "grammar.cfg")

Grammars in nltk cannot combine grammatical categories and lexical items in the
same production rule (`PP -> 'of' NP`). So simply make the lexical items new
grammatical categories. Also, multi word lexical items cannot be used either, so
use `NP -> New_York` instead of `NP -> New York`.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Recursion in Syntatic Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It should be noted that a recursive descent parser cannot parse left-recusive
productions.

.. code-block:: python

    grammar = nltk.CFG.fromstring("""
        S     -> NP VP
        NP    -> Det Nom | PropN
        Nom   -> Adj Nom | N
        VP    -> V Adj | V NP | V S | V NP PP
        PP    -> P NP
        PropN -> 'Buster' | 'Chatterer' | 'Joe'
        Det   -> 'the' | 'a'
        N     -> 'bear' | 'squirrel' | 'tree' | 'fish' | 'log'
        Adj   -> 'angry' | 'frightened' |  'little' | 'tall'
        V     ->  'chased'  | 'saw' | 'said' | 'thought' | 'was' | 'put'
        P     -> 'on'
    """) 

    sent = "the angry bear chased the frightened little squirrel".split()
    sent = "Chatterer said Buster thought the tree was tall".split()


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Parsers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`nltk` has include a number of parsers that can be used. First there is the
top down recursive descent parser. It works by 'predicting' what the input will
be before inspecting the input. This parser has three short-commings:

1. left-recursive productions like `NP -> NP PP` send it into an infinite loop
2. it wastes a lot of time considering words that do not correspond to the input
3. it discards previously parsed results that may be used again

.. code-block:: python

    parser = nltk.RecursiveDescentParser(grammar)
    sent   = 'Mary saw a dog'.split()
    for tree in parser.parse(sent):
        print(tree)

A better approach is a bottom-up parser like shift-reduce. This works by trying
to find a sequence of words and phrases that correspond to the right hand side of
a grammar production. It then replaces them with the left hand side until it
reaches the starting production. The shift-reduce parser in the `nltk` package
does not perform any backtracking so it may miss a parse even if one exists and
it will only find a single parse. In general, shift-reduce parsers usually use
some kind of heuristic to control when to shift or reduce (or resolve conflicts
of multiple reductions). The advantages of this parser over the recursive
descent parser are:

1. they only build a parsing structure from the words in the input
2. they only build each sub-structure once regardless of which reduction is used

.. code-block:: python

    parser = nltk.ShiftReduceParser(grammar)
    sent   = 'Mary saw a dog'.split()
    for tree in parser.parse(sent):
        print(tree)

The *left-corner parser* finds a balance between *top-down* and *bottom-up*
parsers. It is a top-down parser that uses bottom-up filtering to produce the
left corner of each production rule (a preprocessing step). Then, before
descending, it checks if the current context matches the supplied corner.

Chart parsing uses dynamic programming to store previously evaluated sub
problems. The structure it builds is the *well-formed substring table*.
Generally, we can enter `A` in (i, j) if there is a production `A -> B C`,
and we find nonterminal `B` in (i, k) and `C` in (k, j)

.. code-block:: python

    def initialize_wfst(tokens, grammar):
        length = len(tokens)
        table  = [[None for i in range(length + 1)] for j in range(length + 1)]
        for i in range(length):
            productions = grammar.productions(rhs=tokens[i])
            table[i][i + 1] = productions[0].lhs()
        return table

    def complete_wfst(table, tokens, grammar, trace=False):
        index  = { p.rhs() : p.lhs() for p in grammar.productions() }
        length = len(tokens)
        for span in range(2, length + 1):
            for start in range(length + 1 - span):
                end = start + span
                for mid in range(start + 1, end):
                    nt1, nt2 = table[start][mid], table[mid][end]
                    production = (nt1, nt2)
                    if nt1 and nt2 and (production in index):
                        table[start][end] = index[production]
                        if trace:
                            print("[%s] %3s [%s] %3s [%s] ==> [%s] %3s [%s]" % \
                            (start, nt1, mid, nt2, end, start, index[production], end))
        return table

    def display(table, tokens):
        print('\nWFST ' + ' '.join(("%-4d" % i) for i in range(1, len(table))))
        for i in range(len(table) -1 ):
            print("%d   " % i, end=" ")
            for j in range(1, len(table)):
                print("%-4s" % (table[i][j] or '.'), end=" ")
            print()

    tokens = "I shot an elephant in my pajamas".split()
    table1 = inittialize_wfst(tokens, groucho_grammar)
    table2 = complete_wfst(table1, tokens, grammar)
    display(table1, tokens)
    display(table2, tokens)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Dependency Grammar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dependency is a binary asymmetric relation that holds between a head and its
dependents. The head of a sentence is usually the tensed verb, and every other
word is dependent on the head, or connects to it through a dependency path. The
structure is represented with a directed graph with arcs being relations to
the word nodes.

.. code-block:: python

    grammar = nltk.DependencyGrammar.fromstring("""
        'shot' -> 'I' | 'elephant' | 'in'
        'elephant' -> 'an' | 'in'
        'in' -> 'pajamas'
        'pajamas' -> 'my'
    """)
    print(grammar)

A dependent parse is projective if when the word nodes are presented in linear
order, there are no edge crossings. This basically means that a word and all
its descendents form a contiguous sequence of words in the sentence. What
follows is a collection of criteria for deciding the word head:

* H determines the distribution class of C, or the external syntactic properties of C are due to H
* H determines the semantic type of C
* H is obligatory while D may be optional
* H selects D and determines whether it is obligatory or optional
* The morphological form of D is determined by H (e.g. agreement or case government)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Valency and the Lexicon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following are verb phrase productions along with their lexical heads. The
dependents that occur with the `VP` are called the complements and are strong
constraints on which verbs can appear with what complements. The verbs are thus
said to have different **valencies**:

.. code-block:: text

    VP -> V Adj   (was)
    VP -> V NP    (saw)
    VP -> V S     (thought)
    VP -> V NP PP (put)

To make sure we parse sentences correctly such that verbs co-occur with their
correct complements, we need to create sub-categories of verbs:

.. code-block:: text

    Symbol  Meaning             Example
    --------------------------------------------------
    IV      intransitive verbs  barked
    TV      transitive verbs    saw a man
    DatV    dative verbs        gave a dog to a man
    SV      sentential verbs    said that a dog barked

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Grammar Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is extremely complicated to make a strong general parser for a language. This
is complicated by the fact that there are at some times massive numbers of parse
treeds for seemingly simple sentences: "fish fish fish." One way to handle this
is with a weighted grammar. A probabilistic context free grammar (PCFG) is just
such a solution. It associates a probability with each of its productions. The
parser then produces the most likely parse out of the many possible productions.

.. code-block:: python

    grammar = nltk.PCFG.fromstring("""
        S    -> NP VP              [1.0]
        VP   -> TV NP              [0.4]
        VP   -> IV                 [0.3]
        VP   -> DatV NP NP         [0.3]
        TV   -> 'saw'              [1.0]
        IV   -> 'ate'              [1.0]
        DatV -> 'gave'             [1.0]
        NP   -> 'telescopes'       [0.8]
        NP   -> 'Jack'             [0.2]
    """)
    print(grammar)

    parser = nltk.ViterbiParser(grammar)
    for tree in parser.parse(['Jack', 'saw', 'telescopes']):
        print(tree)


--------------------------------------------------------------------------------
Chapter 9: Building Feature Based Grammars
--------------------------------------------------------------------------------

The goal of this chapter is to answer the following questions:

* How can we extend the framework of context free grammars with features so as
  to gain more fine-grained control over grammatical categories and productions?

* What are the main formal properties of feature structures and how do we use
  them computationally?

* What kinds of linguistic patterns and grammatical constructions can we now
  capture with feature based grammars?

We would like to go farther than simply generating the part of speech for a word
and instead provide full *feature structures*. There an be many or few for a
given word. what follows is a simple example of two structures:

.. code-block:: python

    # CAT  -> category
    # ORTH -> spelling (orthography)
    # REF  -> reference
    # REL  -> relation
    kim   = {'CAT': 'NP', 'ORTH': 'Kim', 'REF': 'k'}
    chase = {'CAT': 'V',  'ORTH': 'chased', 'REL': 'chase'}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Attributes and Constraints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

How would we encode *Subject Verb Agreement* into a CFG grammar? The obvious way
would be to make productions for all six forms of subject and verb; however this
will make our grammars huge. Another way is to encode properties into the
grammar:

.. code-block:: text

    #------------------------------------------------------------
    # this adds the property NUM (number) which has values:
    #
    # - sg singular
    # - pl plural
    # - ?n is a variable for that property that each instance is
    #      constrained to once assigned. If the property doesn't
    #      matter, we can leave it empty and the production can
    #      be used for any value.
    #------------------------------------------------------------

    S           -> NP[NUM=?n] VP[NUM=?n]
    NP[NUM=?n]  -> Det[NUM=?n] N[NUM=?n]
    VP[NUM=?n]  -> V[NUM=?n]

    Det[NUM=sg] -> 'this'
    Det[NUM=pl] -> 'these'
    Det         -> 'the' | 'some' | 'any'

    N[NUM=sg]   -> 'dog'
    N[NUM=pl]   -> 'dogs'
    V[NUM=sg]   -> 'runs'
    V[NUM=pl]   -> 'run'

The grammar can have as many or few properties as it wants. There is also an
extension to this system to make the properties and values typed so only
correct values can be supplied:

.. code-block:: python

    from nltk import load_parser [1]

    tokens = 'Kim likes children'.split()
    parser = load_parser('grammars/book_grammars/feat0.fcfg', trace=2)
    for tree in parser.parse(tokens):
        print(tree)

    nltk.data.show_cfg('grammars/book_grammars/feat0.fcfg')

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Terminology
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Features that cannot be decomposed into subparts are referred to as *atomic*. A
special case of *atomic* features are *boolean* features usually represented
with `+` / `-` or `t` / `f`. So a verb that may or may not be auxiliary (can, may
will, and do) could be represented as `V[tense=pres, +AUX]`.

Instead of atomic features, features can be *complex* and make use of *attribute
value matrix* values. This is basically storing a structure as a feature:

.. code-block:: text

    [POS = N           ]
    [                  ]
    [AGR = [PER = 3   ]]
    [      [NUM = pl  ]]
    [      [GND = fem ]]

It helps to think of feature structures as graphs (DAGs). We work with features
structures in nltk as follows:

.. code-block:: python

    # basically a dictionary
    feature = nltk.FeatureStructure(TENSE='past', NUM='sg')
    feature['CASE'] = 'acc'
    print(feature)
    print(feature['TENSE'])

    # these both equal the same value
    complex = nltk.FeatureStructure(POS='N', AGR=feature)
    complex = nltk.FeatStruct("[POS='N', AGR=[TENSE='past', NUM='sg', CASE='acc']]"))

Since the structure is a graph, we can use feature sharing to use the same
information in multiple places in the structure. We do this by using tags or
coindexes to mark the common field:

.. code-block:: python

    # prefix the common feature with (n)
    # reference it with NAME->(n)
    complex = nltk.FeatStruct("""
      [NAME='Lee', ADDRESS=(1)[NUMBER=74, STREET='rue Pascal'],
      SPOUSE=[NAME='Kim', ADDRESS->(1)]]
    """)
    print(complex)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Subsumption and Unification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can order feature structures based on the information they contain. Some are
partial and have less information than a complete structure. This ordering is
called *subsumption*. `S_0` subsumes `S_1` if all the information contained in
`S_1` is also contained in `S_0`. If we have two structures with differing
information, then neither subsumes the other.

However, there are cases when we would like to merge the data in two or more
structures. This is known as unification. It is a symmetric operation so
`a unify b == b unify a`. If a subsuming structure unifies another, the result
is the structure with the most information. If the two structures have divergent
data, they cannot be unified:

.. code-block:: python

    feature1 = nltk.FeatStruct(NUMBER=74, STREET='rue Pascal')
    feature2 = nltk.FeatStruct(CITY='Paris')
    print(feature1.unify(feature2))

    # divergent feature cannot be unified
    feature1 = nltk.FeatStruct(NUMBER=74)
    feature2 = nltk.FeatStruct(NUMBER=75)
    print(feature1.unify(feature2)) # None

It should be noted that if you update a field in shared structure, all fields
that reference that entity will get updated.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Extending a Feature Based Grammar
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of having labels for different kinds of verbs in productions like:

.. code-block:: text
    
    VP -> IV    # intransitive verb
    VP -> TV NP # transitive verb

We can instead use structured features to add subcategories of verbs. This idea
was realized by Generalized Phrase Structure Grammar (GPSG):

.. code-block:: text
    
    VP[TENSE=?t, NUM=?n] -> V[SUBCAT=intrans, TENSE=?t, NUM=?n]
    VP[TENSE=?t, NUM=?n] -> V[SUBCAT=trans, TENSE=?t, NUM=?n] NP
    VP[TENSE=?t, NUM=?n] -> V[SUBCAT=clause, TENSE=?t, NUM=?n] SBar
    
    V[SUBCAT=intrans, TENSE=pres, NUM=sg] -> 'disappears' | 'walks'
    V[SUBCAT=trans, TENSE=pres, NUM=sg]   -> 'sees' | 'likes'
    V[SUBCAT=clause, TENSE=pres, NUM=sg]  -> 'says' | 'claims'
    
    V[SUBCAT=intrans, TENSE=pres, NUM=pl] -> 'disappear' | 'walk'
    V[SUBCAT=trans, TENSE=pres, NUM=pl]   -> 'see' | 'like'
    V[SUBCAT=clause, TENSE=pres, NUM=pl]  -> 'say' | 'claim'
    
    V[SUBCAT=intrans, TENSE=past, NUM=?n] -> 'disappeared' | 'walked'
    V[SUBCAT=trans, TENSE=past, NUM=?n]   -> 'saw'  | 'liked'
    V[SUBCAT=clause, TENSE=past, NUM=?n]  -> 'said' | 'claimed'

Instead of defining this top down, we can use the sub-category to define the
valency of the productions. So a verb like `put` may require `NP` and `PP`
compliments. When one of the arguments is bound, they sub-category can be
reduced until it is an empty list and thus a valid production rule:

.. code-block:: text

    V[SUBCAT=<>]
    |   |
    NP  V[SUBCAT=<NP>]
    |   |
    |   V[SUBCAT=<NP, PP, PP>]
    |   |   |        |
    |   |   NP       PP
    |   |   |        |
    kim put the book on the table

Another feature that we might like to add is the head and child of a phrase
(although not all phrases have a head like coordinate phrases):

* V (verb) are heads of VP
* N (noun) are heads of NP
* A (adjective) are heads of AP
* P (prepositions) are heads of PP

This is addressed with *X-Bar* syntax by abstrating out the notion of phrasal
level. All phrase types should share a structural similarity:

* `N''` -> NP  (a student of French) ; maximal projection
* `N'`  -> NOM (student of French) ; phrasal projection
* `N`   -> N   (student) ; head of phrase ; zero projection

.. code-block:: text

    S        -> N[BAR=2] V[BAR=2]
    N[BAR=2] -> Det N[BAR=1]
    N[BAR=1] -> N[BAR=1] P[BAR=2]
    N[BAR=1] -> N[BAR=0] P[BAR=2]
    N[BAR=1] -> N[BAR=0]XS


Verbs that can be positioned initially in inverted clauses belong to the class
known as auxiliaries. They can be captured with: `S[+INV] -> V[+AUX] NP VP`.

For cases where there are gaps, we can use *slash* categories to add the notion
that a value will be missing (S[+INT]/NP). This gets reduced to a feature of
the word to the left `S[SLASH=NP]`:

* Who do you like __? 
* Who do you claim that you like __?
* Who do you claim that Jody says that you like __?

--------------------------------------------------------------------------------
Chapter 10: Analyzing the Meaning of Sentences
--------------------------------------------------------------------------------

.. todo:: finish http://www.nltk.org/book/ch10.html

--------------------------------------------------------------------------------
Chapter 11: Managing Linguistic Data
--------------------------------------------------------------------------------

.. todo:: finish http://www.nltk.org/book/ch11.html
