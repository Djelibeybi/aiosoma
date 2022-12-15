"""aiosoma CLI."""
from __future__ import annotations

import asyncio
import logging
from functools import wraps
from typing import Any, Iterable

import click
from rich.logging import RichHandler

from . import Shade, SomaConnect

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
)
_LOGGER = logging.getLogger(__name__)

tasks: set[Any] = set()


def coro(f: Any) -> Any:
    @wraps(f)
    def wrapper(*args: Iterable[Any], **kwargs: dict[str, Any]) -> Any:
        return asyncio.run(f(*args, **kwargs))

    return wrapper


async def get_shade_from_name(soma: SomaConnect, name: str) -> Shade | None:
    """Return mac address from blind name."""
    response: dict[str, Any] | bool = await soma.api.list_devices()
    if isinstance(response, dict):
        for device in response.get("shades", {}):
            if device["name"] == name:
                return Shade(soma.api, device["mac"])
    return None


@click.group()
@click.option(
    "--host",
    "-h",
    default="soma-connect.local",
    help="Host name or IP address of SOMA Connect.",
    type=str,
)
@click.option("--port", "-p", default=3000, help="API port of SOMA Connect.", type=int)
@click.pass_context
def cli(context: click.Context, host: str, port: int) -> None:
    """Simple soma CLI interface to control shades."""
    context.obj = SomaConnect(host, port)


@cli.command()
@click.pass_obj
@coro
async def list(obj: SomaConnect) -> None:
    """Output the list of shades discovered by SOMA Connect."""
    soma: SomaConnect = obj.soma_connect
    response: dict[str, Any] | bool = await soma.api.list_devices()
    if isinstance(response, dict):
        shades = [Shade(api=soma.api, **shade) for shade in response["shades"]]
        for shade in shades:
            print(shade)


@cli.command()
@click.option("--mac", "-m", help="Mac address of the shade.", type=str)
@click.option("--name", "-n", help="Name of the shade.", type=str)
@click.pass_obj
@coro
async def open(obj: SomaConnect, mac: str | None, name: str | None) -> None:
    """open shade with provided mac."""
    soma: SomaConnect = obj.soma_connect

    if mac is None and name is None:
        _LOGGER.error("Must provide at least one of --mac or --name.")
        click.echo("Must provide at least one of --mac or --name.")
    elif mac is not None and name is not None:
        _LOGGER.error("Must provide only one of --mac or --name.")
        click.echo("Must provide only one of --mac or --name.")

    if mac is not None:
        shade = Shade(soma.api, mac=mac)
        await shade.open()

    elif name is not None:
        shade_name: Shade | None = await get_shade_from_name(soma, name)
        if isinstance(shade_name, Shade):
            await shade_name.open()


@cli.command()
@click.option("--mac", "-m", help="Mac address of the shade.", type=str)
@click.option("--name", "-n", help="Name of the shade.", type=str)
@click.pass_obj
@coro
async def close(obj: SomaConnect, mac: str | None, name: str | None) -> None:
    """open shade with provided mac."""
    soma: SomaConnect = obj.soma_connect

    if mac is None and name is None:
        _LOGGER.error("Must provide at least one of --mac or --name.")
        click.echo("Must provide at least one of --mac or --name.")
    elif mac is not None and name is not None:
        _LOGGER.error("Must provide only one of --mac or --name.")
        click.echo("Must provide only one of --mac or --name.")

    if mac is not None:
        mac_shade = Shade(soma.api, mac=mac)
        await mac_shade.close()

    elif name is not None:
        name_shade: Shade | None = await get_shade_from_name(soma, name)
        if isinstance(name_shade, Shade):
            await name_shade.close()
