package cse431s.lab3.ast;

public class BooleanLiteralNode extends BaseASTNode {
    private boolean value;
    
    public BooleanLiteralNode(boolean value) {
        super("BooleanLiteral");
        this.value = value;
    }
    
    public boolean getValue() {
        return value;
    }
    
    @Override
    public String toString() {
        return getNodeType() + " (" + value + ")";
    }
}
