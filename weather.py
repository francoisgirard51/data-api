"""
Weather CLI
"""

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"

def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    endpoint = "/geo/1.0/direct"
    params = {"q": query, "limit": 5}  # Demande 5 options au maximum
    url = urllib.parse.urljoin(BASE_URI, endpoint)
    response = requests.get(url, params=params)

    if response.status_code == 200:
        city_data = response.json()
        if city_data:
            if len(city_data) > 1:
                print("Multiple matches found. Please choose a city by index:")
                for i, city in enumerate(city_data):
                    print(f"{i + 1}. {city['name']}, {city['country']}")

                choice = input("Enter the index of the city you want: ")
                try:
                    choice = int(choice)
                    if 1 <= choice <= len(city_data):
                        return city_data[choice - 1]
                    print("Invalid choice. Please select a valid index.")
                except ValueError:
                    print("Invalid input. Please enter the index as a number.")
            return city_data[0]
    return None

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    endpoint = "/data/2.5/forecast"
    params = {"lat": lat, "lon": lon}
    url = urllib.parse.urljoin(BASE_URI, endpoint)
    response = requests.get(url, params=params)

    if response.status_code == 200:
        forecast_data = response.json()
        # Extract the list of weather forecasts
        forecast_list = forecast_data.get("list", [])
        return forecast_list
    return None

def main():
    '''Ask the user for a city and display the weather forecast'''
    city_query = input("Enter a city name: ")

    # Call the search_city function to get the city information
    city = search_city(city_query)

    if city is not None:
        # Extract latitude and longitude from the city data
        lat = city['lat']
        lon = city['lon']

        # Call the weather_forecast function to get the weather forecast
        weather_data = weather_forecast(lat, lon)

        # Display the weather forecast data to the user
        print(weather_data)
    else:
        print("City not found. Please try again.")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
