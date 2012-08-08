--------------------------------------------------------------------------------
 Starting Out 
--------------------------------------------------------------------------------

* True, False == not(True)
* prefix function -> f a b (+ 1 2)
* infix function  -> a f b (1 + 2)
* prefix to infix ->  a `f` b
* functions are called by function name and spaces before parameters
* lists:

  - defined -> [] -> [1] ++ [2,3] -> [1,2,3], 5 : [1,2,3] -> [5,1,2,3]
  - linked lists (right append is expensive)
  - [1,2,3] !! 1 -> 2
  - <, >, >=, <=, == compare lists in lexicographical order
  - compare returns GT, LT, EQ
  - head, tail, last, init -> throw on empty lists
  - lenght, null, reverse, take, drop
  - maximum, minimum, sum, product 
  - 2 `elem` [1,2,3] -> True (think 2 in [])

* ranges:

  - defined -> [1..20], [2,4..20], [20, 19..1]
  - infinite list -> [1..]
  - cycle [1,2,3] -> repeats [1,2,3]
  - repeat 3 -> infinite list of 3
  - replicate 3 10 -> [10, 10, 10]

* list comprehensions:
 
  - defined -> [x*2 | x <- [1..10]]
  - condition -> [x*2 | x <- [1..10], x*2 >= 12]
  - filter -> [x | x <- [1..100], x `mod` 7 == 3]
  - replace -> [ if x < 10 then "A" else "B" | x <- xs, odd x]
  - many predicates -> [ x | x <- xs, odd x, even x]
  - many sources `[ x*y | x <- xs, y <- ys]`
  - can nest comprehensions
  - _ unused pattern match `sum [1 | _ <- xs]`

* tuples:

  - defined ('a', 1, "string") 
  - tuples are strongly typed! [(1, 'a'), ('b', 2, 3)] <- error 
  - fst and snd return first and second value of tuple (of a tuple pair)
  - zip xs ys -> [(x1, y1)..(xn,yn)] <- final lenght is of shortest list

--------------------------------------------------------------------------------
 Types and Typeclasses
--------------------------------------------------------------------------------

* can get type with `:t value`
* type inference through and through (unless we get lost)
* f :: Int -> Int -> Int -> Int (function that takes three ints and returns one)
* Int and Integeger (big int)
* String == [Char]
* type variable == generic
* functions that take type variables are polymorphic functions
* class constraint (==) :: (Eq a) => a -> a -> Bool
  - Eq a type that tests for equality (==)
  - Ord a type that has some kind of ordering (>, <)
  - Show a type that can be converted to a string -> show True
  - Read a type that can be converted from a string to a type::
    
    read "True" || False
    read "1" :: Int
    read "(3, 'a')" :: (Int, Char)

  - Enum a type that is a sequentiall ordered type::

    [LT .. GT]
    pred (succ LT)

  - Bounded a type that has an upper and lower bound::

    minBound :: Int
    maxBound :: Int
	maxBound :: (Bool, Int, Char)

  - Num a type that can act like a number
  - Integral (Int, Integer), Floating (Float, Double)
  - Use fromIntegral to convert Integral to Num

--------------------------------------------------------------------------------
 Syntax in Functions
--------------------------------------------------------------------------------

  - pattern matching::

    lucky :: (Integral a) => a -> String
    lucky 7 = "lucky number"
    lucky x = "unlucky number"

    factorial :: (Integral a) => a -> a
    factorial 0 = 1
    factorial x = x * factorial (x - 1)

    first  :: (a,b,c) -> a
    first     (a,_,_)  = a

    second :: (a,b,c) -> b
    second    (_,b,_)  = b

    third  :: (a,b,c) -> c
    third     (_,_,c)  = c

  - lookup order is defined as top to bottom
  - always define a catch all, otherwise you are going to throw
  - in list comprehensions, a failure will just skip the element::

    xs = [(1,2), (3, 4), (5,6)]
    [a + b | (a, b) <- xs]

  - Can match lists on any pattern of `:`::

    head :: [a] -> a
    head []         = error "Empty list"
    head (x:_)      = x # first:ignore the rest
    head (x:xs)     = x # first:rest
    head (x:y:[])   = x # two elements in the list
    head (x:y:z:[]) = x # three elements in the list

    length' :: (Num b) => [a] -> b  
    length' [] = 0  
    length' (_:xs) = 1 + length' xs  

  - to split a patten and keep the original `all@(x:xs)`
  - guards are basically cond statements (scala style)::

    tester1 :: (RealFloat a) => a -> String
    tester1 value
      | value <= 10.0 = "small value"
      | value <= 20.0 = "medium value"
      | otherwise     = "large value"

    max' :: (Ord a) => a -> a -> a
    max' a b | a > b = a | otherwise = b

    tester2 :: (RealFloat a) => a -> b -> String
    tester2 weight height
      | value <= small  = "small value"
      | value <= medium = "medium value"
      | otherwise       = "large value"
      where value = weight / height ^ 2
            (small, medium) = (10.0, 20.0)

    initials = String -> String -> String
    initials firstname lastname = [f] ++ ". " ++ [l] ++ "."
      where (f:_) = firstname
            (l:_) = lastname

    calcBmi :: (RealFloat a) => [(a, a)] -> [a]
    calcBmi xs = [bmi w h | (w, h) <- xs]
      where bmi weight height = weight / height ^ 2

    calcBmi :: (RealFloat a) => [(a, a)] -> [a]
    calcBmi xs = [bmi | (w, h) <- xs, let bmi = w / h ^ 2, bmi >= 25.0]

  - if no otherwise is defined and no match is made, an error is thrown
  - where clauses are local to the guard (not global namespace)
  - where clauses can be nested
  - let bindings are expressions give immediate scope (not across guards)::

    let <bindings> in <expression>
    cylinder :: (RealFloat a) => a -> a -> a ->
    cylinder r h = 
      let sidearea = 2 * pi * r * h
          toparea  = pi * 2 ^ 2
      in  sidearea + 2 * toparea

  - case (expressions) are basically pattern matchers::

    case expression of pattern -> result
                       pattern -> result
                       pattern -> result

    -- if no case is matched and we fall through, an error is thrown
    describe :: [a] -> String
    describe xs = "The list is " ++ case xs of []  -> "empty"
                                               [x] -> "a singleton list"
                                               xs  -> "a longer list"

--------------------------------------------------------------------------------
 Recursion
--------------------------------------------------------------------------------

  - in haskell, describe what something is and not how to get it::

    replicate' :: (Num i, Ord i) => i -> a -> [a]  -- multiple interfaces for i
    replicate' n x  
        | n <= 0    = []  
        | otherwise = x:replicate' (n-1) x 

    take' :: (Num i, Ord i) => i -> [a] -> [a]  
    take' n _ | n <= 0 = []  
    take' _ []         = []  
    take' n (x:xs) = x : take' (n-1) xs  

    repeat' :: a -> [a]
    repeat' x = x : repeat' x

    zip' :: [a] -> [b] -> [(a,b)]
    zip' [] _ = []
    zip' _ [] = []
    zip' (x:xs) (y:ys) = (x,y) : zip' xs ys

    elem' :: (Eq a) => a -> [a] -> Bool
    elem' a [] = False
    elem' a (x:xs)
      | a == x    = True
      | otherwise = elem' a xs

    quicksort :: [Ord a] => [a] -> [a]
    quicksort [] = []
    quicksort (x:xs) = 
      let smaller = quicksort [a | a <- xs, a <= x]
          bigger  = quicksort [a | a <- xs, a  > x]
      in smaller ++ [x] ++ bigger

--------------------------------------------------------------------------------
 Higher Order Functions
--------------------------------------------------------------------------------

  - functions in haskell take a maximum of one argument (the rest is curried)
  - function application / partially applied functions (currying)::
  
    let minOf4 = max 4
    minOf4 2

  - higher order functions == functions as data::

    apply2 :: (a -> a) -> a -> a -- function -> input -> return
    apply2 f x = f (f x)

    zipWith' :: (a -> b -> c) -> [a] -> [b] -> [c] 
    zipWith' _ [] _ = []
    zipWith' _ _ [] = []
    zipWith' f (x:xs) (y:ys) = f x y : zipWith' f xs ys

    flip' :: (a -> b -> c) -> (b -> a -> c)
    flip' f x y = f y x

  - map takes a function and a list and applies that function to each
    element in the list::

    map :: (a -> b) [a] -> [b]
    map _ [] = []
    map f (x:xs) = f x : map f xs

    [f x | x <- xs] -- essentially map

  - filter takes a predicate and a list and extracts the elements
    where the predicate is true::

    filter :: (a -> Bool) -> [a] -> [a]
    filter _ [] = []
    filter f (x:xs)
      | f x       = x : filter f xs
      | otherwise = filter f xs

    [x | x <- xs, f x] -- essentially filter

  - takeWhile lets you consume an infinite list until a predicate
    evaluates to false. Also, interesting::

    let listofFuncs = map (*) [0..] -- [(0*), (1*), (2*)...]
    ((listofFuncs !! 4) 5)  -- (4*) 5

  - anonymous functions with lambdas::

    (\xs -> length xs > 15) [1,2,3,4,5]

    -- if pattern matching fails in a lambda, an error is thrown
    (\(a, b) -> a + b)(1,2)

    -- the following two are functionally equal because
    -- haskell natively curries every function
    example :: (Num a) => a -> a -> a-> a
    example x y z = x + y + z
    example = \x -> \y -> \z -> x + y + z

  - folds::
 
    -- fold left folds from the left
    sum' :: (Num a) => [a] -> a
    sum' xs = foldl (\acc x -> acc + x) 0 xs
    sum' = foldl (+) 0 -- and shorter because of currying!

    -- fold right folds from the right
    sum' :: (Num a) => [a] -> a
    sum' xs = foldr (\x acc -> acc + x) 0 xs

    -- consing to a list is cheaper than ++, so to build lists, foldr
    map' :: (a -> b) => [a] -> [b]
    map' xs = foldr (\x acc -> f x : acc) [] xs

    -- foldr works on infinite lists, foldl does not
    -- foldl1 foldr1 use the first or last value as the starting accumulator
    -- make sure there is at least one element though or they will throw

  - rebuilding the world with folds::

    max :: (Ord a) => [a] -> a
    max = foldr1 (\x acc -> if x > acc then x else acc)

    prod :: (Num a) => [a] -> a
    prod = foldr1 (*)

    reverse :: [a] -> [a]
    reverse = foldl (\acc x -> x : acc) []

    filter :: (a -> Bool) -> [a] -> [a]
    filter p = foldr (\x acc -> if p x then x : acc else acc) []

    sum :: (Num a) => [a] -> a
    sum = foldr1 (+)

    head :: [a] -> a
    head  = foldr1 (\x _ -> x)

    last :: [a] -> a
    last  = foldl1 (\_ x -> x)

    foldl f a xs = foldr (\x g a -> g(f x a)) id xs a

  - scanning records the intermediate accumulator states::

    scanl (+) 0 [3,5,2,1] -- [0,1,3,8,11]
    scanr (+) 0 [3,5,2,1] -- [11,8,3,1,0]
    -- scanl1 and scanr1 also exist

  - can change the function application to right associative with $::

    sum (map sqrt [1..130])
    sum $ map sqrt [1..130] -- same effect

    sum (filter (> 10) (map (*2) [2..10]))
    sum $ filter (> 10) $ map (*2) [2..10]

    -- function application is a function,
    -- so we can map the application on to other functions
    map ($ 3) [(4+), (10*), (^2), sqrt]

  - function composition operator (.)::

    (.) :: (b -> c) -> (a -> b) -> a -> c
    f . g = \x -> f $ g x

    -- function composition is right associative
    map (negate . sum . tail) [[1..5], [3..6], [1..7]]

    -- can partially apply functions
    sum . replicate 5 . max 6.7 $ 8.9

    -- point free style
    sum xs = fold (+) 0 xs
    sum = fold (+) 0 -- xs is curried, point free style

    fn x = ceiling (negate (tan (cos (max 50 x))))
    fn x = ceiling . negate . tan . cos . max 50

  - use function composition or let clauses to store intermediate results
    to make the code more readable.

--------------------------------------------------------------------------------
 Modules
--------------------------------------------------------------------------------

  - Prelude module is imported by default and contains all common methods
  - Modules must be imported before defining any functions::

    import <module name>                        -- import all of module
    import <module name> (function1, function2) -- only import fx1 and fx2
    import <module name> hiding (function1)     -- prevent fx1 import
    import qualified <module name>              -- import with fq name
    import qualified <module name> as M         -- import with fq name of M

  - Data.List::

    intersperse '.' "name"          -- "n.a.m.e"
    intercalate [1,1] [[2,2],[3,3]] -- [2,2,1,1,3,3]
    transposea  [[1,2,3],[4,5,6]]   -- [[1,4],[2,5],[3,6]]
    foldl' foldr'                   -- strict, non-lazy verions
    concat ["a", "b", "c"]          -- "abc"
    concatMap (replicate 2) [1..4]  -- [1,1,2,2,3,3,4,4]
    and or                          -- boolean and/or on a list
    any (==4) [1,2,3,4]             -- True
    all (==4) [1,2,3,4]             -- False
    take 5 $ iterate (*2) 1         -- [1,2,4,8,16]
    splitAt 3 "galen"               -- ("gal", "en")
    takeWhile (/=' ') "this is a"   -- "this"
    dropWhile (/=' ') "this is a"   -- " is a"
    span                            -- (what takeWhile grabbed, what it didn't)
    break                           -- (split where predicate is true, afterwards)
    isInfixOf                       -- checks if sublist is in a list
    isPrefixOf, isSuffixOf          -- same but for start and end
    elem, notElem                   -- check if element is (not)in a list
    partition                       -- splits list in two based on a predicate result
    find                            -- gets the first element in list that satisfies predicate (Maybe)
    elemIndex                       -- like elem, but returns the index of the value (Maybe)
    elemIndices                     -- returns every index that matches element
    findIndex                       -- like elemIndex, but with a predicate
    findIndices                     -- like elemIndices, but with a predicate
    zip, zipWith                    -- combine two sequences, with a combining function
    zipN, zipWithN                  -- combine N sequences up to 7
    lines                           -- splits text into list of lines split at '\n'
    unlines                         -- rejoins lines into a single string
    words, unwords                  -- split/join sentence/words into tokens/string
    nub [1,2,3,2,3,2,3,4,1,2]       -- [1,2,3,4]    -- removes duplicates
    delete w "hello world"          -- "hello orld" -- deletes first occurence of element
    sort [3,4,1,2]                  -- [1,2,3,4]
    group [1,1,1,2,2,3,2,3,3]       -- [[1,1,1], [2,2], [3] ,[2], 3,3]]
    tails, inits                    -- return list of each incrementing tail/init
    [1..10] \\ [2,5,9]              -- [1,3,4,6,7,8,10] -- list difference
    union, intersect                -- behave like the set functions
    insert 4 [1,2,3,5,2,6]          -- [1,2,3,4,5,2,6] -- insert into a sorted list
    generic{Take, Drop, SplitAt}    -- work with Num instead of Int
    generic{Index, Length, Replicate} -- work with Num instead of Int
    nubBy, deleteBy, unionBy        -- Counterparts that let you specify the predicate
    insersectBy, groupBy            -- instead of defaulting to ==
    sortBy, insertBy,
    maximumBy, minimumBy

    -- the following are functionally equivalent,
    -- group by postive and negative groups
    groupBy (\x y -> (x > 0) == (y > 0)) values
    groupBy ((==) `on` (> 0)) values
    
    sortBy (compare `on` sum) [[1,2,3],[4,5,6], [7,8,9]]

  - Data.Char is fully of methods to test if the char is X::

    any isSpace "my name is" -- True
    all isSpace "my name is" -- False
    generalCategory ' '      -- Space
    generalCategory 'a'      -- LowercaseLetter

  - Example of using some utilities to create the caesar cypher::

    encode :: Int -> String -> String
    encode shift msg =
      let ords   = map ord msg
          shifts = map (+ shift) ords
      in map chr shifts

    decode :: Int -> String -> String
    decode shift msg = encode (negate shift) msg
 
  - To import fully qualified, `import qualified Data.Map as Map`
  - Data.Map (also known as a dictionary...or an ordered tuple tree)::
    
	fromList                         -- converts a list of tuples to a map
	empty                            -- generates an empty map
	insert "key" "value"  Map.empty  -- inserts a tuple into the map
	null Map.empty                   -- True, checks if map is empty
	size Map.empty                   -- 0, reports size of the map
	singleton 3 9                    -- insert 3 9 Map.empty
	lookup key                       -- looks for value by key
	member key                       -- checks to see if key is in the map
	map,filter                       -- much the same
	toList                           -- the inverse of from list
	keys                             -- map fst . toList
	elems                            -- map snd . toList
	fromListWith                     -- from list with a combining function (for dups)
	insertWith                       -- insert with a combining function (for dups)
	
	fromList' = foldr (\(k, v) acc -> Map.insert k v acc) Map.empty
	fromListWith max [(1,0), (1,9)]  -- [(1,9)]
	fromListWith (+) [(1,4), (1,5)]  -- [(1,9)]

  - To import fully qualified, `import qualified Data.Set as Set`
  - Data.Set::

    fromList "hello world"           -- "dehlorw"
    intersection                     -- perform the set intersection
    difference                       -- perform the set difference
    union                            -- perform the set union
    null, size, member, empty        -- methods you know and love
    singleton, insert, delete
    isSubsetOf, isProperSubsetOf     -- proper means has more values
    map, filter

  - it is faster to get a unique list by converted to and from a set than by using nub::

    setNub xs = Set.toList $ Set.fromList xs -- however this breaks the original ordering

  - To define your own module::

    module Geometry.Sphere -- located in Geometry/Sphere.hs
    ( sphereVolume  -- specifically define which functions are exported
    , sphereArea
    ) where

    sphereVolume :: Float -> Float
    sphereVolume radius = (4.0 / 3.0) * pi * (radius ^ 3)
    
    sphereArea :: Float -> Float
    sphereArea radius = 4 * pi * (radius ^ 2)

--------------------------------------------------------------------------------
 Making Types and Typeclasses
--------------------------------------------------------------------------------

  - can define new data types quickly with the data keyword::

    data Bool = False | True
    data Point = Point Float Float deriving (Show)
    data Share = Circle Point Float | Rectangle Point Point deriving(Show)

    nudge :: Shape -> Point -> Shape
    nudge (Circle (Point x y) r) (Point a b) = Circle (Point (x + a) (y + b)) r
    nudge (Rectangle (Point x1 y1) (Point x2 y2) ) (Point a b) = Rectangle (Point (x1 + a) (y1 + b)) (Point (x2 + a) (y2 + b))

  - can export value constructors like the following::

    modules Shapes
    ( Point(..)
    , Shape(..) -- import all Shape, or just Circle, or Rectangle
    ) where     -- if you hide the constructor, users cannot pattern match

  - the record syntax of describing a type::

    data Person = Person { firstName :: String
                         , lastName  :: String
                         , age :: Int
                         , height :: Float
                         , phoneNumber :: String
                         } deriving (Show)

  - Type constructor is basically a generic::

    data Maybe a = Nothing | Just a -- Maybe is not a type
    Maybe Int                       -- Maybe Int is though

    data (Ord K) => Map k v = ...   -- type class constraint, however
                                    -- don't do this as you will have to specify everywhere
                          
  - Some typeclasses give us automatic candy::

    data Person = Person { firstName :: String
                         , lastName  :: String
                         , age :: Int
                         } deriving (Show, Eq, Read) -- can string, read, and ==

    -- Haskell enumerations
    data Day = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday   
               deriving (Eq, Ord, Show, Read, Bounded, Enum)  

  - Use maybe if you know why it failed (one error condition). Use either
    if there are multiple reasons why the failure occurred and we need to
    know why::
    
    data Either a b = Left a | Right b deriving (Eq, Ord, Read, Show)
    Left  "this is the error condition"
    Right "this is the success result"

  - type snyonyms give us a better name (typedef), are not ctors, just types::

    type String = [Char]
    type PhoneNumber = String  
    type Name = String  
    type PhoneBook = [(Name,PhoneNumber)]  

    inPhoneBook :: Name -> PhoneNumber -> PhoneBook -> Bool       -- now we have this
    inPhoneBook :: String -> String -> [(String, String)] -> Bool -- instead of this

    type AssocList k v = [(k,v)]   -- parameterized types
    type IntMap v = Map Int v      -- partially applied types

  - let's make a tree::

    data Tree a = EmptyTree | Node a (Tree a) (Tree a) deriving (Show, Read, Eq)
    
    singleton :: a -> Tree a
    singleton x = Node x EmptyTree EmptyTree
    
    treeInsert :: (Ord a) => a -> Tree a -> Tree a
    treeInsert x EmptyTree = singleton x
    treeInsert x (Node a left right)
        | x == a = Node x left right
        | x  < a = Node a (treeInsert x left) right
        | x  > a = Node a left (treeInsert x right)
    
    treeElem :: (Ord a) => a -> Tree a -> Bool
    treeElem x EmptyTree = False
    treeElem x (Node a left right)
        | x == a = True
        | x  > a = treeElem x right
        | x  < a = treeElem x left

    let numbers = [1,5,6,7,4,6,78,56,0]
    foldr treeInsert EmptyTree numbers -- build a tree with fold!
    
  - typeclasses (mixins), lets learn how to make them::

    class Eq a where  
        (==) :: a -> a -> Bool  
        (/=) :: a -> a -> Bool  
        x == y = not (x /= y)         -- recursively defined in terms of the other
        x /= y = not (x == y)  

    data TrafficLight = Red | Yellow | Green
    instance Eq TrafficLight where          -- if we just inherit from Eq, it does this
        Red == Red       = True             -- minimal complete definition
        Green == Green   = True
        Yellow == Yellow = True
        _ == _           = False

    instance Show TrafficLight where
        show Red    = "Red Light"
        show Green  = "Green Light"
        show Yellow = "Yellow Light"

    instance (Eq m) => Eq (Maybe m) where  
        Just x == Just y = x == y  
        Nothing == Nothing = True  
        _ == _ = False  
 
  - map is an implemenation of fmap (which is like bind map)   
  - examine typeclasses with :info
  - examine type kinds with :k

--------------------------------------------------------------------------------
 Input / Output
--------------------------------------------------------------------------------

  - Doing input::

    putStrLn "something"
    :t putStrLn :: IO ()                    -- IO that returns an empty tuple

    name <- getLine                         -- binds result of IO to name
    :t getLine getline :: IO String

  - main functions are placed in a do block::

    main = do
      foo  <- putStrLn "Insert your name "  -- foo contains ()
      name <- getLine                       -- name contains  :: String
      namex = getLine                       -- namex contains :: IO String
      putStrLn ("Hello" ++ name)            -- have to leave the result for the do block

  - IO operations will only occur within main, or another IO action in a do block
  - `return` makes a monad out of anything, `return "string"`, it does not leave the
    current execution scope.
  - other IO functions(which are lazy)::

    putChar						-- write one character
    putStr                      -- map x putChar
    putStrLn                    -- putStr (x + "\n")
    print                       -- putStrLn . show x

    getChar						-- read one character
    getLine						-- read until \n
    getContents					-- read until EOF

    when                        -- if (bind x predicate) inner(x) else return()
    sequence                    -- peform a list of IO operations
    mapM, mapM_                 -- map over an IO sequence
    forM                        -- like mapM, for [] (\a -> do ...)
    forever                     -- perform a do operation forever
    interact                    -- takes an input line and performs an action on it
    openFile                    -- opens a file in the specified mode

    hGetContents                -- read the contents from a file handle
    hClose                      -- closes a file handle
    hGetLine
    hGetChar
    hPutStr
    hPutStrLn
    hFlush
    readFile                    -- return a stream given a file
    writeFile                   -- store a stream to a file
    appendFile                  -- append a stream to a file
    withFile                    -- does openFile and hClose when leaving scope

    withFile "input.txt" ReadMode (\handle -> do
        contents <- hGetContents handle
        putStr contents)

  - can handle the lazy buffering with the hSetBuffering function::

    hSetBuffering handle NoBuffering               -- no buffering
    hSetBuffering handle LineBuffering             -- newline buffering    
    hSetBuffering handle BlockBuffering (Nothing)  -- block buffering decided by os
    hSetBuffering handle BlockBuffering (Maybe 64) -- block buffering of 64 bytes

  - random takes a StdGen (random source) to generate random types::

    random (mkStdGen seed) :: (type, StdGen)        -- how to use random
    random (mkStdGen 100)  :: (Int, StdGen)         -- get a random int
    randoms (mkStdGen 100) :: [Int]                 -- get an infinite random int list
    randomR (1,6) (mkStdGen 234)                    -- range the random result
    randomRs (1,6) (mkStdGen 234)                   -- range the infinite random result
    getStdGen                                       -- get a true source of randomness
    newStdGen                                       -- get an updated source of randomness (copy)

    -- instead of feeding the resuling generator back, use randoms
    take 5 $ randoms (mkStdGen 11) :: [Int]

    randoms' :: (RandomGen g, Random a) => g -> [a]  
    randoms' gen = let (value, newGen) = random gen in value:randoms' newGen  

  - try catch exist::

    method `catch` handler
    handler :: IOError -> IO ()
    handler ex
        | isDoesNotExistError ex = ...
        | otherwise = ioError ex        -- rethrow as IOError

    -- can use the ioe methods to get information about the error

--------------------------------------------------------------------------------
 Reverse Polish
--------------------------------------------------------------------------------

Hey look a calculator::

    import Data.List

    polish :: String -> Float
    polish = head . foldl folder [] . words
        where folder (x:y:ys) "*"  = (x * y):ys
              folder (x:y:ys) "+"  = (x + y):ys
              folder (x:y:ys) "-"  = (y - x):ys
              folder (x:y:ys) "/"  = (y / x):ys
              folder (x:y:ys) "^"  = (y ** x):ys
              folder (x:ys)   "ln" = log x:ys
              folder ys      "sum" = [sum ys]
              folder xs number     = read number:ys

clever things::

    groupsOf :: Int -> [a] -> [[a]]
    groupsOf 0 _  = undefined
    groupsOf _ [] = []
    groupsOf n xs = take n xs : groupsOf n (drop n xs)

--------------------------------------------------------------------------------
 Fmap and functors
--------------------------------------------------------------------------------

  - Included in Control.Monad.Instances
  - fmap is basically bind that maps over the monad internals::

    fmap reverse getline
    fmap 2+ [1,2,3,4,5]
    fmap (\x -> x ++ "!") (Just "hello")

  - functor is a partially applied (r -> a)::

    instance Functor ((->) r) where             -- this is basically function composition
        fmap f g = (\x -> f (g x))              -- think of like fmap = (.)

    :m + Control.Monad.Instances
    fmap (*3) (+100) 4

  - so fmap lifts the value inside the functor
  - Rules::

    fmap id (Just 3) == id (Just 3)
    fmap (f . g) == fmap f . fmap g

--------------------------------------------------------------------------------
 Applicative functors
--------------------------------------------------------------------------------

  - Included in Control.Applicative
  - Basically mapping a partially applied function into a functor. A function can
    then be applied to this that takes said function as a parameter::

      let a = fmap (*) [1,2,3,4]    -- [Integer -> Integer]
      fmap (\f -> f 9) a            -- [9, 18, 27, 36]

  - Applicative defines two methods: pure and <*>::

    -- pure is the simplest context value (Just for Maybe)
    Just (+3) <*> Just 9            -- Just 12
    pure (+3) <*> Just 9            -- Just 12
    pure (+3) <*> Nothing           -- Nothing
    Nothing   <*> Just 9            -- Nothing
    pure (+)  <*> Just 9 <*> Just 3 -- Just 12

    -- a shortcut
    pure f <*> x <*> y == fmap f x <*> y
    f <$> x <*> y      == fmap f x <*> y

  - The list applicative functor applies every function in fs to every element
    in xs. They can also be partially applied::

    [(+), (*)] <$> [1,2] <*> [3,4] -- [4,5,5,6,3,4,6,8]
    (+) <$> (+3) <*> (*100) $ 5 -- 508

  - ZipList can be used to apply a list of applicative functors to a list of elements::

    -- ZipList doesn't implement show, so getZipList is used
    -- (,) == \x y -> (x,y)
    -- (,,) == \x y z -> (x,y,z)
    getZipList $ (+) <$> ZipList [1,2,3] <*> ZipList [100, 100, 100]
    getZipList $ pure (*2) <*> ZipList [100, 100, 100]
    getZipList $ (,,) <$> ZipList "dog" <*> ZipList "cat" <*> ZipList "rat"
    zipWith (\a b -> (a,b)) [1,2,3] ['a', 'b', 'c'] -- [(1,'a'),(2,'b'),(3,'c')]
    -- also zipWith3...zipWith7

  - liftA2 converts a binary function to an applicative function::

    liftA2 (:) (Just 3) (Just [4]) -- Just [3,4]

  - how could we apply a list of applicatives (say [Just 1, Just 2, Just 3]::

    sequenceA :: (Applicative f) => [f a] -> f [a]  
    sequenceA [] = pure []  
    sequenceA (x:xs) = (:) <$> x <*> sequenceA xs 
    -- or with a fold
    sequenceA = foldr (liftA2 (:)) (pure [])  

  - Check a value against a list of predictes::

    map (\f -> f 7) [(>4),(<10),odd]		-- [True,True,True]  
    and $ map (\f -> f 7) [(>4),(<10),odd]	-- True

    sequenceA [(>4),(<10),odd] 7
    and $ sequenceA [(>4),(<10),odd] 7

  - sequenceA converts (Num a) => [a -> Bool] into (Num a) => a -> [Bool]

--------------------------------------------------------------------------------
 newtype
--------------------------------------------------------------------------------

  - can define new types that are simple wrappers with `newtype`, helpful because
    it is faster on the runtime than using data::

	  newtype ZipList a = ZipList { getZipList :: [a] }
	  newtype ZipList a = ZipList { getZipList :: [a] } deriving (Eq, Show)

  - newtype only supports one value constructor and one field
  - type can be thought of as a type synonym
  - newtype can be thought of as a new type wrapper type, usually used to make
    them instances of certain type classes.
  - data is for making a completely new data type

--------------------------------------------------------------------------------
 monoid
--------------------------------------------------------------------------------

* A monoid is when you have an associative binary function and a value which
  acts as an identity with respect to that function::

    -- defined in import Data.Monoid
    mempty			-- polymorphic constant for identity value
    mappend			-- the binary monoid function
    mconcat			-- takes a list of monoid values and reduces them with mappend
                    -- the default implementation is just a foldr with mappend

The monoid laws are as follows::

    mempty `mappend` x = x
    x `mappend` mempty = x
    (x `mappend` y) `mappend` z = x `mappend` (y` mappend` z)

    list -> [] and ++
    mult -> 1  and * /
    add  -> 0  and + -
    bool -> False and || (any)
    bool -> True and && (all)

Here is an example newtype wrapper for the monoid::

    newtype All = All { getAll :: Bool }  
        deriving (Eq, Ord, Read, Show, Bounded)  

    instance Monoid All where  
        mempty = All True  
        All x `mappend` All y = All (x && y) 

--------------------------------------------------------------------------------
Reader/Writer Monad
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
State Monad
--------------------------------------------------------------------------------

How to make the random module stateful::

    import System.Random  
    import Control.Monad.State  
      
    randomSt :: (RandomGen g, Random a) => State g a  
    randomSt = State random  
      
    threeCoins :: State StdGen (Bool,Bool,Bool)  
    threeCoins = do  
        a <- randomSt  
        b <- randomSt  
        c <- randomSt  
        return (a,b,c)  

--------------------------------------------------------------------------------
Either Monad
--------------------------------------------------------------------------------

Either a b can either be a Right value (success) or Left (failure)::

    import Control.Monad.Error

    Left "broken code" >>= \x -> return (x + 1)
    Right 2 >>= \x -> return (x + 1) :: Either String Int

--------------------------------------------------------------------------------
Monad Tools
--------------------------------------------------------------------------------

Here are some helper methods that can be used with monads::

    liftM (is actually fmap, or <$>)
    fmap  :: (Functor f) => (a -> b) -> f a -> f b
    liftM :: (Monad m)   => (a -> b) -> m a -> m b
    liftM f m = m >>= (\x -> return (f x))

    runWriter $ liftM not $ Writer (True, "logging message")
    runWriter $ fmap not $ Writer (True, "logging message")
    runState (liftM (+100) pop) [1,2,3,4]

    -- can make most monads functors by just
    -- 1. making fmap == liftM

    ap (is actually just <*>)
    Just (+3) <*> Just 5
    Just (+3) `ap` Just 5

    -- can make most monads applicative by just
    -- 1. making pure == return
    -- 2. making <*> == ap

    liftA2 == liftM2
    liftAN == liftMN

We can flatten any nested monad type with `join`::

    join :: (Monad m) => m (m a) -> m a
    join mm = mm >>= \x -> x

    join (Just (Just 9))                                    -- Just 9
    join [[1,2,3],[4,5,6]]                                  -- [1,2,3,4,5,6]
    runWriter $ join (Writer (Writer (1, "aaa"), "bbb"))    -- (1, "bbbaaa")
    join (Right (Right 9)) :: Either String Int             -- Right 9

    m >>= f  ==  join (fmap f m)
    join (Right (Left "shit")) :: Either String Int         -- Left "shit"
    runState (join (State $ \s -> (push 10,1:2:s))) [0,0,0] -- ((), [10, 1,2,0,0,0])

We can filter with context with `filterM`::

    filter (\x -> x < 4) [1,2,3,4,5,6]
    keepSmall :: Int -> Writer [String] Bool
    keepSmall x
        | x < 4 = do
            tell ["keeping" ++ show x]
            return True
        | otherwise = do
            tell [show x ++ " is too big"]
            return False

    fst $ runWriter $ filterM keepSmall [1,2,3,4,5,6]
    mapM_ putStrLn  $ snd $ runWriter $ filterM keepSmall [1,2,3,4,5,6]

    powerset :: [a] -> [[a]]
    powerset xs = filterM (\x -> [True, False]) xs

we can do monadic foldl with `foldM`::

    foldl :: (a -> b -> a) -> a -> [b] -> a  
    foldl (\acc x -> acc + x) 0 [2,8,3,1]       -- 14

    foldM :: (Monad m) => (a -> b -> m a) -> a -> [b] -> m a  
    binSmalls :: Int -> Maybe Int
    binSmalls acc x
        | x > 9     = Nothing
        | otherwise = Just (acc + x)
    foldM binSmalls 0 [2,8,3,1]                 -- Just 14
    foldM binSmalls 0 [2,81,3,1]                -- Nothing

monadic composition is `<=<` which is equal to `.`::

    let f = (+1) . (*100)  
    f 4             -- 401
    
    let g = (\x -> return (x+1)) <=< (\x -> return (x*100))  
    Just 4 >>= g    -- 401

    let f = foldr (.) id [(+1),(*100),(+1)]  
    f 3             -- 401


    -- we can repeat a function N times in this way
    import Data.List  
      
    inMany :: Int -> KnightPos -> [KnightPos]  
    inMany x start = return start >>= foldr (<=<) return (replicate x moveKnight)  

--------------------------------------------------------------------------------
Making a monad
--------------------------------------------------------------------------------

Deterministic list with Rationals to be precise (1%4 instead of 0.25),
(note, the percentages should add to 1)::

    import Data.Ratio
    
    newtype Prob a = Prob { getProb :: [(a, Rational)] } deriving Show    

    instance Functor Prob where
        fmap f (Prob xs) = Prob $ map (\(x,p) -> (f x,p)) xs

    flatten :: Prop (Prop a) -> Prop a
    flatten (Prop xs) = Prop $ concat $ map multAll xs
        where multAll (Prop innerxs,p) = map (\(x,r) -> (x, p*r)) innerxs

    instance Monad Prob where
        return x = Prop [(x, 1%1)]
        m >>= f = flatten (fmap f m)
        fail_ = Prop []

--------------------------------------------------------------------------------
Zippers
--------------------------------------------------------------------------------
