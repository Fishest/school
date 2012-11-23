package studio6;
import common.Listing;
import common.OpenFile;

import autogen.Yylex;
import java_cup.runtime.*;

// $Id: BottomUpParse.java 15 2010-05-08 22:45:52Z cytron $

public abstract class BottomUpParse {

   protected boolean debug = false;
   public BottomUpParse() {
   }

   /** Causes the parser to trace its shift/reduce nature */
   public BottomUpParse setDebug(boolean debug) {
	   this.debug = debug;
	   return this;
   }
   
   /** Run this parser on each testfile */
   public void run() {
	   String[] args = getTestFiles();
	   for (int i=0; i < args.length; ++i) {
		   Listing.get().NewLine(1);
		   System.out.println("\n------------------------------------------------");
		   System.out.println("Run of " + getProblemName() + " test " + args[i]);
		   Listing.get().NewLine(1);
		   try {
			   lr_parser parser = getParser(
					   new Yylex(
							   new OpenFile(args[i])
					   )
			   );
			   if (debug) parser.debug_parse();
			   else parser.parse();

			   System.out.println("\nSuccessful parse");
		   } catch(Throwable t) {
			   t.printStackTrace();
			   System.err.flush(); System.out.flush();
			   System.out.println("\nAborting this test");
		   }
	   }

   }

   /** The parser */
   public abstract lr_parser getParser(Scanner s);
   
   /** Provides an array of file names on which the parse will be run */
   public abstract String[] getTestFiles();
   
   /** Used for identification purpopses */
   public abstract String   getProblemName();

}
