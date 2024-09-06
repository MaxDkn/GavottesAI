# GavottesAI

## Présentation

GavottesAI est une application web créée pour un projet scolaire au lycée. Lors d'une vente de gavottes en porte-à-porte pour financer un voyage, je me suis demandé s'il serait possible de prédire les chances d'achat en fonction des caractéristiques de la maison du prospect. GavottesAI utilise ces critères pour estimer si un client potentiel achètera des gavottes.

## Détails du Projet

Le projet utilise FastAPI comme backend, fonctionnant entièrement en API. Une interface web basique est intégrée dans `backend/frontend.py`, utilisant Bootstrap et Jinja2 pour afficher les résultats de manière simple. Le projet est dockerisé pour faciliter le déploiement.

## Lancer l'Application

### Via Docker :
- Construire et démarrer le conteneur :
    ```bash
    docker-compose build
    docker-compose up
    ```

### Via Python :
- Installer les dépendances et démarrer l'application :
    ```bash
    pip install --no-cache-dir -r requirements.txt
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```
