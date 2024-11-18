from serie_manager import SerieManager
from database import Database
import os

def run():
    """Point d'entrée principal du programme"""
    # Création du gestionnaire de séries
    serie = SerieManager()
    
    # Sélection du dossier
    if not serie.select_directory():
        print("Aucun dossier sélectionné. Fin du programme.")
        return
    
    try:
        # Récupération des infos 
        seasons = serie.get_season_folders()
        episodes = serie.get_total_episodes()
        serie_name = serie.get_serie_name()
        
        # Affichage des résultats
        print(f"\nDossier sélectionné : {serie.get_serie_path()}")
        print(f"\nSérie trouvée : {serie_name}")
        print(f"Saisons trouvées : {seasons}")
        print(f"Nombre de saisons : {len(seasons)}")
        print(f"Nombre d'épisodes : {episodes}")
        
        # Création de la base de données
        db = Database(serie_name, seasons)
        print(f"\nBase de données connectée: {db.db_path}")

        # Insertion des épisodes
        db.insert_episodes_from_serie_manager(serie)

        # Mark un épisode comme "vu"
        db.mark_as_watched("01", 1)
        
        # Fermeture propre de la connexion
        db.close()
        
    except ValueError as e:
        print(f"Erreur : {e}")
        return
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
        return
    
    print("\nConfiguration initiale terminée !")


if __name__ == "__main__":
    run()