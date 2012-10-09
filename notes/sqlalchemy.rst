================================================================================
 SQL Expression Tutorial
================================================================================
 
--------------------------------------------------------------------------------
Initialization
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy import Table, Column, Integer, String
    from sqlalchemy import MetaData, ForeignKey
    
    # this is the underlying db translation layer
    engine = create_engine('sqlite:///:memory', echo=True)
    metadata = MetaData()	# table catalog aggregate
    
    # an example table
    users = Table('users', metadata,
    	Column('id', Integer, primary_key=True),
    	Column('name', String),
    	Column('fullname', String),
    )
    
    # indempotent table creation, based on engine
    metadata.create_all(engine)

--------------------------------------------------------------------------------
Basic Operation
--------------------------------------------------------------------------------

.. code-block:: python

    insert = users.insert()	# blank insert statement
    insert = users.insert().values(name='jack', fullname='Jack John')
    str(insert)
    insert.compile().params	# see the compile parameters
    
    conn = engine.connect()
    result = conn.execute(insert)
    result.inserted_primary_key
    
    conn.execute(users.insert(), id=2, name='wendy', fullname='Wendy Williams')
    conn.execute(users.insert(), [ # all must have same number of keys
    	{ 'name': mark',  fullname': Mark Madison' },
    	{ 'name': sarah', fullname': Sarah Salter' },
    	{ 'name': erin',  fullname': Erin Kimmins' },
    ])
    
    result = engine.execute(...)
    
    metadata.bind = engine
    result = users.insert().execute(...)

--------------------------------------------------------------------------------
Select Operations
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchemy.sql import select
    
    s = select([users])
    result = conn.execute(s)
    for row in result: print row
    
    result = conn.execute(s)
    row = result.fetchone()
    rows = result.fetchall()
    
    # the following are equivalent
    print row['name'], row['fullname']
    print row[1], row[2]
    print row[users.c.name], row[users.c.fullname]
    
    # enumerate all the columns with type
    for key in users.c.keys():
    	print row[key], type(row[key])
    
    # call close if there are remaining rows in the cursor
    result.close()
    
    # selecting explicit columns
    s = select([users.c.name, users.c.fullname])
    # adding a where clause
    s = select([users, other], users.c.id == other.c.user_id)

--------------------------------------------------------------------------------
Override Operators
--------------------------------------------------------------------------------

.. code-block:: python

    users.c.id == other.c.user_id
    users.c.id == 7
    users.c.id != None
    'fred' > users.c.name
    users.c.name + users.c.fullname	# concat operation
    users.c.name.op('custom_operation')('value')
    users.c.name.between('m', 'z')	# range operation

--------------------------------------------------------------------------------
Select Advanced
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchemy.sql import and_, or_, not_
    and_(users.c.name.like('j%'), users.c.id==other.c.user_id,
    	or_(other.c.email_address=='this@that.com', other.c.email_address=='that@this.com'),
    	not_(users.c.id > 5))
    
    users.c.name.like('j%')	\
    	& (users.c.id==other.c.user_id)	\
    	& ((other.c.email_address=='this@that.com') | (other.c.email_address=='that@this.com'))	\
    	& ~(users.c.id > 5)
    
    # can do as construct projection
    (users.c.fullname + ", " + users.c.name).label('title')

--------------------------------------------------------------------------------
Raw Text
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchem.sql import text
    
    s = text("""SELECT users.fullname
                  FROM users, other
                 WHERE users.id = other.user_id
                   AND users.name LIKE :e1""")
    result = conn.execute(s, e1='g%')

--------------------------------------------------------------------------------
Joins
--------------------------------------------------------------------------------

.. code-block:: python

    users.join(other)
    users.outerjoin(other)
    s = select([users.c.fullname], from_obj=[users.join(other)])

--------------------------------------------------------------------------------
Generating Statements
--------------------------------------------------------------------------------

.. code-block:: python

    query = users.select()
    query = query.where(users.c.name == 'jack')
    query = query.order_by(users.c.fullname.desc())
    result = query.execute(query).fetchall()

--------------------------------------------------------------------------------
Functions
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchemy.sql import func
    s = select([func.max(user.c.name, type_=String).label('maxname')]).scalar()

--------------------------------------------------------------------------------
Updates
--------------------------------------------------------------------------------

.. code-block:: python

    u = users.update().where(users.c.name=='jack').values(name='ed')

--------------------------------------------------------------------------------
Deletes
--------------------------------------------------------------------------------

.. code-block:: python

    d = users.delete() # deletes everything
    d = users.delete().where(users.c.name == 'ed')

================================================================================
 SQL ORM Tutorial
================================================================================

--------------------------------------------------------------------------------
Initialization
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String
    from sqlalchemy import MetaData
    from sqlalchemy.orm import sessionmaker
    
    # this is the underlying db translation layer
    engine  = create_engine('sqlite:///:memory', echo=True)
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
    
    # an example table
    class User(Base):
    
    	__tablename__ = 'users'
    
    	id = Column(Integer, primary_key=True)
    	name = Column(String)
    	fullname = Column(String)
    	password = Column(String)
    
    # indempotent table creation, based on engine
    Base.metadata.create_all(engine)
    
    # can see automatically created data
    User.__table__
    User.__mapper__

--------------------------------------------------------------------------------
Basic Operations
--------------------------------------------------------------------------------

.. code-block:: python

    session = Session()
    user1 = User('jack', 'Jack Johnny', 'password)
    session.add(user)
    user2 = session.query(User).filter_by(name='ed').first()
    user1 == user2	# True
    
    session.add_all([
    	User('fred', 'Fred Flinstone', 'password),
    	User('mary', 'Mary Contrary', 'password),
    	User('john', 'Johnny Cash', 'password)
    ])
    user2.password = 'more secure'

--------------------------------------------------------------------------------
Session Status
--------------------------------------------------------------------------------

.. code-block:: python

    session.dirty		# checks for changed models
    session.new			# checks for newly added models
    session.deleted		# checks for newly deleted models
    session.commit()	# commits pending changes
    session.rollback()	# revert pending changes

--------------------------------------------------------------------------------
Querying the ORM
--------------------------------------------------------------------------------

.. code-block:: python

    for user in session.query(User).order_by(User.id):
    	print user.name, user.fullname
    
    for name, fullname in session.query(User.name, User.fullname):
    	print name, fullname
    
    for row in session.query(User, User.name).all():
    	print row	# <User>, name
    
    for row in session.query(User.name.label('name_label')).all():
    for row in session.query(User).order_by(User.id)[1:3]	# limit and offset
    for row in session.query(User.name).filter_by(fullname='Johnny Cash'):
    for row in session.query(User.name).filter(User.fullname=='Johnny Cash'):
    
    # queries are generative (lazy generation)
    query = session.query(User.name).\
    	filter(User.name=='john').\
    	filter(User.fullname=='Johnny Cash')

--------------------------------------------------------------------------------
Filter Operations
--------------------------------------------------------------------------------

.. code-block:: python

    query.filter(User.name == 'fred')
    query.filter(User.name != 'fred')
    query.filter(User.name.like('%ed')
    query.filter(User.name.in_(['ed', 'fred', 'jed']))
    query.filter(~User.name.in_(['ed', 'fred', 'jed']))
    query.filter(User.name == None)	# is null
    query.filter(User.name != None)	# is not null
    query.filter(User.name.match('mary'))
    
    query.filter("id < 224").order_by("id")
    query.filter("id < :value and name=:name").params(value=224, name='fred')
    query.from_statement("SELECT * FROM users where name=:name").params(name='fred')
    query(func.count(User.id)).scalar()
    query(func.count(User.name), User.name).group_by(User.name).all()

--------------------------------------------------------------------------------
Return Values
--------------------------------------------------------------------------------

.. code-block:: python

    query.all()		# executes and returns result list
    query.first()	# executes with limit one
    query.one()		# executes and throws if not only one result
    query.count()	# how many rows would have been returned

--------------------------------------------------------------------------------
Joins
--------------------------------------------------------------------------------

.. code-block:: python

    query.(user, Address).filter(User.id == Address.user_id)
    query.(user).join(Address).filter(Address.email_address == 'this@that.com')
    query.(user).join(Address, User.id == Address.user_id)
    query.(user).outerjoin(User.addresses)

--------------------------------------------------------------------------------
Exists
--------------------------------------------------------------------------------

.. code-block:: python

    from sqlalchemy.sql import exists
    
    query = exists.where(Address.user_id == User.id)
    query(User.name).filter(User.addresses.any())
    query(User.name).filter(User.addresses.any(Address.email_address.like('%gmail.com')))
    query(User.name).filter(User.addresses.has(Address.email_address.like('%gmail.com')))

--------------------------------------------------------------------------------
Delete
--------------------------------------------------------------------------------

.. code-block:: python

    user = query(...)
    session.delete(user)
