================================================================================
Functional Paper Summaries
================================================================================

--------------------------------------------------------------------------------
Universality of Fold
--------------------------------------------------------------------------------

https://www.cs.nott.ac.uk/~gmh/fold.pdf

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The fold Operator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The fold operator for lists can be defined as follows:

.. code-block:: haskell

    fold :: (a -> b -> b) -> b -> ([a] -> b)
    fold f v []      = v
    fold f v (x::xs) = f x (fold f v xs)

Using fold we can define a collection of common operators:

.. code-block:: haskell

    sum :: [Int] -> Int
    sum = fold (+) 0

    product :: [Int] -> Int
    product = fold (*) 1

    and :: [Bool] -> Bool
    and = fold (&) True

    or :: [Bool] -> Bool
    or = fold (|) False

Furthermore we can define a number of the common list operations as fold
operations:

.. code-block:: haskell

    (++) :: [a] -> [a] -> [a]
    (++ xs) = fold (:) xs

    length :: [a] -> Int
    length = fold (\x n -> 1 + n) 0

    reverse :: [a] -> [a]
    reverse = fold (\x xs -> xs ++ [x]) []

    map :: (a -> b) :: ([a] -> [b])
    map f = fold (\x xs -> f x : xs) []

    filter :: (a -> Bool) :: ([a] -> [a])
    filter p = fold (\x xs -> if p x then x : xs else xs) []

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Universal Property of fold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The universal property of fold can be used to prove that two functions on lists
are equal without resorting to proof by induction. The proof also shows that
`fold` is the unique solution to solving this problem.

Continuing, the universal property can also be used as a guide for converting
recursive functions to fold by solving for `v` and `f`.

.. code-block:: haskell

    h w       = v          => h . fold g w = fold f v
    h (g x y) = f x (h y)

Fold can also be composed with another function as follows (fusion property).

.. code-block:: haskell

    // for sum
    (+ a) . fold (+) b = fold (+) (a + b)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generating Tuples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can make fold more powerful by using datatypes instead of simple primitives.
Here is an example using tuples:

.. code-block:: haskell

    sumlength :: [Int] -> (Int, Int)
    sumlength = fold (\x (s,l) -> (s + x, l + 1)) (0, 0)

Some functions cannot be described directly using fold, but by using a companion
function. In summary, any function that can be defined by pairing :

.. code-block:: haskell

    // original defintion
    dropwhile :: (a -> Bool) -> ([a] -> [a])
    dropwhile p [] = []
    dropwhile p (x:xs) = if p x then dropwhile p xs else x:xs

    // using a helper function to grab the free variable xs
    dropwhile' :: (a -> Bool) -> ([a] -> ([a], [a]))
    dropwhile' p = fold f v
      where
        f x (ys, xs) = (if p x then ys else x:xs, x:xs)
        v            = ([], [])

    dropwhile :: (a -> Bool) -> ([a] -> [a])
    dropwhile p = fst . dropwhile' p

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Primitive Recursion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any recursive function on lists can be redefined using fold and tuples. The
basic building blocks for a fold function are:

.. code-block:: haskell

    // for a function h on a list
    h []     = v           => h = fold g v
    h (x:xs) = g x (h xs)

    // for a function h on a list and a base case y
    h y []     = f y             => h y = fold (g y) (f y)
    h y (x:xs) = g y x (h y xs)

    // primitive recursion
    h y []     = f y
    h y (x:xs) = g y x xs (h y xs)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Using fold to Generate Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: haskell

    compose :: [a -> a] -> (a -> a)
    compose = fold (.) id

We can also create functions that fold left (say to process an infinite list in
constant time):

.. code-block:: haskell

    suml :: [Int] -> Int
    suml xs = suml' xs 0
      where
        suml' [] n = n
        suml' (x:xs) n = suml' xs (n + x)

    // redefined using fold
    suml' :: [Int] -> (Int -> Int)
    suml' = fold (\x g -> (\n -> g (n + x))) id

    // redefined using the helper function and fold
    suml :: [Int] -> Int
    suml xs = fold (\x g -> (\n -> g (n + x))) id xs 0

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
foldl
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can generalize the folding of a collection from left to right with the
`foldl` operator:

.. code-block:: haskell

    foldl :: (b -> a -> b) -> b -> ([a] -> b)
    foldl f v []     = v
    foldl f v (x:xs) = foldl f (f v x) xs

    // fold can be defined with foldl, but not vice versa
    foldl f v xs = fold (\x g -> (\a -> g (f a x))) id xs v

We can now redefine functions simply using `foldl`:

.. code-block:: haskell

    suml :: [Int] -> Int
    suml = foldl (+) 0

    reverse :: [a] -> [a]
    reverse = foldl (\xs x -> x : xs) []

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Ackerman Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: haskell

    // using peano numbers instead of reals
    ack :: [Int] -> ([Int] -> [Int])
    ack [] ys         = 1:ys
    ack (x:xs) []     = ack xs [1]
    ack (x:xs) (y:ys) = ack xs (ack (x:xs) ys)

    // using fold twice
    ack :: [Int] -> ([Int] -> [Int])
    ack = fold (\x g - > fold (\y -> g) (g [1])) (1:)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Other Fold Recursion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* fold for regular datatypes
* fold for nested datatypes
* fold for functional datatypes
* monadic fold for imperitive code
* relational fold
* automatic program transformation
* new programming languages
