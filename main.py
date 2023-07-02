from aiohttp import web
from application import routes


app = web.Application()
routes.setup_routes(app)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)
