"""
Test file for the API call
"""

import requests

URL = "https://weather.lewagon.com/geo/1.0/direct?q=Barcelona"
response = requests.get(URL).json()
city = response[0]
print(f"{city['name']}: ({city['lat']}, {city['lon']})")
