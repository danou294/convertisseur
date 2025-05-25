import os
from google.cloud import storage
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

# -----------------------
# CONFIGURATION
# -----------------------

KEY_PATH = "./service_account.json"
USE_EXPLICIT_CREDENTIALS = True

# Votre bucket Firebase Storage exact
BUCKET_NAME = "butter-vdef.firebasestorage.app"

# -----------------------
# FONCTIONS
# -----------------------

def get_storage_client():
    if USE_EXPLICIT_CREDENTIALS:
        creds = service_account.Credentials.from_service_account_file(KEY_PATH)
        print(f"[LOG] Chargé credentials depuis {KEY_PATH}, project_id={creds.project_id}")
        return storage.Client(credentials=creds, project=creds.project_id)
    else:
        print("[LOG] Utilisation de GOOGLE_APPLICATION_CREDENTIALS")
        return storage.Client()

def list_all_blobs(bucket_name: str, client: storage.Client) -> list[str]:
    bucket = client.bucket(bucket_name)
    print(f"[LOG] Tentative de listing complet du bucket '{bucket_name}'…")
    try:
        names = [blob.name for blob in bucket.list_blobs()]
        print(f"[LOG] Nombre total de blobs récupérés sans delimiter: {len(names)}")
        print("[LOG] Extrait – premiers 10 blobs :")
        for n in names[:10]:
            print("   •", n)
        return names
    except Exception as e:
        print(f"[ERROR] Échec listing complet : {e}")
        return []

def list_top_level_dirs(bucket_name: str, client: storage.Client) -> list[str]:
    bucket = client.bucket(bucket_name)
    print(f"[LOG] Tentative de listing avec delimiter='/' pour obtenir les dossiers…")
    try:
        iterator = bucket.list_blobs(prefix="", delimiter="/")
        dirs = sorted(iterator.prefixes)
        print(f"[LOG] Préfixes retournés par iterator.prefixes ({len(dirs)}) :")
        for d in dirs:
            print("   •", d)
        return dirs
    except Exception as e:
        print(f"[ERROR] Échec listing avec delimiter : {e}")
        return []

# -----------------------
# SCRIPT PRINCIPAL
# -----------------------

def main():
    # 1) Initialisation client
    client = get_storage_client()

    # 2) Listing complet
    all_blobs = list_all_blobs(BUCKET_NAME, client)

    # 3) Listing “dossiers”
    dirs = list_top_level_dirs(BUCKET_NAME, client)

    # 4) Synthèse
    if not dirs:
        print("\n❗ AUCUN sous-répertoire détecté à la racine du bucket.")
    else:
        print(f"\n📂 Répertoires détectés à la racine :")
        for d in dirs:
            print(" •", d)

if __name__ == "__main__":
    main()
