"""Tests for aiosoma.Shade class."""
import random
from typing import Union

from aioresponses import aioresponses

from aiosoma import Connect, Shade

from . import HOST, LOOP, MAC, PORT, SUCCESS, URL, gen_shade_state


def get_shade(
    position: Union[int, None] = None,
    light_level: Union[int, None] = None,
    battery_level: Union[int, None] = None,
    battery_percentage: Union[int, None] = None,
) -> Shade:
    """Return a shade."""
    soma = Connect(HOST, PORT)
    return Shade(
        soma,
        name="Lounge",
        mac="aa:aa:aa:bb:bb:bb",
        type="shade",
        gen="2S",
        position=position,
        light_level=light_level,
        battery_level=battery_level,
        battery_percentage=battery_percentage,
    )


def test_get_shade_properties():
    """Fetch shade properties."""
    _position = random.randint(0, 100)
    _light_level = random.randint(0, 6000)
    _battery_level = random.randint(0, 500)
    _battery_percentage = random.randint(0, 100)

    shade = get_shade(
        position=_position,
        light_level=_light_level,
        battery_level=_battery_level,
        battery_percentage=_battery_percentage,
    )

    details = {
        "str": str(shade),
        "repr": repr(shade),
        "name": shade.name,
        "mac": shade.mac,
        "model": shade.model,
        "gen": shade.gen,
        "position": shade.position,
        "light_level": shade.light_level,
        "battery_level": shade.battery_level,
        "battery_percentage": shade.battery_percentage,
    }
    assert details == {
        "str": "Lounge: Shade 2S (aa:aa:aa:bb:bb:bb)",
        "repr": "<Lounge Shade 2S (aa:aa:aa:bb:bb:bb)>",
        "name": "Lounge",
        "mac": "aa:aa:aa:bb:bb:bb",
        "model": "Shade",
        "gen": "2S",
        "position": _position,
        "light_level": _light_level,
        "battery_level": _battery_level,
        "battery_percentage": _battery_percentage,
    }


def test_shade_open():
    """Test Shade.open()."""
    with aioresponses() as mock:
        shade = get_shade()
        print(shade, shade.__repr__)
        mock.get(f"{URL}/open_shade/{MAC}", payload=gen_shade_state())
        open_shade = LOOP.run_until_complete(shade.open())
        assert SUCCESS == open_shade


def test_shade_close():
    """Test Shade.close()."""
    with aioresponses() as mock:
        shade = get_shade()
        mock.get(f"{URL}/close_shade/{MAC}", payload=gen_shade_state())

        close_shade = LOOP.run_until_complete(shade.close())
        assert SUCCESS == close_shade


def test_shade_stop():
    """Test Shade.stop()."""
    with aioresponses() as mock:
        shade = get_shade()
        mock.get(f"{URL}/stop_shade/{MAC}", payload=gen_shade_state())

        stop_shade = LOOP.run_until_complete(shade.stop())
        assert SUCCESS == stop_shade


def test_shade_set_position():
    """Test Shade.set_position()."""
    with aioresponses() as mock:
        shade = get_shade()
        position = random.randint(0, 100)
        mock.get(
            f"{URL}/set_shade_position/{MAC}/{position}",
            payload=gen_shade_state(position=position),
        )

        set_shade_position = LOOP.run_until_complete(
            shade.set_position(
                position=position, close_upwards=False, morning_mode=False
            )
        )
        assert isinstance(set_shade_position, dict)
        _shade_position = set_shade_position.pop("position")
        assert _shade_position == str(position)
        assert SUCCESS == set_shade_position


def test_shade_get_state():
    """Test Shade.get_state()."""
    with aioresponses() as mock:
        shade = get_shade()
        position = random.randint(0, 100)
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position))
        get_state = LOOP.run_until_complete(shade.get_state())
        assert isinstance(get_state, dict)
        _get_state_position = get_state.pop("position")
        assert _get_state_position == str(position)
        assert SUCCESS == get_state


def test_shade_get_battery_level():
    """Test Shade.get_battery_level()."""
    with aioresponses() as mock:
        shade = get_shade()
        battery_level = random.randint(0, 500)
        battery_percentage = random.randint(0, 100)
        mock.get(
            f"{URL}/get_battery_level/{MAC}",
            payload=gen_shade_state(
                battery_level=battery_level, battery_percentage=battery_percentage
            ),
        )
        get_battery_level = LOOP.run_until_complete(shade.get_battery_level())
        assert isinstance(get_battery_level, dict)

        _level = get_battery_level.pop("battery_level")
        _percent = get_battery_level.pop("battery_percentage")

        assert _level == str(battery_level)
        assert _percent == str(battery_percentage)

        assert SUCCESS == get_battery_level


def test_shade_get_light_level():
    """Test Shade.get_light_level()."""
    with aioresponses() as mock:
        shade = get_shade()
        light_level = random.randint(0, 5000)

        mock.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=light_level),
        )
        get_light_level = LOOP.run_until_complete(shade.get_light_level())
        assert isinstance(get_light_level, dict)

        _level = get_light_level.pop("light_level")
        assert _level == str(light_level)
        assert SUCCESS == get_light_level
