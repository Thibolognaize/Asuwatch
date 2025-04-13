import sqlite3
import os

class Database:
    def __init__(self, serie_name, seasons_tuple):
        """Je crée/connecte la base de données SQLite
        
        Args:
            serie_name (str): Nom de la série
            seasons_tuple (tuple): Tuple contenant les noms des saisons
        """
        self.serie_name = serie_name.replace(" ", "_")
        self.seasons = seasons_tuple
        
        # Création du dossier data
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # Connexion à la BDD
        self.db_path = os.path.join(data_dir, f"{self.serie_name}.db")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Création des tables pour chaque saison
        self.create_all_seasons()

    def create_all_seasons(self):
        """Je crée une table pour chaque saison trouvée"""
        try:
            for season in self.seasons:
                # Extrait le numéro de la saison (ex: 'Saison1' -> '1', 'S03' -> '03')
                if season.startswith('Saison'):
                    season_num = season[6:]
                else:  # Format 'S03'
                    season_num = season[1:]
                
                table_name = f"season_{season_num}"
                self.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        episode_number TEXT NOT NULL,
                        watched BOOLEAN DEFAULT 0,
                        watch_date TEXT DEFAULT NULL
                    )
                """)
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables : {e}")
            return False

    def insert_episodes_from_serie_manager(self, serie_manager):

        
        """J'insère tous les épisodes pour chaque saison en utilisant les données de SerieManager
        
        Args:
            serie_manager (SerieManager): Instance de SerieManager contenant les informations sur la série
        """
        try:
            episodes_count = serie_manager.get_count_episodes_bySeason()

            for season, nb_episodes in episodes_count.items():
                #Extrait le numéro de la saison
                if season.startswith('Saison'):
                    season_num = season[6:]
                else:  # Format 'S03'
                    season_num = season[1:]
                
                table_name = f"season_{season_num}"

                # Insert les épisodes avec leur numéro
                for episode_num in range(1, nb_episodes + 1):
                    # Format l'ID et le numéro d'épisode (ex: E01, E02, etc.)
                    episode_str = f"E{episode_num:02d}"
                    
                    self.cursor.execute(f"""
                        INSERT OR IGNORE INTO {table_name} (id, episode_number)
                        VALUES (?, ?)
                    """, (episode_num, episode_str))

                self.conn.commit()
                print(f"Succès ! Insertion d'épisode => {season} !")

        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion des épisodes: {e}")
        except Exception as e:
            print(f"Une erreur inattendue est survenue : {e}")

    def mark_as_watched(self, season_num: str, episode_id: int) -> bool:
        """Marque un épisode comme regardé avec une requête préparée

        Args:
            season_num (str): Numéro de la saison (ex: "01" pour saison 1)
            episode_id (int): ID de l'épisode

        Returns:
            bool: True si succès, False en cas d'erreur
        """
        query = "UPDATE season_{} SET watched = 1 WHERE id = ?".format(season_num)
        
        try:
            self.cursor.execute(query, (episode_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors du marquage comme vu : {e}")
            return False
    

    def close(self):
        """Je ferme la connexion"""
        self.conn.close()