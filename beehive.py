from time import perf_counter
import pandas as pd
from scipy.spatial import distance
import matplotlib.pyplot as plt
import numpy as np
import random


# La classe Bee est un ensemble de méthodes visant à produire un algorithme génétique à partir d'un fichier excel.
# Le fichier excel contient 50 vecteurs qui représentent les coordonnées d'un champ de fleurs que des abeilles doivent
# polliniser. La classe créé une ruche de 100 abeilles puis fait une sélection à chaque pollinisation. Le programme
# sort un graphique qui montre le score de fitness moyen de la ruche au fil des générations.

class Bee:

    
    def __init__(self, xl_file):
        
        # On extrait les données du fichier .xls dans un dataframe du module pandas (les coordonnées des fleurs)
        self.df = pd.read_excel(xl_file)
        # On convertit ce dataframe en liste Python
        self.flowers = [(self.df.iat[i,0], self.df.iat[i,1]) for i in range(len(self.df))]
        
        self.dist_flowers = sorted([distance.sqeuclidean(self.flowers[i], self.flowers[i+1]) for i in range(len(self.flowers)-1)])
        # On créé un vecteur de 100 vecteurs, ces derniers formés par des combinaisons aléatoires des coordonnées de fleurs 
        # C'est ce qui constitue la ruche
        self.hive_zero = [random.sample(self.flowers, len(self.flowers)) for i in range(0,100)]
        
    def sq_euclidean_distances(self, hive):
        
        # On calcule la distance euclidienne de scipy qui est la plus rapide de leur module distance
    
        distances = [[distance.sqeuclidean(hive[j][i], hive[j][i+1]) for i in range(len(self.flowers) - 1)] for j in range(len(hive))]
        return distances
        
    def fitness(self, x):
        
        # On calcule le score de fitness i.e la somme des distances successives que parcourt une abeille lors d'une campagne
        
        fitness = [sum(item) for item in x]
        return fitness
        
    def stochastic_selection(self, fitn, hiv):
        
        # On opère une sélection stochastique: On assigne une probabilité inversement proportionelle au score de fitness
        # à chaque abeille puis on pioche 50 abeilles dans la ruche. On aura ainsi une proportion relativement élévée
        # d'abeille avec un score de fotness bas sans toutefois en avoir trop.
        
        inverse_f = [1/item for item in fitn]
        proba = [item/sum(inverse_f) for item in inverse_f]
        selected = random.choices(hiv, weights = proba, k=50)
        return selected
        
    def shift_cross(self, selected_bees):
        
        # Croisement par décalage. On décale les gènes d'un certain nombre vers la droite. 
        # De la sorte on s'assure qu'il n'y a pas de gène en double pour chaque abeille. 
        # La nouvelle ruche se compose des abeilles sélectionnées et de ces mêmes abeilles 
        # dont les gènes ont subit un certain décalage (2 ici)
        shift_offspring = [item[2:] + item[:2] for item in selected_bees]
        new_hive = selected_bees + shift_offspring
        return new_hive
        
    def cut_cross(self, selected_bees):
        
        # Croisement par simple enjambement. On échange deux blocs de gènes autour d'un point particulier (ici au milieu) 
        # du génome. La nouvelle ruche se compose des abeilles sélectionnées et de ces meêmes abeilles auxquelles
        # ont a opéré la coupe
        
        cut_offspring = [bee[25:] + bee[:25] for bee in selected_bees]
        new_hive = selected_bees + cut_offspring
        return new_hive
        
    def mutate(self, hiv):
        
        # La méthode mutate() remplace remplace les 5 premiers gènes des abeilles par les plus performants
        # Elle devrait être amélioré en remplaçant les gènes en double.
        
        hiv[:5] = self.dist_flowers[:5]
        return hiv
        
    def derivative(self,x):
        
        # La méthode derivative() opère une dérivée simplifiée afin de déterminer si la courbe s'applanit ou non
        # et ainsi déclencher une mutation
        
        der = [np.abs(x[i+1] - x[i]) for i in range(len(x)-1)]
        return der
        
    def normalizer(self, x):
        
        # La méthode normalizer() normalise toutes les valeurs d'un vecteur entre 0 et 1.
        # Cette méthode est utilisée pour afficher les valeurs moyennes de fitness en output
        
        x_norm = [item/sum(x) for item in x]
        return x_norm

        
    def generation(self,steps):
        
        # La méthode generation() met en chaîne les différentes méthodes afin de consturire le processus génératif. 
        # On a opté pour une boucle for étant donné que la mutation, qui aurait supporté un while, n'a pas été implantée.
        # Le processus génératif consiste donc à calculer les distances parcourues par chaque abeilles, leur score de fitness,
        # leur score de fitness moyen, à faire la sélection puis à reéinjecter le résultat dans la boucle pour la prochaine
        # génération. 
        # Ici on essaye les deux types de croisement dans la même boucle de la méthode generation().
        
        # On assigne la ruche de départ pour la génération liée au croisement en décalage
        hive_shift = self.hive_zero
        # On initialise la liste qui contiendra les valeurs moyenne des scores de fitness de 
        # la génération liée au croisement en décalage
        fit_mean_shift = []

        # On assigne la ruche de départ pour la génération liée au croisement par simple enjambement
        hive_cut = self.hive_zero
        # On initialise la liste qui contiendra les valeurs moyenne des scores de fitness de 
        # la génération liée au croisement par simple enjambement
        fit_mean_cut = []

        # On initialise la boucle qui va produire les générations d'abeilles
        for i in range(steps):
                
            # On chaîne le processus calcul de distance/calcul de fitness/sélection/création d'une nouvelle génération
            # pour le croisement en décalage
            distances_shift = self.sq_euclidean_distances(hive_shift)
            fit_shift = self.fitness(distances_shift)
            fit_mean_shift.append(np.mean(fit_shift))
            elite_shift = self.stochastic_selection(fit_shift, hive_shift)
            hive_shift = self.cut_cross(elite_shift)
                
            # On chaîne le processus calcul de distance/calcul de fitness/sélection/création d'une nouvelle génération
            # pour le croisement par simple enjambement
            distances_cut = self.sq_euclidean_distances(hive_cut)
            fit_cut = self.fitness(distances_cut)
            fit_mean_cut.append(np.mean(fit_cut))
            elite_cut = self.stochastic_selection(fit_cut, hive_cut)
            hive_cut = self.shift_cross(elite_cut)

        # On normalise les valeurs moyennes des scores de fitness afin de pouvoir
        # se les représenter entre 0 et 1
        fit_mean_shift_norm =  self.normalizer(fit_mean_shift)
        fit_mean_cut_norm =  self.normalizer(fit_mean_cut)
        
        # On affiche les résultats dans deux graphiques
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.plot(fit_mean_shift_norm, 'tab:green', label = "Fitness moyen pour le croisement en shift" )
        ax1.set_ylabel('score de fitness moyen')
        ax1.legend()
        ax2.plot(fit_mean_cut_norm, 'tab:orange', label = "Fitness moyen pour le croisement en coupe")
        ax2.set_xlabel('nombre de générations')
        ax2.set_ylabel('score de fitness moyen')
        ax2.legend()
        plt.show()
        
        return fit_mean_shift, fit_mean_cut

