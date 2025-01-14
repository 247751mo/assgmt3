import os
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours_studied = db.Column(db.Float, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=False)
    performance_level = db.Column(db.Integer, nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()


@app.route('/')
def index():
    datapoints = DataPoint.query.all()
    return render_template('index.html', datapoints=datapoints)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        try:
            hours_studied = float(request.form['hours_studied'])
            sleep_hours = float(request.form['sleep_hours'])
            performance_level = int(request.form['performance_level'])

            if not hours_studied or not sleep_hours or not performance_level:
                abort(400)
            if hours_studied + sleep_hours > 24:
                abort(400)
            if performance_level < 1 or performance_level > 3:
                abort(400)

            new_datapoint = DataPoint(hours_studied=hours_studied, sleep_hours=sleep_hours, performance_level=performance_level)
            db.session.add(new_datapoint)
            db.session.commit()

            return redirect(url_for('index'))
        except ValueError:
            abort(400)

    return render_template('add.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    datapoint = DataPoint.query.get(id)
    if datapoint is None:
        abort(404, description="Record not found")
    db.session.delete(datapoint)
    db.session.commit()
    flash(f'Data point with ID {id} was successfully deleted!')
    return redirect(url_for('index'))

@app.route('/api/data', methods=['GET'])
def get_data():
    datapoints = DataPoint.query.all()
    if datapoints:
        result = [{"id": dp.id, "hours_studied": dp.hours_studied, "sleep_hours": dp.sleep_hours, "performance_level": dp.performance_level} for dp in datapoints]
        return jsonify(result), 200
    else:
        return jsonify({"error": "No data found"}), 404


@app.route('/api/data', methods=['POST'])
def api_add_data():
    data = request.get_json()

    try:
        hours_studied = float(data['hours_studied'])
        sleep_hours = float(data['sleep_hours'])
        performance_level = int(data['performance_level'])

        if hours_studied + sleep_hours > 24:
            return jsonify({"error": "Hours studied and sleep hours cannot exceed 24 in total"}), 400
        if performance_level < 1 or performance_level > 3:
            return jsonify({"error": "Performance level must be between 1 and 3"}), 400
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid data"}), 400

    new_datapoint = DataPoint(hours_studied=hours_studied, sleep_hours=sleep_hours, performance_level=performance_level)
    db.session.add(new_datapoint)
    db.session.commit()
    return jsonify({"id": new_datapoint.id}), 201

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_data(record_id):
    datapoint = DataPoint.query.get(record_id)

    if datapoint is None:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(datapoint)
    db.session.commit()
    return jsonify({"deleted_record_id": record_id}), 200


if __name__ == '__main__':
    app.run()
