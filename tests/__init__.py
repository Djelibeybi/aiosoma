"""Tests for aiosoma.Connect"""

import asyncio
from typing import Optional
from unittest.mock import AsyncMock

from aiosoma import SomaConnect, SomaShade

HOST = "soma-connect.local"
PORT = 3000
URL = f"http://{HOST}:{PORT}"

MAC = "aa:aa:aa:bb:bb:bb"
NAME = "Lounge"
TYPE = "shade"
GEN = "2S"


LOOP = asyncio.get_event_loop()


DEVICE_LIST: list[dict[str, str]] = [
    {"name": "Lounge", "mac": "aa:aa:aa:bb:bb:bb", "type": "shade", "gen": "2S"},
    {"name": "Kitchen", "mac": "cc:cc:cc:dd:dd:dd", "type": "shade", "gen": "2S"},
    {"name": "Bedroom", "mac": "ee:ee:ee:ff:ff:ff", "type": "shade", "gen": "2"},
]

LIST_DEVICES_PAYLOAD = {
    "result": "success",
    "version": "2.3.1",
    "shades": [
        {
            "name": "Lounge",
            "mac": "aa:aa:aa:bb:bb:bb",
            "type": "shade",
            "gen": "2S",
        },
        {"name": "Kitchen", "mac": "cc:cc:cc:dd:dd:dd", "type": "shade", "gen": "2S"},
        {
            "name": "Bedroom",
            "mac": "ee:ee:ee:ff:ff:ff",
            "type": "shade",
            "gen": "2",
        },
    ],
}

SUCCESS = {"result": "success", "version": "2.3.1", "mac": "aa:aa:aa:bb:bb:bb"}
FAILURE = {"result": "error", "msg": "NOSHADEWITHMAC"}


def mocked_connect() -> SomaConnect:
    """Mocked SOMA Connect."""
    connect = SomaConnect(HOST, PORT)
    return connect


def mocked_bad_connect() -> SomaConnect:
    """Mocked bad SOMA Connect."""
    connect = SomaConnect(HOST, PORT)
    connect.list_devices = AsyncMock(return_value=None)  # type: ignore
    connect.get_shade_position = AsyncMock(return_value=False)  # type: ignore
    connect.get_battery_level = AsyncMock(return_value=False)  # type: ignore
    connect.get_light_level = AsyncMock(return_value=False)  # type: ignore
    connect.set_shade_position = AsyncMock(return_value=False)  # type: ignore
    return connect


def mocked_shade() -> SomaShade:
    """Mocked SOMA Shade."""
    shade = SomaShade(mocked_connect(), MAC, NAME, TYPE, GEN)
    return shade


def mocked_bad_shade() -> SomaShade:
    """Mocked bad shade."""
    shade = SomaShade(mocked_bad_connect(), None, None, None, None)  # type: ignore
    return shade


def gen_bad_state() -> dict[str, str]:
    """Generated a failed response."""
    state = FAILURE.copy()
    return state


def gen_shade_state(
    position: Optional[int] = None,
    battery_level: Optional[int] = None,
    battery_percentage: Optional[int] = None,
    light_level: Optional[int] = None,
) -> dict[str, str]:
    """Generate the state based on position."""
    state = SUCCESS.copy()

    if position is not None:
        state["position"] = str(position)

    if battery_level is not None:
        state["battery_level"] = str(battery_level)

    if battery_percentage is not None:
        state["battery_percentage"] = str(battery_percentage)

    if light_level is not None:
        state["light_level"] = str(light_level)

    return state
