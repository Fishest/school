package common;

import java.io.*;

public class Listing {

   private static final String endl="\n";
   private PrintStream ps;
   private static Listing staticListing;
   private int linenumber, col;
   private static boolean echoStdErr = false;

   public Listing(PrintStream ps, String message) {
     this.ps  = ps;
     staticListing = this;
     StartListing(message);
   }

   public Listing(PrintStream ps) { this(ps, ""); }

   public static Listing get() {  return(staticListing); }

   public void StartListing(String message) {
      out(message);
      linenumber = 0;
      col        = 1;
      NewLine(1);
   }

   public void EndListing(String message) {
      out(message);
   }

   public int getLineNumber() { return(linenumber); }
   public int getColNumber()  { return(col);        }

   private static String makestrlen(String text, int len) {
      String ans = text;
      while (ans.length() < len) ans = " " + ans;
      return(ans);
   }

   private static String makestrlen(int text, int len) {
      return makestrlen(text+"", len);
   }

   public void NewLine(int bump) {
      linenumber += bump;
      if (bump > 0) {
         col = 1;
         out(endl + makestrlen(linenumber,7) + ": ");
      }
      else {
         out(endl + "*" + makestrlen(linenumber,6) + ": ");
      }
   }
   public void echo(String text) {
      col += text.length();
      out(text);
   }
   public void StartMessage() {
      InsertMessage("^^^");
   }
   private void InsertMessage(String text) {
      NewLine(0);
      for (int i=1; i<=col; ++i) out(" ");
      out(text);
   }
   public void EndMessage() {
      InsertMessage("");
   }
   public void EmitMessage(String text) {
      StartMessage();
      out("\n"+text);
      if (echoStdErr) System.err.println("\n"+text);
      EndMessage();
   }
   public void warning(String text) {
      EmitMessage("Warning: " + text);
   }
   public void oops(String text)
   {
      EmitMessage(text);
      EndListing("End.");
      System.err.println(
         "Aborting due to error at line " + linenumber + " column " + col + endl
      );
      System.exit(1);
   }
   private void out(String text) {
      ps.print(text);
   }
}
