"""The SomaConnect class."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import backoff

from .soma_shade import SomaShade

_LOGGER = logging.getLogger(__name__)


def clamp(num: int, min_value: int, max_value: int) -> int:
    """Clamp num to be between min_value and max_value."""
    return max(min(num, max_value), min_value)


class SomaConnect:
    """Represents a connection to SOMA Connect."""

    def __init__(self, host: str, port: int) -> None:
        """Initialise the connection."""
        self._host = host.removeprefix("http://")
        self._port = port
        self._url = f"http://{host}:{port}"
        self._shades: set[SomaShade] = set()

    @property
    def shades(self) -> list[SomaShade] | None:
        """Return a list of discovered shades."""
        if len(self._shades) > 0:
            return list(self._shades)
        return None

    @backoff.on_exception(
        backoff.expo, aiohttp.ClientError, max_tries=3, logger=_LOGGER
    )
    async def _get(self, endpoint: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Issue a request and return the JSON."""
        url = f"{self._url}/{endpoint}"
        params = kwargs if len(kwargs) > 0 else {}

        async with aiohttp.ClientSession(raise_for_status=False) as session:
            async with session.get(url, params=params) as response:
                json: dict[str, Any] = await response.json()
                result = json.get("result", {})

                if result == "error":
                    json.pop("version", None)
                    json.pop("mac", None)

                return json

    async def list_devices(self) -> list[SomaShade] | None:
        """Return list of devices."""
        result = await self._get("list_devices")
        if (shades := result.get("shades", None)) is not None and len(shades) > 0:
            for shade in shades:
                self._shades.add(SomaShade(self, **shade))

            return self.shades

        return None

    async def open_shade(self, mac: str) -> bool:
        """Open the shade."""
        if mac is not None:
            result = await self._get(f"open_shade/{mac}")
            if result.get("result", None) == "success":
                return True
        return False

    async def close_shade(self, mac: str) -> bool:
        """Close the shade."""
        if mac is not None:
            result = await self._get(f"close_shade/{mac}")
            if result.get("result", None) == "success":
                return True
        return False

    async def stop_shade(self, mac: str) -> bool:
        """Stop the shade."""
        if mac is not None:
            result = await self._get(f"stop_shade/{mac}")
            if result.get("result", None) == "success":
                return True
        return False

    async def get_shade_position(self, mac: str) -> int | bool:
        """Get shade state."""
        if mac is not None:
            result = await self._get(f"get_shade_state/{mac}")
            if result.get("result", None) == "success":
                return result.get("position", False)
        return False

    async def set_shade_position(
        self,
        mac: str,
        position: int,
        close_upwards: bool | None = False,
        morning_mode: bool | None = False,
    ) -> bool:
        """Set shade position."""
        kwargs = {}
        if mac is not None and isinstance(position, int):
            position = clamp(position, 0, 100)

            if close_upwards is True:
                kwargs["close_upwards"] = 1
            if morning_mode is True:
                kwargs["morning_mode"] = 1
            result = await self._get(
                f"set_shade_position/{mac}/{str(position)}", **kwargs
            )
            if result.get("result", None) == "success":
                return True
        return False

    async def get_battery_level(self, mac: str) -> tuple[int, int] | bool:
        """Get battery level."""
        if mac is not None:
            result = await self._get(f"get_battery_level/{mac}")
            if result.get("result", None) == "success":
                battery_level = result.get("battery_level", False)
                battery_percentage = result.get("battery_percentage", False)
                return (battery_level, battery_percentage)
        return False

    async def get_light_level(self, mac: str) -> int | bool:
        """Get light level."""
        if mac is not None:
            result = await self._get(f"get_light_level/{mac}")
            if result.get("result", None) == "success":
                light_level = result.get("light_level", False)
                return light_level
        return False
