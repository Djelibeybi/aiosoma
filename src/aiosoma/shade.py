"""The Shade class."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .connect import Connect


@dataclass
class Shade:
    """Represents a SOMA shade."""

    def __init__(
        self,
        soma: Connect,
        mac: str,
        name: str,
        type: str,  # pylint: disable=W0622
        gen: str,
        light_level: int | None = None,
        position: int | None = None,
        battery_level: int | None = None,
        battery_percentage: int | None = None,
    ) -> None:
        """Initialise the Shade."""
        self._soma = soma
        self._mac = mac
        self._name = name
        self._type = type.capitalize()
        self._gen = gen
        self._light_level: int | None = light_level
        self._position: int | None = position
        self._battery_level: int | None = battery_level
        self._battery_percentage: int | None = battery_percentage

    def __str__(self) -> str:
        """Return a string representation of the shade."""
        return f"{self._name}: {self._type.capitalize()} {self._gen} ({self._mac})"

    def __repr__(self) -> str:
        """Return representation of the shade."""
        return f"<{self._name} {self._type} {self._gen} ({self._mac})>"

    @property
    def name(self) -> str:
        """Return the name of the shade."""
        return self._name

    @property
    def mac(self) -> str:
        """Return the mac address of the shade."""
        return self._mac

    @property
    def model(self) -> str:
        """Return the model of the shade."""
        return self._type

    @property
    def gen(self) -> str:
        """Return the generation of the shade."""
        return self._gen

    @property
    def light_level(self) -> int | None:
        """Return the current light level."""
        return self._light_level

    @property
    def position(self) -> int | None:
        """Return the current position."""
        return self._position

    @property
    def battery_level(self) -> int | None:
        """Return the current battery level."""
        return self._battery_level

    @property
    def battery_percentage(self) -> int | None:
        """Return the current battery level."""
        return self._battery_percentage

    async def open(self) -> dict[str, Any] | None:
        """Open this shade."""
        return await self._soma.open_shade(self._mac)

    async def close(self) -> dict[str, Any] | None:
        """Close shade."""
        return await self._soma.close_shade(self._mac)

    async def stop(self) -> dict[str, Any] | None:
        """Stop shade."""
        return await (self._soma.stop_shade(self._mac))

    async def set_position(
        self, position: int, close_upwards: bool = False, morning_mode: bool = False
    ) -> dict[str, Any] | None:
        """Set shade to specific position."""
        return await self._soma.set_shade_position(
            self._mac,
            position,
            close_upwards=close_upwards,
            morning_mode=morning_mode,
        )

    async def get_state(self) -> dict[str, Any] | None:
        """Get shade state."""
        response = await self._soma.get_shade_state(self._mac)
        return response

    async def get_battery_level(self) -> dict[str, int] | None:
        """Get battery level."""
        return await self._soma.get_battery_level(self._mac)

    async def get_light_level(self) -> dict[str, Any] | None:
        """Get light level."""
        return await self._soma.get_light_level(self._mac)
