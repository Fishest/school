package cse431s.lab1.fsa;

/*
 * CSE 431S Programming Assignment 1
 */

import java.util.HashMap;

/**
 * A simple symbol table to hold terminal and nonterminal symbol Tokens.
 */
public class SymbolTable {
    private HashMap<String, Object> terminals;
    private HashMap<String, Object> nonterminals;

    /**
     * Constructs a SymbolTable.
     */
    public SymbolTable() {
        super();
        this.terminals = new HashMap<String, Object>();
        this.nonterminals = new HashMap<String, Object>();
    }

    /**
     * Tests if the specified String corresponds to a Token in the terminals
     * table.
     * 
     * @param s
     *            the String to test.
     * @return <tt>true</tt> if the String is registered as a terminal,
     *         <tt>false</tt> otherwise.
     */
    public boolean isTerminal(String s) {
        return terminals.containsKey(s);
    }

    /**
     * Tests if the specified String corresponds to a Token in the nonterminals
     * table.
     * 
     * @param s
     *            the String to test.
     * @return <tt>true</tt> if the String is registered as a nonterminal,
     *         <tt>false</tt> otherwise.
     */
    public boolean isNonterminal(String s) {
        return nonterminals.containsKey(s);
    }

    /**
     * Adds (or replaces) a symbol in the terminals table.
     * 
     * @param s
     *            the symbol.
     * @param o
     *            the Token corresponding to the symbol.
     */
    public void addTerminal(String s, Object o) {
        terminals.put(s, o);
    }

    /**
     * Adds (or replaces) a symbol in the nonterminals table.
     * 
     * @param s
     *            the symbol.
     * @param o
     *            the Token corresponding to the symbol.
     */
    public void addNonterminal(String s, Object o) {
        nonterminals.put(s, o);
    }

    /**
     * Test code.
     * 
     * Ignores the arguments.
     * 
     * @param args
     *            the command-line arguments.
     */
    public static void main(String[] args) {
        String t = "I am a terminal";
        String nt = "I am a nonterminal";

        SymbolTable st = new SymbolTable();

        st.addNonterminal(nt, nt);
        st.addTerminal(t, t);

        System.out.println("Nonterminal: " + st.isTerminal(nt + " "));
        System.out.println("Terminal: " + st.isTerminal(t + ""));
        System.out.println("Undeclared: " + st.isTerminal("missing"));
    }
}
