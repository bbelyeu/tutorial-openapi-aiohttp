"""Handler for root of tutorial API."""
from aiohttp import web


async def collection_get(request):
    """Root of site which just redirects."""
    raise web.HTTPMovedPermanently('https://github.com/bbelyeu/tutorial-openapi-aiohttp')
