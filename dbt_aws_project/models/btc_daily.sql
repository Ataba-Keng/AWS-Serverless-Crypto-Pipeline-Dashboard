{{ config(materialized='table') }}

SELECT
    -- 1. Conversion de la Date (String -> Date)
    CAST(SUBSTR("Date", 1, 10) AS DATE) as trade_date,
    
    -- 2. Renommage et typage propre
    CAST("Open" AS DECIMAL(10, 2)) as open_price,
    CAST("Close" AS DECIMAL(10, 2)) as close_price,
    CAST("Volume" AS BIGINT) as volume,
    
    -- 3. Petite métrique calculée (Variation journalière)
    CAST("Close" - "Open" AS DECIMAL(10, 2)) as daily_change

FROM {{ source('crypto_source', 'btc_raw') }}