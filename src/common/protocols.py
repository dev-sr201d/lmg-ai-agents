"""Protocol definitions for type hints."""

from typing import Any, Protocol


class GeoLocation(Protocol):
    """Protocol for geopy geocode result location objects."""
    
    @property
    def latitude(self) -> float:
        """The latitude of the location."""
        ...
    
    @property
    def longitude(self) -> float:
        """The longitude of the location."""
        ...
    
    @property
    def address(self) -> str:
        """The full address of the location."""
        ...
    
    @property
    def altitude(self) -> float | None:
        """The altitude of the location, if available."""
        ...
    
    @property
    def raw(self) -> dict[str, Any]:
        """The raw response data from the geocoding service."""
        ...
