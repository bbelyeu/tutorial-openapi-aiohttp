"""Hello World handler tests."""
import json


async def test_hello_world(client):
    """Test Hello World."""
    resp = await client.get(f'/hello-world', headers={'Accept': 'application/json'})
    assert resp.status == 200
    assert 'application/json' in resp.headers['Content-Type']

    text = await resp.text()
    body = json.loads(text)

    assert len(body.keys()) == 1
    assert 'Hello' in body.keys()
    assert body['Hello'] == 'World'
