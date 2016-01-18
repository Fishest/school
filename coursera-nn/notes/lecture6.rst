================================================================================
Lecture 6: Gradient Descent
================================================================================

--------------------------------------------------------------------------------
Overview of Mini Batch Gradient Descent
--------------------------------------------------------------------------------

For stochastic gradient descent, if the dataset is highly redundant you can
compute the gradient of the weights with the first half of the dataset and then
use the second half for the next weight update. In the extreme version we can
do this with a single example at a time to perform an online algorithm (each new
sample is run). However, mini-batch is generally better than online:

* less computation is used than online
* with many cases at once, matrix-matrix multiples can be done in parallel on GPU
* mini-batches must be balanced for all the classes
* this can be approximated by sampling your data in random order

A summary of mini-batch gradient descent is as follows:

1.  Guess and initial learning rate
1a. if the error gets worse or oscillates wildly, decrease the rate
1b. if the error is falling consistently but slowly, increase the rate
2.  Write a program to automate changing the learning rate
3.  Near the end of the algorithm, turn down the learning rate
3a. this removes fluctuations in the final weights by the mini-batches
4.  Turn down the learning rate when the error stops decreasing
4a. use the error on a separate validation set (not used for learning or final test)
