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
