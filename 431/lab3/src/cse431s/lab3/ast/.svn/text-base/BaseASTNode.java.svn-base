package cse431s.lab3.ast;

import java.util.ArrayList;
import java.util.List;

import cse431s.lab3.visitor.ASTVisitor;

public class BaseASTNode implements ASTNode {
    private ArrayList<ASTNode> children = new ArrayList<ASTNode>();
    private ASTNode parent;
    private String nodeType;
    
    public BaseASTNode(String nodeType) {
        this.nodeType = nodeType;
    }
    
    public String getNodeType() {
        return nodeType;
    }

    @Override
    public String toString() {
        return nodeType;
    }

    @Override
    public void accept(ASTVisitor visitor) {
        visitor.previsit(this);
        
        for (ASTNode child : children) {
            child.accept(visitor);
        }
        
        visitor.postvisit(this);
    }

    @Override
    public void addChild(ASTNode node) {
        children.add(node);
    }

    @Override
    public void addChild(int index, ASTNode node) {
        children.add(index, node);
    }

    @Override
    public void addChildren(List<ASTNode> nodes) {
        children.addAll(nodes);
    }

    @Override
    public ASTNode getChild(int index) {
        return children.get(index);
    }

    @Override
    public ArrayList<ASTNode> getChildren() {
        return children;
    }

    @Override
    public ASTNode getParent() {
        return parent;
    }

    @Override
    public void setParent(ASTNode parent) {
        this.parent = parent;
    }
}
