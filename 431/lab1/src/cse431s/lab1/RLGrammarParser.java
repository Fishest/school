package cse431s.lab1;

/*
 * CSE 431S Programming Assignment 1
 */

import cse431s.lab1.fsa.FSA;
import cse431s.lab1.scanner.Scanner;

/**
 * The main entry point of the right-linear grammar parser.
 */
public class RLGrammarParser {

    /**
     * The main entry point of the right-linear grammar parser.
     * 
     * Accepts a file name or URL from which to read the right-linear grammar
     * specification and outputs a textual representation to stdout.
     * 
     * @param args
     *            the command-line arguments.
     */
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java RLGrammarParser file-or-URL");
            System.exit(-1);
        }

        FSA fsa = new FSA();
        fsa.run(new Scanner(Opener.open(args[0])));
    }
}
