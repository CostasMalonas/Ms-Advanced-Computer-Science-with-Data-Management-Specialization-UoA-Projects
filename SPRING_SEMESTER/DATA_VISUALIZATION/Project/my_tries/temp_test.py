import requests

TOKEN = "JJuQpupmfdUwtTwMLvExRrjyxazHyjPY"

def get_available_countries():
    url = f"https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?datasetid=GSOM&locationcategoryid=CNTRY&limit=1000"
    headers = {"token": TOKEN}
    params = {
        "locationcategoryid": "CNTY",  # Country location category
        "limit": 1000,  # Maximum number of records per request
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

# Example usage
countries_data = get_available_countries()
countries = [country["name"] for country in countries_data["results"]]
for country in countries:
    print(country)
