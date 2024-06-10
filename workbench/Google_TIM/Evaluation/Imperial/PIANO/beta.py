import pandas as pd
import airportsdata
import csv

# Load the CSV file
file_path = 'Summary.csv'
data = pd.read_csv(file_path)

# Get the airports data
airports = airportsdata.load('ICAO')

# Function to get country from ICAO code
def get_country(icao_code):
    airport_info = airports.get(icao_code)
    return airport_info['country'] if airport_info else 'Unknown'

# Function to get IATA code from ICAO code
def get_iata(icao_code):
    airport_info = airports.get(icao_code)
    return airport_info['iata'] if airport_info else 'Unknown'

# Split the callsign into airline code and flight number
data[['airline_code', 'flight_number_split']] = data['callsign'].str.extract(r'([A-Z]+)(\d+)')

# Map origin and destination airports to countries
data['depctry'] = data['origin_airport'].apply(get_country)
data['arrctry'] = data['destination_airport'].apply(get_country)

# Map origin and destination airports to IATA codes
data['depapt'] = data['origin_airport'].apply(get_iata)
data['arrapt'] = data['destination_airport'].apply(get_iata)

data['distance'] = data['total_distance_km'] * 0.539957

data['days'] = 1
data['NFlts'] = 1

data['deptim'] = 545
data['arrtim'] = 645

data['efffrom'] = 20190101
data['effto'] = 20190102

data['inpacft'] = 310 
data['seats'] = 247

# Select relevant columns
selected_columns = data[['airline_code', 'flight_number_split', 'depapt', 'depctry', 'arrapt', 'arrctry', 'deptim', 'arrtim', 'days', 'distance', 'inpacft', 'seats', 'efffrom', 'effto', 'NFlts']].copy()

# Rename the columns to match the new format
selected_columns.rename(columns={'flight_number_split': 'fltno'}, inplace=True)
selected_columns.rename(columns={'airline_code': 'carrier'}, inplace=True)

# Convert all entries to strings and encapsulate them within double quotes
selected_columns = selected_columns.applymap(lambda x: f'"{str(x)}"')

# Add double quotes to column names
selected_columns.columns = [f'"{col}"' for col in selected_columns.columns]

# Write the new dataframe to a CSV file
output_file_path_updated = 'Output/ICL_Flights.csv'
selected_columns.to_csv(output_file_path_updated, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

output_file_path_updated
