"""Pytest setup stuff."""
import datetime

import pytest
from dateutil.parser import parse

import main


@pytest.fixture(scope='function', autouse=True)
async def client(aiohttp_client):
    """Setup the aiohttp client for tests."""
    app = await main.get_app()
    return await aiohttp_client(app.app)


def kudo_asserts(kudo):
    """Assert format of a kudo object."""
    assert 'id' in kudo
    assert 'kudo' in kudo
    assert 'created_dt' in kudo
    assert 'updated_dt' in kudo
    assert isinstance(kudo['id'], int)
    assert isinstance(kudo['kudo'], str)
    assert isinstance(kudo['created_dt'], str)
    assert isinstance(kudo['updated_dt'], str)
    created_dt = parse(kudo['created_dt'])
    assert isinstance(created_dt, datetime.datetime)
    updated_dt = parse(kudo['updated_dt'])
    assert isinstance(updated_dt, datetime.datetime)
