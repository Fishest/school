package cse431s.lab5.codegen;

import java.io.PrintStream;

import cse431s.lab5.ast.ASTNode;
import cse431s.lab5.ast.BooleanLiteralNode;
import cse431s.lab5.ast.ClassNode;
import cse431s.lab5.ast.IdentifierNode;
import cse431s.lab5.ast.IntegerLiteralNode;
import cse431s.lab5.ast.TypeNode;
import cse431s.lab5.semantic.SymbolInfo;
import cse431s.lab5.visitor.SimpleVisitor;

/**
 * An AST visitor which generates Jasmin code.
 */
public class CodeGenVisitor implements SimpleVisitor {
    private PrintStream stream;
    private int labelIndex;
    private String className;
    private ClassNode classNode;
    private boolean returnGenerated;

    
    // Fix all of the FIXMEs below.
    
    
    public CodeGenVisitor(PrintStream stream) {
        this.stream = stream;
    }
    
    @Override
    public void visit(ASTNode node) throws Exception {
        switch (node.getNodeType()) {
        case ADDITION:
            visitAdditionNode(node);
            break;
            
        case ASSIGN:
            visitAssignNode(node);
            break;

        case BOOLEAN_AND:
            visitBooleanAndNode(node);
            break;
            
        case BOOLEAN_LITERAL:
            visitBooleanLiteralNode(node);
            break;
            
        case BOOLEAN_NOT:
            visitBooleanNotNode(node);
            break;
            
        case BOOLEAN_OR:
            visitBooleanOrNode(node);
            break;
            
        case CLASS:
            visitClassNode(node);
            break;
            
        case DIVISION:
            visitDivisionNode(node);
            break;
            
        case EQUAL:
            visitEqualNode(node);
            break;
            
        case GREATER_THAN:
            visitGreaterThanNode(node);
            break;
            
        case GREATER_THAN_OR_EQUAL:
            visitGreaterThanOrEqualNode(node);
            break;
            
        case IF_STATEMENT:
            visitIfStatementNode(node);
            break;
            
        case INTEGER_LITERAL:
            visitIntegerLiteralNode(node);
            break;
            
        case LESS_THAN:
            visitLessThanNode(node);
            break;
            
        case LESS_THAN_OR_EQUAL:
            visitLessThanOrEqualNode(node);
            break;
            
        case METHOD_ACCESS:
            visitMethodAccessNode(node);
            break;
            
        case METHOD_DECLARATION:
            visitMethodDeclarationNode(node);
            break;
            
        case MULTIPLICATION:
            visitMultiplicationNode(node);
            break;
            
        case NOT_EQUAL:
            visitNotEqualNode(node);
            break;
            
        case PARAMETER:
            visitParameterNode(node);
            break;
            
        case RETURN_STATEMENT:
            visitReturnStatementNode(node);
            break;
            
        case SUBTRACTION:
            visitSubtractionNode(node);
            break;
            
        case UNARY_MINUS:
            visitUnaryMinusNode(node);
            break;
            
        case UNARY_PLUS:
            visitUnaryPlusNode(node);
            break;
            
        case VAR_USE:
            visitVarUse(node);
            break;
            
        case WHILE_STATEMENT:
            visitWhileStatementNode(node);
            break;

        case ARGUMENTS:
        case BLOCK:
        case BOOLEAN_TYPE:
        case CAST:
        case CHAR_LITERAL:
        case CHAR_TYPE:
        case CLASS_BODY:
        case COMPILATION_UNIT:
        case DECLARATIONS:
        case DOUBLE_TYPE:
        case EMPTY_STATEMENT:
        case EXPRESSION_STATEMENT:
        case FIELD_DECLARATION:
        case FLOAT_LITERAL:
        case IDENTIFIER:
        case INT_TYPE:
        case LOCAL_VAR_DECLARATION:
        case NULL_LITERAL:
        case PARAMETERS:
        case POST_DECREMENT:
        case POST_INCREMENT:
        case PRE_DECREMENT:
        case PRE_INCREMENT:
        case STRING_LITERAL:
        case VARIABLE_DECLARATION:
        case VARIABLE_DECLARATIONS:
        case VOID:
        default:
            visitAllChildren(node);
        }
    }
    
    private void visitAllChildren(ASTNode node) throws Exception {
        for (ASTNode child : node.getChildren()) {
            child.accept(this);
        }
    }
    
    private void visitAdditionNode(ASTNode node) throws Exception {
        node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	stream.println("  iadd");
 
    }
    
    private void visitAssignNode(ASTNode node) throws Exception {
    	node.getChild(1).accept(this);
    	IdentifierNode idNode = (IdentifierNode) node.getChild(0);
        SymbolInfo si = idNode.getSymbolInfo();
        int lvIndex = si.getLocalVarIndex();
        
        if (lvIndex >= 0 && lvIndex <= 3) {
        	stream.println("  istore_" + lvIndex);
        } else {
        	stream.println("  istore " + lvIndex);
        }
        returnGenerated = false;
    }
    
    private void visitBooleanAndNode(ASTNode node) throws Exception {
        node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	stream.println("  iand");
    	returnGenerated = false;
    }

    private void visitBooleanLiteralNode(ASTNode node) {
    	BooleanLiteralNode bnode = (BooleanLiteralNode)node;
    	if (bnode.getValue()) {
    		stream.println("  iconst_1");
    	} else {
    		stream.println("  iconst_0");
    	}
    	returnGenerated = false;
    }

    private void visitBooleanNotNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	stream.println("  iconst_1");
    	stream.println("  ixor");
    	returnGenerated = false;
    }

    private void visitBooleanOrNode(ASTNode node) throws Exception {
        node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	stream.println("  ior");
    	returnGenerated = false;
    }

    private void visitClassNode(ASTNode node) throws Exception {
        classNode = (ClassNode) node;
        
        IdentifierNode idNode = (IdentifierNode) node.getChild(0);
        className = idNode.getValue();
        
        stream.println(".class public " + className);
        stream.println(".super java/lang/Object");
        stream.println("");

        outputDefaultConstructor();
        outputMainMethod();
        outputPrintlnMethod();

        returnGenerated = false;
       
        node.getChild(1).accept(this);
    }
    
    private void visitDivisionNode(ASTNode node) throws Exception {
        node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	stream.println("  idiv");
    	returnGenerated = false;
    }

    private void visitEqualNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	String trueLabel = generateLabel();
    	String falseLabel = generateLabel();
    	stream.println("  if_icmpeq " + trueLabel);
    	stream.println("  iconst_0");
    	stream.println("  goto " + falseLabel);
    	stream.println(trueLabel + ":");
    	stream.println("  iconst_1");
    	stream.println(falseLabel + ":");    	
    	returnGenerated = false;
    }
    
    private void visitGreaterThanNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	String trueLabel = generateLabel();
    	String falseLabel = generateLabel();
    	stream.println("  if_icmpgt " + trueLabel);
    	stream.println("  iconst_0");
    	stream.println("  goto " + falseLabel);
    	stream.println(trueLabel + ":");
    	stream.println("  iconst_1");
    	stream.println(falseLabel + ":");    	
    	returnGenerated = false;
    }

    private void visitGreaterThanOrEqualNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	String trueLabel = generateLabel();
    	String falseLabel = generateLabel();
    	stream.println("  if_icmpge " + trueLabel);
    	stream.println("  iconst_0");
    	stream.println("  goto " + falseLabel);
    	stream.println(trueLabel + ":");
    	stream.println("  iconst_1");
    	stream.println(falseLabel + ":");    	
    	returnGenerated = false;
    }

    private void visitIfStatementNode(ASTNode node) throws Exception {
    	String elseLabel = generateLabel();
    	String exitLabel = generateLabel();
    	stream.println("; if statement");
    	node.getChild(0).accept(this);
    	stream.println("  ifeq " + elseLabel);    	
    	node.getChild(1).accept(this);
    	stream.println("  goto " + exitLabel);
    	stream.println(elseLabel + ":");
    	if (node.getChildren().size() == 3) {
    		node.getChild(2).accept(this);
    	}
    	stream.println(exitLabel + ":");
    	stream.println("; end if");
    }

    private void visitIntegerLiteralNode(ASTNode node) {
    	IntegerLiteralNode inode = (IntegerLiteralNode)node;
    	int value = inode.getValue();
    	if (value >= 0 && value <= 5) {
    		stream.println("  iconst_" + value);
    	} else if (value == -1) {
    		stream.println("  iconst_m1");
    	} else {
    		stream.println("  ldc " + value);
    	}
    	returnGenerated = false;
    }
    
    private void visitLessThanNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	String trueLabel = generateLabel();
    	String falseLabel = generateLabel();
    	stream.println("  if_icmplt " + trueLabel);
    	stream.println("  iconst_0");
    	stream.println("  goto " + falseLabel);
    	stream.println(trueLabel + ":");
    	stream.println("  iconst_1");
    	stream.println(falseLabel + ":");    	
    	returnGenerated = false;
    }

    private void visitLessThanOrEqualNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	String trueLabel = generateLabel();
    	String falseLabel = generateLabel();
    	stream.println("  if_icmple " + trueLabel);
    	stream.println("  iconst_0");
    	stream.println("  goto " + falseLabel);
    	stream.println(trueLabel + ":");
    	stream.println("  iconst_1");
    	stream.println(falseLabel + ":");    	
    	returnGenerated = false;
    }

    private void visitMethodAccessNode(ASTNode node) throws Exception {
        node.getChild(1).accept(this);
        
        IdentifierNode idNode = (IdentifierNode) node.getChild(0);
        String methodName = idNode.getValue();
        String sig = classNode.getMethodSig(methodName);
        stream.println("  invokestatic " + className + "/" + sig);
        returnGenerated = false;
    }
    
    private void visitMethodDeclarationNode(ASTNode node) throws Exception {
        IdentifierNode idNode = (IdentifierNode) node.getChild(0);
        String methodName = idNode.getValue();
        
        TypeNode typeNode = (TypeNode) node.getChild(2);
        String returnType = typeNode.getType().getSignature();
        
        stream.println("");
        stream.println(";");
        stream.println("; method");
        stream.println(";");
        
        stream.print(".method public static " + methodName + "(");
        node.getChild(1).accept(this);
        stream.println(")" + returnType);
        
        stream.println("  .limit locals 10");
        stream.println("  .limit stack 10");

        node.getChild(3).accept(this);
        
        if (!returnGenerated) {
            stream.println("  return");
            returnGenerated = true;
        }
        
        stream.println(".end method");
    }
    
    private void visitMultiplicationNode(ASTNode node) throws Exception {
       	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	stream.println("  imul");
    	returnGenerated = false;
 
    }

    private void visitNotEqualNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	String trueLabel = generateLabel();
    	String falseLabel = generateLabel();
    	stream.println("  if_icmpne " + trueLabel);
    	stream.println("  iconst_0");
    	stream.println("  goto " + falseLabel);
    	stream.println(trueLabel + ":");
    	stream.println("  iconst_1");
    	stream.println(falseLabel + ":");    	
    	returnGenerated = false;
    }

    private void visitParameterNode(ASTNode node) throws Exception {
        TypeNode typeNode = (TypeNode) node.getChild(1);
        String typeSig = typeNode.getType().getSignature();
        stream.print(typeSig);
        returnGenerated = false;
    }
    
    private void visitReturnStatementNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	stream.println("  ireturn");
    	returnGenerated = true;   	
    }

    private void visitSubtractionNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	node.getChild(1).accept(this);
    	stream.println("  isub");
    	returnGenerated = false;
    }
    
    private void visitUnaryMinusNode(ASTNode node) throws Exception {
        node.getChild(0).accept(this);
    	stream.println("  ineg");
    	returnGenerated = false;
    }

    private void visitUnaryPlusNode(ASTNode node) throws Exception {
    	node.getChild(0).accept(this);
    	returnGenerated = false;
    }

    private void visitVarUse(ASTNode node) {
        IdentifierNode idNode = (IdentifierNode) node.getChild(0);
        SymbolInfo si = idNode.getSymbolInfo();
        int lvIndex = si.getLocalVarIndex();
        
        if (lvIndex >= 0 && lvIndex <= 3) {
        	stream.println("  iload_" + lvIndex);
        } else {
        	stream.println("  iload " + lvIndex);
        }
        returnGenerated = false;
    }
    
    private void visitWhileStatementNode(ASTNode node) throws Exception {
    	String startLabel = generateLabel();
    	String exitLabel = generateLabel();

    	stream.println("; while statement");
    	stream.println(startLabel + ":");
    	node.getChild(0).accept(this);
    	stream.println("  ifeq " + exitLabel);
    	node.getChild(1).accept(this);
    	stream.println("  goto " + startLabel);
    	stream.println(exitLabel + ":");
    	stream.println("; end while");
    	returnGenerated = false;    	
    }
    
    private String generateLabel() {
        return "label" + (++labelIndex);
    }

    private void outputDefaultConstructor() {
        stream.println("");
        stream.println(";");
        stream.println("; standard constructor");
        stream.println(";");
        stream.println(".method public <init>()V");
        stream.println("  aload_0");
        stream.println("  invokenonvirtual java/lang/Object/<init>()V");
        stream.println("  return");
        stream.println(".end method");
        stream.println("");
    }
    
    private void outputMainMethod() {
        stream.println("");
        stream.println(";");
        stream.println("; main method");
        stream.println(";");
        stream.println(".method public static main([Ljava/lang/String;)V");
        stream.println("  invokestatic " + className + "/program()V");
        stream.println("  return");
        stream.println(".end method");
        stream.println("");
    }
    
    private void outputPrintlnMethod() {
        stream.println("");
        stream.println(";");
        stream.println("; println method");
        stream.println(";");
        stream.println(".method public static println(I)V");
        stream.println("  .limit stack 2");
        stream.println("  getstatic java/lang/System/out Ljava/io/PrintStream;");
        stream.println("  iload_0");
        stream.println("  invokevirtual java/io/PrintStream/println(I)V");
        stream.println("  return");
        stream.println(".end method");
        stream.println("");
    }
}
