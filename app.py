import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_datapoint(datapoint_id):
    conn = get_db_connection()
    datapoint = conn.execute('SELECT * FROM datapoints WHERE id = ?',
                        (datapoint_id,)).fetchone()
    conn.close()
    if datapoint is None:
        abort(404)
    return datapoint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():  # put application's code here
    conn = get_db_connection()
    datapoints = conn.execute('SELECT * FROM datapoints').fetchall()
    conn.close()
    return render_template('index.html', datapoints=datapoints)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        hours_studied = float(request.form['hours_studied'])
        sleep_hours = float(request.form['sleep_hours'])
        performance_level = request.form['performance_level']

        if hours_studied+sleep_hours > 24:
            abort(400)

        if not hours_studied or not sleep_hours or not performance_level:
            abort(400)

        try:
            performance_level = int(performance_level)
        except ValueError:
            abort(400)

        if performance_level < 1 or performance_level > 3:
            abort(400)

        # If all validation passes, add the datapoint to the database
        conn = get_db_connection()
        conn.execute('INSERT INTO datapoints (hours_studied, sleep_hours, performance_level) VALUES (?, ?, ?)',
                     (hours_studied, sleep_hours, performance_level))
        conn.commit()
        conn.close()

        # Redirect to home page
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    datapoint = get_datapoint(id)
    conn = get_db_connection()
    if datapoint is None:
        # If the record doesn't exist, show a 404 error page
        conn.close()
        abort(404)
    conn.execute('DELETE FROM datapoints WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(datapoint['id']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
