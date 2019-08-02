"""Kudos GET method tests."""
import json

from tests import conftest


async def test_get(client):
    """Test Kudos GET method."""
    resp = await client.get('/kudos', headers={'Accept': 'application/json'})
    assert resp.status == 200
    assert 'application/json' in resp.headers['Content-Type']

    text = await resp.text()
    body = json.loads(text)

    assert isinstance(body, list)
    for kudo in body:
        conftest.kudo_asserts(kudo)
