from httpx import AsyncClient
from aiohttp import web
from .consts import *
import json
from typing import Any, Dict
from pydantic import BaseModel, EmailStr, ValidationError


class Email(BaseModel):
    """
    Email object for an email input handling
    Attributes:
        email: email provided by user
    """
    email: EmailStr


class CometResponse:
    """
    CometResponse object is for serializing comet API responses
    """
    def __init__(self, result_json: Dict[str, Any]):
        self.email = result_json['email']
        self.first_name = result_json['firstName']
        self.job_title = result_json['jobTitle']
        self.last_name = result_json['lastName']
        self.phone_number = result_json['phoneNumber']
        self.profile_picture_url = result_json['profilePictureUrl']
        self.corporate = result_json['corporate']
        self.freelance = result_json['freelance']
        self.team_member = result_json['teamMember']


async def get_user_info(request: web.Request) -> web.Response:
    """
    Retrieve user information from the platform using provided email and password
    Args:
        request (web.Request): incoming http request
    Returns:
        web.Response: response containing user information or an error message
    """
    content_type = request.content_type
    if content_type == 'application/json':
        data = await request.json()
    elif content_type == 'application/x-www-form-urlencoded':
        data = await request.post()
    else:
        return web.Response(text='415: Unsupported media type', status=415)

    try:
        email_data = Email(email=data.get('email'))
        email = email_data.email
    except ValidationError:
        return web.Response(text='400: Invalid email', status=400)

    password = data.get('password')
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
            comet_response = CometResponse(res_json['data']['authenticate'])
            return web.Response(text=json.dumps(vars(comet_response)), status=response.status_code)
        else:
            return web.Response(text=str(response.status_code) + ': ' +
                                'Email and password are required', status=response.status_code)


async def provide_form(request: web.Request) -> web.Response:
    """
    Render the html form for user to provide credentials
    Args:
        request (web.Request): incoming http request
    Returns:
        web.Response: response containing the html-form
    """
    return web.Response(text=HTML_FORM, content_type='text/html')
