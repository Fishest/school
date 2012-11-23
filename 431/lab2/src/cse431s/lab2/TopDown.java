/*
 * CSE 431S Programming Assignment 2
 */

package cse431s.lab2;

import cse431s.lab2.scanner.Scanner;
import cse431s.lab2.topdown.TDParser;

/**
 * Runs the TDParser on the specified file or URL.
 */
public class TopDown {

    /**
     * The main entry point of the top-down version of the prefix expression
     * evaluator parser.
     * 
     * Accepts a file name or URL from which to read the prefix expressions.
     * 
     * @param args
     *            the command-line arguments.
     */
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java TopDown file-or-URL");
            System.exit(-1);
        }

        TDParser parser = new TDParser(new Scanner(Opener.open(args[0])));
        parser.parse();
    }
}
