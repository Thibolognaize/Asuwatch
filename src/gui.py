import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
import sqlite3
import os
from serie_manager import SerieManager
from database import Database

class SerieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Séries")
        self.root.geometry("600x400")  # Définir la taille initiale de la fenêtre
        self.db = None
        self.serie_name = None

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#007BFF", foreground="black", font=("Arial", 12))
        style.configure("TLabel", padding=6, font=("Arial", 12))

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.init_db_button = ttk.Button(frame, text="Choisir une série et initialiser la BDD", command=self.initialize_db)
        self.init_db_button.pack(pady=10, fill=tk.X)
        self.init_db_button.bind("<Enter>", lambda e: self.on_hover(self.init_db_button, "#0056b3"))
        self.init_db_button.bind("<Leave>", lambda e: self.on_leave(self.init_db_button, "#007BFF"))

        self.manage_episodes_button = ttk.Button(frame, text="Gérer les épisodes vus/non vus", command=self.open_episode_manager, state=tk.DISABLED)
        self.manage_episodes_button.pack(pady=10, fill=tk.X)
        self.manage_episodes_button.bind("<Enter>", lambda e: self.on_hover(self.manage_episodes_button, "#0056b3"))
        self.manage_episodes_button.bind("<Leave>", lambda e: self.on_leave(self.manage_episodes_button, "#007BFF"))

    def on_hover(self, button, color):
        button.config(style="Hover.TButton")
        style = ttk.Style()
        style.configure("Hover.TButton", background=color)

    def on_leave(self, button, color):
        button.config(style="TButton")
        style = ttk.Style()
        style.configure("TButton", background=color)

    def initialize_db(self):
        serie_manager = SerieManager()
        if not serie_manager.select_directory():
            messagebox.showwarning("Sélection", "Aucun dossier sélectionné.")
            return

        try:
            seasons = serie_manager.get_season_folders()
            self.serie_name = serie_manager.get_serie_name()

            self.db = Database(self.serie_name, seasons)
            self.db.insert_episodes_from_serie_manager(serie_manager)

            messagebox.showinfo("Succès", "Base de données initialisée avec succès.")
            self.manage_episodes_button.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Erreur", f"Erreur : {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur inattendue est survenue : {e}")

    def open_episode_manager(self):
        if not self.db:
            messagebox.showwarning("Initialisation", "Veuillez d'abord initialiser la base de données.")
            return

        episode_manager_window = tk.Toplevel(self.root)
        episode_manager_window.title(f"Gérer les épisodes - {self.serie_name}")
        episode_manager_window.geometry("500x400")  # Définir la taille initiale de la fenêtre
        EpisodeManager(episode_manager_window, self.db)

class EpisodeManager:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.conn = db.conn
        self.cursor = db.cursor

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        self.season_label = ttk.Label(frame, text="Sélectionnez la saison:")
        self.season_label.pack(anchor="w")

        self.season_var = tk.StringVar()
        self.season_menu = ttk.OptionMenu(frame, self.season_var, self.load_seasons()[0] if self.load_seasons() else "", *self.load_seasons(), command=self.load_episodes)
        self.season_menu.pack(fill=tk.X, pady=5)

        self.episode_listbox = tk.Listbox(frame, selectmode=tk.EXTENDED, font=("Arial", 12))
        self.episode_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)

        self.mark_watched_button = ttk.Button(button_frame, text="Marquer comme regardé", command=self.mark_as_watched)
        self.mark_watched_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.mark_watched_button.bind("<Enter>", lambda e: self.on_hover(self.mark_watched_button, "#0056b3"))
        self.mark_watched_button.bind("<Leave>", lambda e: self.on_leave(self.mark_watched_button, "#007BFF"))

        self.mark_unwatched_button = ttk.Button(button_frame, text="Marquer comme non regardé", command=self.mark_as_unwatched)
        self.mark_unwatched_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.mark_unwatched_button.bind("<Enter>", lambda e: self.on_hover(self.mark_unwatched_button, "#0056b3"))
        self.mark_unwatched_button.bind("<Leave>", lambda e: self.on_leave(self.mark_unwatched_button, "#007BFF"))

    def on_hover(self, button, color):
        button.config(style="Hover.TButton")
        style = ttk.Style()
        style.configure("Hover.TButton", background=color)

    def on_leave(self, button, color):
        button.config(style="TButton")
        style = ttk.Style()
        style.configure("TButton", background=color)

    def load_seasons(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
        seasons = [table[0][7:] for table in tables if table[0].startswith('season_')]
        return tuple(seasons)

    def load_episodes(self, season):
        season_num = season
        table_name = f"season_{season_num}"

        self.cursor.execute(f"SELECT id, episode_number, watched FROM {table_name}")
        episodes = self.cursor.fetchall()

        self.episode_listbox.delete(0, tk.END)
        for episode in episodes:
            status = "Vu" if episode[2] else "Non vu"
            self.episode_listbox.insert(tk.END, f"{episode[1]} - {status}")

    def mark_as_watched(self):
        selected_indices = self.episode_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Sélection", "Veuillez sélectionner au moins un épisode.")
            return

        season_num = self.season_var.get()
        watch_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = f"UPDATE season_{season_num} SET watched = 1, watch_date = ? WHERE id = ?"

        try:
            for episode_id in selected_indices:
                self.cursor.execute(query, (watch_date, episode_id + 1))
            self.conn.commit()
            self.load_episodes(self.season_var.get())
            messagebox.showinfo("Succès", "Épisodes marqués comme regardés.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour des épisodes : {e}")

    def mark_as_unwatched(self):
        selected_indices = self.episode_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Sélection", "Veuillez sélectionner au moins un épisode.")
            return

        season_num = self.season_var.get()
        query = f"UPDATE season_{season_num} SET watched = 0, watch_date = NULL WHERE id = ?"

        try:
            for episode_id in selected_indices:
                self.cursor.execute(query, (episode_id + 1,))
            self.conn.commit()
            self.load_episodes(self.season_var.get())
            messagebox.showinfo("Succès", "Épisodes marqués comme non regardés.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la mise à jour des épisodes : {e}")

    def close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerieApp(root)
    root.mainloop()