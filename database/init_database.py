import sqlite3

# connect to sqlite3
conn = sqlite3.connect('ec530_sqlite.db')
c = conn.cursor()

# tables initialization, drop existing tables to clear database
target_table_name = 'clients'
c.execute(f"DROP TABLE IF EXISTS {target_table_name}")

# check if table clients exists, if not, create it
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (target_table_name,))
result = c.fetchone()
if result:
    print(f"table {target_table_name} exists")
else:
    # create table users
    c.execute('''CREATE TABLE clients (uid INTEGER PRIMARY KEY AUTOINCREMENT, username text NOT NULL UNIQUE, 
    ip_addr text NOT NULL)''')
    print("create table " + target_table_name)

# tables initialization, drop existing tables to clear database
target_table_name = 'history_connections'
c.execute(f"DROP TABLE IF EXISTS {target_table_name}")

# check if table users exists, if not, create it
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (target_table_name,))
result = c.fetchone()
if result:
    print(f"table {target_table_name} exists")
else:
    # create table users
    c.execute('''CREATE TABLE history_connections (cid INTEGER PRIMARY KEY AUTOINCREMENT, connection_time text, 
    username1 text, ip_addr1 text, username2 text, ip_addr2 text, message text)''')
    print("create table " + target_table_name)

# tables initialization, drop existing tables to clear database
target_table_name = 'users'
c.execute(f"DROP TABLE IF EXISTS {target_table_name}")

# check if table users exists, if not, create it
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (target_table_name,))
result = c.fetchone()
if result:
    print(f"table {target_table_name} exists")
else:
    # create table users
    c.execute('''CREATE TABLE users (uid INTEGER PRIMARY KEY AUTOINCREMENT, username text UNIQUE, 
    password text)''')
    print("create table " + target_table_name)
