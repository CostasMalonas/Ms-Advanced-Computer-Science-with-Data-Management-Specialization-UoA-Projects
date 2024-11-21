import requests
import json

# Define the URL. Replace <datatypeid> with a specific data type ID.
url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data?datasetid=GSOM?datatypeid=CNTRY"

# Define the header
headers = {
    "token": "JJuQpupmfdUwtTwMLvExRrjyxazHyjPY"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check the request was successful
if response.status_code == 200:
    # Print the data
    print(response.json())
else:
    print(f"Request failed with status code {response.status_code}")