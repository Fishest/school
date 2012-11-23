.class public Test1
.super java/lang/Object

;
;  Team members:
;
;
;
;
;  Answer questions 1) - 5) below
;     and turn in this file, appropriately modified,  with the console output
;

;
; standard initializer
;
.method public <init>()V
   aload_0
;
;  1)  Why is the method call below "nonvirtual"?
;  Because we are calling the constructor for the Object class,
;  and constructors cannot be virtual. 
;
   invokenonvirtual java/lang/Object/<init>()V
   return
.end method

.method public static bar()I
;
;  2) What happens if you change the stack limit to 1?  
;  We get a stack overflow
;
;  3) What determines the stack limit?
;  The number of locals in the current stack frame
;
   .limit stack  3
   .limit locals 0

   ;bipush 100
   ;bipush 4
   ;imul
   ;bipush 31
   sipush 431
   ;iadd   
;
;  4) Why not just bipush 431 directly?
;  Because it exceeds the size for the byte type (2^8)
;  5) What is the most efficient way (in terms of number of bytecodes) to
;      get 431 on the stack?  Modify this code to do that.
;  Use a at least two bytes pushed on the stack (sipush 431)
;
   ireturn
.end method

;
;  Do not change the signature of this method
;
.method public static foo(I)V
   .limit locals 3 
   .limit stack  2

   ;
   ;    reg 0 - the incoming parameter
   ;    reg 1 - will contain the System.out PrintStream object 
   ;               (really known as java.lang.System.out)
   ;    reg 2 - a temporary
   ;

   getstatic java/lang/System/out Ljava/io/PrintStream;
   astore 1

   ;
   ;  push the supplied parameter on top of stack
   ;
   iload 0
   ;
   ;  convert it to a String
   ;
   invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
   ;
   ;   that string returned from valueOf(I) is now on top of stack
   ;
   astore 2  ;  store the result so we can print it below
   ;
   ; ... and print it
   ;
   aload 1    ; push the PrintStream object
   aload 2    ; push the string we just created and then print it
   invokevirtual java/io/PrintStream/print(Ljava/lang/String;)V
   ;
   ;
   return
.end method

;
;  Do not change any code below this line
;
.method public static main([Ljava/lang/String;)V
       ; set limits used by this method
       .limit locals 1   ; = parameters + locals
       .limit stack  1
        invokestatic Test1/bar()I 
        invokestatic Test1/foo(I)V
        return
.end method
