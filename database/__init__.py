import sqlite3

connection = sqlite3.connect('database/verifiedUsers.db')
cursor = connection.cursor()

# create user table
# contains: 
	# email as primary key
	# username as discord username
	# num_reg as number of times email has been registered/associated with a discord account
userTable = '''CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, 
												id INTEGER,
												num_reg INTEGER)'''
cursor.execute(userTable)

connection.commit()