"""Async SOMA Connect API with exponential backoff."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

import aiohttp
import backoff
from rich import print

__version__ = "0.1.0"

_LOGGER = logging.getLogger(__name__)


@dataclass
class SomaConnect:
    host: str
    port: int
    api: AioSoma = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Instantiate the API."""
        self.api = AioSoma(self.host, self.port)

    @property
    def soma_connect(self) -> SomaConnect:
        """Return itself."""
        return self


@dataclass
class Shade:
    """Represents a SOMA shade."""

    api: AioSoma
    mac: str
    name: str = field(default="", init=False)
    type: str = field(default="", init=False)
    gen: str = field(default="", init=False)

    def __str__(self) -> str:
        """Return a string representation of the shade."""
        return f"{self.name}: {self.type.capitalize()} {self.gen} ({self.mac})"

    async def open(self) -> bool:
        """Open this shade."""
        return bool(await self.api.open_shade(self.mac))

    async def close(self) -> bool:
        """Close shade."""
        return bool(await self.api.close_shade(self.mac))

    async def stop(self) -> bool:
        """Stop shade."""
        return bool(await (self.api.stop_shade(self.mac)))

    async def set_position(
        self, position: int, close_upwards: bool = False, morning_mode: bool = False
    ) -> bool:
        """Set shade to specific position."""
        return bool(
            await self.api.set_shade_position(
                self.mac,
                position,
                close_upwards=close_upwards,
                morning_mode=morning_mode,
            )
        )

    async def state(self) -> dict[str, Any] | bool:
        """Get shade state."""
        return await self.api.get_shade_state(self.mac)

    async def battery_level(self) -> int:
        """Get battery level."""
        response = await self.api.get_battery_level(self.mac)
        print(response)
        return 0

    async def light_level(self) -> int:
        """Get light level."""
        response = await self.api.get_light_level(self.mac)
        print(response)
        return 0


def backoff_hdlr(details: dict[str, Any]) -> None:
    """Log when we back off."""
    _LOGGER.debug(f"Backing off: {details}")


def success_hdlr(details: dict[str, Any]) -> None:
    """Log success."""
    response = details.get("value", None)
    if response is not None:
        _LOGGER.info(f"Success: {response}")


def giveup_hdlr(details: dict[str, Any]) -> None:
    _LOGGER.error(f"Failed: {details}")


class AioSoma:
    def __init__(self, host: str, port: int) -> None:
        """Initialise the connection."""
        self._host = host.removeprefix("http://")
        self._port = port
        self._url = f"http://{host}:{port}"

    @backoff.on_predicate(
        backoff.expo,
        max_tries=3,
        on_backoff=backoff_hdlr,
        on_giveup=giveup_hdlr,
        on_success=success_hdlr,
    )
    async def _get(
        self, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any] | bool:
        """Issue a request and return the JSON."""
        url = f"{self._url}/{endpoint}"
        _LOGGER.debug("Target URL: %s", url)
        params = {}
        if len(kwargs) > 0:
            params = {key: value for key, value in kwargs.items()}

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(url, params=params) as response:
                json: dict[str, Any] = await response.json()
                result = json.get("result", None)

                if result == "success":
                    return json

                return False

    async def list_devices(self) -> dict[str, Any] | bool:
        """Return list of devices."""
        return await self._get("list_devices")

    async def open_shade(self, mac: str) -> dict[str, Any] | bool:
        """Open the shade."""
        if mac is not None:
            return await self._get(f"open_shade/{mac}")

    async def close_shade(self, mac: str) -> dict[str, Any] | bool:
        """Close the shade."""
        if mac is not None:
            return await self._get(f"close_shade/{mac}")

    async def stop_shade(self, mac: str) -> dict[str, Any] | bool:
        """Stop the shade."""
        if mac is not None:
            return await self._get(f"stop_shade/{mac}")

    async def get_shade_state(self, mac: str) -> dict[str, Any] | bool:
        """Get shade state."""
        if mac is not None:
            return await self._get(f"get_shade_state/{mac}")

    async def set_shade_position(
        self,
        mac: str,
        position: int,
        close_upwards: bool | None = False,
        morning_mode: bool | None = False,
    ) -> dict[str, Any] | bool:
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

    async def get_battery_level(self, mac: str) -> dict[str, Any] | bool:
        """Get battery level."""
        if mac is not None:
            return await self._get(f"get_battery_level/{mac}")

    async def get_light_level(self, mac: str) -> dict[str, Any] | bool:
        """Get battery level."""
        if mac is not None:
            return await self._get(f"get_light_level/{mac}")
