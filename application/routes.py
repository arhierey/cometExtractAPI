from .handlers import get_user_info, provide_form
from aiohttp import web


def setup_routes(app: web.Application) -> None:
    """
    Connect the endpoints to the handlers
    Args:
        app (web.Application): running application
    Returns:
        None
    """
    app.router.add_post('/fetch', get_user_info)
    app.router.add_get('/', provide_form)
