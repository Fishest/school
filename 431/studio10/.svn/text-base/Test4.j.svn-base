.class public Test4
.super java/lang/Object

;
;  Team members:
;
;
;    Answer question:
;        9)  Assuming big-endian format,
;             what is the value in hex of the first 4 bytes of a .class file?
;        0xCAFE 0xBABE
;    Handle question 10) below, and turn in this file, appropriately modified,
;      with your console output
;
;    Consider the contest as explained below
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
   sipush 431
   ireturn
.end method

;
;  Do not change the signature of this method
;
.method public static foo(I)V
   .limit locals 1 
   .limit stack  2
Label:   
   ; print our number
   getstatic java/lang/System/out Ljava/io/PrintStream;
   iload_0
   invokevirtual java/io/PrintStream/println(I)V

   ; decrement and recurse
   iinc 0 -1
   iload_0
   ifge Label
   
   ;
   ; 10) Rewrite the above code to print integers, starting at the
   ;       value of the supplied parameter, and counting down to 0,
   ;       including 0.  Print just one integer per line.
   ;
   ;     Contest:  develop a solution that uses the fewest bytecodes in
   ;       the resulting .class file.  The build process will indicate
   ;       the size of your .class file.
   ;     You can change anything you wish in this file except for the
   ;        existing methods' signatures -- they must stay the same.
   ;     You can introduce new methods if you wish.
   ;     You may not introduce any new classes
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
        invokestatic Test4/bar()I 
        invokestatic Test4/foo(I)V
        return
.end method
