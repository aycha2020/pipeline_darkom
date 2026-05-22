import pandas as pd
from config.db_config import engine


def clean_data():

    print(" CLEANING STARTED ")

    
    # lecture des données brutes depuis la table staging.darkom_raw dans un DataFrame pandas
 
    query = """
    SELECT *
    FROM staging.darkom_raw
    """

    df = pd.read_sql(query, engine)

    print("Rows before:", len(df))

   
    # SUPPRESSION DES DUPLICATS les doublons basés sur l'identifiant de l'annonce - annonce_id
  
    df = df.drop_duplicates(
        subset=["annonce_id"]
    )

  
    # CONVERTION DES TYPES des données - conversion des dates et des numériques, gestion des erreurs de conversion
   
    df["date_publication"] = pd.to_datetime(
        df["date_publication"],
        errors="coerce"
    )

    numeric_cols = [
        "prix",
        "surface",
        "nb_chambres",
        "nb_salles_bain",
        "etage",
        "annee_construction"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

  
    # values manquantes - imputation simple en fonction du type de variable et règles métier simples
  
    df["quartier"] = (
    df["quartier"]
    .fillna(df["quartier"].mode()[0])
)
    df["ville"] = (
        df["ville"]
        .fillna("Non spécifiée")
    )

    df["type_bien"] = (
        df["type_bien"]
        .fillna("Appartement")
    )

    df["transaction"] = (
        df["transaction"]
        .fillna("Vente")
    )

    df["nb_chambres"] = (
        df["nb_chambres"]
        .fillna(
            df["nb_chambres"].median()
        )
    )

    df["nb_salles_bain"] = (
        df["nb_salles_bain"]
        .fillna(
            df["nb_salles_bain"].median()
        )
    )

    df["etage"] = (
        df["etage"]
        .fillna(0)
    )

    df["annee_construction"] = (
        df["annee_construction"]
        .fillna(
            df[
                "annee_construction"
            ].median()
        )
    )

    
    # standardisation des textes les valeurs textuelles - nettoyage de base et mise en majuscule
  

    text_cols = [
        "ville",
        "quartier",
        "type_bien",
        "transaction"
    ]


    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    df["ville"] = (
        df["ville"].str.strip()
        .str.lower().replace("Casa", "casablanca")
    )

    
    # outliers - suppression des valeurs aberrantes basées sur des règles métier simples et des seuils raisonnables pour les prix, surfaces, etc.

    df = df[df["prix"] > 0]

    df = df[df["surface"] > 0]

    df = df[
        df["nb_chambres"] <= 20
    ]

    df = df[
        df["nb_salles_bain"] <= 15
    ]

    current_year = (
        pd.Timestamp.today().year
    )

    df = df[
        df["annee_construction"]
        <= current_year
    ]

   
    # enregistrement des données nettoyées dans la table clean.darkom_clean
    

    df.to_sql(
        name="darkom_clean",
        schema="clean",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        " clean.darkom_clean created"
    )

    print(
        "Rows after:",
        len(df)
    )

    print(
        "=== CLEANING FINISHED ==="
    )