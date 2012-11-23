.class public Test2
.super java/lang/Object

;
;  Team members:
;
;
;
;
;   Answer question 6) below and turn in this file,
;       appropriately modified,  with the console output
;

;
; standard initializer
;
.method public <init>()V
   aload_0
   invokenonvirtual java/lang/Object/<init>()V
   return
.end method

.method public static bar()I
   .limit stack  3
   .limit locals 0

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
   ;astore 1

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
   ;astore 2  ;  store the result so we can print it below
   ;
   ; ... and print it
   ;
   ;aload 1    ; push the PrintStream object
   ;aload 2    ; push the string we just created and then print it
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
       .limit locals 1   ; = parameters + locals
       .limit stack  1
        invokestatic Test2/bar()I 
        invokestatic Test2/foo(I)V
        return
.end method
