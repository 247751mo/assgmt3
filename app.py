import os
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
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

# Explicitly call the table creation function
create_tables()

if __name__ == '__main__':
    app.run()
# Home page route
@app.route('/')
def index():
    datapoints = DataPoint.query.all()
    return render_template('index.html', datapoints=datapoints)

# Add a new data point
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        try:
            hours_studied = float(request.form['hours_studied'])
            sleep_hours = float(request.form['sleep_hours'])
            performance_level = int(request.form['performance_level'])

            # Validation
            if hours_studied + sleep_hours > 24:
                flash("Hours studied and sleep hours cannot exceed 24 in total.")
                return redirect(url_for('add'))
            if performance_level < 1 or performance_level > 3:
                flash("Performance level must be between 1 and 3.")
                return redirect(url_for('add'))

            # Add data to the database
            new_datapoint = DataPoint(hours_studied=hours_studied, sleep_hours=sleep_hours, performance_level=performance_level)
            db.session.add(new_datapoint)
            db.session.commit()

            return redirect(url_for('index'))
        except ValueError:
            flash("Invalid input. Please ensure all fields are filled correctly.")
            return redirect(url_for('add'))

    return render_template('add.html')

# Delete a data point
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
    datapoints = DataPoint.query.all()  # Get all records from the database
    if datapoints:
        result = [{"id": dp.id, "hours_studied": dp.hours_studied, "sleep_hours": dp.sleep_hours, "performance_level": dp.performance_level} for dp in datapoints]
        return jsonify(result), 200
    else:
        return jsonify({"error": "No data found"}), 404  # Handle the case where no data is found


# API endpoint: Add a new data point
@app.route('/api/data', methods=['POST'])
def api_add_data():
    data = request.get_json()

    # Validate the data
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

    # Add the new data point
    new_datapoint = DataPoint(hours_studied=hours_studied, sleep_hours=sleep_hours, performance_level=performance_level)
    db.session.add(new_datapoint)
    db.session.commit()
    return jsonify({"id": new_datapoint.id}), 201

@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_data(record_id):
    datapoint = DataPoint.query.get(record_id)  # Get the record by ID

    if datapoint is None:
        return jsonify({"error": "Record not found"}), 404  # If record not found

    db.session.delete(datapoint)  # Delete the record
    db.session.commit()  # Commit the transaction to the database

    return jsonify({"deleted_record_id": record_id}), 200  # Return a success message


# Run the app
if __name__ == '__main__':
    app.run()
