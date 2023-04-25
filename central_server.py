from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to EC530 project: P2P Pro!'


@app.route('/online')
def live_clients():
    # connect to sqlite3 database
    conn = sqlite3.connect('database/ec530_sqlite.db')
    c = conn.cursor()
    c.execute("SELECT username, ip_addr FROM clients")
    content = c.fetchall()
    c.close()

    return str(content)


@app.route('/login')
def login():
    try:
        # connect to sqlite3 database
        conn = sqlite3.connect('database/ec530_sqlite.db')
        c = conn.cursor()
        username = request.args.get('username')
        password = request.args.get('password')

        c.execute("SELECT password FROM users WHERE username=?", (username,))

        ret= c.fetchone()
        if ret is None:
            return 'Fail'

        password_in_db = ret[0]
        c.close()
        if password_in_db == password:
            return 'Success'
        else:
            return 'Fail'
    except Exception as e:
        print(e)
        return 'Fail'


@app.route('/register')
def register():
    try:
        # connect to sqlite3 database
        conn = sqlite3.connect('database/ec530_sqlite.db')
        c = conn.cursor()
        username = request.args.get('username')
        password = request.args.get('password')

        c.execute("SELECT password FROM users WHERE username=?", (username,))

        if c.fetchone() is not None:
            return 'Fail'

        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        c.close()
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'


@app.route('/add_client')
def add_client():
    try:
        # connect to sqlite3 database
        conn = sqlite3.connect('database/ec530_sqlite.db')
        c = conn.cursor()
        username = request.args.get('username')
        ip_addr = request.args.get('ip_addr')

        c.execute("INSERT INTO clients (username, ip_addr) VALUES (?, ?)", (username, ip_addr))
        conn.commit()
        c.close()
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'


if __name__ == '__main__':
    print("Central server starting...")

    connection = sqlite3.connect('database/ec530_sqlite.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM clients")
    connection.commit()
    connection.close()
    print("Live clients database initialized")

    app.run(port=10000)
