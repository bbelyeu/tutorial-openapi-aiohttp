"""Kudos Resource DELETE method tests."""
import psycopg2

import main


async def test_put(client):
    """Test Kudos Resource DELETE method."""
    app = await main.get_app()
    async with app.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as db:
            sql = "insert into kudos (kudo) values ('delete me') returning id"
            await db.execute(sql)
            row = await db.fetchone()

    resp = await client.delete(f"/kudos/{row['id']}")
    assert resp.status == 204

    text = await resp.text()
    assert text == ''

    async with app.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as db:
            sql = 'select * from kudos where id = %(id)s'
            await db.execute(sql, {'id': row['id']})
    assert not db.rowcount
