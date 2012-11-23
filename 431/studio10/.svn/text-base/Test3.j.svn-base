.class public Test3
.super java/lang/Object

;
;  Team members:
;
;
;
;    Answer questions 7 and 8 below and turn in this file, 
;        appropriately modified, with your console output
;

;
; standard initializer
;
.method public <init>()V
   aload_0
   invokenonvirtual java/lang/Object/<init>()V
   return
.end method

.method public bar()I
   .limit stack  3
   .limit locals 1

   bipush 100
   bipush 4
   imul
   bipush 31
   iadd
   ireturn
.end method

;
;  Do not change the signature of this method
;
.method public foo(I)V
   .limit locals 4 
   .limit stack  2

   ;
   ;    reg 0 - 7) What is this register used for?
   ;    This is the current object instance (this or self)
   ;
   ;            8) What is the difference between this class and Test2?
   ;               How does that difference affect the code here?
   ;
   ;    This is a class instance and a non static method. This means we need
   ;    to have a handle to self as the first parameter.
   ;
   ;    reg 1 - the incoming parameter
   ;    reg 2 - will contain the System.out PrintStream object 
   ;               (really known as java.lang.System.out)
   ;    reg 3 - a temporary
   ;

   getstatic java/lang/System/out Ljava/io/PrintStream;
   ;astore 2

   ;
   ;  push the supplied parameter on top of stack
   ;
   iload 1
   ;
   ;  convert it to a String
   ;
   invokestatic java/lang/String/valueOf(I)Ljava/lang/String;
   ;
   ;   that string returned from valueOf(I) is now on top of stack
   ;
   ;astore 3  ;  store the result so we can print it below
   ;
   ; ... and print it
   ;
   ;aload 2    ; push the PrintStream object
   ;aload 3    ; push the string we just created and then print it
   invokevirtual java/io/PrintStream/print(Ljava/lang/String;)V
   ;
   ;  6) Rewrite the above code to avoid using any locals except 0
   ;       You must still receive the parameter in reg 0
   ;
   return
.end method

;
;  Do not change any code below this line
;
.method public static main([Ljava/lang/String;)V
       ; set limits used by this method
       .limit locals 3   ; = parameters + locals
       .limit stack  2
       ;
       ;             
       
        new Test3
        dup
        invokenonvirtual Test3/<init>()V
        astore 1
        aload 1
        invokevirtual Test3/bar()I 
        istore 2
        aload 1
        iload 2
        invokevirtual Test3/foo(I)V
        return
.end method
