import os 
import tkinter as tk
from tkinter import filedialog

class SerieManager:
    """Classe qui gère les interactions avec les dossiers de séries"""
    
    def __init__(self):
        """Je crée une nouvelle instance pour gérer une série TV"""
        self.serie_path = None  # Chemin du dossier sélectionné
    
    def select_directory(self) -> bool:
        """J'ouvre une fenêtre pour choisir le dossier de la série.
        
        Returns:
            bool: True si un dossier a été sélectionné, False sinon
        """
        root = tk.Tk()
        root.withdraw()  # Je cache la fenêtre principale Tkinter
        self.serie_path = filedialog.askdirectory(title="Sélectionnez le dossier de la série")
        
        if self.serie_path:
            print(f"Répertoire sélectionné : {self.serie_path}")
            return True
        return False

    def get_season_folders(self) -> tuple:
        """Je récupère la liste des dossiers de saisons dans un ordre trié.
        
        Returns:
            tuple: Liste triée des noms de dossiers de saisons
        
        Raises:
            ValueError: Si aucun dossier n'est sélectionné
        """
        if not self.serie_path:
            raise ValueError("Aucun dossier sélectionné")
            
        season_folders = []
        
        for item in os.listdir(self.serie_path):
            full_path = os.path.join(self.serie_path, item)
            if os.path.isdir(full_path) and item.startswith(('Saison', 'S')):
                season_folders.append(item)
        
        return tuple(sorted(season_folders))
    
    def get_total_episodes(self) -> int:
        """Je compte le nombre total d'épisodes dans toutes les saisons.
        
        Returns:
            int: Nombre total d'épisodes
        
        Raises:
            ValueError: Si aucun dossier n'est sélectionné
        """
        if not self.serie_path:
            raise ValueError("Aucun dossier sélectionné")

        return sum(
            count for count in self.get_count_episodes_bySeason().values()
        )
    
    def get_count_episodes_bySeason(self) -> dict:
        """Je compte le nombre d'épisodes dans chaque saison.
        
        Returns:
            dict: Dictionnaire avec les saisons comme clés et le nombre d'épisodes comme valeurs
        
        Raises:
            ValueError: Si aucun dossier n'est sélectionné
        """
        if not self.serie_path:
            raise ValueError("Aucun dossier sélectionné")

        episodes_count = {}
        seasons = self.get_season_folders()
        
        for season in seasons:
            season_path = os.path.join(self.serie_path, season)
            # Compte uniquement les fichiers (pas les dossiers)
            episodes = [item for item in os.listdir(season_path) 
                       if os.path.isfile(os.path.join(season_path, item))]
            episodes_count[season] = len(episodes)
            
        return episodes_count
    
    def get_serie_path(self) -> str:
        """Je renvoie le chemin du dossier série sélectionné.
        
        Returns:
            str: Chemin du dossier ou None si aucun dossier n'est sélectionné
        """
        return self.serie_path
    
    def get_serie_name(self) -> str:
        """Je renvoie le nom de la série sélectionnée.
        
        Returns:
            str: Nom de la série
        
        Raises:
            ValueError: Si aucun dossier n'est sélectionné
        """
        if not self.serie_path:
            raise ValueError("Aucun dossier sélectionné")
        return os.path.basename(self.serie_path)