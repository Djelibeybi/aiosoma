"""The Shade class."""
from __future__ import annotations

import datetime

from .soma_connect import SomaConnect


class SomaShade:
    """Represents a SOMA shade."""

    def __init__(
        self,
        soma: SomaConnect,
        mac: str,
        name: str,
        type: str,  # pylint: disable=redefined-builtin
        gen: str,
    ) -> None:
        """Initialise the Shade."""
        self._soma = soma
        self._mac = mac
        self._name = name
        self._type: str | None = type.capitalize() if type else None
        self._gen: str | None = gen or None
        self._position: int | None = None
        self._battery_level: int | None = None
        self._battery_percentage: int | None = None
        self._light_level: int | None = None
        self._light_level_last_updated: datetime.datetime | None = None

    def __str__(self) -> str:
        """Return a string representation of the shade."""
        return f"{self.name}: {self.model[0]} {self.model[1]} ({self.mac})"

    def __repr__(self) -> str:
        """Return representation of the shade."""
        return f"<{self.name} {self.model[0]} {self.model[1]} ({self.mac})>"

    def __hash__(self) -> int:
        """Return an integer hash for the mac address of the shade."""
        return hash(self._mac)

    @property
    def name(self) -> str:
        """Return the name of the shade."""
        return self._name

    @property
    def mac(self) -> str:
        """Return the mac address of the shade."""
        return self._mac

    @property
    def model(self) -> tuple[str | None, str | None]:
        """Return the model (type, gen) of the shade."""
        return (self._type, self._gen)

    @property
    def position(self) -> int | None:
        """Return the current position."""
        if self._position is not None:
            return int(self._position)
        return None

    @property
    def battery_level(self) -> int | None:
        """Return the current battery level."""
        if self._battery_level is not None:
            return int(self._battery_level)
        return None

    @property
    def battery_percentage(self) -> int | None:
        """Return the current battery level."""
        if self._battery_percentage is not None:
            return int(self._battery_percentage)
        return None

    @property
    def light_level(self) -> int | None:
        """Return the current light level."""
        if self._light_level is not None:
            return int(self._light_level)
        return None

    async def open(self) -> bool:
        """Open this shade."""
        return await self._soma.open_shade(self._mac)

    async def close(self) -> bool:
        """Close shade."""
        return await self._soma.close_shade(self._mac)

    async def stop(self) -> bool:
        """Stop shade."""
        return await self._soma.stop_shade(self._mac)

    async def set_position(
        self, position: int, close_upwards: bool = False, morning_mode: bool = False
    ) -> bool:
        """Set shade to specific position."""
        result = await self._soma.set_shade_position(
            self._mac,
            position,
            close_upwards=close_upwards,
            morning_mode=morning_mode,
        )
        if result is True:
            self._position = position

        return result

    async def get_current_position(self) -> int | None:
        """Update and return shade position."""
        response = await self._soma.get_shade_position(self._mac)
        if response is not False:
            self._position = response
            return self.position
        return None

    async def get_current_battery_level(self) -> int | None:
        """Get battery level."""
        response = await self._soma.get_battery_level(self._mac)
        if isinstance(response, tuple):
            self._battery_level = response[0]
            self._battery_percentage = response[1]
            return self.battery_level
        return None

    async def get_current_light_level(self) -> int | None:
        """
        Asks SOMA Connect to retrieve the light level from the motor at
        most once every ten minutes.

        The rate limiting is done to minimise the impact on the battery life
        of each motor as the request has to be made using an active Bluetooth
        connection.
        """

        # only update the light level value if there is no current value
        # or if there is a value, at most once every 10 minutes
        if (
            self._light_level is None
            or self._light_level_last_updated is None
            or (
                datetime.datetime.now() - self._light_level_last_updated
                > datetime.timedelta(minutes=10)
            )
        ):
            light_level = await self._soma.get_light_level(self._mac)
            self._light_level = light_level
            self._light_level_last_updated = datetime.datetime.now()

        return self.light_level
