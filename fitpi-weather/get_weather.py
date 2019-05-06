import configparser
import requests

def get_weather_url():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['WEATHER_URL']

def get_forecast_url():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['FORECAST_URL']
 
def get_weather():
    return requests.get(get_weather_url()).json()

def get_forecast():
    return requests.get(get_forecast_url()).json()
 
def main():
    weather = get_weather()
 
    print(weather['main']['temp'])
    print(weather)
 
if __name__ == '__main__':
    main()