import numpy as np
import random

def charger_fichier(numero_instance):
    with open(f"theo/gr/gr{numero_instance}.txt", "r") as f:
        lignes = int(f.readline().split()[1])
        colonnes = int(f.readline().split()[1])
        grille = np.zeros((lignes, colonnes), dtype=int)
        cibles = []
        obstacles = []
        f.readline() # Pour sauter la ligne vide
        
        for ligne in f:
            elements = ligne.split()
            if elements[0] == "CIBLE":
                x, y = int(elements[1]), int(elements[2])
                grille[x][y] = 1
                cibles.append((x, y))
            elif elements[0] == "OBSTACLE":
                x, y = int(elements[1]), int(elements[2])
                grille[x][y] = -1
                obstacles.append((x, y))
                
    return lignes, colonnes, grille, cibles, obstacles

def initialiser_population(taille_population, lignes, colonnes):
    return [np.random.choice([0, 1], size=(lignes, colonnes)) for _ in range(taille_population)]

def fitness(solution, grille):
    surveillants = solution
    cases_couvertes = update_cases_couvertes(surveillants, grille)
    
    score = 0
    for i in range(grille.shape[0]):
        for j in range(grille.shape[1]):
            if grille[i][j] == 1 and cases_couvertes[i][j] == 0:
                score += 1

    return score

def selection_tournoi(population, grille, taille_tournoi):
    meilleure_solution = None
    meilleur_fitness = np.inf

    for _ in range(taille_tournoi):
        solution = random.choice(population)
        fitness_solution = fitness(solution, grille)

        if fitness_solution < meilleur_fitness:
            meilleure_solution = solution
            meilleur_fitness = fitness_solution

    return meilleure_solution

def croisement(parent1, parent2):
    lignes, colonnes = parent1.shape
    ligne_croisement = random.randint(0, lignes)
    
    enfant1 = np.vstack((parent1[:ligne_croisement, :], parent2[ligne_croisement:, :]))
    enfant2 = np.vstack((parent2[:ligne_croisement, :], parent1[ligne_croisement:, :]))
    
    return enfant1, enfant2

def mutation(solution, taux_mutation):
    for i in range(solution.shape[0]):
        for j in range(solution.shape[1]):
            if random.random() < taux_mutation:
                solution[i][j] = 1 - solution[i][j]

    return solution

def algo_genetique(grille, taille_population, taille_tournoi, taux_mutation, nombre_generations):
    lignes, colonnes = grille.shape
    
    population = initialiser_population(taille_population, lignes, colonnes)
    
    for _ in range(nombre_generations):
        nouvelle_population = []
        
        while len(nouvelle_population) < taille_population:
            parent1 = selection_tournoi(population, grille, taille_tournoi)
            parent2 = selection_tournoi(population, grille, taille_tournoi)
            
            enfant1, enfant2 = croisement(parent1, parent2)
            
            enfant1 = mutation(enfant1, taux_mutation)
            enfant2 = mutation(enfant2, taux_mutation)
            
            nouvelle_population.append(enfant1)
            nouvelle_population.append(enfant2)
        
        population = nouvelle_population
    
    meilleure_solution = min(population, key=lambda solution: fitness(solution, grille))
    
    return meilleure_solution

def algo_glouton(numero_instance):
    lignes, colonnes, grille, cibles, obstacles = charger_fichier(numero_instance)
    surveillants = np.zeros((lignes, colonnes), dtype=int)
    
    for i in range(lignes):
        for j in range(colonnes):
            if grille[i][j] == 0 and est_benefique_ajouter_surveillant(i, j, grille, cibles, surveillants):
                surveillants[i][j] = 1
                
    with open("res_"+str(numero_instance)+".txt", 'w') as f:
        f.write("EQUIPE 007\n")
        f.write("INSTANCE " + str(numero_instance) + "\n")
        for i in range(lignes):
            for j in range(colonnes):
                if surveillants[i][j] == 1:
                    f.write(str(i) + " " + str(j) + "\n")
                    
    return surveillants

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

def est_benefique_ajouter_surveillant(x, y, grille, cibles, surveillants):
    temp_surveillants = surveillants.copy()
    temp_surveillants[x][y] = 1
    cases_couvertes_avant = update_cases_couvertes(surveillants, grille)
    cases_couvertes_apres = update_cases_couvertes(temp_surveillants, grille)
    
    for cible in cibles:
        if cases_couvertes_avant[cible[0]][cible[1]] == 0 and cases_couvertes_apres[cible[0]][cible[1]] == 1:
            return True
    return False

# Charger la grille
lignes, colonnes, grille, cibles, obstacles = charger_fichier(1)

# Exécuter l'algorithme glouton
surveillants_glouton = algo_glouton(1)
print("Surveillants trouvés par l'algorithme glouton :")
print(surveillants_glouton)

# Définir les paramètres de l'algorithme génétique
taille_population = 50
taille_tournoi = 5
taux_mutation = 0.01
nombre_generations = 100

# Exécuter l'algorithme génétique
surveillants_genetique = algo_genetique(grille, taille_population, taille_tournoi, taux_mutation, nombre_generations)
print("Surveillants trouvés par l'algorithme génétique :")
print(surveillants_genetique)
