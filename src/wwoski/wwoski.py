import requests
import pandas as pd
import matplotlib.pyplot as plt

class SkiWeatherAPI:
    def __init__(self, api_key):
        """
        Initialize the SkiWeatherAPI with an API key.

        Parameters:
        api_key (str): Your World Weather Online API key.
        """
        self.api_key = api_key
        self.base_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"

    def get_weather_data(self, location_name, num_of_days):
        """
        Retrieve weather data for a given location and number of days.

        Parameters:
        location_name (str): Location name (city, zip code, etc.)
        num_of_days (int): Number of days for the forecast (up to the API's limit).

        Returns:
        dict: JSON response containing weather data.
        raises error for invalid API key or location.
        """
        params = {
            "key": self.api_key,
            "q": location_name,
            "num_of_days": num_of_days,
            "format": "json",
            "tp": 24
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Will raise HTTPError for bad responses (4xx, 5xx)
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise ValueError(f"Other error occurred: {err}")

        weather_data = response.json()

        if "error" in weather_data["data"]:
            error_message = weather_data["data"]["error"][0]["msg"]
            raise ValueError(f"Error from API: {error_message}")
        
        return weather_data

    def transform_to_dataframe(self, weather_data):
        """
        Transform the JSON weather data into a pandas DataFrame.

        Parameters:
        weather_data (dict): JSON weather data from the API.

        Returns:
        pd.DataFrame: DataFrame containing selected weather information.
        raises error for invalid location data.
        """
        if "error" in weather_data:
            raise ValueError(f"Error in weather data: {weather_data['error']}")

        weather_list = weather_data['data']['weather']
        records = []
        for day in weather_list:
            hourly_data = day.get('hourly', [])
            snow_chances = []
            visibilities = []
            
            for hour in hourly_data:
                chance_of_snow = hour.get('chanceofsnow')
                visibility = hour.get('visibility')
                
                if chance_of_snow is not None:
                    try:
                        snow_chances.append(float(chance_of_snow))
                    except ValueError:
                        pass
                
                if visibility is not None:
                    try:
                        visibilities.append(float(visibility))
                    except ValueError:
                        pass

            avg_chance_of_snow = sum(snow_chances) / len(snow_chances) if snow_chances else None
            avg_visibility = sum(visibilities) / len(visibilities) if visibilities else None

            records.append({
                "date": day["date"],
                "max_temp_C": float(day["maxtempC"]),
                "min_temp_C": float(day["mintempC"]),
                "total_snow_cm": float(day["totalSnow_cm"]),
                "chance_of_snow": avg_chance_of_snow,
                "avg_visibility_km": avg_visibility 
            })
        
        return pd.DataFrame(records)

    def save_to_csv(self, dataframe, filename):
        """
        Save the DataFrame to a CSV file.

        Parameters:
        dataframe (pd.DataFrame): DataFrame to save.
        filename (str): Name of the CSV file.
        """
        dataframe.to_csv(filename, index=False)

    def plot_weather_data(self, dataframe):
        """
        Create a line + bar chart for the weather data (max, min temperature, and snow depth) with separate y-axes for temperature + precipitation, and date on the x-axis.
    
        Parameters:
        dataframe (pd.DataFrame): DataFrame containing weather data.
        """
        fig, ax1 = plt.subplots(figsize=(10, 6))
    
        # plot max and min temperatures on the left y-axis
        ax1.plot(dataframe['date'], dataframe['max_temp_C'], label='Max Temp (C)', marker='o', color='firebrick')
        ax1.plot(dataframe['date'], dataframe['min_temp_C'], label='Min Temp (C)', marker='o', color='navy')
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Temperature (C)", color='black')
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.legend(loc="upper left")
    
        # precipitation on right axis
        ax2 = ax1.twinx()
        ax2.bar(dataframe['date'], dataframe['total_snow_cm'], label='Snow Depth (cm)', alpha=0.5, color='skyblue')
        ax2.set_ylabel("Snow Depth (cm)", color='black')
        ax2.tick_params(axis='y', labelcolor='black')
        ax2.legend(loc="upper right")
    
        plt.title("Weather Forecast")
        fig.tight_layout()
        plt.show()