.source Factorial.j
.class public Factorial
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
  .limit locals 4
  .limit stack 3

  getstatic java/lang/System/out Ljava/io/PrintStream;

  aload 0
  iconst_0
  aaload

  ;
  ; convert String at top of stack to int
  ;
  invokestatic java/lang/Integer/parseInt(Ljava/lang/String;)I

  ;
  ; copy top of stack to local var 1
  ;
  dup
  istore 1

  iconst_1
  if_icmpgt Label4

  iconst_1

  goto Label1

Label4:

  iconst_1
  istore 2

Label3:
  iload 1
  iconst_1
  if_icmple Label2

  iload 1
  iload 2
  imul

  istore 2

  iload 1
  iconst_1
  isub
  istore 1

  goto Label3

Label2:

  iload 2

Label1:


  ;
  ; print int at top of stack
  ;
  invokevirtual java/io/PrintStream/println(I)V

  return
.end method
