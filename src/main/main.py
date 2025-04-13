from controllers.main_controller import MainController

def run():
    """Point d'entrée principal du programme"""
    controller = MainController()
    controller.start()

if __name__ == "__main__":
    run()
