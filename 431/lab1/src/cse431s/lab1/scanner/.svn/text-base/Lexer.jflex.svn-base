/*
 * CSE 431S Programming Assignment 1
 */
 
package cse431s.pa1.fsa;

/**
 * A scanner for right-linear grammar specifications in CUP syntax.
 */

%%

%class Lexer
%type Token
%yylexthrow ScannerException
%unicode
%line
%column

LineTerminator = \r|\n|\r\n
WhiteSpace     = {LineTerminator} | [ \t\f]

Identifier = [:jletter:] [:jletterdigit:]*

%%

"non"        { return new Token(Token.NON); }
"terminal"   { return new Token(Token.TERMINAL); }
"start"      { return new Token(Token.START); }
"with"       { return new Token(Token.WITH); }
","          { return new Token(Token.COMMA); }
"|"          { return new Token(Token.OR); }
";"          { return new Token(Token.SEMICOLON); }
"::="        { return new Token(Token.DEFINE); }
{Identifier} { return new Token(Token.IDENTIFIER, yytext()); }

{WhiteSpace} { /* ignore */ }

.            { throw new ScannerException("Illegal character \""
                 + yytext() + "\""); }
