import pandas as pd

def to_bool(val):
    """
    Retourne True si val n'est ni NaN, ni vide après strip(), ni égal à '0', 'NON' ou 'FALSE'.
    """
    if pd.isna(val):
        return False
    s = str(val).strip().upper()
    return s not in ["", "0", "NON", "FALSE"]

# Charger le fichier Excel (adapter le chemin si besoin)
df = pd.read_excel("Echantillon.xlsx", sheet_name="Feuil1", header=1)
df.columns = df.columns.str.strip()
df = df.fillna("")

# Sélection des colonnes de base
cols_basic = [
    "Ref", "Vrai Nom", "Adresse", "Arrondissement", "Téléphone",
    "Site web", "Lien Google", "Lien Menu", "Horaires",
    "Lien de réservation", "Lien de votre compte instagram",
    "Station(s) de métro à proximité"
]
basic = df[cols_basic].replace(r'^\s*$', "non_renseigné", regex=True)

# Renommer la colonne 'Ref' en 'tag'
basic.rename(columns={'Ref': 'tag'}, inplace=True)

# Types de restaurants
type_cols = [
    "Restaurant", "Restaurant haut de gamme", "Restaurant gastronomique",
    "Restaurant étoilé", "Brasserie", "Cave à manger",
    '"Fast" (à emporter, sandwicherie...)', "Boulangerie/pâtisserie",
    "Concept brunch", "Concept goûter", "Coffee shop/salon de thé", "Bar"
]
basic["types"] = df[type_cols].apply(
    lambda row: ";".join([col for col in type_cols if row[col].strip() != ""]),
    axis=1
)

# Moments de la journée
basic["petit_dejeuner"] = df["Petit-déjeuner"].apply(to_bool)
basic["brunch_general"] = df["Brunch"].apply(to_bool)
basic["brunch_samedi"] = df["Brunch le samedi"].apply(to_bool)
basic["brunch_dimanche"] = df["Brunch le dimanche"].apply(to_bool)
basic["brunch_toute_la_semaine"] = basic.apply(
    lambda r: r["brunch_general"] and not r["brunch_samedi"] and not r["brunch_dimanche"],
    axis=1
)
for col, name in [
    ("Déjeuner", "dejeuner"), ("Goûter", "gouter"),
    ("Drinks", "drinks"), ("Dîner", "diner"), ("Apéro", "apero")
]:
    basic[name] = df[col].apply(to_bool)

# Lieux
basic["dans_la_rue"] = df["Dans la rue"].apply(to_bool)
basic["dans_une_galerie"] = df["Dans une galerie"].apply(to_bool)
basic["dans_un_musee"] = df["Dans un musée"].apply(to_bool)
basic["dans_un_monument"] = df["Dans un monument"].apply(to_bool)
basic["hotel_name"] = df["Dans un hôtel"].str.strip()
basic["dans_un_hotel"] = basic["hotel_name"] != ""
basic["other_lieu"] = df["Other"].apply(to_bool)

# Ambiance
basic["ambiance_classique"] = df["Classique"].apply(to_bool)
basic["ambiance_intimiste"] = df["Intimiste/tamisé"].apply(to_bool)
basic["ambiance_festif"] = df["Festif"].apply(to_bool)
basic["ambiance_date"] = df["Date"].apply(to_bool)

# Tranche de prix
price_cols = ["€", "€€", "€€€", "€€€€"]
basic["price_range"] = df.apply(
    lambda r: next((col for col in price_cols if to_bool(r[col])), ""),
    axis=1
)

# Cuisine
cuisine_cols = [
    "Africain", "Américain", "Chinois", "Coréen", "Français", "Grec",
    "Indien", "Israélien", "Italien", "Japonais", "Libanais", "Mexicain",
    "Oriental", "Péruvien", "Sud-Américain", "Thaï", "Vietnamien", "Other"
]
basic["cuisines"] = df[cuisine_cols].apply(
    lambda row: ";".join([col for col in cuisine_cols if row[col].strip() != ""]),
    axis=1
)

# Restrictions alimentaires
restriction_cols = [
    "Casher (certifié)", "Casher friendly (tout est casher mais pas de teouda)",
    "Viande casher", "Végétarien", "Vegan"
]
basic["restrictions"] = df[restriction_cols].apply(
    lambda row: ";".join([col for col in restriction_cols if row[col].strip() != ""]),
    axis=1
)

# Terrasse
basic["has_terrace"] = df["OUI/NON"].apply(to_bool)
basic["terrace_locs"] = df.apply(
    lambda r: ";".join(
        loc for loc, col in [
            ("terrasse_classique", "Terrasse classique"),
            ("cour", "Cour"),
            ("rooftop", "Rooftop")
        ] if to_bool(r[col])
    ),
    axis=1
)

# More info
info_col = "Avez-vous d'autres précisions à nous apporter sur votre établissement ?"
basic["more_info"] = df[info_col].str.strip()

# Sauvegarde CSV final
output = "all_restaurants_data.csv"
basic.to_csv(output, index=False, encoding="utf-8-sig")
print(f"Fichier '{output}' créé : {basic.shape[0]} lignes, {basic.shape[1]} colonnes.")
