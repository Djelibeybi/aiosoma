"""Tests for aiosoma.Connect class."""
import random
import re

import pytest
from aioresponses import aioresponses

from aiosoma import SomaConnect

from . import (
    DEVICE_LIST,
    HOST,
    LIST_DEVICES_PAYLOAD,
    MAC,
    PORT,
    URL,
    gen_bad_state,
    gen_shade_state,
    mocked_connect,
)


@pytest.mark.asyncio()
async def test_soma_connect_version():
    """Test the version property is returned."""
    with aioresponses() as mocked_response:
        soma = mocked_connect()
        mocked_response.get(f"{URL}/list_devices", payload=LIST_DEVICES_PAYLOAD)
        await soma.list_devices()
        assert soma.version == "2.3.1"


@pytest.mark.asyncio()
async def test_list_devices():
    """Test soma.list_devices()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        mocked_response.get(
            f"{URL}/list_devices",
            payload=LIST_DEVICES_PAYLOAD,
        )
        response = await soma.list_devices()
        assert isinstance(response, list)
        assert (device in DEVICE_LIST for device in response)
        mocked_response.assert_called_once()


@pytest.mark.asyncio()
async def test_failed_list_devices():
    """Test failed response to list_devices request."""
    with aioresponses() as mocked_response:
        soma = mocked_connect()
        mocked_response.get(f"{URL}/list_devices", payload=gen_bad_state())
        shade_list = await soma.list_devices()
        assert shade_list is None
        assert soma.devices is None


@pytest.mark.asyncio()
async def test_open_shade():
    """Test soma.open_shade()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        mocked_response.get(f"{URL}/open_shade/{MAC}", payload=gen_shade_state())
        response = await soma.open_shade(MAC)
        assert response is True
        mocked_response.assert_called_once()


@pytest.mark.asyncio()
async def test_close_shade():
    """Test soma.close_shade()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        mocked_response.get(f"{URL}/close_shade/{MAC}", payload=gen_shade_state())
        response = await soma.close_shade(MAC)
        assert response is True
        mocked_response.assert_called_once()


@pytest.mark.asyncio()
async def test_stop_shade():
    """Test soma.stop_shade()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        mocked_response.get(f"{URL}/stop_shade/{MAC}", payload=gen_shade_state())
        response = await soma.stop_shade(MAC)
        assert response is True
        mocked_response.assert_called_once()


@pytest.mark.asyncio()
async def test_get_shade_state():
    """Test soma.get_shade_state()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        position = random.randint(0, 100)
        mocked_response.get(
            f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position)
        )
        response = await soma.get_shade_position(MAC)
        assert response == str(position)
        mocked_response.assert_called_once()


@pytest.mark.asyncio()
async def test_set_shade_position():
    """Test soma.set_shade_position()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        position = random.randint(0, 100)
        mocked_response.get(
            f"{URL}/set_shade_position/{MAC}/{position}", payload=gen_shade_state()
        )
        mocked_response.get(
            f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position)
        )
        set_resp = await soma.set_shade_position(MAC, position)
        get_resp = await soma.get_shade_position(MAC)

        mocked_response.assert_called()

        assert set_resp is True
        assert get_resp == str(position)


@pytest.mark.asyncio()
async def test_set_shade_position_options():
    """Test soma.set_shade_position() with open_upwards."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        position = random.randint(0, 100)
        mocked_response.get(
            f"{URL}/set_shade_position/{MAC}/{position}?close_upwards=1&morning_mode=1",
            payload=gen_shade_state(),
        )
        mocked_response.get(
            f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position)
        )
        set_resp = await soma.set_shade_position(
            MAC, position, close_upwards=True, morning_mode=True
        )

        get_resp = await soma.get_shade_position(MAC)

        mocked_response.assert_called()
        assert set_resp is True
        assert get_resp == str(position)


@pytest.mark.asyncio()
async def test_set_shade_position_below_zero():
    """Test soma.set_shade_position() with position < 0."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        mocked_response.get(
            f"{URL}/set_shade_position/{MAC}/0", payload=gen_shade_state()
        )
        response = await soma.set_shade_position(MAC, -20)

        mocked_response.assert_called()
        assert response is True


@pytest.mark.asyncio()
async def test_set_shade_position_above_100():
    """Test soma.set_shade_position() with position > 100."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        mocked_response.get(
            f"{URL}/set_shade_position/{MAC}/100", payload=gen_shade_state()
        )
        response = await soma.set_shade_position(MAC, 120)

        mocked_response.assert_called()
        assert response is True


@pytest.mark.asyncio()
async def test_get_battery_level():
    """Test soma.get_battery_level()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        battery_level = random.randint(0, 500)
        battery_percentage = random.randint(0, 100)
        mocked_response.get(
            f"{URL}/get_battery_level/{MAC}",
            payload=gen_shade_state(
                battery_level=battery_level, battery_percentage=battery_percentage
            ),
        )
        response = await soma.get_battery_level(MAC)
        mocked_response.assert_called_once()
        assert isinstance(response, tuple)
        assert response[0] == str(battery_level)
        assert response[1] == str(battery_percentage)


@pytest.mark.asyncio()
async def test_get_light_level():
    """Test soma.get_light_level()."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)
        light_level = random.randint(0, 6000)
        mocked_response.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=light_level),
        )
        response = await soma.get_light_level(MAC)
        mocked_response.assert_called_once()
        assert response == str(light_level)


@pytest.mark.asyncio()
async def test_without_mac():
    """Test soma with mac == None."""
    with aioresponses() as mocked_response:
        soma = SomaConnect(HOST, PORT)

        pattern = re.compile(r"^http://soma-connect\.local\:3000/.*$")
        mocked_response.get(pattern, payload=gen_bad_state(), repeat=True)

        assert await soma.open_shade(MAC) is False
        assert await soma.open_shade(None) is False  # type: ignore

        assert await soma.close_shade(MAC) is False
        assert await soma.close_shade(None) is False  # type: ignore

        assert await soma.stop_shade(MAC) is False
        assert await soma.stop_shade(None) is False  # type: ignore

        assert await soma.get_shade_position(MAC) is False
        assert await soma.get_shade_position(None) is False  # type: ignore

        assert await soma.set_shade_position(None, 10) is False  # type: ignore
        assert await soma.set_shade_position(MAC, None) is False  # type: ignore
        assert await soma.set_shade_position(MAC, 10) is False

        assert await soma.get_battery_level(MAC) is False
        assert await soma.get_battery_level(None) is False  # type: ignore

        assert await soma.get_light_level(MAC) is False
        assert await soma.get_light_level(None) is False  # type: ignore
