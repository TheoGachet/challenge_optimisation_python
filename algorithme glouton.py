import numpy as np

for i in range(1, 17):
    numero_instance = i

    # Initialisation des listes pour stocker les coordonnées des cibles et des obstacles
    cible = []
    obstacle = []
    
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

    # Affichage de la matrice
    #print(grille)

    # Création d'une matrice cases_couvertes de la même taille que la grille
    cases_couvertes = np.zeros_like(grille)

    # Création d'une matrice surveillants de la même taille que la grille
    surveillants = np.zeros_like(grille)

    #print("Cases couvertes :\n", cases_couvertes)
    #print("Surveillants :\n", surveillants)
    #print("Grille :\n", grille)

    coordonnees_surveillants = []

    for i in range(lignes):
        for j in range(colonnes):
            if (grille[i][j] != -1) and (couvre_nouvelle_cible(i, j, grille, cases_couvertes)):
                surveillants[i][j] = 1
                coordonnees_surveillants.append((i,j))
                update_cases_couvertes(surveillants, grille, cases_couvertes)

    #print(coordonnees_surveillants)
    
    # Écriture des résultats dans le fichier res+numero_instance.txt
    print("Code exécuté pour l'instance {}".format(numero_instance))
    with open(f"theo/res_opti/res_{numero_instance}.txt", "w") as f:
        f.write("EQUIPE 007\n")
        f.write(f"INSTANCE {numero_instance}\n")
        for i in range(lignes):
            for j in range(colonnes):
                if surveillants[i][j] == 1:
                    f.write(f"{i} {j}\n")

