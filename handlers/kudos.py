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


async def collection_post(request):
    """Post a new kudo object and save to db."""
    data = await request.json()

    sql = 'insert into kudos (kudo) values (%(kudo)s) returning *;'
    async with request.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as db:
            await db.execute(sql, data)
            row = await db.fetchone()

    body = bytes(json.dumps(row, default=main.serialize), 'utf-8')
    return web.Response(body=body, status=201, headers={'Content-Type': 'application/json'})


async def resource_get(id, request):
    """Get a Kudo object by id."""
    sql = 'select * from kudos where id = %(id)s;'
    async with request.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            await cur.execute(sql, {'id': id})
            data = await cur.fetchone()

    body = bytes(json.dumps(data, default=main.serialize), 'utf-8')
    return web.Response(body=body, headers={'Content-Type': 'application/json'})


async def resource_put(id, request):
    """Update a Kudo object by id."""
    data = await request.json()

    sql = 'update kudos set kudo = %(kudo)s, updated_dt = NOW() where id = %(id)s returning *;'
    async with request.app['db_conn'].acquire() as conn:
        async with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            await cur.execute(sql, {'id': id, 'kudo': data['kudo']})
            data = await cur.fetchone()

    body = bytes(json.dumps(data, default=main.serialize), 'utf-8')
    return web.Response(body=body, headers={'Content-Type': 'application/json'})
