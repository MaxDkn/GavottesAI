from fastapi import Request, APIRouter, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.auth import login_for_access_token
import httpx


frontend_router = APIRouter()
templates = Jinja2Templates(directory="templates")
api_url = "http://127.0.0.1:8000"


@frontend_router.get('/')
async def hello_world_html_page(request: Request):
    list_test = []
    list_test.append(request.cookies.get("username"))
    list_test.append(request.cookies.get("password"))
    list_test.append(request.cookies.get("test"))
    
    cookie_value = list_test
    
    return templates.TemplateResponse("index.html", {"request": request, 'cookies': cookie_value})


@frontend_router.post("/cookie/")
def create_cookie(message: str):
    response = JSONResponse(content={})
    response.set_cookie(key="username", value=message.upper())
    response.set_cookie(key="password", value=message.lower())
    response.set_cookie(key="token", value=message.center(20))
    return response


@frontend_router.get("/read-cookie/")
def read_cookie(request: Request):
    cookie_value = request.cookies.get("fakesession")
    if cookie_value:
        return {"cookie_value": cookie_value}
    else:
        return {"message": "No cookie found"}
    

@frontend_router.get('/login', name='login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login_form.html", {"request": request})


@frontend_router.post('/login', response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'password',
            'username': username,
            'password': password,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{api_url}/api/auth/get_user_token', headers=headers, data=data)
            response.raise_for_status()  # Vérifie si la requête a échoué
        except httpx.HTTPStatusError as errh:
            msg = {'error':'username or password is wrong.', 'server_error': str(errh)}
        except httpx.RequestError as errc:
            msg = {"error": "something is wrong, don't worry, it's not your fault", 'server_error': str(errc)}
        else:
            msg = {'success': 'Logged In! jwt: "' + response.json()['access_token']+ '"'}
    return templates.TemplateResponse("login_form.html", {"request": request, **msg})


@frontend_router.get('/sign-up', name='sign-up', response_class=HTMLResponse)
async def sign_up_html_page(request: Request):
    return templates.TemplateResponse('signup_form.html', {'request': request})


@frontend_router.post('/sign-up', response_class=HTMLResponse)
async def sign_up_html_page(request: Request, username: str = Form(...), password: str = Form(...)):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    data = {
        'username': username,
        'password': password,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{api_url}/api/auth/create_user', headers=headers, json=data)
            response.raise_for_status()  # Vérifie si la requête a échoué
        except httpx.HTTPStatusError as errh:
            msg = {'error':'username already taken.'}
            #  return {'error': 'HTTP Error', 'details': str(errh)}
        except httpx.RequestError as errc:
            msg = {"error": "something is wrong, don't worry, it's not your fault"}
            #  return {'error': 'Connection Error', 'details': str(errc)}
        else:
            msg = {'success': 'Account created!'}
    templates_response = templates.TemplateResponse('signup_form.html', {'request': request, **msg})
    if 'success' in msg.keys():
        templates_response.set_cookie(key='username', value=username)
        templates_response.set_cookie(key='password', value=password)
    return templates_response
