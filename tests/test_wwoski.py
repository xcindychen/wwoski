from wwoski import SkiWeatherAPI
import os
import requests
from dotenv import load_dotenv

load_dotenv()
valid_api_key=os.getenv('API_KEY') # your valid API keys should be put in the .env file
invalid_api_key = "invalid_api_key"
valid_location = "Stowe"
invalid_location = "InvalidLocation"

def test_get_weather_data(api_key, location, num_of_days):
    """
    Test the `get_weather_data` method with different inputs.
    """
    api = SkiWeatherAPI(api_key)
    print(f"Testing get_weather_data with API key: {api_key} and location: {location}...")
    
    try:
        weather_data = api.get_weather_data(location, num_of_days)
        print("Weather data retrieved successfully!")
        print(weather_data) 
    except ValueError as e:
        print(f"Error occurred (API not valid): {e}")

def test_transform_to_dataframe(api_key, location, num_of_days):
    """
    Test the `transform_to_dataframe` method with valid weather data.
    """
    api = SkiWeatherAPI(api_key)
    
    print(f"Testing transform_to_dataframe for location: {location}...")
    
    try:
        weather_data = api.get_weather_data(location, num_of_days)
        weather_df = api.transform_to_dataframe(weather_data)
        print("DataFrame created successfully!")
        print(weather_df) 
    except ValueError as e:
        print(f"Error occurred (Invalid location): {e}")

def test_save_to_csv(api_key, location, num_of_days):
    """
    Test the `save_to_csv` method by saving to a file.
    """
    api = SkiWeatherAPI(api_key)
    
    print(f"Testing save_to_csv for location: {location}...")
    
    try:
        weather_data = api.get_weather_data(location, num_of_days)
        weather_df = api.transform_to_dataframe(weather_data)
        filename = "weather_forecast.csv"
        api.save_to_csv(weather_df, filename)
        
        if os.path.exists(filename):
            print(f"CSV file {filename} saved successfully!")
        else:
            print(f"Failed to save CSV file {filename}.")
    except Exception as e:
        print(f"Error occurred: {e}")

def test_plot_weather_data(api_key, location, num_of_days):
    """
    Test the `plot_weather_data` method by plotting the weather data.
    """
    api = SkiWeatherAPI(api_key)
    
    print(f"Testing plot_weather_data for location: {location}...")
    
    try:
        weather_data = api.get_weather_data(location, num_of_days)
        weather_df = api.transform_to_dataframe(weather_data)
        api.plot_weather_data(weather_df)
        print("Weather data plotted successfully!")
    except Exception as e:
        print(f"Error occurred (Invalid location): {e}")

def run_tests():
    """
    Run the tests with valid API key and location, invalid API key, and invalid location.
    """
    num_of_days = 7 
    
    # Test valid API key and location
    test_get_weather_data(valid_api_key, valid_location, num_of_days)
    test_transform_to_dataframe(valid_api_key, valid_location, num_of_days)
    test_save_to_csv(valid_api_key, valid_location, num_of_days)
    test_plot_weather_data(valid_api_key, valid_location, num_of_days)
    
    # Test invalid API key
    test_get_weather_data(invalid_api_key, valid_location, num_of_days)
    test_transform_to_dataframe(invalid_api_key, valid_location, num_of_days)
    test_save_to_csv(invalid_api_key, valid_location, num_of_days)
    test_plot_weather_data(invalid_api_key, valid_location, num_of_days)
    
    # Test valid API key and invalid location
    test_get_weather_data(valid_api_key, invalid_location, num_of_days)
    test_transform_to_dataframe(valid_api_key, invalid_location, num_of_days)
    test_save_to_csv(valid_api_key, invalid_location, num_of_days)
    test_plot_weather_data(valid_api_key, invalid_location, num_of_days)
    
    # Test invalid API key and invalid location
    test_get_weather_data(invalid_api_key, invalid_location, num_of_days)
    test_transform_to_dataframe(invalid_api_key, invalid_location, num_of_days)
    test_save_to_csv(invalid_api_key, invalid_location, num_of_days)
    test_plot_weather_data(invalid_api_key, invalid_location, num_of_days)

if __name__ == "__main__":
    run_tests()
