====== Guru of the Week ======

What follows are my notes on Herb Sutter's GotW series.  More information can
be found on the site at [http://www.gotw.ca Guru of the Week]

** 1. Variable Initialization **
{{{
	SomeType t;     # uses default Sometype::Sometype()
	SomeType t();   # definition for a function that returns Sometype
	SomeType t = u; #is equivalent to
	SomeType t(u);  # if u is of a different type
	SomeType t(Sometype(u));
	# So that u is termporarily converted to SomeType
}}}

** 2. Temporary Objects **
{{{
	string FindAddr( list<Employee> l, string name )
	{
		for(list<Employee>::iterator i = l.begin();
			i != l.end(); i++ ) {
			if( *i == name )
				return (*i).addr;
		}
		return "";
	}
}}}

  - list<Employee> l should be passed by const references
  - string name should be passed by const references
    * Passing by value copies both values to the stack
  - i++ should be changed to ++i
    * Post increment must increment and return a decremented temporary
  - *i == name creates a temporary for paramter conversion (string)
  - return ""; builds a temporary string to return
    * Follow single-entry/single-exit
	* Declare local variable for return that can be optimized by compiler
  - Don't return references to local objects (they are on the stack)

** 3 Using the Standard Library **
{{{
	string FindAddr( const list<Employee>& l,
					 const string& name )
	{
		string addr;
		list<Employee>::const_iterator i =
		  find(l.begin(), l.end(), name);
		
		if (i != l.end())
			addr = (*i).addr;
		return addr;
	}
}}}

  - Using the STL algorithms is faster, easier, and safer
    * It removes extra temporaries and repeated calls to l.end()

** 4 Class Mechanics **
  - Watch out for silent conversions. One good way to avoid them is to make ctors explicit when possible
  - Prefer using "a op= b" instead of "a = a op b" for arithmetic operations
  - Prefer these guidelines for making an operator a member vs. nonmember function
  - Always return stream references from operator<< and operator>>
  - Prefer to implement postincrement in terms of preincrement

** 5 Overriding Virtual Functions **
  - Make base class destructors virtual
  - When providing a function with the same name as an inherited function, be sure to bring the inherited functions into scope with a "using" declaration if you don't want to hide them.
  - Never change the default parameters of overridden inherited functions.
    * The compiler will use the static type(base class) default paramaters and the dynamic type function
  - Reserach: g++ -fdump-class-hierarchy <file>.cpp

** 6 Const Correctness **
