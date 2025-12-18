{{ config(materialized='table') }}

-- Pour qu'Athena lise le CSV brut, on doit souvent définir une "external table" d'abord
-- Mais dbt-athena gère ça intelligemment.

SELECT 
    Date,
    Open,
    High,
    Low,
    "Close" as Close_Price, -- Close est un mot réservé SQL, on le quote
    Volume
FROM {{ source('raw_data', 'btc_history') }}
-- Ici, tu devras configurer un fichier sources.yml pour pointer vers ton S3