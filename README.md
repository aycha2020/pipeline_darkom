Darkom.ma – Data Engineering & BI Project
     CONTEXTE

Ce projet consiste à concevoir un pipeline de données complet à partir de données brutes issues de la plateforme immobilière Darkom.ma.

L’objectif est de transformer un fichier CSV contenant des annonces immobilières en un système d’analyse décisionnelle basé sur un Data Warehouse et des dashboards Power BI.

 Objectif du projet
Transformer des données brutes en données exploitables
Construire un Data Warehouse structuré
Préparer les données pour l’analyse BI
Créer des dashboards interactifs pour l’aide à la décision
 Architecture du projet

Le pipeline suit une architecture standard :

CSV → Staging → Clean Data → Data Warehouse → Power BI

⚙️ Technologies utilisées
PostgreSQL
Python (Pandas)
Power BI
Power Query
DAX
CSV
 Étapes du projet
1. Staging

Chargement des données brutes dans une base PostgreSQL sans transformation.

2. Cleaning
Suppression des doublons
Gestion des valeurs manquantes
Correction des types de données
Traitement des valeurs aberrantes
Standardisation des données
3. Feature Engineering
Prix par m²
Âge du bien
Catégories de prix et de surface
Variables temporelles (année, mois, trimestre)
4. Data Warehouse
Modélisation en étoile (Star Schema)
Création des tables de faits et dimensions
Optimisation pour l’analyse BI
5. Power BI
Connexion à PostgreSQL
Création de mesures DAX
Construction de dashboards interactifs
 Dashboards réalisés
Vue globale du marché immobilier
Analyse des prix
Analyse géographique
Analyse des tendances
 Résultat final

Un système complet permettant d’analyser le marché immobilier marocain à travers des visualisations dynamiques et des indicateurs métiers.
