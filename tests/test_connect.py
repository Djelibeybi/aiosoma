# type: ignore

"""Tests for aiosoma.Connect class."""
import random
import re

from aioresponses import aioresponses

from aiosoma import Connect

from . import (
    FAILURE,
    HOST,
    LIST_DEVICES_PAYLOAD,
    LOOP,
    MAC,
    PORT,
    SUCCESS,
    URL,
    gen_bad_state,
    gen_shade_state,
)


def test_failed_get():
    """Test soma.set_shade_position()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(f"{URL}/open_shade/{MAC}", payload=gen_bad_state())
        get_resp = LOOP.run_until_complete(soma.open_shade(MAC))

        mock.assert_called()
        assert FAILURE == get_resp


def test_list_devices():
    """Test soma.list_devices()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(
            f"{URL}/list_devices",
            payload=LIST_DEVICES_PAYLOAD,
        )
        response = LOOP.run_until_complete(soma.list_devices())
        assert LIST_DEVICES_PAYLOAD == response
        mock.assert_called_once()


def test_open_shade():
    """Test soma.open_shade()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(f"{URL}/open_shade/{MAC}", payload=gen_shade_state())
        response = LOOP.run_until_complete(soma.open_shade(MAC))
        assert SUCCESS == response
        mock.assert_called_once()


def test_close_shade():
    """Test soma.close_shade()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(f"{URL}/close_shade/{MAC}", payload=gen_shade_state())
        response = LOOP.run_until_complete(soma.close_shade(MAC))
        assert SUCCESS == response
        mock.assert_called_once()


def test_stop_shade():
    """Test soma.stop_shade()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(f"{URL}/stop_shade/{MAC}", payload=gen_shade_state())
        response = LOOP.run_until_complete(soma.stop_shade(MAC))
        assert SUCCESS == response
        mock.assert_called_once()


def test_get_shade_state():
    """Test soma.get_shade_state()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        position = random.randint(0, 100)
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position))
        response = LOOP.run_until_complete(soma.get_shade_state(MAC))
        assert isinstance(response, dict)
        assert response["position"] == str(position)
        mock.assert_called_once()


def test_set_shade_position():
    """Test soma.set_shade_position()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        position = random.randint(0, 100)
        mock.get(
            f"{URL}/set_shade_position/{MAC}/{position}", payload=gen_shade_state()
        )
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position))
        set_resp = LOOP.run_until_complete(soma.set_shade_position(MAC, position))
        get_resp = LOOP.run_until_complete(soma.get_shade_state(MAC))

        mock.assert_called()

        assert SUCCESS == set_resp
        assert isinstance(get_resp, dict)
        assert get_resp["position"] == str(position)


def test_set_shade_position_options():
    """Test soma.set_shade_position() with open_upwards."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        position = random.randint(0, 100)
        mock.get(
            f"{URL}/set_shade_position/{MAC}/{position}?close_upwards=1&morning_mode=1",
            payload=gen_shade_state(),
        )
        mock.get(f"{URL}/get_shade_state/{MAC}", payload=gen_shade_state(position))
        set_resp = LOOP.run_until_complete(
            soma.set_shade_position(
                MAC, position, close_upwards=True, morning_mode=True
            )
        )
        get_resp = LOOP.run_until_complete(soma.get_shade_state(MAC))

        mock.assert_called()
        assert SUCCESS == set_resp

        assert isinstance(get_resp, dict)
        assert get_resp["position"] == str(position)


def test_set_shade_position_below_zero():
    """Test soma.set_shade_position() with position < 0."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(f"{URL}/set_shade_position/{MAC}/0", payload=gen_shade_state())
        response = LOOP.run_until_complete(soma.set_shade_position(MAC, -20))

        mock.assert_called()
        assert SUCCESS == response


def test_set_shade_position_above_100():
    """Test soma.set_shade_position() with position > 100."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        mock.get(f"{URL}/set_shade_position/{MAC}/100", payload=gen_shade_state())
        response = LOOP.run_until_complete(soma.set_shade_position(MAC, 120))

        mock.assert_called()
        assert SUCCESS == response


def test_get_battery_level():
    """Test soma.get_battery_level()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        battery_level = random.randint(0, 500)
        battery_percentage = random.randint(0, 100)
        mock.get(
            f"{URL}/get_battery_level/{MAC}",
            payload=gen_shade_state(
                battery_level=battery_level, battery_percentage=battery_percentage
            ),
        )
        response = LOOP.run_until_complete(soma.get_battery_level(MAC))
        mock.assert_called_once()
        assert isinstance(response, dict)
        assert response["battery_level"] == str(battery_level)
        assert response["battery_percentage"] == str(battery_percentage)


def test_get_light_level():
    """Test soma.get_light_level()."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)
        light_level = random.randint(0, 6000)
        mock.get(
            f"{URL}/get_light_level/{MAC}",
            payload=gen_shade_state(light_level=light_level),
        )
        response = LOOP.run_until_complete(soma.get_light_level(MAC))
        mock.assert_called_once()
        assert isinstance(response, dict)
        assert response["light_level"] == str(light_level)


def test_without_mac():
    """Test soma with mac == None."""
    with aioresponses() as mock:
        soma = Connect(HOST, PORT)

        no_mac = None  # pylint: disable=redefined-outer-name,invalid-name
        pattern = re.compile(r"^http://soma-connect\.local\:3000/.*$")
        mock.get(pattern, payload=None)

        resp = LOOP.run_until_complete(soma.open_shade(no_mac))  # noqa
        assert resp is None

        resp = LOOP.run_until_complete(soma.close_shade(no_mac))
        assert resp is None

        resp = LOOP.run_until_complete(soma.stop_shade(no_mac))
        assert resp is None

        resp = LOOP.run_until_complete(soma.get_shade_state(no_mac))
        assert resp is None

        resp = LOOP.run_until_complete(soma.set_shade_position(no_mac, 10))
        assert resp is None

        resp = LOOP.run_until_complete(
            soma.set_shade_position("aa:bb:cc:dd:ee:ff", None)
        )
        assert resp is None

        resp = LOOP.run_until_complete(soma.get_battery_level(no_mac))
        assert resp is None

        resp = LOOP.run_until_complete(soma.get_light_level(no_mac))
        assert resp is None
