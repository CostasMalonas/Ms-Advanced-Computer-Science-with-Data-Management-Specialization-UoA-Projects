import time
from datetime import datetime
from statistics import median

import requests
from dateutil.relativedelta import relativedelta
from tqdm import tqdm

# Define the header
headers = {
    "token": "MMbckUthGxPJhtXxxBQlxNrqnmTtvQTf"
}

# Define the base URL for API requests
base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/"

# Global variables for rate limiting
MAX_REQUESTS_PER_SECOND = 5
REQUESTS_INTERVAL = 1.0 / MAX_REQUESTS_PER_SECOND
last_request_time = None


# Function to make API requests and handle errors
def make_api_request(url):
    global last_request_time

    # Check if rate limit needs to be enforced
    if last_request_time is not None:
        elapsed_time = time.time() - last_request_time
        if elapsed_time < REQUESTS_INTERVAL:
            time.sleep(REQUESTS_INTERVAL - elapsed_time)

    response = requests.get(url, headers=headers)
    last_request_time = time.time()  # Update the last request time

    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results']  # Handle the case when response format contains 'results' key
        else:
            return data  # Return the response as-is
    else:
        print(f"Request to {url} failed with status code {response.status_code}")
        print("Error details:", response.text)
        return None


# Function to get the list of countries
def get_countries():
    countries_url = f"{base_url}locations?datasetid=GSOM&locationcategoryid=CNTRY&limit=1000"
    return make_api_request(countries_url)


# Function to get temperature data for a country
def get_temperature_data(country_id, start_date, end_date):
    data_url = f"{base_url}data?datasetid=GSOM&datatypeid=TMAX,TMIN&units=metric&locationid={country_id}&startdate={start_date:%Y-%m-%d}&enddate={end_date:%Y-%m-%d}&limit=1000"
    return make_api_request(data_url)


# Main function
def main():
    print("Fetching countries...")
    countries = get_countries()
    if not countries:
        exit()
    print("Countries fetched.")

    yearly_temperatures = {}  # Structure to store median yearly temperature per country per year

    # Calculate median yearly temperature for each country
    num_countries = len(countries)
    with tqdm(total=num_countries, ncols=80, desc="Processing Countries") as pbar:
        for country in countries:
            country_id = country['id']
            start_date = datetime.strptime(country['mindate'], '%Y-%m-%d')
            end_date = datetime.strptime(country['maxdate'], '%Y-%m-%d')

            yearly_temps = {}
            while start_date.year <= end_date.year:
                next_year_start_date = datetime(start_date.year + 1, start_date.month,
                                                start_date.day) if start_date.year < end_date.year else end_date

                temperature_data = get_temperature_data(country_id, start_date,
                                                        next_year_start_date - relativedelta(days=1))
                if not temperature_data:
                    break

                for data in temperature_data:
                    date = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S')
                    year = date.year
                    if year in yearly_temps:
                        yearly_temps[year].append(data['value'])
                    else:
                        yearly_temps[year] = [data['value']]

                start_date = next_year_start_date

            median_temps = {year: median(temps) for year, temps in yearly_temps.items()}
            yearly_temperatures[country['name']] = median_temps

            pbar.update(1)

    # Print yearly temperatures for each country
    for country, temperatures in yearly_temperatures.items():
        print(f"Yearly Temperatures of {country}:")
        for year, temp in temperatures.items():
            print(f"Year: {year}, Temperature: {temp}")


# Execute the main function when the script is run
if __name__ == '__main__':
    main()
