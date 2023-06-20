from unittest.mock import MagicMock, patch

import pytest

from app import WeatherApp, OW_API_KEY, DEFAULT_CITY


@patch("app.requests.get")
def test_weather_data(mock_get):
    # Mock the API response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "weather": [{"description": "Rain"}],
        "main": {"temp": 22.05, "humidity": 71},
    }
    mock_get.return_value = mock_response

    app = WeatherApp()
    weather_data = app.get_weather_data("London")

    # Assert that API was called with the correct URL
    mock_get.assert_called_with(
        f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={OW_API_KEY}"
    )

    # Assert that the correct weather data was returned
    assert weather_data == {
        "weather": [{"description": "Rain"}],
        "main": {"temp": 22.05, "humidity": 71},
    }


@patch("app.sqlite3.connect")
def test_save_weather(mock_db):
    # Mock the database connection
    mock_conn = MagicMock()
    mock_db.return_value = mock_conn

    app = WeatherApp()
    app.save_weather(
        {"weather": [{"description": "Rain"}], "main": {"temp": 22.05, "humidity": 71}},
        "London",
    )

    # Assert that database connection was opened and commit was called
    mock_db.assert_called_with("weather_app.db")
    mock_conn.commit.assert_called_once()


@patch("builtins.input", return_value="Berlin")
def test_get_city(mock_input):
    app = WeatherApp()
    city = app.get_city()

    # Assert that the input() was called
    mock_input.assert_called_once_with("Enter your city: ")

    # Assert that the correct city was returned
    assert city == "Berlin"


@patch("builtins.input", return_value="")
def test_get_city_empty_input(mock_input):
    app = WeatherApp()
    city = app.get_city()

    # Assert that the input() was called
    mock_input.assert_called_once_with("Enter your city: ")

    # Assert that the correct city was returned
    assert city == DEFAULT_CITY
