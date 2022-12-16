"""The SomaAPI class."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import backoff

_LOGGER = logging.getLogger(__name__)


class Connect:
    """Represents a connection to SOMA Connect."""

    def __init__(self, host: str, port: int) -> None:
        """Initialise the connection."""
        self._host = host.removeprefix("http://")
        self._port = port
        self._url = f"http://{host}:{port}"

    @backoff.on_exception(
        backoff.expo, aiohttp.ClientError, max_tries=3, logger=_LOGGER
    )
    async def _get(
        self, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Issue a request and return the JSON."""
        url = f"{self._url}/{endpoint}"
        params = {}
        if len(kwargs) > 0:
            params = {k: v for k, v in kwargs.items()}

        async with aiohttp.ClientSession(raise_for_status=False) as session:
            async with session.get(url, params=params) as response:
                json: dict[str, Any] = await response.json()
                result = json.get("result", None)

                if result == "error":
                    json.pop("version", None)
                    json.pop("mac", None)

                return json

    async def list_devices(self) -> dict[str, Any] | None:
        """Return list of devices."""
        return await self._get("list_devices")

    async def open_shade(
        self, mac: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Open the shade."""
        if mac is not None:
            return await self._get(f"open_shade/{mac}", **kwargs)

    async def close_shade(self, mac: str) -> dict[str, Any] | None:
        """Close the shade."""
        if mac is not None:
            return await self._get(f"close_shade/{mac}")

    async def stop_shade(self, mac: str) -> dict[str, Any] | None:
        """Stop the shade."""
        if mac is not None:
            return await self._get(f"stop_shade/{mac}")

    async def get_shade_state(self, mac: str) -> dict[str, Any] | None:
        """Get shade state."""
        if mac is not None:
            return await self._get(f"get_shade_state/{mac}")

    async def set_shade_position(
        self,
        mac: str,
        position: int,
        close_upwards: bool | None = False,
        morning_mode: bool | None = False,
    ) -> dict[str, Any] | None:
        """Set shade position."""
        kwargs = {}
        if mac is not None and isinstance(position, int):
            if position < 0:
                position = 0
            if position > 100:
                position = 100
            if close_upwards is True:
                kwargs["close_upwards"] = 1
            if morning_mode is True:
                kwargs["morning_mode"] = 1
            return await self._get(
                f"set_shade_position/{mac}/{str(position)}", **kwargs
            )

    async def get_battery_level(self, mac: str) -> dict[str, Any] | None:
        """Get battery level."""
        if mac is not None:
            return await self._get(f"get_battery_level/{mac}")

    async def get_light_level(self, mac: str) -> dict[str, Any] | None:
        """Get battery level."""
        if mac is not None:
            return await self._get(f"get_light_level/{mac}")
