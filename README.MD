# Asuwatch

Asuwatch est un gestionnaire de visionnage de séries TV qui vous permet de suivre les épisodes que vous avez regardés. Il analyse automatiquement la structure de vos dossiers de séries et crée une base de données SQLite pour stocker votre progression.

## 📋 Fonctionnalités

- Interface graphique pour la sélection du dossier de série
- Détection automatique des saisons et épisodes
- Support des formats de nommage de dossiers "SaisonXX" et "SXX"
- Base de données SQLite pour stocker la progression
- Marquage des épisodes comme "vus"
- Gestion robuste des erreurs

## 🛠️ Prérequis

- Python 3.12 ou supérieur
- tkinter (inclus dans Python)

## 🚀 Installation

1. Clonez le repository :
```bash
git clone [url-du-repo]
cd asuwatch
```

2. Lancez le programme :
```bash
python src/main.py
```

## 📁 Structure du Projet

```
asuwatch/
├── src/                 # Code source
│   ├── database.py      # Gestion de la base de données SQLite
│   ├── main.py         # Point d'entrée de l'application
│   └── serie_manager.py # Gestion des dossiers de séries
├── data/               # Dossier contenant les bases de données SQLite
└── .gitignore         # Configuration Git
```

## 🎯 Utilisation

1. Lancez le programme :
```bash
python src/main.py
```

2. Sélectionnez le dossier de votre série via la fenêtre de dialogue
3. Le programme :
   - Analysera la structure du dossier
   - Créera une base de données
   - Initialisera le suivi des épisodes

## 📊 Structure de la Base de Données

Chaque série a sa propre base de données SQLite avec :
- Une table par saison nommée `season_XX`
- Colonnes : 
  - `id` : ID auto-incrémenté
  - `episode_number` : Numéro de l'épisode (format EXX)
  - `watched` : État de visionnage (0/1)
  - `watch_date` : Date de visionnage

## 📑 Format des Dossiers Supportés

Structure attendue des dossiers :
```
Nom_de_la_Serie/
├── Saison1/
│   ├── Episode1.mp4
│   └── Episode2.mp4
└── S02/
    ├── Episode1.mp4
    └── Episode2.mp4
```

## 🐛 Gestion des Erreurs

Le programme inclut une gestion complète des erreurs pour :
- Sélection de dossier invalide
- Erreurs de lecture de dossiers
- Problèmes de base de données
- Erreurs inattendues

## 🤝 Contribution

1. Fork le projet
2. Créez votre branche de fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📝 Notes de Développement

- Le code utilise la PEP 8 pour le style
- Documentation complète avec docstrings
- Gestion des erreurs avec try/except
- Utilisation de types hints pour améliorer la maintenabilité

## ⚠️ Limitations Connues

- Ne gère pas encore la modification en masse des statuts de visionnage
- Ne supporte pas les sous-titres séparés
- Pas de support pour les métadonnées d'épisodes
- Interface utilisateur limitée à la sélection de dossier

## 🔜 Améliorations Futures Possibles

- Interface graphique complète
- Support des métadonnées d'épisodes
- Export/Import des données de visionnage
- Support multi-séries simultané
- Statistiques de visionnage
- Support des films

## 📄 Licence

Ce projet est sous licence MIT (à confirmer).
