import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

# Get the current working directory
current_directory = os.getcwd()

# Construct the full path to the database file
database_path = os.path.join(current_directory, "Resources", "hawaii.sqlite")

app = Flask("HAWAIVE")

# Configure SQLAlchemy to use the full database path
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"

db = SQLAlchemy(app)

# Create an application context to avoid "Working outside of application context" error
app.app_context().push()

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(db.engine, reflect=True)  # Use the SQLAlchemy engine

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Define the home route and provide route descriptions.
@app.route('/')
def home():
    """
    Displays a welcome message and lists available routes.

    Returns:
        str: A formatted HTML message with available routes.
    """
    return (
        f"Welcome to the Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        '<a href="/api/v1.0/precipitation" target="_blank">/api/v1.0/precipitation</a> - Precipitation data for the last 12 months<br/>'
        '<a href="/api/v1.0/stations" target="_blank">/api/v1.0/stations</a> - List of weather stations<br/>'
        '<a href="/api/v1.0/tobs" target="_blank">/api/v1.0/tobs</a> - Temperature observations for the last 12 months of the most active station<br/>'
        '<a href="/api/v1.0/start_date" target="_blank">/api/v1.0/start_date</a> - Minimum, average, and maximum temperatures from the start_date to the end of the dataset<br/>'
        '<a href="/api/v1.0/start_date/end_date" target="_blank">/api/v1.0/start_date/end_date</a> - Minimum, average, and maximum temperatures between start_date and end_date'
    )

# Define the precipitation route and provide a route description.
@app.route('/api/v1.0/precipitation')
def precipitation():
    """
    Retrieve and return precipitation data for the last 12 months.

    Returns:
        jsonify: JSON representation of precipitation data.
    """
    # Create a session using the db object
    session = Session(db.engine)

    # Query the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date one year from the most recent date.
    one_year_ago = (datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)).strftime('%Y-%m-%d')

    # Query the last 12 months of precipitation data.
    precipitation_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary.
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    session.close()  # Close the session
    return jsonify(precipitation_dict)

# Define the stations route and provide a route description.
@app.route('/api/v1.0/stations')
def stations():
    """
    Retrieve and return a list of weather stations.

    Returns:
        jsonify: JSON representation of weather stations.
    """
    # Create a session using the db object
    session = Session(db.engine)

    # Query all weather stations.
    station_data = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries.
    stations_list = [{"Station ID": station, "Station Name": name} for station, name in station_data]
    
    session.close()  # Close the session
    return jsonify(stations_list)

# Define the temperature observations route and provide a route description.
@app.route('/api/v1.0/tobs/<start_date>')
def tobs_start_date_route(start_date):
    """
    Retrieve and return temperature observations for the last 12 months of the most active station
    from start_date to the end of the dataset.

    Args:
        start_date (str): Start date for temperature analysis.

    Returns:
        jsonify: JSON representation of temperature observations.
    """
    # Create a session using the db object
    session = Session(db.engine)

    # Find the most active station.
    most_active_station = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station)\
        .order_by(func.count(Measurement.station).desc())\
        .first()[0]

    # Query temperature observations for the last 12 months of the most active station from start_date.
    tobs_data = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= start_date).all()

    # Convert the query results to a list of dictionaries.
    tobs_list = [{"Date": date, "Temperature": tobs} for date, tobs in tobs_data]

    session.close()  # Close the session
    return jsonify(tobs_list)

# Define start route and provide route descriptions.
@app.route('/api/v1.0/<start_date>')
def start_date_route(start_date):
    """
    Retrieve and return minimum, average, and maximum temperatures from start_date to the end of the dataset.

    Args:
        start_date (str): Start date for temperature analysis.

    Returns:
        jsonify: JSON representation of temperature statistics.
    """
    # Create a session using the db object
    session = Session(db.engine)

    # Query minimum, average, and maximum temperatures from start_date to the end of the dataset.
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).all()

    # Convert the query results to a dictionary.
    temperature_stats = {
        "Minimum Temperature": temp_stats[0][0],
        "Average Temperature": temp_stats[0][1],
        "Maximum Temperature": temp_stats[0][2]
    }

    # Close the session
    session.close()

    # Return the temperature statistics as JSON
    return jsonify(temperature_stats)

# Define start and end route and provide route descriptions.
@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end_date_route(start_date, end_date):
    """
    Retrieve and return minimum, average, and maximum temperatures between start_date and end_date.

    Args:
        start_date (str): Start date for temperature analysis.
        end_date (str): End date for temperature analysis.

    Returns:
        jsonify: JSON representation of temperature statistics.
    """
    # Create a session using the db object
    session = Session(db.engine)

    # Query minimum, average, and maximum temperatures between start_date and end_date.
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Convert the query results to a dictionary.
    temperature_stats = {
        "Minimum Temperature": temp_stats[0][0],
        "Average Temperature": temp_stats[0][1],
        "Maximum Temperature": temp_stats[0][2]
    }

    # Close the session
    session.close()

    # Return the temperature statistics as JSON
    return jsonify(temperature_stats)

# Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
