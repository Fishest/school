/*
 * CSE 431S Programming Assignment 2
 */

package cse431s.lab2.topdown;

import java.util.ArrayList;
import java.util.Arrays;

import cse431s.lab2.scanner.Scanner;
import cse431s.lab2.scanner.ScannerException;
import cse431s.lab2.scanner.Symbol;
import cse431s.lab2.scanner.sym;

/**
 * A recursive-descent parser for the prefix expression evaluator.
 */
public class TDParser {
    private Scanner scanner;
    private Symbol lookahead;

    /**
     * Constructs a new TDParser which will read input from the specified
     * scanner.
     * 
     * @param scanner
     */
    public TDParser(Scanner scanner) {
        this.scanner = scanner;
        this.lookahead = scanner.peek();
    }

    /**
     * Currently just prints out the token numbers. You need to modify this (and
     * add methods as necessary) so that it performs a top-down parse.
     */
    public void parse() {        
        try {
        	start();
        } catch (ScannerException ex) {
        	System.out.println("Error parsing the supplied input: " + ex.getMessage());
        	ex.printStackTrace();        	
    	}
        //Symbol token = scanner.peek();
        //while (token.sym != sym.EOF) {
        //    System.out.println("Next token will be " + token);
        //    scanner.advance();
        //    token = scanner.peek();
        //}
    }
    
    /**
     * Attempts to match the next symbol and advance the scanner
     * @param symbol The symbol to attemp to match
     * @throws ScannerException
     */
    private void match(int symbol) throws ScannerException
    {
    	if (lookahead.sym == symbol) {
    		scanner.advance();
    		lookahead = scanner.peek();    	
    	} else {
    		throw new ScannerException("Expected " + symbol + " got " + lookahead.sym);
    	}
    }
    
    /**
     * Handles parsing expressions until the end of file
     * @throws ScannerException
     */
    private void start() throws ScannerException
    {
    	if (lookahead.sym == sym.lparen) {
    		expressions();
    		match(sym.EOF);
    	} else {
    		throw new ScannerException("invalid syntax for 'start' expression");
    	}
    }
    
    /**
     * Handles parsing one or more expressions
     * @throws ScannerException
     */
    private void expressions() throws ScannerException
    {
    	if (lookahead.sym == sym.lparen) {
    		System.out.println(expression());
    		expressions2();    		
    	} else {
    		throw new ScannerException("invalid syntax for 'expressions' expression");
    	}   	
    }
    
    /**
     * Handles parsing the second level recursive definition of expressions
     * @throws ScannerException
     */
    private void expressions2() throws ScannerException
    {
    	if (lookahead.sym == sym.lparen) {
    		expressions();    		
    	} else if (lookahead.sym == sym.EOF) {
    		// lambda transition, do nothing
    	} else {
    		throw new ScannerException("invalid syntax for 'expression2' expression");
    	}   	
    }
    
    /**
     * Handles parsing a single expression
     * @return The result of the expression
     * @throws ScannerException
     */
    private int expression() throws ScannerException
    {
    	int result = 0;
    	
    	if (lookahead.sym == sym.lparen) {
    		match(sym.lparen);
    		result = body();
    		match(sym.rparen);
    	} else {
    		throw new ScannerException("invalid syntax for 'expression' expression");
    	}    	
    	
    	return result;
    }
    
    /**
     * Handles parsing a body calculation
     * @return The result of the calculation
     * @throws ScannerException
     */
    private int body() throws ScannerException
    {
    	int result = 0;
    	
    	switch (lookahead.sym)
    	{
    		case sym.plus:
    		{
    			match(sym.plus);
    			int left = argument();
    			int right = argument();
    			result = left + right;
    			break;
    		}    			
    		case sym.minus:
    		{
    			match(sym.minus);
    			int left = argument();
    			int right = argument();
    			result = left - right;    			
    			break;
    		}    			
    		case sym.times:
    		{
    			match(sym.times);
    			int left = argument();
    			int right = argument();
    			result = left * right;
    			break;
    		}    			
    		case sym.divide:
    		{
    			match(sym.divide);
    			int left = argument();
    			int right = argument();
    			result = left / right;
    			break;
    		}
    		case sym.negate:
    		{
    			match(sym.negate);
    			int left = argument();
    			result = -left;
    			break;
    		}
    		case sym.sum:
    		{
    			match(sym.sum);
    			ArrayList<Integer> values = arguments();
    			for (int value : values)
    				result += value;
    			break;
    		}
    		case sym.product:
    		{
    			match(sym.product);
    			result = 1;
    			ArrayList<Integer> values = arguments();
    			for (int value : values)
    				result *= value;
    			break;
    		}
    			
    		case sym.mean:
    		{
    			match(sym.mean);
    			ArrayList<Integer> values = arguments();
    			for (int value : values)
    				result += value;
    			result /= values.size();
    			break;
    		}
    		default:
    			throw new ScannerException("invalid syntax for 'body' expression");
    	}
    	
    	return result;
    }    
    
    /**
     * Handles parsing a single argument
     * @return The parsed argument value
     * @throws ScannerException
     */
    private int argument() throws ScannerException
    {
    	int result = 0;
    	
    	if (lookahead.sym == sym.lparen) {
    		result = expression();
    	} else if (lookahead.sym == sym.number) {
    		result = (Integer) lookahead.value; 
    		match(sym.number);    		
    	} else {
    		throw new ScannerException("invalid syntax for 'argument' expression");
    	}
    	
    	return result;
    }
    
    /**
     * Handles parsing a collection of variable arguments
     * @return An ArrayList<Integer> of the parsed arguments
     * @throws ScannerException
     */
    private ArrayList<Integer> arguments() throws ScannerException
    {
    	ArrayList<Integer> result = new ArrayList<Integer>();
    	
    	if (lookahead.sym == sym.lparen || lookahead.sym == sym.number) {
    		result.add(argument());
    		arguments2(result);    		
    	} else {
    		throw new ScannerException("invalid syntax for 'arguments' expression");
    	}
    	
    	return result;
    }
    
    /**
     * Handles parsing the second level recursive definition of arguments
     * @param result The result structure to add arguments to
     * @throws ScannerException
     */
    private void arguments2(ArrayList<Integer> result) throws ScannerException
    {
    	if (lookahead.sym == sym.lparen || lookahead.sym == sym.number) {
    		result.add(argument());
    		arguments2(result);
    	} else if(lookahead.sym == sym.rparen) {
    		// lambda transition, do nothing    
    	} else {
    		throw new ScannerException("invalid syntax for 'arguments2' expression");
    	}    	    	
    }    
}
