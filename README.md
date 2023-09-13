# SQLAlchemy Challenge: SurfsUp

## Project Description

This project, titled **SurfsUp**, involves analyzing climate data for Honolulu, Hawaii, to assist with holiday vacation planning. The analysis includes exploring 
climate data stored in an SQLite database using Python, SQLAlchemy ORM queries, Pandas, and Matplotlib. The project is divided into two parts:

### Part 1: Analyze and Explore the Climate Data

In this section, utilizing Python and SQLAlchemy, perform a basic climate analysis and data exploration 
of the climate database. 

The following steps outline the analysis:

1. Connect to the SQLite database using SQLAlchemy's `create_engine()` function.

2. Reflect the database tables into classes using `automap_base()` and create references 
to the `station` and `measurement` classes.

3. Link Python to the database by creating a SQLAlchemy session. 

*It's essential to close the session properly.*

4. **Perform a precipitation analysis**:
   - Find the most recent date in the dataset.
   - Retrieve the previous 12 months of precipitation data.
   - Load the results into a Pandas DataFrame, sort it by date, and plot the data.
   - Print summary statistics for the precipitation data.

5. **Conduct a station analysis**:
   - Calculate the total number of stations in the dataset.
   - Identify the most active station with the highest number of observations.
   - Find the lowest, highest, and average temperatures for the most active station.
   - Query the previous 12 months of temperature observation (TOBS) data 
for the most active station and plot it as a histogram.

### Part 2: Design Your Climate App

In the second part, a Flask API is designed based on the analysis and queries from Part 1. 
The following routes are created:

- `/`: The homepage that lists all available routes.
- `/api/v1.0/precipitation`: Returns the last 12 months of precipitation data in JSON format.
- `/api/v1.0/stations`: Returns a JSON list of weather stations.
- `/api/v1.0/tobs`: Queries the previous year's temperature observations for the most active station and returns them in JSON format.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Returns JSON lists of minimum, average, and maximum temperatures for specified date ranges.

## Usage

- Run the Flask app using `python app.py` to access the climate data API and explore the available routes.




