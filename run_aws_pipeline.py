import os
import time

def run_step(step_name, command):
    print(f"\n🚀 [AWS] Lancement de : {step_name}...")
    start = time.time()
    exit_code = os.system(command)
    duration = round(time.time() - start, 2)
    
    if exit_code != 0:
        print(f"❌ ÉCHEC de {step_name} !")
        exit(1)
    print(f"✅ {step_name} terminé en {duration}s")

if __name__ == "__main__":
    print("☁️  DÉMARRAGE DU PIPELINE AWS SERVERLESS")
    
    # 1. Ingestion (Python -> S3)
    run_step("Ingestion vers S3", "python extract_to_s3.py")
    
    # 2. Transformation (dbt + Athena)
    # On précise le dossier et le profil local
    run_step("Transformation dbt (Athena)", "cd dbt_aws_project && dbt run --profiles-dir .")
    
    print("\n✨ PIPELINE CLOUD TERMINÉ ✨")