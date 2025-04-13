class MainView:
    def __init__(self, controller):
        """
        Initialise la vue principale avec un contrôleur.

        Args:
            controller (MainController): Le contrôleur principal de l'application.
        """
        self.controller = controller

    def show_main_menu(self):
        """
        Affiche le menu principal à l'utilisateur.
        """
        print("Bienvenue dans ASUWatch!")
        print("1. Sélectionner un dossier de médias")
        print("2. Afficher les médias")
        print("3. Marquer un épisode comme vu")
        print("4. Quitter")

        choice = input("Choisissez une option : ")
        if choice == "1":
            self.controller.select_media_directory()
        elif choice == "2":
            self.controller.display_media()
        elif choice == "3":
            self.controller.mark_episode_as_watched()
        elif choice == "4":
            print("Au revoir!")
            exit()
        else:
            print("Option invalide. Veuillez réessayer.")
            self.show_main_menu()

    def display_media(self, media_list):
        """
        Affiche la liste des médias.

        Args:
            media_list (list): Liste des médias à afficher.
        """
        print("Liste des médias :")
        for media in media_list:
            print(f"Type: {media['type']}, Titre: {media['title']}, Saisons: {media['seasons']}")

    def get_user_input(self, prompt):
        """
        Obtient une entrée de l'utilisateur.

        Args:
            prompt (str): Le message à afficher à l'utilisateur.

        Returns:
            str: L'entrée de l'utilisateur.
        """
        return input(prompt)
