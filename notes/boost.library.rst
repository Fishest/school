================================================================================
Boost Libraries
================================================================================

--------------------------------------------------------------------------------
Phoenix
--------------------------------------------------------------------------------

http://www.boost.org/doc/libs/1_55_0/libs/phoenix/doc/

--------------------------------------------------------------------------------
Spirit
--------------------------------------------------------------------------------

http://www.boost.org/doc/libs/1_54_0/libs/spirit/doc/

Spirit is an object-oriented, recursive-descent parser and output generation
library. It allows you to write grammars and format descriptions using a format
similar to Extended Backus Naur Form (EBNF) directly in C++. These inline grammar
specifications can mix freely with other C++ code, as they are implmented as
tempmlates, and are immediately executable. Spirit is composed of four pieces of
software:

* `boost::spirit::classic` - classic parser library
* `boost::spirit::qi` - recursive descent parser
* `boost::spirit::lex` - creates tokenizer / lexers
* `boost::spirit::karma` - generator that roughly uses QI for output

An example Extended Backus Naur Form (EBNF) calculator and the corresponding
Spirit parser is as follows:


.. code-block:: c++

    // group       ::= '(' expression ')'
    // factor      ::= integer | group
    // term        ::= factor (('*' factor) | ('/' factor))*
    // expression  ::= term (('+' term) | ('-' term))*

    group       = '(' >> expression >> ')';
    factor      = integer | group;
    term        = factor >> *(('*' >> factor) | ('/' >> factor));
    expression  = term >> *(('+' >> term) | ('-' >> term));
