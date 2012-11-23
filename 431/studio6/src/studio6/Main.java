package studio6;
import common.Listing;
import common.OpenFile;

import java_cup.runtime.*;
import autogen.*;

// $Id: Main.java 19 2010-05-09 22:49:43Z cytron $

public class Main {
	public static void main(String args[]) throws Exception {
	      new Listing(System.out, "Studio 6");

//	      new Problem1() {
//	      public lr_parser getParser(Scanner s) {
//	      return new Parsercup1(s);
//	      }
//	      }.run();
	      
	      new Problem2() {
	    	  public lr_parser getParser(Scanner s) {
	    		  return new Parsercup2(s);
	    	  }
	      }.run();
	      
	      new Problem3() {
	      public lr_parser getParser(Scanner s) {
	      return new Parsercup3(s);
	      }
	      }.run();

//	      new Problem4() {
//	      public lr_parser getParser(Scanner s) {
//	      return new Parsercup4(s);
//	      }
//	      }.run();

//	      new Problem5() {
//	      public lr_parser getParser(Scanner s) {
//	      return new Parsercup5(s);
//	      }
//	      }.run();

	}

}

abstract class Problem1 extends BottomUpParse {
	public String getProblemName() { return "Problem 1a"; }
	public String[] getTestFiles() {
		return new String[] {
				"TestFiles/cup1.good1", 
				"TestFiles/cup1.good2"
		};
	}

}

abstract class Problem2 extends BottomUpParse {
	public String getProblemName() { return "Problem 2"; }
	public String[] getTestFiles() {
		return new String[] {
				"TestFiles/cup2.good1",  // Same testfiles as Problem 1
				"TestFiles/cup2.good2",
				"TestFiles/cup2.good3",
				"TestFiles/cup2.bad"
		};
	}

}

abstract class Problem3 extends BottomUpParse {
	public String getProblemName() { return "Problem 3"; }
	public String[] getTestFiles() {
		return new String[] {
				"TestFiles/cup3.good", 
				"TestFiles/cup3.bad"
		};
	}

}

abstract class Problem4 extends BottomUpParse {
	public String getProblemName() { return "Problem 4"; }
	public String[] getTestFiles() {
		return new String[] {
				"TestFiles/cup4.good1", 
				"TestFiles/cup4.good2"
		};
	}

}

abstract class Problem5 extends BottomUpParse {
	public String getProblemName() { return "Problem 5"; }
	public String[] getTestFiles() {
		return new String[] {
				"TestFiles/cup5.good1", 
				"TestFiles/cup5.good2"
		};
	}

}
