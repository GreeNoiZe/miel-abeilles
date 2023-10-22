# miel-abeilles
Genetic algorithm study

Le programme miel-abeille est une classe dont l'appel génère un algorithme génétique qui simule plusieurs générations d'abeilles
au travers de diverses sélections. Le principe d'un tel algorithme repose sur un ensemble de données de départ qui constituent une population dont chaque membre a un génome. En fonction de la nature du problème on détermine la performance des génomes de la population grâce au 'score de fitness'. On opère ensuite une sélection des individus sur la population, cette sélection peut être caractérisée de diverses manières. Dans notre cas on a choisi une sélection aléatoire en attribuant une probabilité de choix plus importante aux individus les plus performants. Après cette étape on fait un croisement depuis la population sélectionnée afin d'obtenir de nouveaux individus et reconstituer une population avec une meilleure performance, c'est la nouvelle génération. Dans notre cas on a opté pour deux types de croisement, le croisement par simple enjambement et le croisement par décalage de génome. Le croisement par simple enjambement consiste, à partir de deux parents, à coller deux blocs de génomes de parents différents qu'on a coupé au même endroit.

on obtient alors un nouvel individu avec des caractéristiques meilleures.

On recommence le processus jusqu'au point d'arrêt choisi. Au bout d'un certain temps la performance des individus peut avoir tendance à stagner et on peut avoir recours à une mutation. 

de même nombre avec une performance 


Dans notre cas on a utilisé la sélection par simple enjambement qui consiste, à partir de deux parents, à coller deux blocs de génomes qu'on a coupé au même endroit, chaque bloc appartenant à l'un des parents. On obtient alors un nouvel individu avec des caractéristiques 
