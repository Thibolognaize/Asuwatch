import sqlite3

# .connect() => Créer une connexion avec bdd et la créée si n'existes pas déjà
# .cursor() => Permet d'executer de pointer l'execution de requetes 
# .execute() => Execute les requetes
# .commit() => Enregistre les changements des insert

# Ici nous verifions l'utilisation de fonctions pour créer des tables 
# Création de table : 
def creer_table(db, db_table):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {db_table}")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {db_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                nom TEXT,
                prenom TEXT,
                age INTEGER,
                classe TEXT
                )""")
    conn.close()

creer_table("eleves.db", "Eleve")

# Insertion "Classique"
conn = sqlite3.connect("eleves.db")
cur = conn.cursor()
cur.execute("""INSERT INTO Eleve (id, nom, prenom, age, classe) 
            VALUES (1, 'Dupont', 'Jean', 15, '2A')""")
conn.commit()

# Insertion "Dynamique" (par tuple)
eleve_2 = ('Dupont', 'Jeanne', 17, 'TG2')
cur.execute("""INSERT INTO Eleve (nom, prenom, age, classe) 
            VALUES (?, ?, ?, ?)""", eleve_2)
conn.commit()

# Insertion "Dynamique" (par dictionnaire)
eleve_3 = {'nom': 'Marchand', 'prenom': 'Marie', 'age': 15, 'classe': '2A'}
cur.execute("""INSERT INTO Eleve (nom, prenom, age, classe) 
            VALUES (:nom, :prenom, :age, :classe)""", eleve_3)
conn.commit()

# Insertion par boucle
liste_eleves = [
    ('Martin', 'Adeline', 16, '1G1'),
    ('Dupont', 'Christophe', 15, '2A'),
    ('Richard', 'Moche', 16, '1G2'),
    ('Boudou', 'François', 17, 'TG2'),
]
# Méthonde avec boucle python:
# for eleve in liste_eleves:
#     cur.execute("""INSERT INTO Eleve (nom, prenom, age, classe) 
#             VALUES (?, ?, ?, ?)""", eleve)
# conn.commit()

# Méthode avec executemany() (mysqlite3):
cur.executemany("""INSERT INTO Eleve (nom, prenom, age, classe)
                VALUES (?, ?, ?, ?)""", liste_eleves)
conn.commit()

# Renvoyer des resultats (Select par ex):
# res = cur.execute("SELECT * FROM Eleve")

# Retourne tous les resultats
# print(res.fetchall())

# Retourne resultats dans une liste
# print(list(res))

# Retourne premier resultat sous curseur
# print(res.fetchone())
# print(res.fetchone())

# Retourne les 3 premiers resultats:
# print(res.fetchmany(3))

# ICI ATTENTION : Il faut passer en param un TUPLE ! donc si on cherche un résultat avec un seul resultat on écrit
# tout de même la virgule !!
res = cur.execute("SELECT id, nom, prenom FROM Eleve WHERE nom = ?", ('Dupont',))
# print(res.fetchall())
# Autre méthode:
res = cur.execute("SELECT id, nom, prenom FROM Eleve WHERE nom = :nom", {'nom': 'Dupont'})
# print(res.fetchall())

def recuperer_eleves_par_nom(nom):
    conn = sqlite3.connect('eleves.db')
    cur = conn.cursor()
    res = cur.execute("SELECT id, nom, prenom FROM Eleve WHERE nom = ?", (nom,))
    eleves = res.fetchall() #On stock le resultat pour return
    conn.close()
    return eleves #Après avoir fermé la connexion

print(recuperer_eleves_par_nom("Dupont"))
print(recuperer_eleves_par_nom("Richard"))
# Si élève non existant renvoi liste vide:
print(recuperer_eleves_par_nom("Zeubi"))

conn.close()

