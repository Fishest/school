/*
 * CSE 431S Programming Assignment 3
 */

package cse431s.lab3.ast;

import java.util.ArrayList;
import java.util.List;

import cse431s.lab3.visitor.ASTVisitor;

/**
 * The AST Node interface.
 */
public interface ASTNode {

    /**
     * Accepts visitors (the Visitor pattern).
     */
    void accept(ASTVisitor visitor);
    
    /**
     * Adds a node to the end of the list of children.
     */
    void addChild(ASTNode node);

    /**
     * Adds a node to the list of children at the specified location.
     */
    void addChild(int index, ASTNode node);
    
    /**
     * Adds a list of nodes to the end of the list of children.
     */
    void addChildren(List<ASTNode> nodes);
    
    /**
     * Returns the list of children.
     */
    ArrayList<ASTNode> getChildren();
    
    /**
     * Returns the child at the specified location.
     */
    ASTNode getChild(int index);
    
    void setParent(ASTNode parent);
    ASTNode getParent();
}
