import httpx
from typing import Optional
from datetime import datetime
from collections import Counter
from fastapi import Request, APIRouter, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


frontend_router = APIRouter()
templates = Jinja2Templates(directory="templates")
api_env_url = ""


@frontend_router.get('/', name='home')
async def page_with_all_houses(request: Request):
    print(str(request.base_url).rstrip('/'))
    #  ------------------Ce code permet de vérifier si la session est active------------------
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        async with httpx.AsyncClient() as client:
            response_username = await client.get(f'{api_url}/api/auth/me', headers=headers)
            response = await client.get(f'{api_url}/api/house/me', headers=headers)
            if not (response_username.status_code == 200 or response.status_code == 200):
                return RedirectResponse(url='/login')
            username = response_username.json()['username']
    else:
        return RedirectResponse(url='/landing-page')
    #  ----------------------------------------------------------------------------------------------
    tables = response.json()
    total_price = 0
    for table in tables:
        date_obj = datetime.strptime(table['DayTime'], "%Y-%m-%dT%H:%M:%S")
        table['DayTime'] = str(date_obj.day) + date_obj.strftime(" %B %H:%M")
        total_price += table['Price']
        table['Price'] = f"{int(table['Price'])}€" if int(table['Price']) == table['Price'] else f"{table['Price']}€"

    # Trie d'abord par nombre de maisons (descendant), puis par nom de rue et numéro d'adresse
    tables = sorted(tables, key=lambda x: (-Counter(address['StreetName'] for address in tables)[x['StreetName']], x['StreetName'], x['AddressNumber']))
    return templates.TemplateResponse("index.html", {"request": request, 'username': username, 'tables': tables, 'total_price': total_price})


@frontend_router.get('/create', name='create')
async def create_house_html_form(request: Request):
    #  ------------------Ce code permet de vérifier si la session est active------------------
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_url}/api/house/me', headers=headers)
            if not response.status_code == 200:
                return RedirectResponse(url='/login')
            response = response.json()
            response = response[-1] if len(response) > 0 else {}

    else:
        return RedirectResponse(url='/landing-page')
    #  ----------------------------------------------------------------------------------------------
    
    return templates.TemplateResponse('create_form.html', {'request': request, **response})


@frontend_router.post('/create')
async def send_form_to_api(request: Request, AddressNumber: int = Form(...), StreetName: str = Form(...), Respond: str = Form(...), Size: str = Form(...), SecurityGateOrAlarm: str = Form(...), Dog: str = Form(...), Age: Optional[str] = Form(None), Gender: Optional[str] = Form(None), Price: Optional[float] = Form(0)):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        content = {"AddressNumber": AddressNumber,
                   "StreetName": StreetName,
                   "Respond": Respond=='Yes',
                   "Size": Size,
                   "SecurityGateOrAlarm": SecurityGateOrAlarm=='Yes',
                   "Dog": Dog,
                   "Price": Price * int(Respond=="Yes")}
        if Respond:
            content['Age'] = Age
            content['Gender'] = Gender
        async with httpx.AsyncClient() as client:
            response = await client.post(f'{api_url}/api/house/create', headers=headers, json=content)
            if not response.status_code == 200:
                return templates.TemplateResponse('create_form.html', {'request': request, 'error': response.json()['detail']})
    else:
        return RedirectResponse(url='/landing-page')
    #  ----------------------------------------------------------------------------------------------
    
    return RedirectResponse(url='/', status_code=303)


@frontend_router.get('/edit/{house_id}', name='edit', response_class=HTMLResponse)
async def edit_html_page(request: Request, house_id: int):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    notification = {}
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_url}/api/house/{house_id}', headers=headers)
            if not response.status_code == 200:
                try:
                    notification['error'] = response.json()['detail']
                except:
                    notification['error'] = "Il s'est produit une erreur."
    else:
        return RedirectResponse(url='/landing-page')
    
    return templates.TemplateResponse('update_form.html', {'request': request, 'house_id': house_id, **response.json(), **notification})


@frontend_router.post('/edit/{house_id}')
async def edit_send_to_api(request: Request, house_id: int, AddressNumber: int = Form(...), StreetName: str = Form(...), Respond: str = Form(...), Size: str = Form(...), SecurityGateOrAlarm: str = Form(...), Dog: str = Form(...), Age: Optional[str] = Form(None), Gender: Optional[str] = Form(None), Price: Optional[float] = Form(0)):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    notification = {}
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        async with httpx.AsyncClient() as client:
            response_original_house = await client.get(f'{api_url}/api/house/{house_id}', headers=headers)
            if not response_original_house.status_code == 200:
                notification['error'] = response_original_house.json()['detail']
            form_dict = {"AddressNumber": AddressNumber,
                         "StreetName": StreetName,
                         "Respond": Respond == "Yes",
                         "Size": Size,
                         "SecurityGateOrAlarm": SecurityGateOrAlarm == "Yes",
                         "Dog": Dog,
                         "Age": Age,
                         "Gender": Gender,
                         "Price": Price * int(Respond=='Yes')}
            diff = {'id': response_original_house.json()['id']}
            for key, value in form_dict.items():
                if value != response_original_house.json()[key]:
                    diff[key] = value
            if len(diff) > 1:
                response = await client.patch(f'{api_url}/api/house/edit', headers=headers, json=diff)
                if not response.status_code == 200:
                    try:
                        notification['error'] = response.json()['detail']
                    except:
                        notification['error'] = "Il s'est produit une erreur."
                    return templates.TemplateResponse('update_form.html', {'request': request, 'house_id': house_id, **response_original_house.json(), **notification})
    else:
        return RedirectResponse(url='/landing-page')
    return RedirectResponse(url='/', status_code=303)


@frontend_router.get('/delete/{house_id}', name='delete')
async def delete_house(request: Request, house_id: int):
    #  ------------------Ce code permet de vérifier si la session est active------------------
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}',
                   'Content-Type': 'application/json'}
        async with httpx.AsyncClient() as client:
            response = await client.request('DELETE', f'{api_url}/api/house/delete', headers=headers, json={'id': house_id})
            if response.status_code == 401:
                return RedirectResponse(url='/login')
    else:
        return RedirectResponse(url='/landing-page')
    #  ----------------------------------------------------------------------------------------------
    return RedirectResponse(url='/', status_code=303)


@frontend_router.get('/logout', name='logout')
async def delete_session_cookies(request: Request):
    request.cookies.clear()
    redirect_response = RedirectResponse('/landing-page', status_code=303)
    redirect_response.delete_cookie(key='fakesession')
    return redirect_response


@frontend_router.get('/login', name='login', response_class=HTMLResponse)
async def login_html_page(request: Request):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_url}/api/auth/me', headers=headers)
            if response.status_code == 200:
                return RedirectResponse(url='/')
    return templates.TemplateResponse("login_form.html", {"request": request})


@frontend_router.post('/login', response_class=HTMLResponse)
async def login_post_form(request: Request, username: str = Form(...), password: str = Form(...)):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    headers = {'accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'password',
            'username': username,
            'password': password,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'}
    notification = {}
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{api_url}/api/auth/get_user_token', headers=headers, data=data)
        if not response.status_code == 200:
            try:
                notification['error'] = response.json()['detail']
            except:
                notification['error'] = "Il s'est produit une erreur."
        else:
            index_redirect_for = RedirectResponse('/', status_code=303)
            index_redirect_for.set_cookie(key='fakesession', value=response.json()['access_token'])
            return index_redirect_for
    return templates.TemplateResponse("login_form.html", {"request": request, **notification})


@frontend_router.get('/sign-up', name='sign-up', response_class=HTMLResponse)
async def sign_up_html(request: Request):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    bearer_access_token = request.cookies.get('fakesession')
    if bearer_access_token:
        headers = {'accept': 'application/json',
                   'Authorization': f'Bearer {bearer_access_token}'}
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_url}/api/auth/me', headers=headers)
            if response.status_code == 200:
                return RedirectResponse(url='/')
    return templates.TemplateResponse('signup_form.html', {'request': request})


@frontend_router.post('/sign-up', response_class=HTMLResponse)
async def sign_up_post_form(request: Request, username: str = Form(...), password: str = Form(...)):
    api_url = str(request.base_url).rstrip('/') if not api_env_url else api_env_url
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    data = {'username': username,
            'password': password}
    notification = {}
    async with httpx.AsyncClient() as client:
        response = await client.post(f'{api_url}/api/auth/create_user', headers=headers, json=data)
        if not response.status_code == 200:
            try:
                notification['error'] = response.json()['detail']
            except:
                notification['error'] = "Il s'est produit une erreur."
        else:
            async with httpx.AsyncClient() as client:
                headers = {'accept': 'application/json',
                           'Content-Type': 'application/x-www-form-urlencoded'}
    
                data = {'grant_type': 'password',
                        'username': username,
                        'password': password,
                        'scope': '',
                        'client_id': 'string',
                        'client_secret': 'string'}
                response = await client.post(f'{api_url}/api/auth/get_user_token', headers=headers, data=data)
                if not response.status_code == 200:
                    try:
                        notification['error'] = response.json()['detail']
                    except:
                        notification['error'] = "Il s'est produit une erreur."
                else:
                    response_page = RedirectResponse('/', status_code=303)
                    response_page.set_cookie('fakesession', value=response.json()['access_token'])
                    return response_page
    return templates.TemplateResponse('signup_form.html', {'request': request, **notification})


@frontend_router.get('/landing-page', name='landing-page')
async def landing_page(request: Request):
    return templates.TemplateResponse('welcome.html', {'request': request})