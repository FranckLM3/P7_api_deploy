# Déployer l'API sur Cloud Run

Ce guide décrit comment builder et déployer cette API FastAPI sur Google Cloud Run.

## Prérequis
- Compte Google Cloud avec facturation activée sur le projet
- gcloud SDK installé (macOS: `brew install --cask google-cloud-sdk`)
- Docker installé (`brew install docker`)

## 1. Activer les APIs nécessaires
```bash
PROJECT_ID=openclassrooms-477011
gcloud config set project $PROJECT_ID

gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## 2. Build & Déploiement manuels
```bash
IMAGE=gcr.io/$PROJECT_ID/credit-score-api

# Build & push l'image via Cloud Build
gcloud builds submit --tag $IMAGE .

# Déployer sur Cloud Run (adapter la région)
REGION=europe-west1

gcloud run deploy credit-score-api \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

La commande de déploiement affichera l'URL publique du service.

## 3. Déploiement automatique via GitHub Actions
Créer un compte de service et ajouter sa clé JSON en secret GitHub.

```bash
# Créer le service account
SA=github-deploy
SA_EMAIL=$SA@$PROJECT_ID.iam.gserviceaccount.com

gcloud iam service-accounts create $SA --display-name "GitHub Deploy"

# Rôles (ajuster selon vos politiques)
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/run.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:$SA_EMAIL" --role="roles/cloudbuild.builds.builder"

# Créer la clé JSON (à copier dans GitHub Secret GCP_SA_KEY)
gcloud iam service-accounts keys create key.json --iam-account "$SA_EMAIL"
```

Secrets GitHub requis dans le repo:
- `GCP_PROJECT` = votre ID de projet
- `GCP_REGION` = ex: `europe-west1`
- `GCP_SA_KEY` = contenu du fichier `key.json`

Le workflow `.github/workflows/deploy-cloudrun.yml` se chargera de builder et déployer à chaque push sur `main`.

## 4. Configurer le Dashboard
Une fois l'URL Cloud Run obtenue, définir la variable d'environnement côté dashboard:
- `CREDIT_SCORE_API_URL=https://<votre-url-cloud-run>`

Le dashboard utilisera l'API Cloud Run par défaut et basculera sur le modèle local seulement si l'API est indisponible.
