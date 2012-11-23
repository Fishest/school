package autogen;
import common.Listing;
import java_cup.runtime.*;


%%
%cup
%public

%line
%char
%eofval{
  return makeSymbol(sym.EOF);
%eofval}



%{
  private void echo() {
	Listing.get().echo(yytext());
  }
  private Symbol makeSymbol(int nSymType) {
    return makeSymbol(nSymType, yytext());
  }

  private Symbol makeSymbol(int nSymType, Object secondarg) {
    echo();
    return new Symbol(nSymType, yychar, yychar + yytext().length() - 1,
                        secondarg);
  }
%}


ALPHA=[A-Za-z]
DIGIT=[0-9]
BLANKS=[\ \t\b\015]
NEWLINE=[\n]

%%
"(*"([^)*]|")"|"*""*"*[^)*])*"*""*"*")"
{
	Listing.get().echo(yytext());
}
{NEWLINE}
{
	Listing.get().NewLine(1);
}
{BLANKS}+  
{ 
	Listing.get().echo(yytext());
}
"abstract" {
   return makeSymbol(sym.ABSTRACT); } 
"float" {
   return makeSymbol(sym.FLOAT); } 
"int" {
   return makeSymbol(sym.INT); } 
"nonabstract" {
   return makeSymbol(sym.NONABSTRACT); } 
"object" {
   return makeSymbol(sym.OBJECT); } 
"package" {
   return makeSymbol(sym.PACKAGE); } 
"private" {
   return makeSymbol(sym.PRIVATE); } 
"protected" {
   return makeSymbol(sym.PROTECTED); } 
"public" {
   return makeSymbol(sym.PUBLIC); } 
"void" {
   return makeSymbol(sym.VOID); } 
"a" {
   return makeSymbol(sym.a); } 
"b" {
   return makeSymbol(sym.b); } 
"beef" {
   return makeSymbol(sym.beef); } 
"c" {
   return makeSymbol(sym.c); } 
"chicken" {
   return makeSymbol(sym.chicken); } 
"d" {
   return makeSymbol(sym.d); } 
"e" {
   return makeSymbol(sym.e); } 
"eggdropsoup" {
   return makeSymbol(sym.eggdropsoup); } 
"eggroll" {
   return makeSymbol(sym.eggroll); } 
"hotsoursoup" {
   return makeSymbol(sym.hotsoursoup); } 
"(" {
   return makeSymbol(sym.lparen); } 
"name" {
   return makeSymbol(sym.name); } 
"noodlesoup" {
   return makeSymbol(sym.noodlesoup); } 
")" {
   return makeSymbol(sym.rparen); } 
"salad" {
   return makeSymbol(sym.salad	); } 
";" {
   return makeSymbol(sym.semi); } 
"shrimp" {
   return makeSymbol(sym.shrimp); } 
"tofu" {
   return makeSymbol(sym.tofu); } 
"wonton" {
   return makeSymbol(sym.wonton); } 
"x" {
   return makeSymbol(sym.x); } 
"if" {
   return makeSymbol(sym.IF); } 
"else" {
   return makeSymbol(sym.ELSE); } 
.
{
	Listing.get().echo(yytext());
	Listing.get().oops("bad input");
}
