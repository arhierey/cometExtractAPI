from httpx import AsyncClient
from aiohttp import web
from .consts import *


async def get_user_info(request):
    content_type = request.content_type
    if content_type == 'application/json':
        data = await request.json()
    elif content_type == 'application/x-www-form-urlencoded':
        data = await request.post()
    else:
        return web.Response(text='Unsupported media type', status=415)

    email = data.get('email')
    password = data.get('password')

    api_path = 'https://api.comet.co/api/graphql'

    query = QUERY

    payload = {
        'operationName': 'authenticate',
        'variables':
            {'email': email, 'password': password, 'signupToken': 'null'},
            'query': query
    }

    async with AsyncClient() as cli:

        response = await cli.post(api_path, json=payload)
        if response.status_code == 200:
            return web.Response(text=response.text)
        else:
            return web.Response(text="Email and password are required query parameters.", status=response.status_code)


async def provide_form(request):
    html_form = HTML_FORM

    return web.Response(text=html_form, content_type='text/html')
