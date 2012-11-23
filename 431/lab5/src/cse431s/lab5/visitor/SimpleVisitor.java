/*
 * CSE 431S Programming Assignment 3
 */

package cse431s.lab5.visitor;

import cse431s.lab5.ast.ASTNode;

/**
 * A simplified AST Visitor interface.
 */
public interface SimpleVisitor {
    void visit(ASTNode node) throws Exception;
}
