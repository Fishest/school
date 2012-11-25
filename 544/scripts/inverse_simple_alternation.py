from common import *

users   = get_users(sys.argv[1:])
cake    = get_cake(users[0])
factory = get_algorithm('InverseAlternatingChoice')
print factory(users, cake).divide()
