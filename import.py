import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Charger le CSV structuré
df = pd.read_csv("all_restaurants_data.csv")

# Chemin vers votre fichier de clé privée Firebase
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

# Connexion à Firestore
db = firestore.client()

# Nom de la collection Firestore
collection_name = "restaurants"

# 1. Supprimer tous les documents existants dans la collection
print(f"🗑️ Suppression de tous les documents dans la collection '{collection_name}'...")
docs = db.collection(collection_name).stream()
deleted = 0
for doc in docs:
    db.collection(collection_name).document(doc.id).delete()
    deleted += 1
print(f"→ {deleted} documents supprimés.")

# 2. Réimporter chaque ligne du CSV comme un document
print("⬆️ Réimportation des données depuis 'echantillons_structure.csv'...")
for _, row in df.iterrows():
    doc_id = row.get("id") or None  # Utilise l'ID du restaurant si disponible
    data = row.dropna().to_dict()   # Supprime les valeurs NaN
    if doc_id:
        db.collection(collection_name).document(str(doc_id)).set(data)
    else:
        db.collection(collection_name).add(data)

print("✅ Données importées avec succès dans Firestore.")