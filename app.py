import sqlite3
import time

from decouple import config
import requests

OW_API_KEY = config("OW_API_KEY")
DEFAULT_CITY = "Alicante"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"


class WeatherApp:
    def __init__(self, db_name="weather_app.db"):
        self.db_name = db_name

    def get_city(self):
        city = input("Enter your city: ")
        if not city:
            city = DEFAULT_CITY
        return city

    def get_weather_data(self, city):
        url = BASE_URL.format(city, OW_API_KEY)
        response = requests.get(url)
        return response.json()

    def save_weather(self, weather_data, city):
        description = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        timestamp = int(time.time())  # Unix timestamp

        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS weather
                     (city text, description text, temperature real, humidity real, timestamp integer)"""
        )
        c.execute(
            "INSERT INTO weather VALUES (?, ?, ?, ?, ?)",
            (city, description, temperature, humidity, timestamp),
        )
        conn.commit()
        conn.close()
        print(f"Saved weather data for {city}")

    def __call__(self, city=None):
        if city is None:
            city = self.get_city()
        weather_data = self.get_weather_data(city)
        self.save_weather(weather_data, city)


if __name__ == "__main__":  # pragma: no cover
    app = WeatherApp()
    app()
