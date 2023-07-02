from .handlers import get_user_info


def setup_routes(app):
    app.router.add_get('/fetch', get_user_info)
