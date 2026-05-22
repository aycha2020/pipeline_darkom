import pandas as pd
from config.db_config import engine


def build_warehouse():

    print("=== WAREHOUSE STARTED ===")

   
    # LOAD FEATURES DATA

    query = """
    SELECT *
    FROM clean.darkom_features
    """

    df = pd.read_sql(query, engine)

    print("Rows loaded:", len(df))

   
    # 1. DIM LOCALISATION
  
    dim_localisation = (
        df[["ville", "quartier"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_localisation[
        "localisation_id"
    ] = (
        dim_localisation.index + 1
    )


    # 2. DIM BIEN
    
    dim_bien = (
        df[
            [
                "type_bien",
                "categorie_surface",
                "age_bien"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_bien["bien_id"] = (
        dim_bien.index + 1
    )

    
    # 3. DIM TRANSACTION
   
    dim_transaction = (
        df[["transaction"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_transaction[
        "transaction_id"
    ] = (
        dim_transaction.index + 1
    )

    
    # 4. DIM DATE
  
    dim_date = (
        df[
            [
                "date_publication",
                "annee_publication",
                "mois_publication",
                "trimestre_publication"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim_date["date_id"] = (
        dim_date.index + 1
    )

   
    # MERGE DIMENSIONS
  

    # localisation
    df = df.merge(
        dim_localisation,
        on=["ville", "quartier"],
        how="left"
    )

    # bien
    df = df.merge(
        dim_bien,
        on=[
            "type_bien",
            "categorie_surface",
            "age_bien"
        ],
        how="left"
    )

    # transaction
    df = df.merge(
        dim_transaction,
        on=["transaction"],
        how="left"
    )

    # date publication 
    df = df.merge(
        dim_date,
        on=[
            "date_publication",
            "annee_publication",
            "mois_publication",
            "trimestre_publication"
        ],
        how="left"
    )

  
    # création de fact_annonces

    fact_annonces = df[
        [
            "annonce_id",
            "prix",
            "surface",
            "prix_m2",
            "nb_chambres",
            "nb_salles_bain",
            "localisation_id",
            "bien_id",
            "transaction_id",
            "date_id"
        ]
    ]

   
    # CHARGEMENT DES TABLES DANS LE DATA WAREHOUSE
  

    dim_localisation.to_sql(
        "dim_localisation",
        schema="bi_schema",
        con=engine,
        if_exists="replace",
        index=False
    )

    dim_bien.to_sql(
        "dim_bien",
        schema="bi_schema",
        con=engine,
        if_exists="replace",
        index=False
    )

    dim_transaction.to_sql(
        "dim_transaction",
        schema="bi_schema",
        con=engine,
        if_exists="replace",
        index=False
    )

    dim_date.to_sql(
        "dim_date",
        schema="bi_schema",
        con=engine,
        if_exists="replace",
        index=False
    )

    fact_annonces.to_sql(
        "fact_annonces",
        schema="bi_schema",
        con=engine,
        if_exists="replace",
        index=False
    )

    print(" Data Warehouse Created")
    print("=== WAREHOUSE FINISHED ===")