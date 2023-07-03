from httpx import AsyncClient
from aiohttp import web
from .consts import *
import json
import re


async def get_user_info(request):
    content_type = request.content_type
    if content_type == 'application/json':
        data = await request.json()
    elif content_type == 'application/x-www-form-urlencoded':
        data = await request.post()
    else:
        return web.Response(text='415: Unsupported media type', status=415)

    email = data.get('email')
    password = data.get('password')

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return web.Response(text='400: Invalid email', status=400)
    if not password:
        return web.Response(text='400: Password required', status=400)

    api_path = 'https://api.comet.co/api/graphql'
    payload = {
        'operationName': 'authenticate',
        'variables':
            {'email': email, 'password': password, 'signupToken': 'null'},
            'query': QUERY
    }

    async with AsyncClient() as cli:

        response = await cli.post(api_path, json=payload)
        if response.status_code == 200:
            res_json = json.loads(response.text)
            if 'errors' in res_json:
                code = res_json['errors'][0]['extensions']['code']
                message = res_json['errors'][0]['message']
                return web.Response(text=str(code) + ': ' + message, status=code)

            return web.Response(text=response.text, status=response.status_code)
        else:
            return web.Response(text=str(response.status_code) + ': ' +
                                'Email and password are required', status=response.status_code)


async def provide_form(request):
    return web.Response(text=HTML_FORM, content_type='text/html')
