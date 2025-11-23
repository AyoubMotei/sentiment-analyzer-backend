# Sentiment Analyzer Backend

Ce dépôt contient le backend de l'application d'analyse de sentiment. Il est construit avec FastAPI pour offrir des performances élevées et une API moderne, avec une gestion de l'authentification par jeton JWT et un service d'analyse de sentiment basé sur l'API Hugging Face Inference.

## Table des Matières

- [Architecture du Projet](#architecture-du-projet)
- [Technologies Utilisées](#technologies-utilisées)
- [Configuration de l'Environnement](#configuration-de-lenvironnement)
- [Lancement du Projet](#lancement-du-projet)
- [Endpoints de l'API](#endpoints-de-lapi)
- [Détails de l'Implémentation](#détails-de-limplémentation)
- [Tests](#tests)
- [Lien vers le Frontend](#lien-vers-le-frontend)

## Architecture du Projet

Le projet suit une structure modulaire pour séparer clairement les responsabilités (Authentication, Services AI, API principale).

```
sentiment-analyzer-backend/
├── app/
│   ├── auth.py         # Logique JWT (Création/Vérification de Token) et BDD utilisateurs
│   ├── main.py         # Application FastAPI principale, définition des routes et CORS
│   └── services/
│       └── ai_service.py # Service d'IA pour l'analyse de sentiment (Hugging Face)
├── tests/
│   ├── test_auth.py    # Tests unitaires pour l'authentification (avec TestClient)
│   └── test_api.py     # Tests d'intégration de l'API (authentification et prédiction)
├── .env        # Fichier pour les variables d'environnement
└── requirements.txt    # Dépendances Python
```

## Technologies Utilisées

- **FastAPI**: Framework web Python moderne pour la construction rapide d'API
- **Pydantic**: Utilisé pour la validation des données d'entrée (schémas de requête)
- **JWT (python-jose)**: Pour la création et la vérification des tokens d'authentification
- **Hugging Face InferenceClient**: Pour interagir avec le modèle d'analyse de sentiment (`nlptown/bert-base-multilingual-uncased-sentiment`)
- **Pytest**: Framework de test

## Configuration de l'Environnement

Le backend utilise des variables d'environnement pour sécuriser et configurer les services externes.

### Fichier .env

Vous devez créer un fichier nommé `.env` à la racine du projet et le remplir avec les clés suivantes :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `HF_API_KEY` | Clé d'API (Token) pour le service Hugging Face Inference | `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `JWT_SECRET` | Chaîne secrète utilisée pour signer les tokens JWT. DOIT être complexe et conservée secrète | `mon_secret_ultra_securise_123` |
| `ALGORITHM` | Algorithme de hachage pour JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée de validité des tokens en minutes | `60` |

## Lancement du Projet

### 1. Installation des dépendances

```bash
# Créez et activez un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Sous Linux/macOS
# ou
.\venv\Scripts\activate   # Sous Windows

# Installez les dépendances
pip install -r requirements.txt
```

### 2. Démarrage du Serveur

Lancez le serveur Uvicorn depuis la racine du projet :

```bash
uvicorn app.main:app --reload
```

Le serveur sera accessible à l'adresse `http://127.0.0.1:8000`. La documentation Swagger UI est disponible sur `http://127.0.0.1:8000/docs`.

## Endpoints de l'API

### 1. Endpoint Racine 

| Méthode | Chemin | Description |
|---------|--------|-------------|
| GET | `/` | Vérifie que l'API est en ligne |

### 2. Authentification 

| Méthode | Chemin | Description | Schéma de Requête |
|---------|--------|-------------|-------------------|
| POST | `/login` | Authentifie un utilisateur et retourne un token JWT | `{ "username": "user", "password": "password" }` |

**Utilisateurs de Test** (stockés dans `app/auth.py`) :
- `admin` / `admin123`
- `user` / `password`

### 3. Prédiction (Sécurisé)

| Méthode | Chemin | Description | Headers Requis | Schéma de Requête |
|---------|--------|-------------|----------------|-------------------|
| POST | `/predict` | Effectue l'analyse de sentiment sur un texte. Requiert un token JWT | `Authorization: Bearer <token>` | `{ "text": "Un texte à analyser" }` |

**Exemple de Réponse de `/predict` :**

```json
{
  "text": "J'aime beaucoup ce produit.",
  "score": 5,
  "sentiment": "positif",
  "user": "user"
}
```

## Détails de l'Implémentation

### app/auth.py

Ce module gère le cycle de vie du JWT :

- `create_access_token(username)`: Crée un JWT encodé avec le nom d'utilisateur (`sub`) et une date d'expiration (`exp`)
- `login(username, password)`: Vérifie les identifiants par rapport à une base de données interne (`USERS_DB`) et génère un token
- `verify_token(token)`: Fonction de dépendance FastAPI (`Depends`) qui décode le token, vérifie sa validité et son expiration. Elle lève une `HTTPException(401)` en cas d'échec

### app/services/ai_service.py

Ce service est le cœur de l'analyse :

- Il utilise la classe `huggingface_hub.InferenceClient` pour communiquer avec le modèle `nlptown/bert-base-multilingual-uncased-sentiment`
- Le modèle retourne une classification en étoiles (1 à 5). La logique Python traduit ces étoiles en catégories :
  - **1 ou 2 étoiles** : négatif
  - **3 étoiles** : neutre
  - **4 ou 5 étoiles** : positif
- Il gère également des erreurs spécifiques (clé API non configurée, modèle en chargement, clé invalide) pour fournir des messages d'erreur clairs

### app/main.py

Le fichier principal configure :

- **CORS**: Permet les requêtes depuis l'URL de développement du frontend (`http://localhost:3000`)
- **Endpoints**: Associe les chemins URL aux fonctions d'application
- **Sécurité**: L'endpoint `/predict` utilise `token: dict = Depends(verify_token)` pour s'assurer que l'utilisateur est authentifié avant d'appeler le service d'IA

## Tests

La suite de tests est essentielle pour garantir le bon fonctionnement des composants.

### Exécution des Tests

#### Tests unitaires

```bash
# Pour les tests unitaires (test_auth.py) :
pytest tests/test_auth.py
```

#### Tests d'intégration

```bash
# Les tests d'intégration nécessitent que le serveur soit lancé
# Assurez-vous que le serveur tourne sur http://127.0.0.1:8000

# Dans un terminal, lancez le serveur :
uvicorn app.main:app --reload

# Dans un autre terminal, lancez les tests d'intégration :
python tests/test_api.py
```

### Fichier tests/test_auth.py

Ce fichier contient des tests unitaires rapides utilisant le `TestClient` de FastAPI pour vérifier que :

- `test_login_success`: Un utilisateur valide reçoit un statut 200 et un `access_token`
- `test_login_failure`: Un utilisateur invalide reçoit un statut 401 (Unauthorized)

### Fichier tests/test_api.py

Ce fichier contient des tests d'intégration qui vérifient le fonctionnement complet de l'API :

- **Test Login** : Authentification d'un utilisateur et récupération du token JWT
- **Test Predict** : Analyse de sentiment sur un texte en utilisant le token d'authentification

Le script teste le flux complet : connexion → obtention du token → prédiction sécurisée.

## Lien vers le Frontend

https://github.com/AyoubMotei/sentiment-analyzer-frontend.git

