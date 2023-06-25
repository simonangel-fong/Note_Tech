import psycopg2 as pg2

conn = pg2.connect(database='dvdrental', user='postgres', password='Simon!23')

# create a cursor
cur = conn.cursor()

# Pass in a PostgreSQL query as a string
cur.execute("SELECT * FROM payment")

# Return a tuple of the first row as Python objects
data = cur.fetchone()
print('fetchone', data)

# Return All rows at once
# data = cur.fetchall()
# print('fetchall', data)

# Return N number of rows
data = cur.fetchmany(10)
print('fetchmany', data)

# Inserting Information
query1 = '''
        DROP TABLE new_table;
        CREATE TABLE new_table (
            userid integer
            , tmstmp timestamp
            , type varchar(10)
        );
        '''
cur.execute(query1)
# commit the changes to the database
conn.commit()
# Don't forget to close the connection!
# killing the kernel or shutting down juptyer will also close it
conn.close()
