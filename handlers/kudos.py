"""Handler for Kudos APIs."""
import json

import psycopg2
from aiohttp import web

import main


async def collection_get(request):
    """Get a list of Kudo objects."""
    sql = 'select * from kudos;'
    async with request.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            await cur.execute(sql)
            data = await cur.fetchall()

    body = bytes(json.dumps(data, default=main.serialize), 'utf-8')
    return web.Response(body=body, headers={'Content-Type': 'application/json'})
