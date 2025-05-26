from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
import random

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Mock weather data
MOCK_WEATHER_DATA = {
    "Beijing": {
        "temperature": {"min": 15, "max": 25},
        "conditions": ["Sunny", "Cloudy", "Rainy"],
        "humidity": {"min": 30, "max": 70},
        "wind_speed": {"min": 5, "max": 15}
    },
    "Shanghai": {
        "temperature": {"min": 18, "max": 28},
        "conditions": ["Sunny", "Cloudy", "Rainy"],
        "humidity": {"min": 40, "max": 80},
        "wind_speed": {"min": 3, "max": 12}
    },
    "Guangzhou": {
        "temperature": {"min": 20, "max": 30},
        "conditions": ["Sunny", "Cloudy", "Rainy"],
        "humidity": {"min": 50, "max": 90},
        "wind_speed": {"min": 2, "max": 10}
    }
}

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@mcp.tool()
async def get_city_weather(city: str) -> str:
    """Get weather information for a specific city.

    Args:
        city: Name of the city (e.g. Beijing, Shanghai, Guangzhou)
    """
    if city not in MOCK_WEATHER_DATA:
        return f"Sorry, weather data for {city} is not available."

    weather_data = MOCK_WEATHER_DATA[city]
    current_time = datetime.now()
    
    # Generate random weather data based on the city's ranges
    temp = random.randint(weather_data["temperature"]["min"], weather_data["temperature"]["max"])
    condition = random.choice(weather_data["conditions"])
    humidity = random.randint(weather_data["humidity"]["min"], weather_data["humidity"]["max"])
    wind_speed = random.randint(weather_data["wind_speed"]["min"], weather_data["wind_speed"]["max"])
    
    # Generate 3-day forecast
    forecast = []
    for i in range(3):
        forecast_day = current_time + timedelta(days=i)
        forecast_temp = random.randint(weather_data["temperature"]["min"], weather_data["temperature"]["max"])
        forecast_condition = random.choice(weather_data["conditions"])
        forecast.append(f"{forecast_day.strftime('%Y-%m-%d')}: {forecast_temp}°C, {forecast_condition}")

    return f"""
Current Weather in {city}:
Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
Temperature: {temp}°C
Condition: {condition}
Humidity: {humidity}%
Wind Speed: {wind_speed} km/h

3-Day Forecast:
{chr(10).join(forecast)}
"""

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
