"""Handler for Hello World tutorial API."""
from aiohttp import web


async def collection_get(request):
    """Hello."""
    return web.json_response({'Hello': 'World'})
