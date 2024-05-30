import sqlite3

# Create a connection object
conn = sqlite3.connect('database.db')
c = conn.cursor()

# # Create a table with column names LEFT and RIGHT, both int
# c.execute('''CREATE TABLE IF NOT EXISTS data
#                 (LEFT int, RIGHT int)''')
#
# # Insert some data
# c.execute("INSERT INTO data VALUES (1, 2)")

# # insert some data
# c.execute("INSERT INTO data VALUES (1, 2)")

# # check how many rows are in the table
# c.execute("SELECT * FROM data")
# print(c.fetchall())

# initialize the table by inserting five rows of -1
for i in range(5):
    c.execute("INSERT INTO data VALUES (-1, -1)")



# Commit the transaction
conn.commit()

# Close the connection
conn.close()

if __name__ == '__main__':
    pass
