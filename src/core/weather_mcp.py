"""Weather MCP Server using FastMCP."""

from typing import Any
import httpx
from fastmcp import FastMCP
from geopy.geocoders import Nominatim # type: ignore

from common.protocols import GeoLocation

# Create the MCP server
mcp = FastMCP("Weather Service")


@mcp.tool()
async def get_weather_forecast(city_name: str) -> dict[Any, Any]:
    """
    Get weather forecast for a city.
    
    Args:
        city_name: The name of the city to get weather forecast for.
        
    Returns:
        A dictionary containing the weather forecast data including
        temperature, humidity, and other meteorological information.
    """
    # Initialize geocoder
    geolocator = Nominatim(user_agent="weather_mcp_service")
    
    # Get coordinates for the city
    location: GeoLocation | None = geolocator.geocode(city_name)
    if not location:
        return {"error": f"Could not find location for city: {city_name}"}
    
    latitude = location.latitude
    longitude = location.longitude
    
    # Fetch weather data from Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "weather_code"],
        "timezone": "auto",
        "forecast_days": 7
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch weather data: {response.status_code}"}
        
        weather_data = response.json()
    
    return {
        "city": city_name,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude
        },
        "current": weather_data.get("current", {}),
        "daily": weather_data.get("daily", {}),
        "units": {
            "current_units": weather_data.get("current_units", {}),
            "daily_units": weather_data.get("daily_units", {})
        }
    }


if __name__ == "__main__":
    mcp.run()
