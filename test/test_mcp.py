"""Test for Weather MCP Server.

Start MCP before running test using:
    fastmcp run src/core/weather_mcp.py --transport sse
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


SERVER_URL = "http://localhost:8000/sse"


async def test_get_weather_forecast():
    """Test the get_weather_forecast method with Hamburg."""
    async with sse_client(SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")
            
            # Call get_weather_forecast with Hamburg
            result = await session.call_tool(
                "get_weather_forecast",
                arguments={"city_name": "Hamburg"}
            )
            
            print(f"\nWeather forecast for Hamburg:")
            print(result.content)
            
            return result


if __name__ == "__main__":
    asyncio.run(test_get_weather_forecast())
