/*
 * CSE 431S Programming Assignment 2
 */

package cse431s.pa2.scanner;

/**
 * A scanner for a prefix expression evaluator.
 */

%%

%class Lexer
%type Symbol
%yylexthrow ScannerException
%unicode
%line
%column

NEWLINE    = \r|\n|\r\n
WHITESPACE = [ \t\f]
DIGIT=[0-9]

%%

"(*"([^*]|"*"+[^)*])*"*"+")" { /* ignore */ }

//([^\n])*{NEWLINE} { /* ignore */ }

{WHITESPACE}+ { /* ignore */ }
{NEWLINE}     { /* ignore */ }

"sum"     { return (new Symbol(sym.sum)); }
"product" { return (new Symbol(sym.product)); }
"negate"  { return (new Symbol(sym.negate)); }
"plus"    { return (new Symbol(sym.plus)); }
"minus"   { return (new Symbol(sym.minus)); }
"times"   { return (new Symbol(sym.times)); }
"divide"  { return (new Symbol(sym.divide)); }
"mean"    { return (new Symbol(sym.mean)); }
"("       { return (new Symbol(sym.lparen)); }
")"       { return (new Symbol(sym.rparen)); }
{DIGIT}+  { return (new Symbol(sym.number, new Integer(yytext()))); }

.         { throw new ScannerException("Illegal character \"" + yytext() + "\""); }
