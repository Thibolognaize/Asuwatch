import os
import re
from models.media_manager import MediaManager
from models.database_manager import DatabaseManager
from views.main_view import MainView

class MainController:
    def __init__(self):
        """
        Initialise le contrôleur principal avec les gestionnaires de médias et de base de données.
        """
        self.media_manager = MediaManager()
        self.db_manager = DatabaseManager()
        self.view = MainView(self)

    def start(self):
        """
        Démarre l'application en affichant le menu principal.
        """
        self.view.show_main_menu()

    def select_media_directory(self):
        """
        Permet à l'utilisateur de sélectionner un dossier de médias.
        """
        if self.media_manager.select_directory():
            media_info = self.media_manager.get_media_info()
            for media in media_info:
                media_id = self.db_manager.insert_media(media['type'], media['title'], media['path'])

                # Traiter les films directement
                if media['type'] == "Film":
                    film_files = [f for f in os.listdir(media['path']) if f.endswith('.mkv')]
                    for film_file in film_files:
                        self.db_manager.insert_episode(media_id, None, film_file, is_film=True)

                # Traiter les séries et animes avec des saisons
                if media['seasons']:
                    for season in media['seasons']:
                        season_number = self.media_manager.extract_season_number(season)
                        if season_number is not None:
                            season_id = self.db_manager.insert_saison(media_id, season_number)
                            episodes = self.media_manager.get_episodes_in_season(os.path.join(media['path'], season))
                            for episode in episodes:
                                episode_number = self.extract_episode_number(episode)
                                if episode_number is not None:
                                    self.db_manager.insert_episode(media_id, season_id, episode_number)
            print("Médias importés avec succès!")
        else:
            print("Aucun dossier sélectionné.")

    def extract_episode_number(self, episode_name):
        """
        Extrait le numéro de l'épisode à partir du nom du fichier de l'épisode.

        Args:
            episode_name (str): Le nom du fichier de l'épisode.

        Returns:
            int: Le numéro de l'épisode, ou None si aucun numéro n'est trouvé.
        """
        match = re.search(r'(\d+)', episode_name)
        if match:
            return int(match.group(1))
        return None

    def display_media(self):
        """
        Affiche la liste des médias.
        """
        media_list = self.db_manager.get_all_media()
        self.view.display_media(media_list)

    def mark_episode_as_watched(self):
        """
        Marque un épisode comme vu.
        """
        episode_id = self.view.get_user_input("Entrez l'ID de l'épisode à marquer comme vu : ")
        watch_date = self.view.get_user_input("Entrez la date de visionnage (format AAAA-MM-JJ) : ")
        self.db_manager.mark_episode_as_watched(episode_id, watch_date)
        print("Épisode marqué comme vu.")
