# type: ignore
"""Tests for aiosoma."""

import asyncio
import random
import re
from typing import Optional

from aioresponses import aioresponses

from aiosoma import AioSoma

MAC = "aa:aa:aa:bb:bb:bb"
HOST = "soma-connect.local"
PORT = 3000
URL = f"http://{HOST}:{PORT}"

LOOP = asyncio.get_event_loop()
SOMA = AioSoma(HOST, PORT)

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


def gen_shade_state(
    position: Optional[int] = None, battery_level: Optional[int] = None
) -> dict[str, str]:
    """Generate the state based on position."""
    state = SUCCESS.copy()
    if position is not None:
        state["position"] = str(position)
    elif battery_level is not None:
        state["battery_level"] = str(battery_level)
    return state


def test_list_devices():
    """Test aiosoma.list_devices()."""
    with aioresponses() as mock:
        mock.get(
            f"{URL}/list_devices",
            payload=LIST_DEVICES_PAYLOAD,
        )
        response = LOOP.run_until_complete(SOMA.list_devices())
        assert LIST_DEVICES_PAYLOAD == response
        mock.assert_called_once()


def test_open_shade():
    """Test aiosoma.open_shade()."""
    with aioresponses() as mock:
        mock.get(f"{URL}/open_shade/{MAC}", payload=gen_shade_state())
        response = LOOP.run_until_complete(SOMA.open_shade(MAC))
        assert SUCCESS == response
        mock.assert_called_once()


def test_close_shade():
    """Test aiosoma.close_shade()."""
    with aioresponses() as mock:
        mock.get(f"{URL}/close_shade/{MAC}", payload=gen_shade_state())
        response = LOOP.run_until_complete(SOMA.close_shade(MAC))
        assert SUCCESS == response
        mock.assert_called_once()


def test_stop_shade():
    """Test aiosoma.stop_shade()."""
    with aioresponses() as mock:
        mock.get(f"{URL}/stop_shade/{MAC}", payload=gen_shade_state())
        response = LOOP.run_until_complete(SOMA.stop_shade(MAC))
        assert SUCCESS == response
        mock.assert_called_once()


def test_get_shade_state():
    """Test aiosoma.get_shade_shade()."""
    with aioresponses() as mock:
        position = random.randint(0, 100)
        mock.get(f"{URL}/stop_shade/{MAC}", payload=gen_shade_state(position))
        response = LOOP.run_until_complete(SOMA.stop_shade(MAC))
        assert response["position"] == str(position)
        mock.assert_called_once()


def test_set_shade_position():
    """Test aiosoma.set_shade_position()."""
    with aioresponses() as mock:
        position = random.randint(0, 100)
        mock.get(
            f"{URL}/set_shade_position/{MAC}/{position}", payload=gen_shade_state()
        )
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position))
        set_resp = LOOP.run_until_complete(SOMA.set_shade_position(MAC, position))
        get_resp = LOOP.run_until_complete(SOMA.get_shade_state(MAC))

        mock.assert_called()
        assert SUCCESS == set_resp
        assert get_resp["position"] == str(position)


def test_set_shade_position_below_zero():
    """Test aiosoma.set_shade_position() with position < 0."""
    with aioresponses() as mock:
        mock.get(f"{URL}/set_shade_position/{MAC}/0", payload=gen_shade_state())
        response = LOOP.run_until_complete(SOMA.set_shade_position(MAC, -20))

        mock.assert_called()
        assert SUCCESS == response


def test_set_shade_position_above_100():
    """Test aiosoma.set_shade_position() with position > 100."""
    with aioresponses() as mock:
        mock.get(f"{URL}/set_shade_position/{MAC}/100", payload=gen_shade_state())
        response = LOOP.run_until_complete(SOMA.set_shade_position(MAC, 120))

        mock.assert_called()
        assert SUCCESS == response


def test_get_battery_level():
    """Test aiosoma.get_battery_level()."""
    with aioresponses() as mock:
        battery_level = random.randint(0, 100)
        mock.get(
            f"{URL}/get_battery_level/{MAC}",
            payload=gen_shade_state(battery_level=battery_level),
        )
        response = LOOP.run_until_complete(SOMA.get_battery_level(MAC))
        mock.assert_called_once()
        assert response["battery_level"] == str(battery_level)


def test_without_mac():
    """Test aiosoma with mac == None."""
    with aioresponses() as mock:
        MAC = None
        pattern = re.compile(r"^http://soma-connect\.local\:3000/.*$")
        mock.get(pattern, payload=None)

        resp = LOOP.run_until_complete(SOMA.open_shade(MAC))  # noqa
        assert resp is None

        resp = LOOP.run_until_complete(SOMA.close_shade(MAC))
        assert resp is None

        resp = LOOP.run_until_complete(SOMA.stop_shade(MAC))
        assert resp is None

        resp = LOOP.run_until_complete(SOMA.get_shade_state(MAC))
        assert resp is None

        resp = LOOP.run_until_complete(SOMA.set_shade_position(MAC, 10))
        assert resp is None

        resp = LOOP.run_until_complete(
            SOMA.set_shade_position("aa:bb:cc:dd:ee:ff", None)
        )
        assert resp is None

        resp = LOOP.run_until_complete(SOMA.get_battery_level(MAC))
        assert resp is None
