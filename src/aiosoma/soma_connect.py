"""The SomaConnect class."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import backoff

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
        self._version: str = ""
        self._devices: set[tuple[str, str, str, str]] = set()

    @property
    def devices(self) -> list[tuple[str, str, str, str]] | None:
        """Return a list of discovered shades."""
        if len(self._devices) > 0:
            return [device for device in self._devices]
        return None

    @property
    def version(self) -> str:
        """Return the SOMA Connect version."""
        return self._version

    @backoff.on_exception(
        backoff.expo, aiohttp.ClientError, max_tries=3, logger=_LOGGER
    )
    async def _get(self, endpoint: str, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Issue a request and return the JSON."""
        url = f"{self._url}/{endpoint}"
        params = kwargs if len(kwargs) > 0 else {}

        async with aiohttp.ClientSession(raise_for_status=False) as session:
            async with session.get(url, params=params) as response:
                json: dict[str, str] = await response.json()
                result: str = json.get("result", "")

                if result == "error":
                    json.pop("version", None)
                    json.pop("mac", None)

                if (version := json.get("version", None)) is not None:
                    self._version = version

                return json

    async def list_devices(self) -> list[tuple[str, str, str, str]] | None:
        """Return list of devices."""
        result = await self._get("list_devices")
        if (devices := result.get("shades", None)) is not None and len(devices) > 0:
            for device in devices:
                self._devices.add(
                    (device["name"], device["mac"], device["type"], device["gen"])
                )

            return self.devices

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

    async def get_light_level(self, mac: str) -> int | None:
        """Get light level."""
        if mac is not None:
            result = await self._get(f"get_light_level/{mac}")
            if result.get("result", None) == "success":
                light_level = result.get("light_level", False)
                return light_level
        return None
