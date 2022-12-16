"""aiosoma CLI."""
from __future__ import annotations

import asyncio
import socket
from functools import wraps
from typing import Any, Iterable

import click
from rich import box
from rich import print as markup
from rich.console import Console
from rich.pretty import pprint
from rich.table import Table

from . import Connect, Shade

JSON_OUTPUT: bool = False


def coro(func: Any) -> Any:
    """Function annotation to mark a command as an async coroutine."""

    @wraps(func)
    def wrapper(*args: Iterable[Any], **kwargs: dict[str, Any]) -> Any:
        return asyncio.run(func(*args, **kwargs))

    return wrapper


async def get_shade(
    soma: Connect, mac: str | None = None, name: str | None = None
) -> Shade | None:
    """Get Shade from provided parameters."""

    if mac is None and name is None:
        raise click.UsageError("Must provide at least one of --mac or --name")

    if mac is not None and name is not None:
        raise click.UsageError("Must provide only one of --mac or --name")

    if mac is not None:
        return await get_shade_from_mac(soma, mac)

    if name is not None:
        return await get_shade_from_name(soma, name)

    return None


async def get_shade_from_mac(soma: Connect, mac: str) -> Shade | None:
    """Return shade with specified mac"""
    response = await soma.list_devices()
    if isinstance(response, dict):
        for shade in response.get("shades", {}):
            if shade["mac"] == mac:
                return Shade(soma, **shade)
    return None


async def get_shade_from_name(soma: Connect, name: str) -> Shade | None:
    """Return shade with specified name"""
    response = await soma.list_devices()
    if isinstance(response, dict):
        for device in response.get("shades", {}):
            if device["name"] == name:
                return Shade(soma, **device)
    return None


def handle_result(result: dict[str, Any] | bool) -> None:
    """Handle the result."""
    if JSON_OUTPUT is True:
        pprint(result)
    elif result is False:
        markup("response: [bold red]error[/bold red]")
    elif isinstance(result, dict) and result.get("result", "") == "success":
        markup("response: [bold green]success[/bold green]")


@click.group()
@click.option(
    "--host",
    default="soma-connect",
    help="Host name or IP address of SOMA Connect.",
    type=str,
)
@click.option("--port", default=3000, help="API port of SOMA Connect", type=int)
@click.option(
    "--json", is_flag=True, default=False, help="Return result in JSON format"
)
@click.pass_context
def cli(context: click.Context, host: str, port: int, json: bool) -> None:
    """Simple soma CLI interface to control shades."""
    global JSON_OUTPUT  # pylint: disable=global-statement

    context.obj = Connect(host, port)
    JSON_OUTPUT = json

    try:
        ip_addr = socket.gethostbyname(host)
        _ = socket.create_connection((ip_addr, port), 1)

    except socket.gaierror as exc:
        raise click.UsageError(f"{host} not found") from exc

    except ConnectionError as exc:
        raise click.UsageError(f"unable to connect to {host}:{port}") from exc


@cli.command()
@click.pass_obj
@coro
async def list_shades(soma: Connect) -> None:
    """Output the list of shades discovered by SOMA Connect."""

    response: dict[str, Any] | bool = await soma.list_devices()
    if isinstance(response, dict):
        if JSON_OUTPUT is True:
            pprint(response)
        else:
            console = Console()
            table = Table("name", "mac ", "model", "gen", box=box.ASCII)
            for shade in response["shades"]:
                _shade = Shade(soma, **shade)
                table.add_row(_shade.name, _shade.mac, _shade.model, _shade.gen)
            console.print(table)


@cli.command()
@click.option("--mac", "-m", help="Mac address of the shade.", type=str)
@click.option("--name", "-n", help="Name of the shade.", type=str)
@click.pass_obj
@coro
async def open_shade(soma: Connect, mac: str | None, name: str | None) -> None:
    """Open a shade by providing either its MAC address or name."""

    shade: Shade | None = await get_shade(soma, mac, name)
    if shade is not None:
        handle_result(await shade.open())


@cli.command()
@click.option("--mac", "-m", help="Mac address of the shade", type=str)
@click.option("--name", "-n", help="Name of the shade", type=str)
@click.pass_obj
@coro
async def close_shade(soma: Connect, mac: str | None, name: str | None) -> None:
    """Close a shade by providing either its MAC address or name"""

    shade: Shade | None = await get_shade(soma, mac, name)
    if shade is not None:
        handle_result(await shade.close())


@cli.command()
@click.option(
    "--position",
    required=True,
    type=click.IntRange(0, 100, clamp=True),
    help="Target position (0-100)",
)
@click.option(
    "--upwards", is_flag=True, default=False, help="Close upwards (requires Tilt)"
)
@click.option(
    "--slow/--fast",
    default=False,
    help="Enable morning mode (quieter and slower)",
)
@click.option("--mac", "-m", help="Mac address of the shade", type=str)
@click.option("--name", "-n", help="Name of the shade", type=str)
@click.pass_obj
@coro
async def set_position(
    soma: Connect,
    position: int,
    upwards: bool,
    slow: bool,
    mac: str | None,
    name: str | None,
) -> None:
    """
    Set a shade to specific position

    Includes support for opening Tilt shades upwards and for enabling morning
    mode which makes the shade quieter but slower.
    """
    shade: Shade | None = await get_shade(soma, mac, name)
    kwargs: dict[str, bool] = {"close_upwards": False, "morning_mode": False}
    if upwards is True:
        kwargs["close_upwards"] = True
    if slow is True:
        kwargs["morning_mode"] = True
    if shade is not None:
        handle_result(await shade.set_position(position, **kwargs))


@cli.command
@click.option("--mac", "-m", help="Mac address of the shade", type=str)
@click.option("--name", "-n", help="Name of the shade", type=str)
@click.pass_obj
@coro
async def stop_shade(soma: Connect, mac: str | None, name: str | None) -> None:
    """
    Stop all motion on the shade
    """
    shade: Shade | None = await get_shade(soma, mac, name)
    if shade is not None:
        handle_result(await shade.stop())


@cli.command
@click.option("--mac", "-m", help="Mac address of the shade", type=str)
@click.option("--name", "-n", help="Name of the shade", type=str)
@click.pass_obj
@coro
async def get_position(soma: Connect, mac: str | None, name: str | None) -> None:
    """Return the current state of a shade"""

    shade: Shade | None = await get_shade(soma, mac, name)
    if isinstance(shade, Shade):
        result: dict[str, Any] | bool = await shade.get_state()
        if isinstance(result, dict):
            if JSON_OUTPUT is True:
                pprint(result)
            else:
                _shade = Shade(
                    soma,
                    shade.mac,
                    shade.name,
                    shade.model,
                    shade.gen,
                    position=result["position"],
                )
                _position = (
                    f"{_shade.position}%" if _shade.position is not None else "/a"
                )
                console = Console()
                table = Table(show_header=False, box=box.ASCII)
                table.add_row("name", _shade.name)
                table.add_row("mac", _shade.mac)
                table.add_row("position", _position)
                console.print(table)


@cli.command
@click.option("--mac", "-m", help="Mac address of the shade.", type=str)
@click.option("--name", "-n", help="Name of the shade.", type=str)
@click.pass_obj
@coro
async def get_battery_level(soma: Connect, mac: str | None, name: str | None) -> None:
    """Return the current state of the shade."""

    shade: Shade | None = await get_shade(soma, mac, name)
    if isinstance(shade, Shade):
        result: dict[str, Any] | bool = await shade.get_battery_level()
        if isinstance(result, dict):
            if JSON_OUTPUT is True:
                pprint(result)
            else:
                _shade = Shade(
                    soma,
                    shade.mac,
                    shade.name,
                    shade.model,
                    shade.gen,
                    battery_level=result["battery_level"],
                    battery_percentage=result["battery_percentage"],
                )
                _battery_level = (
                    f"{_shade.battery_level}"
                    if _shade.battery_level is not None
                    else "n/a"
                )
                _battery_percentage = (
                    f"{_shade.battery_percentage}%"
                    if _shade.battery_percentage is not None
                    else "n/a"
                )
                console = Console()
                table = Table(show_header=False, box=box.ASCII)
                table.add_row("name", _shade.name)
                table.add_row("mac", _shade.mac)
                table.add_row("battery lvl", _battery_level)
                table.add_row("battery %", _battery_percentage)
                console.print(table)


@cli.command
@click.option("--mac", "-m", help="Mac address of the shade", type=str)
@click.option("--name", "-n", help="Name of the shade", type=str)
@click.pass_obj
@coro
async def get_light_level(soma: Connect, mac: str | None, name: str | None) -> None:
    """Return the current state of a shade"""

    shade: Shade | None = await get_shade(soma, mac, name)
    if isinstance(shade, Shade):
        result: dict[str, Any] | bool = await shade.get_light_level()
        if isinstance(result, dict):
            if JSON_OUTPUT is True:
                pprint(result)
            else:
                _shade = Shade(
                    soma,
                    shade.mac,
                    shade.name,
                    shade.model,
                    shade.gen,
                    light_level=result["light_level"],
                )
                _light_level = (
                    f"{_shade.light_level}" if _shade.light_level is not None else "n/a"
                )
                console = Console()
                table = Table(show_header=False, box=box.ASCII)
                table.add_row("name", _shade.name)
                table.add_row("mac", _shade.mac)
                table.add_row("light level", _light_level)
                console.print(table)
