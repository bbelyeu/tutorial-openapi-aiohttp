"""Kudos Resource PUT method tests."""
import json

import psycopg2
from dateutil.parser import parse

import main
from tests import conftest


async def test_put(client):
    """Test Kudos Resource PUT method."""
    app = await main.get_app()
    async with app.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as db:
            sql = "insert into kudos (kudo) values ('update me') returning *"
            await db.execute(sql)
            row = await db.fetchone()

    data = {'kudo': 'this is an update'}
    resp = await client.put(f"/kudos/{row['id']}", json=data,
                            headers={'Accept': 'application/json'})
    assert resp.status == 200
    assert 'application/json' in resp.headers['Content-Type']

    text = await resp.text()
    body = json.loads(text)

    conftest.kudo_asserts(body)
    assert body['id'] == row['id']
    assert body['kudo'] == 'this is an update'
    assert body['created_dt'] != body['updated_dt']
    created_dt = parse(body['created_dt'])
    updated_dt = parse(body['updated_dt'])
    assert updated_dt > created_dt
