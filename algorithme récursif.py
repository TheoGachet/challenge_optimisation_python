import numpy as np

def meilleur_surveillant(grille, surveillants, cases_couvertes):
        meilleur_i, meilleur_j = -1, -1
        meilleur_gain = 0

        # Parcourir chaque case de la grille
        for i in range(grille.shape[0]):
            for j in range(grille.shape[1]):
                # Simuler l'ajout d'un surveillant à la case (i, j) si elle n'est pas un obstacle
                if grille[i][j] != -1:
                    # Calculer le gain en cibles couvertes si un surveillant était ajouté à (i, j)
                    gain = 0
                    new_cases_couvertes = np.copy(cases_couvertes)
                    
                    for k in range(j+1, grille.shape[1]): # Parcourir à droite
                        if grille[i][k] == -1:
                            break
                        new_cases_couvertes[i][k] = 1
                        if grille[i][k] == 1 and cases_couvertes[i][k] == 0:
                            gain += 1
                    
                    for k in range(j-1, -1, -1): # Parcourir à gauche
                        if grille[i][k] == -1:
                            break
                        new_cases_couvertes[i][k] = 1
                        if grille[i][k] == 1 and cases_couvertes[i][k] == 0:
                            gain += 1
                    
                    for k in range(i+1, grille.shape[0]): # Parcourir en bas
                        if grille[k][j] == -1:
                            break
                        new_cases_couvertes[k][j] = 1
                        if grille[k][j] == 1 and cases_couvertes[k][j] == 0:
                            gain += 1
                    
                    for k in range(i-1, -1, -1): # Parcourir en haut
                        if grille[k][j] == -1:
                            break
                        new_cases_couvertes[k][j] = 1
                        if grille[k][j] == 1 and cases_couvertes[k][j] == 0:
                            gain += 1

                    # Si le gain est plus élevé que le meilleur gain actuel, mettre à jour le meilleur gain et les coordonnées du meilleur surveillant
                    if gain > meilleur_gain:
                        meilleur_gain = gain
                        meilleur_i, meilleur_j = i, j

        return meilleur_i, meilleur_j

def update_cases_couvertes(surveillants, grille, cases_couvertes):
        # Parcourir la matrice surveillants
        for i in range(surveillants.shape[0]):
            for j in range(surveillants.shape[1]):
                if surveillants[i][j] == 1:
                    cases_couvertes[i][j] = 1
                    # Parcourir les cases dans la même ligne à droite du surveillant jusqu'à un obstacle
                    for k in range(j+1, surveillants.shape[1]):
                        if grille[i][k] == -1:
                            break
                        cases_couvertes[i][k] = 1
                    
                    # Parcourir les cases dans la même ligne à gauche du surveillant jusqu'à un obstacle
                    for k in range(j-1, -1, -1):
                        if grille[i][k] == -1:
                            break
                        cases_couvertes[i][k] = 1
                    
                    # Parcourir les cases dans la même colonne en bas du surveillant jusqu'à un obstacle
                    for k in range(i+1, surveillants.shape[0]):
                        if grille[k][j] == -1:
                            break
                        cases_couvertes[k][j] = 1
                    
                    # Parcourir les cases dans la même colonne en haut du surveillant jusqu'à un obstacle
                    for k in range(i-1, -1, -1):
                        if grille[k][j] == -1:
                            break
                        cases_couvertes[k][j] = 1
                    
        return cases_couvertes

def couvre_nouvelle_cible(i, j, grille, cases_couvertes):
        # Créer une copie de cases_couvertes pour simuler l'ajout d'un surveillant
        new_cases_couvertes = np.copy(cases_couvertes)

        # Mettre à jour new_cases_couvertes pour refléter l'ajout d'un surveillant à (i, j)
        for k in range(j+1, grille.shape[1]): # Parcourir à droite
            if grille[i][k] == -1:
                break
            new_cases_couvertes[i][k] = 1
        
        for k in range(j-1, -1, -1): # Parcourir à gauche
            if grille[i][k] == -1:
                break
            new_cases_couvertes[i][k] = 1
        
        for k in range(i+1, grille.shape[0]): # Parcourir en bas
            if grille[k][j] == -1:
                break
            new_cases_couvertes[k][j] = 1
        
        for k in range(i-1, -1, -1): # Parcourir en haut
            if grille[k][j] == -1:
                break
            new_cases_couvertes[k][j] = 1

        # Si le surveillant est placé sur une case cible, compter cela comme couvrant la cible
        if grille[i][j] == 1:
            new_cases_couvertes[i][j] = 1

        # Vérifier si l'ajout du surveillant permet de couvrir une nouvelle cible
        for i in range(grille.shape[0]):
            for j in range(grille.shape[1]):
                if grille[i][j] == 1 and new_cases_couvertes[i][j] == 1 and cases_couvertes[i][j] == 0:
                    return True

        # Si aucune nouvelle cible n'est couverte, retourner False
        return False

def afficher_nombre_lignes():
        nom_fichier = f"theo/res_opti/res_{numero_instance}.txt"
        try:
            with open(nom_fichier, 'r') as fichier:
                lignes = fichier.readlines()
                nombre_lignes = len(lignes)
                print(f"Instance {numero_instance} : {nombre_lignes-2} surveillants.")
        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'existe pas.")

for i in range(1, 2):
    numero_instance = 1
    best_score = 9

    # Initialisation des listes pour stocker les coordonnées des cibles et des obstacles
    cible = []
    obstacle = []   

    # Ouverture du fichier gr1.txt en mode lecture
    with open(f"theo/gr/gr{numero_instance}.txt", "r") as f:
        # Lecture de la première ligne pour obtenir le nombre de lignes
        key, value = f.readline().strip().split()
        if key == "LIGNES":
            lignes = int(value)

        # Lecture de la deuxième ligne pour obtenir le nombre de colonnes
        key, value = f.readline().strip().split()
        if key == "COLONNES":
            colonnes = int(value)
        
        # Sauter la ligne vide
        f.readline()
        
        # Lecture du reste du fichier ligne par ligne
        for line in f:
            # Split chaque ligne en mot-clé et valeurs
            data = line.strip().split()
            key = data[0]
            value = [int(data[i]) for i in range(1, len(data))]
            
            # Ajoute les coordonnées à la liste appropriée en fonction du mot-clé
            if key == "CIBLE":
                cible.append(tuple(value))
            elif key == "OBSTACLE":
                obstacle.append(tuple(value))

    # Création d'une matrice de zéros de taille lignes x colonnes
    grille = np.zeros((lignes, colonnes))

    # Marquer les cibles avec 1 et les obstacles avec -1
    for i, j in cible:
        grille[i][j] = 1

    for i, j in obstacle:
        grille[i][j] = -1

    # Création d'une matrice cases_couvertes de la même taille que la grille
    cases_couvertes = np.zeros_like(grille)

    # Création d'une matrice surveillants de la même taille que la grille
    surveillants = np.zeros_like(grille)

    coordonnees_surveillants = []

    for i in range(lignes):
        for j in range(colonnes):
            if (grille[i][j] != -1) and (couvre_nouvelle_cible(i, j, grille, cases_couvertes)):
                while True:
                    i, j = meilleur_surveillant(grille, surveillants, cases_couvertes)
                    
                    # Si aucun surveillant ne peut être ajouté pour couvrir plus de cibles, arrêter l'algorithme
                    if i == -1 and j == -1:
                        break

                    # Sinon, ajouter le meilleur surveillant à la grille
                    surveillants[i][j] = 1
                    cases_couvertes = update_cases_couvertes(surveillants, grille, cases_couvertes)

                surveillants[i][j] = 1
                coordonnees_surveillants.append((i,j))
                update_cases_couvertes(surveillants, grille, cases_couvertes)

    # Écriture des résultats dans le fichier res+numero_instance.txt
    with open(f"theo/res_opti/res_{numero_instance}.txt", "w") as f:
        f.write("EQUIPE 007\n")
        f.write(f"INSTANCE {numero_instance}\n")
        for i in range(lignes):
            for j in range(colonnes):
                if surveillants[i][j] == 1:
                    f.write(f"{i} {j}\n")
        
    afficher_nombre_lignes()

def lancer_jeu(grille, surveillants, cases_couvertes):
    # Liste pour stocker toutes les configurations de surveillants générées
    configurations = []
    # Parcourir chaque case de la grille
    for i in range(grille.shape[0]):
        for j in range(grille.shape[1]):
            # Si la case n'est ni un obstacle ni déjà couverte par un surveillant
            if grille[i][j] != -1 and surveillants[i][j] != 1:
                # Créer une copie des surveillants et des cases couvertes pour ne pas modifier les originaux
                new_surveillants = np.copy(surveillants)
                new_cases_couvertes = np.copy(cases_couvertes)

                # Ajouter un surveillant à la case courante
                nb_surv += 1
                new_surveillants[i][j] = 1
                new_cases_couvertes = update_cases_couvertes(new_surveillants, grille, new_cases_couvertes)

                # Appel récursif de lancer_jeu sur la nouvelle grille avec le surveillant ajouté
                new_configurations = lancer_jeu(grille, new_surveillants, new_cases_couvertes)

                # Ajouter toutes les nouvelles configurations à la liste de configurations
                configurations.extend(new_configurations)

                if nb_surv > 9:
                    break

    # Si aucune nouvelle configuration n'a été générée (c'est-à-dire si aucune case ne pouvait recevoir un surveillant),
    # alors la configuration actuelle est une configuration finale valide, donc on l'ajoute à la liste
    if len(configurations) == 0:
        configurations.append(surveillants)
        print(configurations)

    return configurations

def score_configuration(grille, configuration):
    # Initialiser le score à 0
    score = 0

    # Parcourir chaque case de la grille
    for i in range(grille.shape[0]):
        for j in range(grille.shape[1]):
            # Si la case est une cible et qu'elle est couverte par un surveillant dans la configuration, augmenter le score
            if grille[i][j] == 1 and configuration[i][j] == 1:
                score += 1

    return score

def compte(liste):
    total = 0
    for e in liste:
        if e == 1:
            total += 1
    return total

# Lancer le jeu et obtenir toutes les configurations possibles
configurations = lancer_jeu(grille, surveillants, cases_couvertes)
print(configurations)

# Évaluer chaque configuration et stocker les scores dans une liste
scores = [score_configuration(grille, config) for config in configurations]
print(scores)

# Trouver l'indice de la meilleure configuration
meilleur_index = np.argmax(scores)

# Choisir la meilleure configuration
meilleure_configuration = configurations[meilleur_index]

print(meilleure_configuration)