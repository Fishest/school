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
