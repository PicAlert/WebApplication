from flask import Flask, jsonify, request, abort, render_template 
from flask import session, redirect, url_for, escape
import psycopg2, urlparse, os, hashlib

if 'DATABASE_URL' in os.environ:
    urlparse.uses_netloc.append('postgres')
    db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
    secret_key = os.environ['secret_key']
else:
    config = {}
    execfile('settings.conf', config)
    urlparse.uses_netloc.append('postgres')
    db_url = urlparse.urlparse(config['DATABASE_URL'])
    secret_key = config['secret_key']

app = Flask(__name__)

conn = psycopg2.connect(
    database=db_url.path[1:],
    user=db_url.username,
    password=db_url.password,
    host=db_url.hostname,
    port=db_url.port
)

# conn.cursor will return a cursor object to perform queries
cur = conn.cursor() # https://wiki.postgresql.org/wiki/Psycopg2_Tutorial

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username or password.'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid username or password.'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('landing'))
#     return render_template('login.html', error=error)

app.secret_key = secret_key

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)