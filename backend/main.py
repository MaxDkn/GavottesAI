from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.auth import auth_router
from backend.crud import crud_router
from backend.frontend import frontend_router


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
app.include_router(frontend_router, prefix="", tags=['frontend'])


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return StaticFiles(directory="static").lookup_path("images/favicon.ico")
