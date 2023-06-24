import numpy as np

def charger_fichier(numero_instance):
    with open(f"theo/gr/gr{numero_instance}.txt", "r") as f:
        lignes = int(next(f).split()[-1])
        colonnes = int(next(f).split()[-1])
        grille = np.zeros((lignes, colonnes), dtype=int)
        cibles = []
        obstacles = []
        next(f)  # skip the empty line
        for line in f:
            if "CIBLE" in line:
                _, x, y = line.split()
                x, y = int(x), int(y)
                grille[x][y] = 1
                cibles.append((x, y))
            elif "OBSTACLE" in line:
                _, x, y = line.split()
                x, y = int(x), int(y)
                grille[x][y] = -1
                obstacles.append((x, y))
    return lignes, colonnes, grille, cibles, obstacles


def update_cases_couvertes(surveillants, grille):
    lignes, colonnes = grille.shape
    cases_couvertes = np.zeros((lignes, colonnes), dtype=int)
    
    for i in range(lignes):
        for j in range(colonnes):
            if surveillants[i][j] == 1:
                for k in range(j+1, colonnes):
                    if grille[i][k] == -1:
                        break
                    cases_couvertes[i][k] = 1
                
                for k in range(j-1, -1, -1):
                    if grille[i][k] == -1:
                        break
                    cases_couvertes[i][k] = 1
                
                for k in range(i+1, lignes):
                    if grille[k][j] == -1:
                        break
                    cases_couvertes[k][j] = 1
                
                for k in range(i-1, -1, -1):
                    if grille[k][j] == -1:
                        break
                    cases_couvertes[k][j] = 1
                    
    return cases_couvertes

def recherche_locale(grille, max_iterations_sans_amelioration):
    lignes, colonnes = grille.shape
    surveillants = np.zeros((lignes, colonnes), dtype=int)
    best_score = len(cibles)

    for _ in range(max_iterations_sans_amelioration):
        score_actuel = best_score
        for i in range(lignes):
            for j in range(colonnes):
                if grille[i][j] == 0 or grille[i][j] == 1:
                    surveillants[i][j] ^= 1
                    cases_couvertes = update_cases_couvertes(surveillants, grille)
                    score = sum(cases_couvertes[cible[0]][cible[1]] for cible in cibles)
                    if score < best_score:
                        best_score = score
                    else:
                        surveillants[i][j] ^= 1

        if score_actuel == best_score:
            break

    return surveillants

# Charger la grille
lignes, colonnes, grille, cibles, obstacles = charger_fichier(1)

# Exécuter la recherche locale
surveillants = recherche_locale(grille, 1000)
print("Surveillants trouvés par la recherche locale :")
print(surveillants)