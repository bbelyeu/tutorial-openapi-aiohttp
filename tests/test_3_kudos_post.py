"""Kudos Collection POST method tests."""
import datetime
import json

import psycopg2

import main
from tests import conftest


async def test_post(client):
    """Test Kudos Collection POST method."""
    data = {'kudo': 'This is a really great test.'}
    resp = await client.post('/kudos', json=data, headers={'Content-Type': 'application/json'})

    assert resp.status == 201
    assert 'application/json' in resp.headers['Content-Type']

    text = await resp.text()
    body = json.loads(text)

    conftest.kudo_asserts(body)

    # Let's read from the db and see if this worked
    app = await main.get_app()
    async with app.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as db:
            sql = 'select * from kudos where id = %(id)s'
            await db.execute(sql, {'id': body['id']})
            row = await db.fetchone()

    assert row
    assert row['kudo'] == data['kudo']
    assert row['created_dt']
    assert isinstance(row['created_dt'], datetime.datetime)
