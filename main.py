"""App entry point."""
import asyncio
import datetime
import os

import aiopg
import connexion
import uvloop


async def get_app():
    """Get the app."""
    opts = {"swagger_ui": True}
    app = connexion.AioHttpApp(__name__, only_one_api=True, options=opts,
                               specification_dir='spec/')
    app.add_api('resolved.yaml', pass_context_arg_name='request', strict_validation=True)
    # Removed validate_responses=True because of protocol buffers
    # Can also use debug=True if needed in dev

    # Add db connection pool
    dsn = 'dbname=tutorial_openapi_aiohttp user={user} host={host} port={port}'.format(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        user=os.environ.get('DB_USER', 'dev'),
    )
    app.app['db_conn'] = await aiopg.create_pool(dsn, minsize=10, maxsize=500, timeout=10)

    return app


def serialize(obj):
    """Serialize datetimes for json dumps."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError('Type {} not serializable'.format(type(obj)))


if __name__ == '__main__':
    # Use uvloop instead of default event loop - it's faster
    POLICY = uvloop.EventLoopPolicy()
    asyncio.set_event_loop_policy(POLICY)
    LOOP = asyncio.get_event_loop()
    APP = LOOP.run_until_complete(get_app())
    APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
    APP_PORT = os.environ.get('APP_PORT', 9000)
    APP.run(port=APP_PORT, host=APP_HOST)
