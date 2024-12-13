import os
import pytest
from unittest.mock import patch
from wwoski import SkiWeatherAPI
from dotenv import load_dotenv

load_dotenv()

# Constants
VALID_API_KEY = os.getenv("API_KEY")  # Valid API key from .env file
INVALID_API_KEY = "invalid_api_key"
VALID_LOCATION = "Stowe"
INVALID_LOCATION = "InvalidLocation"
NUM_OF_DAYS = 7

# Sample mock response with the correct structure
MOCK_WEATHER_DATA = {
    "data": {
        "weather": [
            {
                "date": "2024-12-13",
                "maxtempC": "2",
                "mintempC": "-5",
                "hourly": [
                    {"time": "0", "tempC": "-2", "windspeedKmph": "15", "humidity": "80"},
                ],
            }
        ]
    }
}

@pytest.mark.parametrize(
    "api_key,location,expected_success",
    [
        (VALID_API_KEY, VALID_LOCATION, True),
        (INVALID_API_KEY, VALID_LOCATION, False),
        (VALID_API_KEY, INVALID_LOCATION, False),
        (INVALID_API_KEY, INVALID_LOCATION, False),
    ],
)
@patch("wwoski.SkiWeatherAPI.get_weather_data")
def test_get_weather_data(mock_get_weather_data, api_key, location, expected_success):
    """
    Test the `get_weather_data` method with different inputs.
    """
    if expected_success:
        mock_get_weather_data.return_value = MOCK_WEATHER_DATA
    else:
        mock_get_weather_data.side_effect = ValueError("Invalid API key or location")

    api = SkiWeatherAPI(api_key)

    if expected_success:
        weather_data = api.get_weather_data(location, NUM_OF_DAYS)
        assert weather_data == MOCK_WEATHER_DATA
    else:
        with pytest.raises(ValueError):
            api.get_weather_data(location, NUM_OF_DAYS)


@pytest.mark.parametrize(
    "api_key,location",
    [(VALID_API_KEY, VALID_LOCATION)],
)
@patch("wwoski.SkiWeatherAPI.get_weather_data")
def test_transform_to_dataframe(mock_get_weather_data, api_key, location):
    """
    Test the `transform_to_dataframe` method with valid weather data.
    """
    mock_get_weather_data.return_value = MOCK_WEATHER_DATA

    api = SkiWeatherAPI(api_key)
    weather_data = api.get_weather_data(location, NUM_OF_DAYS)
    weather_df = api.transform_to_dataframe(weather_data)

    assert not weather_df.empty
    assert "date" in weather_df.columns


@pytest.mark.parametrize(
    "api_key,location",
    [(VALID_API_KEY, VALID_LOCATION)],
)
@patch("wwoski.SkiWeatherAPI.get_weather_data")
def test_save_to_csv(mock_get_weather_data, api_key, location, tmp_path):
    """
    Test the `save_to_csv` method by saving to a file.
    """
    mock_get_weather_data.return_value = MOCK_WEATHER_DATA

    api = SkiWeatherAPI(api_key)
    weather_data = api.get_weather_data(location, NUM_OF_DAYS)
    weather_df = api.transform_to_dataframe(weather_data)

    csv_file = tmp_path / "weather_forecast.csv"
    api.save_to_csv(weather_df, str(csv_file))

    assert csv_file.exists()


@pytest.mark.parametrize(
    "api_key,location",
    [(VALID_API_KEY, VALID_LOCATION)],
)
@patch("wwoski.SkiWeatherAPI.get_weather_data")
def test_plot_weather_data(mock_get_weather_data, api_key, location):
    """
    Test the `plot_weather_data` method by plotting the weather data.
    """
    mock_get_weather_data.return_value = MOCK_WEATHER_DATA

    api = SkiWeatherAPI(api_key)
    weather_data = api.get_weather_data(location, NUM_OF_DAYS)
    weather_df = api.transform_to_dataframe(weather_data)

    # Ensure the method runs without error (visual inspection is manual)
    api.plot_weather_data(weather_df)


if __name__ == "__main__":
    pytest.main()

