import os
import sqlite3

import pytest

from app import WeatherApp


@pytest.fixture
def db():
    db = "test.db"
    yield db
    # teardown
    os.remove(db)


def test_app(capfd, db):
    app = WeatherApp(db)
    app("London")
    out, err = capfd.readouterr()
    assert out == "Saved weather data for London\n"
    assert err == ""

    conn = sqlite3.connect(db)
    c = conn.cursor()
    ret = c.execute("select * from weather")
    rows = ret.fetchall()
    assert len(rows) == 1

    row1 = rows[0]
    assert len(row1) == 5
    assert row1[0] == "London"
    assert isinstance(row1[1], str)
    assert isinstance(row1[2], float)
    assert isinstance(row1[3], float)
    assert isinstance(row1[4], int)
