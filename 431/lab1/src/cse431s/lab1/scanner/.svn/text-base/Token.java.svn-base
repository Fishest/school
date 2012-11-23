package cse431s.lab1.scanner;

/*
 * CSE 431S Programming Assignment 1
 */

/**
 * A simple token ADT for use with the right-linear grammar parser.
 */
public class Token {

    /* The token types. */
    public final static int NON = 0;
    public final static int TERMINAL = 1;
    public final static int START = 2;
    public final static int WITH = 3;
    public final static int COMMA = 4;
    public final static int OR = 5;
    public final static int SEMICOLON = 6;
    public final static int DEFINE = 7;
    public final static int IDENTIFIER = 8;
    public final static int EOF = 9;

    /* The token names. The order needs to match the int values above. */
    private final static String[] names = { "NON", "TERMINAL", "START", "WITH",
            "COMMA", "OR", "SEMICOLON", "DEFINE", "IDENTIFIER", "EOF" };

    private int type;
    private String value;

    /**
     * Constructs a Token with the specified type and a null value.
     * 
     * It does not check that the type is actually valid.
     * 
     * @param type
     *            the type of the Token.
     */
    public Token(int type) {
        this(type, "");
    }

    /**
     * Constructs a Token with the specified type and value.
     * 
     * @param type
     *            the type of the Token.
     * @param value
     *            the value of the Token.
     */
    public Token(int type, String value) {
        super();
        this.type = type;
        this.value = value;
    }

    /**
     * Returns the type of the Token.
     * 
     * @return the type of the Token.
     */
    public int getType() {
        return type;
    }

    /**
     * Returns the value of the Token.
     * 
     * @return the value of the Token.
     */
    public String getValue() {
        return value;
    }

    /*
     * (non-Javadoc)
     * 
     * @see java.lang.Object#equals(java.lang.Object)
     */
    public boolean equals(Object obj) {
        if (obj instanceof Token) {
            Token other = (Token) obj;
            return this.type == other.type && (this.value == null) ? (other.value == null)
                    : this.value.equals(other.value);
        }

        return false;
    }

    /*
     * (non-Javadoc)
     * 
     * @see java.lang.Object#hashCode()
     */
    public int hashCode() {
        return type + ((this.value == null) ? 0 : this.value.hashCode());
    }

    /*
     * (non-Javadoc)
     * 
     * @see java.lang.Object#toString()
     */
    public String toString() {
        String str = "Token " + names[type];

        if (!value.equals("")) {
            str += " \"" + value + "\"";
        }

        return str;
    }
}
