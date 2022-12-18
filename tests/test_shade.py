"""Tests for aiosoma.Shade class."""
import datetime
import random

import pytest
from aioresponses import aioresponses
from freezegun import freeze_time

from aiosoma import SomaShade

from . import (
    DEVICE_LIST,
    MAC,
    URL,
    gen_bad_state,
    gen_shade_state,
    mocked_bad_shade,
    mocked_connect,
    mocked_shade,
)


def test_somashades_from_list_devices():
    """Test the SomaShade class properties."""

    shades: set[SomaShade] = set()
    for device in DEVICE_LIST:
        shades.add(
            SomaShade(
                mocked_connect(),
                name=device[0],
                mac=device[1],
                type=device[2],
                gen=device[3],
            )
        )

    for shade in shades:

        if shade.name == "Lounge":
            assert str(shade) == "Lounge: Shade 2S (aa:aa:aa:bb:bb:bb)"
            assert repr(shade) == "<Lounge Shade 2S (aa:aa:aa:bb:bb:bb)>"
        elif shade.name == "Kitchen":
            assert str(shade) == "Kitchen: Shade 2S (cc:cc:cc:dd:dd:dd)"
            assert repr(shade) == "<Kitchen Shade 2S (cc:cc:cc:dd:dd:dd)>"
        elif shade.name == "Bedroom":
            assert str(shade) == "Bedroom: Shade 2 (ee:ee:ee:ff:ff:ff)"
            assert repr(shade) == "<Bedroom Shade 2 (ee:ee:ee:ff:ff:ff)>"


@pytest.mark.asyncio()
async def test_bad_response():
    """Test failed result from SOMA Connect."""
    with aioresponses() as mock:
        shade = mocked_shade()
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_bad_state())
        get_current_position = await shade.get_current_position()
        assert get_current_position is None
        assert shade.position is None


@pytest.mark.asyncio()
async def test_get_shade_position():
    """Fetch shade properties."""
    mock_position = random.randint(0, 100)
    shade = mocked_shade()

    with aioresponses() as mock:
        mock.get(
            f"{URL}/get_shade_state/{MAC}",
            payload=gen_shade_state(position=mock_position),
        )
        await shade.get_current_position()
        assert shade.position == mock_position


@pytest.mark.asyncio()
async def test_get_shade_battery_level():
    """Fetch shade properties."""
    mock_battery_level = random.randint(0, 500)
    mock_battery_percentage = random.randint(0, 100)
    shade = mocked_shade()

    with aioresponses() as mock:
        mock.get(
            f"{URL}/get_battery_level/{MAC}",
            payload=gen_shade_state(
                battery_level=mock_battery_level,
                battery_percentage=mock_battery_percentage,
            ),
        )
        await shade.get_current_battery_level()
        assert shade.battery_level == mock_battery_level
        assert shade.battery_percentage == mock_battery_percentage


@pytest.mark.asyncio()
async def test_get_shade_light_level():
    """Fetch shade properties."""
    mock_light_level = random.randint(0, 6000)
    shade = mocked_shade()

    with aioresponses() as mock:
        mock.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=mock_light_level),
        )
        await shade.get_current_light_level()
        assert shade.light_level == mock_light_level


@pytest.mark.asyncio()
async def test_shade_open():
    """Test Shade.open()."""
    with aioresponses() as mock:
        shade = mocked_shade()
        mock.get(f"{URL}/open_shade/{MAC}", payload=gen_shade_state())

        open_shade = await shade.open()
        assert open_shade is True


@pytest.mark.asyncio()
async def test_shade_close():
    """Test Shade.close()."""
    with aioresponses() as mock:
        shade = mocked_shade()
        mock.get(f"{URL}/close_shade/{MAC}", payload=gen_shade_state())

        close_shade = await shade.close()
        assert close_shade is True


@pytest.mark.asyncio()
async def test_shade_stop():
    """Test Shade.stop()."""
    with aioresponses() as mock:
        shade = mocked_shade()
        mock.get(f"{URL}/stop_shade/{MAC}", payload=gen_shade_state())

        stop_shade = await shade.stop()
        assert stop_shade is True


@pytest.mark.asyncio()
async def test_shade_set_position():
    """Test Shade.set_position()."""
    with aioresponses() as mock:
        shade = mocked_shade()
        position = random.randint(0, 100)
        mock.get(
            f"{URL}/set_shade_position/{MAC}/{position}",
            payload=gen_shade_state(position=position),
        )

        set_shade_position = await shade.set_position(
            position=position, close_upwards=False, morning_mode=False
        )

        assert set_shade_position is True
        assert shade.position == position


@pytest.mark.asyncio()
async def test_shade_get_position():
    """Test Shade.get_position()."""

    with aioresponses() as mock:
        shade = mocked_shade()
        mock_position = random.randint(0, 100)
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(mock_position))

        get_current_position = await shade.get_current_position()
        assert isinstance(get_current_position, int)
        assert shade.position == mock_position


@pytest.mark.asyncio()
async def test_shade_get_battery_level():
    """Test Shade.get_battery_level()."""
    with aioresponses() as mock:
        shade = mocked_shade()
        mock_battery_level = random.randint(0, 500)
        mock_battery_percentage = random.randint(0, 100)
        mock.get(
            f"{URL}/get_battery_level/{MAC}",
            payload=gen_shade_state(
                battery_level=mock_battery_level,
                battery_percentage=mock_battery_percentage,
            ),
        )
        get_current_battery_level = await shade.get_current_battery_level()
        assert isinstance(get_current_battery_level, int)

        assert shade.battery_level == mock_battery_level
        assert shade.battery_percentage == mock_battery_percentage


@pytest.mark.asyncio()
async def test_shade_get_light_level():
    """Test Shade.get_light_level()."""
    with aioresponses() as mock:
        shade = mocked_shade()
        mock_light_level = random.randint(0, 5000)

        mock.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=mock_light_level),
        )
        get_current_light_level = await shade.get_current_light_level()
        assert isinstance(get_current_light_level, int)
        assert shade.light_level == mock_light_level


@pytest.mark.asyncio()
async def test_shade_get_light_level_limit():
    """Test Shade.get_light_level() is time limited."""
    shade = mocked_shade()
    with aioresponses() as mock:
        mock_first_light_level = random.randint(0, 5000)
        mock.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=mock_first_light_level),
        )

        get_current_light_level = await shade.get_current_light_level()
        assert isinstance(get_current_light_level, int)
        assert shade.light_level == mock_first_light_level

    with aioresponses() as mock, freeze_time(datetime.datetime.now()) as frozen_time:
        mock_second_light_level = random.randint(0, 5000)
        mock.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=mock_second_light_level),
        )

        frozen_time.tick(datetime.timedelta(minutes=3))
        await shade.get_current_light_level()
        assert shade.light_level == mock_first_light_level

        frozen_time.tick(datetime.timedelta(minutes=10))
        await shade.get_current_light_level()
        assert shade.light_level == mock_second_light_level


@pytest.mark.asyncio()
async def test_shade_failures():
    """Test code paths when things fail."""
    shade = mocked_bad_shade()

    assert shade.battery_level is None
    assert shade.battery_percentage is None
    assert shade.position is None
    assert shade.light_level is None

    await shade.get_current_battery_level()
    assert shade.battery_level is None
    assert shade.battery_percentage is None

    assert await shade.set_position(10) is False

    await shade.get_current_position()
    assert shade.position is None

    await shade.get_current_light_level()
    assert shade.light_level is None

    shade._light_level_last_updated = (  # pylint: disable=protected-access
        datetime.datetime.now()
    )

    with freeze_time(datetime.datetime.now()) as frozen_time:
        frozen_time.tick(datetime.timedelta(minutes=3))
        await shade.get_current_light_level()
        assert shade.light_level is None
