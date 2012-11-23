/*
 * CSE 431S Programming Assignment 2
 */

package cse431s.lab2.scanner;

/**
 * A simple Symbol type.
 */
public class Symbol {
    public int sym;
    public int left, right;
    public Object value;

    public Symbol(int id, int l, int r, Object o) {
        this(id);
        left = l;
        right = r;
        value = o;
    }

    public Symbol(int id, Object o) {
        this(id, -1, -1, o);
    }

    public Symbol(int id, int l, int r) {
        this(id, l, r, null);
    }

    public Symbol(int sym_num) {
        this(sym_num, -1);
        left = -1;
        right = -1;
        value = null;
    }

    Symbol(int sym_num, int state) {
        sym = sym_num;
    }

    public String toString() {
        return "#" + sym;
    }
}
