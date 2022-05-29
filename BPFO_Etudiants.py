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
from tkinter import Y
from mip import *
# Import du paquet time pour calculer le temps de résolution
import time 

print(" %%%% FORMULATION 1 %%%% ")

# Création du modèle vide 
model1 = Model(name = "BPFO_1", solver_name="CBC")  # Utilisation de CBC (remplacer par GUROBI pour utiliser cet autre solveur)

# Création des variables x et y
x = [model1.add_var(name="x(" + str(i) + ")", lb=0, ub=1, var_type=BINARY) for i in range(nb_objets*nb_boites)]
y = [model1.add_var(name="y(" + str(k) + ")", lb=0, ub=1, var_type=BINARY) for k in range(nb_boites)]

# Ajout de la fonction objectif au modèle
model1.objective = minimize(xsum(y[k] for k in range (nb_boites)))


# Ajout des contraintes au modèle
for i in range(nb_objets):
    [model1.add_constr(xsum([x[i + k*nb_objets] for k in range(nb_boites)]) == 1)]

for k in range (nb_objets):
    for j in range (nb_objets):
        [model1.add_constr(xsum(poids[i]*x[i + k*nb_objets] for i in range (nb_objets)) <= x[j + k*nb_objets]*fragilite[j] + M*(1 - x[j + k*nb_objets]))]

for i in range (nb_objets):
    for k in range(nb_boites):
        [model1.add_constr(x[i + k*nb_boites] <= y[k])] 

for i in range(nb_objets - 1):
    [model1.add_constr(y[i] >= y[i + 1])]



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
                if (x[i + k*nb_objets].x >= 1e-4):
                    print("\t Objet ",i, " à ", x[i + k*nb_objets].x*100, "%")
else:
    print("Pas de solution calculée")
print("----------------------------------\n")





print(" %%%% FORMULATION 2 %%%% ")

# Création du modèle vide 
model2 = Model(name = "BPFO_2", solver_name="CBC")  # Utilisation de CBC (remplacer par GUROBI pour utiliser cet autre solveur)

# Création des variables z et y
r = [model2.add_var(name="r(" + str(i) + ")", lb=0, ub=1, var_type=BINARY) for i in range(nb_objets)]
z = [model2.add_var(name="z(" + str(i) + ")", lb=0, ub=1, var_type=BINARY) for i in range(nb_objets*nb_objets)]

# Ajout de la fonction objectif au modèle
model2.objective = minimize(xsum(r[i] for i in range (nb_objets)))

# Ajout des contraintes au modèle
for j in range(nb_objets):
    [model2.add_constr(r[j] + xsum(z[i + j*nb_objets] for i in range (j - 1)) == 1)]

for i in range(nb_objets):
    [model2.add_constr(poids[i]*r[i] + (xsum(z[i + j*nb_objets]*poids[j] for j in range (i + 1, nb_objets))) <= fragilite[i]*r[i])]

for i in range(nb_objets):
    for j in range(nb_objets):
        [model2.add_constr(z[i + j*nb_objets] <= r[i])]


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
                if (z[i + j*nb_objets].x >= 1e-4):
                    print("\t Objet ",j, " à ", z[i + j*nb_objets].x*100, "%")
else:
    print("Pas de solution calculée")
print("----------------------------------\n")
