import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name='asuwatch.db'):
        """
        Initialise la connexion à la base de données SQLite.

        Args:
            db_name (str): Le nom de la base de données. Par défaut, 'asuwatch.db'.
        """
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Crée les tables nécessaires pour stocker les informations sur les médias,
        saisons et épisodes si elles n'existent pas déjà.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                path TEXT NOT NULL
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Saison (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_id INTEGER NOT NULL,
                season_number INTEGER NOT NULL,
                FOREIGN KEY (media_id) REFERENCES Media (id)
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Episode (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_id INTEGER,
                saison_id INTEGER,
                episode_number INTEGER,
                is_film BOOLEAN DEFAULT 0,
                watched BOOLEAN DEFAULT 0,
                watch_date TEXT DEFAULT NULL,
                FOREIGN KEY (saison_id) REFERENCES Saison (id),
                FOREIGN KEY (media_id) REFERENCES Media (id)
            )
            """
        )
        self.conn.commit()

    def insert_media(self, media_type, title, path):
        """
        Insère un nouvel enregistrement de média dans la table Media.

        Args:
            media_type (str): Le type de média (Film, Série, Anime).
            title (str): Le titre du média.
            path (str): Le chemin du dossier du média.

        Returns:
            int: L'ID du média nouvellement inséré.
        """
        self.cursor.execute(
            "INSERT INTO Media (type, title, path) VALUES (?, ?, ?)",
            (media_type, title, path)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_saison(self, media_id, season_number):
        """
        Insère un nouvel enregistrement de saison dans la table Saison.

        Args:
            media_id (int): L'ID du média auquel la saison appartient.
            season_number (int): Le numéro de la saison.

        Returns:
            int: L'ID de la saison nouvellement insérée.
        """
        self.cursor.execute(
            "INSERT INTO Saison (media_id, season_number) VALUES (?, ?)",
            (media_id, season_number)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_episode(self, media_id, saison_id, episode_number, is_film=False):
        """
        Insère un nouvel enregistrement d'épisode dans la table Episode.

        Args:
            media_id (int): L'ID du média auquel l'épisode appartient.
            saison_id (int): L'ID de la saison à laquelle l'épisode appartient.
            episode_number (int): Le numéro de l'épisode.
            is_film (bool): Indique si l'épisode est un film.
        """
        self.cursor.execute(
            "INSERT INTO Episode (media_id, saison_id, episode_number, is_film) VALUES (?, ?, ?, ?)",
            (media_id, saison_id, episode_number, is_film)
        )
        self.conn.commit()

    def mark_episode_as_watched(self, episode_id, watch_date):
        """
        Marque un épisode comme vu en mettant à jour la colonne 'watched' et 'watch_date'.

        Args:
            episode_id (int): L'ID de l'épisode à marquer comme vu.
            watch_date (str): La date à laquelle l'épisode a été vu.
        """
        self.cursor.execute(
            "UPDATE Episode SET watched = 1, watch_date = ? WHERE id = ?",
            (watch_date, episode_id)
        )
        self.conn.commit()

    def get_all_media(self):
        """
        Récupère tous les enregistrements de médias de la table Media.

        Returns:
            list: Une liste de tous les médias sous forme de tuples.
        """
        self.cursor.execute("SELECT * FROM Media")
        return self.cursor.fetchall()

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        self.conn.close()
