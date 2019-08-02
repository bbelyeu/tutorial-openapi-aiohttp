"""Kudos Resource GET method tests."""
import json

from tests import conftest


async def test_get(client):
    """Test Kudos Resource GET method."""
    resp = await client.get('/kudos/1', headers={'Accept': 'application/json'})
    assert resp.status == 200
    assert 'application/json' in resp.headers['Content-Type']

    text = await resp.text()
    body = json.loads(text)

    assert body['id'] == 1
    conftest.kudo_asserts(body)
