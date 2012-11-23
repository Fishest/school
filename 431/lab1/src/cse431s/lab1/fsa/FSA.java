package cse431s.lab1.fsa;

import cse431s.lab1.scanner.Scanner;
import cse431s.lab1.scanner.Token;

/*
 * CSE 431S Programming Assignment 1
 */

/**
 * Implements a finite state automaton.
 * 
 * The GOTO and ACTION tables need to be filled in with the appropriate state
 * and action numbers respectively; the ENDSTATE variable needs to be set
 * to the accepting state number; and the switch statement needs to be filled
 * in with the code for the actions.
 */
public class FSA {

	/*
	 * A table of states cross symbols.  Each row corresponds to a state and
	 * each column corresponds to a symbols.  Each entry for a row should be
	 * the state to go to from that row's state on that column's symbol.
	 */
	private static int GOTO[][] = {
       /*  N    T    S    W    C    O    S    D    I */
       /*  O    E    T    I    O    R    E    E    D */
       /*  N    R    A    T    M         M    F    E */
       /*       M    R    H    M         I    I    T */
       /*       I    T         A         C    N    I */
       /*       N                        O    E    F */
       /*       A                        L         I */
       /*       L                        O         E */
       /*                                N         R */
        {  1,   2,  17,  17,  17,  17,  17,  17,  17 } /*   0 */,
        { 17,   3,  17,  17,  17,  17,  17,  17,  17 } /*   1 */,
        {  5,   5,   5,   5,  17,  17,  17,  17,   5 } /*   2 */,
        {  4,   4,   4,   4,  17,  17,  17,  17,   4 } /*   3 */,
        {  6,   6,   6,   6,  17,  17,  17,  17,   6 } /*   4 */,
        {  7,   7,   7,   7,  17,  17,  17,  17,   7 } /*   5 */,
        { 17,  17,  17,  17,   4,  17,   8,  17,  17 } /*   6 */,
        { 17,  17,  17,  17,   5,  17,   8,  17,  17 } /*   7 */,
        {  1,   2,   9,  17,  17,  17,  17,  17,  17 } /*   8 */,
        { 10,  10,  10,  10,  17,  17,  17,  17,  17 } /*   9 */,
        { 11,  11,  11,  11,  17,  17,  17,  17,  11 } /*  10 */,
        { 17,  17,  17,  17,  17,  17,  12,  17,  17 } /*  11 */,
        { 13,  13,  13,  13,  17,  17,  17,  17,  13 } /*  12 */,
        { 17,  17,  17,  17,  17,  17,  17,  14,  17 } /*  13 */,
        { 15,  15,  15,  15,  17,  17,  17,  17,  15 } /*  14 */,
        { 16,  16,  16,  16,  17,  14,  12,  17,  16 } /*  15 */,
        { 17,  17,  17,  17,  17,  14,  12,  17,  17 } /*  16 */,
        { 17,  17,  17,  17,  17,  17,  17,  17,  17 } /*  17 */
	};

	/*
	 * A table of states cross symbols.  Each row corresponds to a state and
	 * each column corresponds to a symbols.  Each entry for a row should be
	 * the action to execute when going from that row's state on that column's
	 * symbol.
	 */
	private static int ACTION[][] = {
       /*  N    T    S    W    C    O    S    D    I */
       /*  O    E    T    I    O    R    E    E    D */
       /*  N    R    A    T    M         M    F    E */
       /*       M    R    H    M         I    I    T */
       /*       I    T         A         C    N    I */
       /*       N                        O    E    F */
       /*       A                        L         I */
       /*       L                        O         E */
       /*                                N         R */
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   0 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   1 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   2 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   3 */,
        {  1,   1,   1,   1,   0,   0,   0,   0,   1 } /*   4 */,
        {  2,   2,   2,   2,   0,   0,   0,   0,   2 } /*   5 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   6 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   7 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   8 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*   9 */,
        {  3,   3,   3,   3,   0,   0,   0,   0,   3 } /*  10 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*  11 */,
        {  4,   4,   4,   4,   0,   0,   0,   0,   4 } /*  12 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*  13 */,
        {  5,   5,   5,   5,   0,   0,   0,   0,   5 } /*  14 */,
        {  7,   7,   7,   7,   0,   6,   6,   0,   7 } /*  15 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*  16 */,
        {  0,   0,   0,   0,   0,   0,   0,   0,   0 } /*  17 */
	};
	
	/* The accepting state (we only allow one). */
	private static int ENDSTATE = 12;
	
	/*
	 * The String to output on transitions to accepting states in the input
	 * right-linear grammar.
	 */
	private static final String FINAL = "$FINAL$";


	/**
	 * Constructs an FSA.
	 */
	public FSA() {
		super();
	}
	

	/**
	 * Runs the FSA on the input.
	 * 
	 * @param scanner
	 *            the Scanner from which to read the Tokens.
	 */
	public void run(Scanner scanner) {
		SymbolTable symbols = new SymbolTable();

		int state = 0;

		String term = null;
		String nonterm = null;

		while (scanner.hasNext()) {
			Token token = scanner.next();
			String value = getTokenValue(token);

			int action = ACTION[state][token.getType()];
			int newstate = GOTO[state][token.getType()];

/*			System.out.println("State " + state + " Performing action "
					+ action + " and going to " + newstate + " " + token.toString());*/
			
			/*
			 * Each case in this switch statements should correspond to the
			 * transition actions.
			 */
			switch (action) {
			
				/*
				 * ignored transition
				 */
				case 0: 	 	
					break;
				
				/*
				 * add non terminal definition
				 */		
				case 1:
					if (symbols.isNonterminal(value)) {
						oops("multiple definitions of nonterminal " + value);
					}
					symbols.addNonterminal(value, token);
					break;
					
				/*
				 * add terminal definition
				 */		
				case 2:	
					if (symbols.isTerminal(value)) {
						oops("multiple definitions of terminal " + value);
					}
					symbols.addTerminal(value, token);
					break;
					
				/*
				 * define start state
				 */
				case 3:					
					if (!symbols.isNonterminal(value)) {
						oops("undefined start nonterminal specified " + value);
					}
					System.out.println("Start " + value);
					break;
					
				/*
				 * start of nonterminal description
				 */
				case 4:
					if (!symbols.isNonterminal(value)) {
						oops("undefined nonterminal specified " + value);
					}
					nonterm = value;
					break;
					
				/*
				 * first step of terminal description
				 */
				case 5:
					if (!symbols.isTerminal(value)) {
						oops("undefined terminal specified " + value);
					}
					term = value;
					break;
				
				/*
				 * finished defining nonterminal
				 */
				case 6:
					System.out.println("Edge " + nonterm + " " + FINAL + " " + term);
					break;
				
				/*
				 * second step of terminal description
				 */
				case 7:
					if (!symbols.isNonterminal(value)) {
						oops("undefined nonterminal specified " + value);
					}
					System.out.println("Edge " + nonterm + " " + value + " " + term);
					break;										
					
			}

			state = newstate;
		}
		
		if (state != ENDSTATE) {
			oops("end in bad state (" + state + ")");
		}
	}

	/**
	 * Gets the correct value of the token
	 * 
	 * @param token The token to get the value of
	 * @return The string value of the token
	 */
	private static String getTokenValue(Token token) {
		String value = token.getValue();
		
		if (value.isEmpty()) {
			value = token.toString().split(" ")[1].toLowerCase();
		}
		
		return value;
	}

	/**
	 * Outputs an error message and aborts processing.
	 * 
	 * @param s
	 *            the error detail message.
	 */
	private void oops(String s) {
		System.err.println("Error: " + s);
		System.out.println("ABORT");
		System.exit(-1);
	}
}
