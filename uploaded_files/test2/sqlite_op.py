# this is the file to implement sqlite database API
import sqlite3

# connect to sqlite3 database
conn = sqlite3.connect('database/ec530_sqlite.db')
c = conn.cursor()


# insert a new client into clients table
def insert_clients(username, ip_addr):
    try:
        c.execute("INSERT INTO clients (username, ip_addr) VALUES (?, ?)", (username, ip_addr))
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True


# get all clients from clients table
def get_clients():
    c.execute("SELECT username, ip_addr FROM clients")
    return c.fetchall()


# insert a new connection text into history_connections table
def insert_history_connections(connection_time, username1, ip_addr1, username2, ip_addr2, message):
    try:
        c.execute("INSERT INTO history_connections (connection_time, username1, ip_addr1, username2, ip_addr2, "
                  "message) "
                  "VALUES (?, ?, ?, ?, ?, ?)", (connection_time, username1, ip_addr1, username2, ip_addr2, message))
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True


# get all connections from history_connections table
def get_history_connections():
    c.execute("SELECT connection_time, username1, ip_addr1, username2, ip_addr2, message FROM history_connections")
    return c.fetchall()

# insert_clients("test1", "127.0.0.1")
# print(get_clients())
