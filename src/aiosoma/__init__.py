"""Async SOMA Connect API with exponential backoff."""
from __future__ import annotations

import aiohttp
import backoff

__version__ = "0.0.0"


class AioSoma:
    def __init__(self, host: str, port: int) -> None:
        """Initialise the connection."""
        self._host = host.removeprefix("http://")
        self._port = port
        self._url = f"http://{host}:{port}"

    @backoff.on_exception(
        backoff.expo,
        [aiohttp.ClientError, aiohttp.ClientTimeout, aiohttp.ServerTimeoutError],
        max_time=5,
    )
    async def _get(self, endpoint: str) -> str:
        """Issue a request and return the JSON."""
        url = f"{self._url}/{endpoint}"
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(url) as response:
                return await response.json()

    async def list_devices(self) -> str:
        """Return list of devices."""
        return await self._get("list_devices")

    async def open_shade(self, mac: str) -> str:
        """Open the shade."""
        if mac is not None:
            return await self._get(f"open_shade/{mac}")

    async def close_shade(self, mac: str) -> str:
        """Close the shade."""
        if mac is not None:
            return await self._get(f"close_shade/{mac}")

    async def stop_shade(self, mac: str) -> str:
        """Stop the shade."""
        if mac is not None:
            return await self._get(f"stop_shade/{mac}")

    async def get_shade_state(self, mac: str) -> str:
        """Get shade state."""
        if mac is not None:
            return await self._get(f"get_shade_state/{mac}")

    async def set_shade_position(self, mac: str, position: int) -> str:
        """Set shade position."""
        if mac is not None and isinstance(position, int):
            if position < 0:
                position = 0
            if position > 100:
                position = 100
            return await self._get(f"set_shade_position/{mac}/{str(position)}")

    async def get_battery_level(self, mac: str) -> str:
        """Get battery level."""
        if mac is not None:
            return await self._get(f"get_battery_level/{mac}")
