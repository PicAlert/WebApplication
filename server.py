from flask import Flask, jsonify, request, abort, render_template
import psycopg2, urlparse, os

if 'DATABASE_URL' in os.environ:
    urlparse.uses_netloc.append('postgres')
    db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
else:
    config = {}
    execfile('settings.conf', config)
    urlparse.uses_netloc.append('postgres')
    db_url = urlparse.urlparse(config['DATABASE_URL'])
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
def landing():
     return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username or password.'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password.'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('landing'))
    return render_template('login.html', error=error)

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port, debug=True)