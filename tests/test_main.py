from asyncio_soma_connect.main import add


def test_add():
    assert add(1, 1) == 2
