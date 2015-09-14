================================================================================
Lecture 4: Learning the Next Word
================================================================================

--------------------------------------------------------------------------------
Learning to Predict the Next Word
--------------------------------------------------------------------------------

The presented neural network attempts to encode relationships about family
structure. The first hidden layer is six neurons which takes convolved inputs
from a first layer network (each neuron representing a single person (1/0)).
This hidden layer creates a bottleneck that attempts to learn features from
the raw inputs. The next slide shows a view of how each input causes a response
in each neuron (the learned features):

- English / Italian is one neuron (English is positive, Italian is negative)
- left / right branch of tree (left is positive, right is negative)
- ancestors are incoded in another tree (older his positive, younger is negative)

If we have a large database of relationship triples `(a relationship b)`, we could
run it through a similar network and produce a knowledge neural network.

* https://www.freebase.com/
* http://wiki.dbpedia.org/

--------------------------------------------------------------------------------
The Softmax Output Function
--------------------------------------------------------------------------------

This is a way to make the outputs of a neuron sum to 1 so they can easily
represent a PDF of the mutually probable outcomes.

Shortcomings with the squared error cost function:

- if the desired output is 1 and the output is 0.00001, there is no gradient
  for a logistic unit that can fix this error.
- if the outputs don't sum to 1, there is no good way to compute a probability

We can solve this by forcing the outputs to model a PDF:

.. code-block:: math

    y_i = \frac{e^z_i}{\sum_{j \set group} e^z_j}
    z_i = logic for y_i
    z_j = all logics for that group
    y_i = output of neuron

    \frac{\partial y_i}{\partial z_i} = y_i * (1 - y_i)

The correct cost function is cross-entropy. `C` has a large gradient change
when the target value is `1` and the output is almost `0`. So this will case
a large update when different and a small update when getting closer.

.. code-block:: math

    C = - \sum_j t_j * log(y_j)
    t = target value

    \frac{\partial C}{\partial z_i}
      = \sum_j \frac{\partial C}{\partial y_j} * \frac{\partial y_j}{\partial z_i}
      = y_i - t_i

--------------------------------------------------------------------------------
Neuro-Probabilistic Language Models
--------------------------------------------------------------------------------

We cannot model speech recognition systems using audio waves alone as the input
world is too messy. As such, we need to add some statistical model to help us
guess what the correct next word should be. For this we can use something simple
like the Trigram Model (we stick to 3 because otherwise we will have probabilities
of zero most examples):

.. code-block:: math

    P(w_3 = c | w_1 = a, w_2 = b) = count(abc)
    ----------------------------    ---------
    P(w_3 = d | w_1 = a, w_2 = b) = count(abd)

The trigram model also fails to understand similar words / sentences. It only uses
the words it sees. We can do better by converting the words into features and using
them to train a model (Bengio's Model).

.. code-block:: text

    [          large softmax units (one per word)         ] (must be 100,000 or more)
    |                          |                          |
    | [predict output word from features of input words]  | (need lots of training data)
    |            |                           |            |
    [learned encoding word t_1] [learned encoding word t_2] (may overfit and must be small)
    |                                                     |
    [index at word t_1]                 [index at word t_2] (basically a lookup table)

How can we deal with the large number of outputs? We can instead create a serial
architecture where we run each candidate word through as an input with the previous
two words. Then the final output is a logic score for that candidate word. We can
then choose the word with the largest response. Another idea is to train a model that
outputs a feature vector that maps to nodes in a tree. Then to find the correct word,
we use the feature vector to choose "left or right."

Another idea is to train a general feature representation for a window of words (size 11).
We then can replace a word in the middle with the correct word or a random word. The output
should respond highly if the word is good and low if it does not. This network can then
be used for a number of different NLP tasks.

We can look at how the newtork learns similar words by mapping them to a 2D embedding such
that similar words are clustered with each other. We can also use `t-sne` to place similar
clusters near each other as well. We can train this example simply using strings of words
from Wikipedia (no supervision). The network can predict word meanings simply from context.
