import os
import re

class MediaManager:
    def __init__(self):
        """
        Initialise une nouvelle instance de MediaManager.
        """
        self.media_path = None

    def select_directory(self):
        """
        Permet à l'utilisateur de sélectionner le répertoire contenant les médias.

        Returns:
            bool: True si un répertoire valide est sélectionné, False sinon.
        """
        self.media_path = input("Entrez le chemin du répertoire des médias : ")
        return os.path.isdir(self.media_path)

    def get_media_info(self):
        """
        Extrait les informations sur les médias à partir du répertoire sélectionné.

        Returns:
            list: Une liste de dictionnaires contenant des informations sur chaque média.

        Raises:
            ValueError: Si aucun répertoire n'est sélectionné.
        """
        if not self.media_path:
            raise ValueError("Aucun répertoire sélectionné")

        media_info = []
        for item in os.listdir(self.media_path):
            item_path = os.path.join(self.media_path, item)
            if os.path.isdir(item_path):
                media_type = self.determine_media_type(item)
                media_info.append({
                    "type": media_type,
                    "title": item,
                    "path": item_path,
                    "seasons": self.get_season_folders(item_path) if media_type in ["Serie", "Anime"] else []
                })
        return media_info

    def determine_media_type(self, folder_name):
        """
        Détermine le type de média en fonction du nom du dossier.

        Args:
            folder_name (str): Le nom du dossier.

        Returns:
            str: Le type de média ('Film', 'Serie', 'Anime', ou 'Unknown').
        """
        if "film" in folder_name.lower():
            return "Film"
        elif "serie" in folder_name.lower():
            return "Serie"
        elif "anime" in folder_name.lower():
            return "Anime"
        return "Unknown"

    def get_season_folders(self, path):
        """
        Récupère la liste des dossiers de saisons dans le répertoire donné.

        Args:
            path (str): Le chemin du répertoire à analyser.

        Returns:
            list: Une liste des noms de dossiers de saisons.
        """
        season_folders = [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
        return season_folders

    def get_episodes_in_season(self, season_path):
        """
        Récupère la liste des épisodes dans un dossier de saison.

        Args:
            season_path (str): Le chemin du dossier de la saison.

        Returns:
            list: Une liste des noms de fichiers d'épisodes.
        """
        episodes = [item for item in os.listdir(season_path) if os.path.isfile(os.path.join(season_path, item))]
        return episodes

    def extract_season_number(self, season_name):
        """
        Extrait le numéro de la saison à partir du nom du dossier de la saison.

        Args:
            season_name (str): Le nom du dossier de la saison.

        Returns:
            int: Le numéro de la saison, ou None si aucun numéro n'est trouvé.
        """
        match = re.search(r'(\d+)', season_name)
        if match:
            return int(match.group(1))
        return None
