import os

from flask import Flask, request, jsonify, send_from_directory
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

        ret = c.fetchone()
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


@app.route('/delete_client')
def delete_client():
    try:
        # connect to sqlite3 database
        conn = sqlite3.connect('database/ec530_sqlite.db')
        c = conn.cursor()
        username = request.args.get('username')

        c.execute("DELETE FROM clients WHERE username=?", (username,))
        conn.commit()
        c.close()
        return 'Success'
    except Exception as e:
        print(e)
        return 'Fail'


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    username = request.form['username']
    file = request.files['file']
    filename = file.filename
    if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], username)):
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], username))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], username, filename))

    return jsonify({'filename': filename})


app.config['UPLOAD_FOLDER'] = 'uploaded_files'


@app.route('/share/<username>/<filename>', methods=['GET'])
def download(username, filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], username+'/'+filename, as_attachment=True)


@app.route('/storage')
def storage():
    username = request.args.get('username')
    files = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], username))
    return jsonify({'files': files})



if __name__ == '__main__':
    print("Central server starting...")

    connection = sqlite3.connect('database/ec530_sqlite.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM clients")
    connection.commit()
    connection.close()
    print("Live clients database initialized")

    app.run(port=10000)
