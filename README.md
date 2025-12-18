# ☁️ AWS Serverless Crypto Pipeline & Dashboard

![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20Athena-232F3E?style=flat&logo=amazon-aws&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Athena-FF694B?style=flat&logo=dbt&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)

Ce projet est une démonstration d'une **Modern Data Stack 100% Serverless** sur AWS.
Il automatise l'extraction de données financières (Bitcoin), leur stockage, leur transformation et leur visualisation sans gérer aucun serveur (No-Ops).

## 🏗 Architecture

Le pipeline suit une logique ELT (Extract, Load, Transform) optimisée pour le Cloud :

1.  **Ingestion (Python) :** Script local extrayant les données boursières via API et les envoyant vers un **Data Lake S3**.
2.  **Storage (Amazon S3) :** Stockage durable et économique des fichiers CSV bruts.
3.  **Compute (Amazon Athena) :** Moteur de requête SQL distribué pour analyser les fichiers directement dans S3.
4.  **Transformation (dbt) :** Nettoyage, typage et enrichissement des données via SQL modulaire.
5.  **Visualisation (Streamlit) :** Dashboard interactif connecté à Athena pour le suivi en temps réel.

## 🛠 Tech Stack

* **Cloud Provider :** AWS (S3, Athena, IAM, Glue Catalog)
* **Orchestration :** Python Scripts
* **Transformation :** dbt (data build tool) avec l'adaptateur `dbt-athena-community`
* **App Web :** Streamlit + AWS Wrangler (`awswrangler`)

## 🚀 Installation & Démarrage

### 1. Pré-requis
* Un compte AWS actif.
* Un utilisateur IAM avec les droits `AmazonS3FullAccess` et `AmazonAthenaFullAccess`.
* Python 3.9+ installé.

### 2. Cloner le projet
```bash
git clone [https://github.com/votre-pseudo/aws-serverless-crypto.git](https://github.com/votre-pseudo/aws-serverless-crypto.git)
cd aws-serverless-crypto
```
### 3. Environnement Virtuel
```Bash

python3 -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configuration (.env)

Créez un fichier .env à la racine du projet avec vos identifiants AWS :
```Ini, TOML

AWS_ACCESS_KEY_ID=VOTRE_CLE_PUBLIQUE
AWS_SECRET_ACCESS_KEY=VOTRE_CLE_SECRETE
AWS_REGION=eu-west-3
S3_BUCKET_NAME=nom-de-votre-bucket-data-lake
```
## ▶️ Utilisation
### 1. Lancer le Pipeline Data (ETL)

Ce script lance l'ingestion vers S3 puis la transformation dbt sur Athena.
```Bash
python run_aws_pipeline.py
```
### 2. Lancer le Dashboard

Pour visualiser les résultats :
```Bash
streamlit run dashboard.py
```
## 📊 Transformations dbt

Le modèle btc_daily effectue :

    Parsing de la date (Format ISO).

    Typage strict (Decimal pour les prix).

    Calcul du KPI daily_change (Clôture - Ouverture).
