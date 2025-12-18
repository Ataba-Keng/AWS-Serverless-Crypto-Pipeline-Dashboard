import streamlit as st
import awswrangler as wr
import pandas as pd
import os
import boto3
from dotenv import load_dotenv

# 1. Config de la page
st.set_page_config(page_title="Crypto Dashboard AWS", page_icon="📈")
st.title("💰 Suivi Bitcoin - Architecture Serverless")
st.markdown("Données ingérées via **S3**, transformées par **dbt** et requêtées via **Athena**.")

# 2. Chargement des secrets (.env)
load_dotenv()
AWS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET = os.getenv("AWS_SECRET_KEY")
REGION = os.getenv("REGION", "eu-north-1")

# On utilise le bucket de résultats pour qu'Athena stocke ses temp files
STAGING_BUCKET = f"s3://{os.getenv('BUCKET_NAME')}/athena-results/" 
# Note: Si tu as utilisé un bucket différent pour les résultats dans dbt, mets-le ici.
# Sinon, assure-toi juste que ce chemin existe.

# 3. Fonction pour récupérer la donnée (Mise en cache pour ne pas payer à chaque clic)
@st.cache_data(ttl=3600) # Cache les données pour 1 heure
def get_data():
    session = boto3.Session(
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
        region_name=REGION
    )
    
    # Requête SQL sur ta table dbt clean
    query = "SELECT * FROM analytics.btc_daily ORDER BY trade_date"
    
    try:
        df = wr.athena.read_sql_query(
            sql=query,
            database="crypto_db",
            boto3_session=session,
            s3_output=STAGING_BUCKET, # Athena a besoin d'un endroit pour écrire le résultat temporaire
            ctas_approach=False
        )
        return df
    except Exception as e:
        st.error(f"Erreur de connexion AWS : {e}")
        return pd.DataFrame()

# 4. Chargement
with st.spinner('Connexion à AWS Athena en cours...'):
    df = get_data()

if not df.empty:
    # 5. Affichage des KPIs (Dernier prix connu)
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Prix Fermeture (Close)", 
            value=f"${last_row['close_price']}", 
            delta=f"{last_row['daily_change']}"
        )
    with col2:
        st.metric(label="Volume", value=f"{last_row['volume']:,}")
    with col3:
        st.metric(label="Date", value=str(last_row['trade_date']))

    # 6. Graphique Interactif
    st.subheader("Evolution du prix")
    # Streamlit gère le graphique automatiquement
    st.line_chart(df, x="trade_date", y=["open_price", "close_price"])
    
    # 7. Affichage des données brutes (Optionnel)
    with st.expander("Voir les données tabulaires"):
        st.dataframe(df)

else:
    st.warning("Aucune donnée trouvée. Vérifie ton pipeline d'ingestion.")