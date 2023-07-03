from .handlers import get_user_info, provide_form


def setup_routes(app):
    # TODO: maybe I need GET, PUT and so on to
    app.router.add_post('/fetch', get_user_info)
    app.router.add_get('/', provide_form)
