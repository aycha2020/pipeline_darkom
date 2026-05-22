import pandas as pd
from config.db_config import engine


def feature_engineering():

    print("=== FEATURE ENGINEERING STARTED ===")

   
    # lecture des données nettoyées depuis la table clean.darkom_clean dans un DataFrame pandas
   
    query = """
    SELECT *
    FROM clean.darkom_clean
    """

    df = pd.read_sql(query, engine)

    print("Rows loaded:", len(df))

    
    # 1. PRIX AU M2 - création d'une nouvelle variable de prix au mètre carré

    df["prix_m2"] = (
        df["prix"] / df["surface"]
    )

   
    # 2. AGE DU BIEN - calcul de l'âge du bien à partir de l'année de construction et de l'année en cours
    
    current_year = (
        pd.Timestamp.today().year
    )

    df["age_bien"] = (
        current_year
        - df["annee_construction"]
    )

    # 3. CATEGORIE PRIX - classification des biens en catégories de prix basées sur des seuils métier simples
    
    def categorie_prix(prix):

        if prix < 500000:
            return "Economique"

        elif prix < 1500000:
            return "Moyen"

        elif prix < 3000000:
            return "Haut Standing"

        else:
            return "Luxe"

    df["categorie_prix"] = (
        df["prix"]
        .apply(categorie_prix)
    )

   
    # 4. CATEGORIE SURFACE - classification des biens en catégories de surface basées sur des seuils métier simples
    
    def categorie_surface(surface):

        if surface < 80:
            return "Petit"

        elif surface <= 150:
            return "Moyen"

        else:
            return "Grand"

    df["categorie_surface"] = (
        df["surface"]
        .apply(categorie_surface)
    )

    
    # 5. EXTRACTION DE CARACTERISTIQUES TEMPORALLES - extraction de l'année, du mois et du trimestre de publication à partir de la date de publication
   
    df["annee_publication"] = (
        df["date_publication"]
        .dt.year
    )

    df["mois_publication"] = (
        df["date_publication"]
        .dt.month
    )

    df["trimestre_publication"] = (
        df["date_publication"]
        .dt.quarter
    )

  
    # 6. enregistrement des données enrichies dans une nouvelle table clean.darkom_features dans la base de données PostgreSQL
    
    df.to_sql(
        name="darkom_features",
        schema="clean",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(
        "clean.darkom_features created"
    )

    print(
        "Final rows:",
        len(df)
    )

    print(
        "=== FEATURE ENGINEERING FINISHED ==="
    )