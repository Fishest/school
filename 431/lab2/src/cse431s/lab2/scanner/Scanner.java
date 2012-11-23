/*
 * CSE 431S Programming Assignment 2
 */

package cse431s.lab2.scanner;

import java.io.DataInputStream;
import java.io.IOException;

import cse431s.lab2.Opener;

/**
 * A CUP compatible scanner.
 */
public class Scanner {
    protected Lexer scanner; // The JFlex produced scanner.
    protected Symbol nextToken; // The lookahead token.

    /**
     * Creates the scanner and reads the first lookahead token.
     * 
     * @param istream
     *            the input stream to tokenize.
     */
    public Scanner(DataInputStream istream) {
        super();

        this.scanner = new Lexer(istream);

        try {
            this.nextToken = scanner.yylex();
        } catch (IOException e) {
            this.nextToken = null;
        } catch (ScannerException e) {
            this.nextToken = null;
        }
    }

    /**
     * Peeks at the lookahead token without consuming it.
     * 
     * @return the next Token.
     */
    public Symbol peek() {
        return (nextToken == null) ? new Symbol(sym.EOF) : nextToken;
    }

    /**
     * Tests if the input stream has more tokens.
     * 
     * @return <tt>true</tt> if the input stream has more tokens, <tt>false</tt>
     *         otherwise.
     */
    public boolean hasNext() {
        return nextToken != null;
    }

    /**
     * Consumes and returns the next token.
     * 
     * @return the next Token.
     */
    public Symbol next_token() {
        Symbol old = peek();
        advance();
        return old;
    }

    /**
     * Consumes and returns the next token.
     * 
     * @return the next Token.
     */
    public Symbol nextToken() {
        return this.next_token();
    }

    /**
     * Consumes and returns the next token.
     * 
     * @return the next Token.
     */
    public Symbol next() {
        return this.next_token();
    }

    /**
     * Consumes a token without returning the value.
     */
    public void advance() {
        if (nextToken != null) {
            try {
                nextToken = scanner.yylex();
            } catch (IOException e) {
                nextToken = null;
            } catch (ScannerException e) {
                nextToken = null;
            }
        }
    }

    /**
     * Test code.
     * 
     * Accepts a file name or URL from which to create the input stream.
     * 
     * @param args
     *            the command-line arguments.
     */
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java Scanner file-or-URL");
            System.exit(-1);
        }

        Scanner scanner = new Scanner(Opener.open(args[0]));
        Symbol token = scanner.next();
        while (token.sym != sym.EOF) {
            System.out.println(token);
            token = scanner.next();
        }
    }
}
