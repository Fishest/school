.source Fibonacci.j
.class public Fibonacci
.super java/lang/Object

;
; standard constructor
;
.method public <init>()V
  aload_0
  invokenonvirtual java/lang/Object/<init>()V
  return
.end method

;
; main method
;
.method public static main([Ljava/lang/String;)V
  .limit locals 3 ; i, x, y
  .limit stack  4 ; 

  ;
  ; Setup output stream
  ; PrintStream output = java.lang.System.out;
  ;
  getstatic java/lang/System/out Ljava/io/PrintStream;
  
  ;
  ; Parse command line arguments
  ; int i = Integer.parseInt(args[0]);
  ;
  aload_0
  iconst_0
  aaload
  invokestatic java/lang/Integer/parseInt(Ljava/lang/String;)I
  istore_0

  ;
  ; initialize x and y
  ; int x = 0, y = 1;
  ;
  iconst_0
  istore_1
  iconst_1
  istore_2
  
  ;
  ; Test quick exit condition
  ; if (i > 2) return i;
  ;
  iload_0
  iconst_2
  if_icmpgt Loop  
  iload_0
  goto Exit
  
Loop:  
  ;
  ; Perform the computation
  ; x = y; y = x + y;
  ;
  iload_1
  iload_2
  dup
  istore_1
  iadd
  istore_2
  
  ;
  ; Check the exit condition
  ; if (--x <= 1) return y;
  ;
  iinc 0 -1
  iload_0
  iconst_1
  if_icmpgt Loop
  iload_2  	
  

Exit:
  ;
  ; Print the top variable to the output stream
  ; output.println(result); return;
  ;  
  invokevirtual java/io/PrintStream/println(I)V
  return
.end method
