# wwoski

World weather online ski and mountain weather data API wrapper

## Installation

```bash
$ pip install wwoski
```

## Usage

Example Usage:
- Get the ski weather data in json formmat (It contains all the weather data the website provides.)
api = SkiWeatherAPI("your_api_key")
weather_json = api.get_weather_data("stowe", 7)
- Transform selected ski weather data (in json format) to panda dataframe 
weather_df = api.transform_to_dataframe(weather_json)
- Save to csv
api.save_to_csv(weather_df, "weather_forecast.csv")
- Visualization: the min/max temperature(C) and snow depth in the input location.
api.plot_weather_data(weather_df)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`wwoski` was created by HsiYu Chen. It is licensed under the terms of the MIT license.

## Credits

`wwoski` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
