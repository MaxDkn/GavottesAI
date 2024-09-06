from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.auth import auth_router
from backend.crud import crud_router
from backend.frontend import frontend_router
from backend.ai import ai_router


"""ToDo
[+] Traduire les pages de connection en français.
[+] Mettre l'icone sur le site web.
[+] Changer l'affichage quand pas de tables.
[-] Faire une page de présentation du projet.
[-] Faire une login-page jolie.
[+] Auto Suggestion pour nouvelle maison.

[-] Mettre à jour le github + photos
[-] Nom - Prénom - Classe

[-] IA
[-] Carte interactive
"""


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(auth_router, prefix="/api/auth", tags=['auth'])
app.include_router(crud_router, prefix="/api/house", tags=['house'])
app.include_router(ai_router, prefix="/api/ai", tags=['ai'])
app.include_router(frontend_router, prefix="", tags=['frontend'])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return StaticFiles(directory="static").lookup_path("images/favicon.ico")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code in {404, 405}:
        return RedirectResponse('landing-page', status_code=303)
        return PlainTextResponse("Hello World", status_code=exc.status_code)
    # Let other exceptions pass through the default handler
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
