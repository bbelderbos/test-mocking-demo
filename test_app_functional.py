import os
import sqlite3

import pytest

from app import WeatherApp


@pytest.fixture
def db():
    db = "test.db"
    yield db
    os.remove(db)


def test_weather_app_end_to_end(db, capfd):
    app = WeatherApp(db)
    app("london")
    out, _ = capfd.readouterr()
    assert out == "Saved weather data for london\n"
    conn = sqlite3.connect(app.db_name)
    c = conn.cursor()
    ret = c.execute("SELECT * FROM weather")
    rows = ret.fetchall()
    assert len(rows) == 1
    row1 = rows[0]
    assert len(row1) == 5
    assert row1[0] == "london"
    assert isinstance(row1[1], str)
    assert isinstance(row1[2], float)
    assert isinstance(row1[3], float)
    assert isinstance(row1[4], int)
