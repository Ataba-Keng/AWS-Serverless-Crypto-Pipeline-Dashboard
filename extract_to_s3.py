import boto3
import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from io import StringIO
from  dotenv import load_dotenv 

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION = os.getenv("REGION")

def main():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION
    )

    print("extraction des donnees BTC..")
    btc = yf.Ticker("BTC-USD")
    df = btc.history(period="1d")
    df.reset_index(inplace=True)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    date_str = datetime.now().strftime("%Y-%m-%d")
    file_key = f"raw/btc/{date_str}.csv"
    
    print("envoi vers S3 : s3://{BUCKET_NAME}/{file_key}")
    s3_client.put_object(
        Bucket = BUCKET_NAME,
        Key = file_key,
        Body = csv_buffer.getvalue()
    )

    print("extraction terminee.")

if __name__ == "__main__":
    main()

