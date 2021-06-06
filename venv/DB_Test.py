import psycopg2

conn = psycopg2.connect(database="testdb", user = "postgres", password = "Abcd1234", host = "127.0.0.1", port = "5432")

print ("Opened database successfully")

cur = conn.cursor()

#TO CREATE A TABLE

# cur.execute('''CREATE TABLE COMPANY
#       (ID INT PRIMARY KEY     NOT NULL,
#       NAME           TEXT    NOT NULL,
#       AGE            INT     NOT NULL,
#       ADDRESS        CHAR(50),
#       SALARY         REAL);''')
#print ("Table created successfully")

#TO INSERT TO TABLE

# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Prasanna', 32, 'California', 20000.00 )");
#
# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )");
#
# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )");
#
# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )");
# print ("Records created successfully")

#SELECT DATA FROM DB

# cur.execute("SELECT id, name, address, salary  from COMPANY")
# rows = cur.fetchall()
# for row in rows:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3], "\n")
#
# print ("Operation done successfully")

#UPDATE DATA OF DB
# cur.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
# conn.commit()
# print ("Total number of rows updated :", cur.rowcount)
#
# cur.execute("SELECT id, name, address, salary  from COMPANY")
# rows = cur.fetchall()
# for row in rows:
#    print ("ID = ", row[0])
#    print ("NAME = ", row[1])
#    print ("ADDRESS = ", row[2])
#    print ("SALARY = ", row[3], "\n")
#
# print ("UPDATE done successfully")

#DELETE FROM DB

cur.execute("DELETE from COMPANY where ID=2;")
conn.commit()
print ("Total number of rows deleted :", cur.rowcount)

cur.execute("SELECT id, name, address, salary  from COMPANY")
rows = cur.fetchall()
for row in rows:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("ADDRESS = ", row[2])
   print ("SALARY = ", row[3], "\n")

print ("DELETE done successfully")


#conn.commit()
conn.close()