#chemin relatif vers le fichier (l'utilisation .. permet de revenir au dossier parent)
datafileName = 'bpfo_instances/toyInstance2.BPPFI.dat'

#ouverture du fichier, le ferme automatiquement à la fin et gère les exceptions
with open(datafileName, "r") as file:
    # lecture de la 1ère ligne et séparation des éléments de la ligne
    # dans un tableau en utilisant l'espace comme séparateur
    line = file.readline()  
    lineTab = line.split()
    
    # la valeur de la 1ère ligne correspond au nombre d'objets
    # (attention de penser à convertir la chaîne de caractère en un entier)
    nb_objets = int(lineTab[0])

    # création d'un tableau qui stockera les poids des objets
    poids = []
    # création d'un tableau qui stockera les fragilités des objets
    fragilite = []
    M = 0
    
    # pour chaque ligne contenant les informations sur les objets
    for i in range(nb_objets):
        # lecture de la ligne suivante et séparation des éléments de la ligne
        # dans un tableau en utilisant l'espace comme séparateur
        line = file.readline()
        lineTab = line.split()
        
        # ajout de l'élément de la 1ère case au tableau qui contient le poids de l'objet
        poids.append(int(lineTab[0])) 
        # ajout de l'élément de la 2ème case au tableau qui contient la fragilité de l'objet 
        fragilite.append(int(lineTab[1]))
        if (int(lineTab[1]) > M):
            M = int(lineTab[1])
            
# Affichage des informations lues
print("Nombre d'objets = ", nb_objets)
print("Poids des objets = ", poids)
print("Fragilité des objets = ", fragilite)

nb_boites = nb_objets

# Import du paquet PythonMIP et de toutes ses fonctionnalités
from mip import *
# Import du paquet time pour calculer le temps de résolution
import time 

print(" %%%% FORMULATION 1 %%%%% ")

# Création du modèle vide 
model1 = Model(name = "BPFO_1", solver_name="CBC")  # Utilisation de CBC (remplacer par GUROBI pour utiliser cet autre solveur)

# Création des variables z et y
y = 
x = 

# Ajout de la fonction objectif au modèle


# Ajout des contraintes au modèle











# Ecrire le modèle (ATTENTION ici le modèle est très grand)
model1.write("bpfo.lp") #à décommenter si vous le souhaitez

# Indication au solveur d'un critère d'optimalité : gap relatif en dessous duquel la résolution sera stoppée et la solution considérée comme optimale
model1.max_mip_gap = 1e-6
# Indication au solveur d'un critère d'optimalité : gap absolu en dessous duquel la résolution sera stoppée et la solution considérée comme optimale 
model1.max_mip_gap_abs = 1e-8

# Lancement du chronomètre
start = time.perf_counter()

# Résolution du modèle
status = model1.optimize(max_seconds = 120)

# Arrêt du chronomètre et calcul du temps de résolution
runtime = time.perf_counter() - start

print("\n----------------------------------")
if status == OptimizationStatus.OPTIMAL:
    print("Status de la résolution: OPTIMAL")
elif status == OptimizationStatus.FEASIBLE:
    print("Status de la résolution: TEMPS LIMITE et UNE SOLUTION REALISABLE CALCULEE")
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print("Status de la résolution: TEMPS LIMITE et AUCUNE SOLUTION CALCULEE")
elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
    print("Status de la résolution: IRREALISABLE")
elif status == OptimizationStatus.UNBOUNDED:
    print("Status de la résolution: NON BORNE")
    
print("Temps de résolution (s) : ", runtime)
print("----------------------------------")

# Si le modèle a été résolu à l'optimalité ou si une solution a été trouvée dans le temps limite accordé
if model1.num_solutions>0:
    print("Solution calculée")
    print("-> Valeur de la fonction objectif de la solution calculée : ",  model1.objective_value)  # ne pas oublier d'arrondir si le coût doit être entier
    print("-> Meilleure borne inférieure sur la valeur de la fonction objectif = ", model1.objective_bound)
    for k in range(nb_boites):
        if (y[k].x >= 1e-4):
            print("- La boîte ",k , " ouverte à ", y[k].x*100,"% contient les objets")
            for i in range(nb_objets):
                if (x[i][k].x >= 1e-4):
                    print("\t Objet ",i, " à ", x[i][k].x*100, "%")
else:
    print("Pas de solution calculée")
print("----------------------------------\n")

#if model1.num_solutions>0: # Si une solution a été calculée
#    solutionfileName = 'solution_cap41.txt' #nom du fichier solution
#    with open(solutionfileName, 'w') as file:  #ouvre le fichier, le ferme automatiquement à la fin et gère les exceptions
#        file.write(str(model1.objective_value)) #Il faut convertir les valeurs numériques en chaîne de caractères
#        file.write("\n") #Je passe à la ligne suivante
#        for i in range(nb_warehouses):
#            if (z[i].x >= 0.5):
#                file.write(str(i)) 
#                file.write("\n") #Je passe à la ligne suivante
#                for j in range(nb_customers):
#                    if (y[j][i].x >= 1e-4):
#                        file.write(str(j)+" "+str(round(y[j][i].x * 100,2)))
#                        file.write("\n") #Je passe à la ligne suivante


print(" %%%% FORMULATION 2 %%%%% ")

# Création du modèle vide 
model2 = Model(name = "BPFO_1", solver_name="CBC")  # Utilisation de CBC (remplacer par GUROBI pour utiliser cet autre solveur)

# Création des variables z et y
r =
z =

# Ajout de la fonction objectif au modèle



# Ajout des contraintes au modèle










# Ecrire le modèle (ATTENTION ici le modèle est très grand)
model2.write("bpfo2.lp") #à décommenter si vous le souhaitez

# Indication au solveur d'un critère d'optimalité : gap relatif en dessous duquel la résolution sera stoppée et la solution considérée comme optimale
model2.max_mip_gap = 1e-6
# Indication au solveur d'un critère d'optimalité : gap absolu en dessous duquel la résolution sera stoppée et la solution considérée comme optimale 
model2.max_mip_gap_abs = 1e-8

# Lancement du chronomètre
start = time.perf_counter()

# Résolution du modèle
status = model2.optimize(max_seconds = 120)

# Arrêt du chronomètre et calcul du temps de résolution
runtime = time.perf_counter() - start

print("\n----------------------------------")
if status == OptimizationStatus.OPTIMAL:
    print("Status de la résolution: OPTIMAL")
elif status == OptimizationStatus.FEASIBLE:
    print("Status de la résolution: TEMPS LIMITE et UNE SOLUTION REALISABLE CALCULEE")
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print("Status de la résolution: TEMPS LIMITE et AUCUNE SOLUTION CALCULEE")
elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
    print("Status de la résolution: IRREALISABLE")
elif status == OptimizationStatus.UNBOUNDED:
    print("Status de la résolution: NON BORNE")
    
print("Temps de résolution (s) : ", runtime)
print("----------------------------------")

# Si le modèle a été résolu à l'optimalité ou si une solution a été trouvée dans le temps limite accordé
if model2.num_solutions>0:
    print("Solution calculée")
    print("-> Valeur de la fonction objectif de la solution calculée : ",  model2.objective_value)  # ne pas oublier d'arrondir si le coût doit être entier
    print("-> Meilleure borne inférieure sur la valeur de la fonction objectif = ", model2.objective_bound)
    for i in range(nb_objets):
        if (r[i].x >= 1e-4):
            print("- La boîte représentée par ",i , " est ouverte à ", r[i].x*100,"% contient les objets")
            print("\t Objet ",i, " à ", r[i].x*100, "%")
            for j in range(i+1,nb_objets):
                if (z[i][j].x >= 1e-4):
                    print("\t Objet ",j, " à ", z[i][j].x*100, "%")
else:
    print("Pas de solution calculée")
print("----------------------------------\n")
