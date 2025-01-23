# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

### Setup Docker ###
Pour lancer le serveur qui nous sert d'API, j'ai tout d'abord configuré le Dockerfile qui récupère le fichier requirement.txt et l'installe sur une image python 3.11. Il suffit donc d'exécuter la commande "**docker build -t XXX**" (_XXX représentant un nom quelconque donné à l'image_) pour construire l'image Docker, puis, d'exécuter la commande "**docker run -p 8000:8000 XXX**" pour démarrer le serveur dans le container.

### Lancement du pipeline ###
Pour démarrer le pipeline de données, il suffit d'exécuter la commande "**python script.py**". Le pipeline s'éxecute une fois par jour, et stocke les données générées dans la base de données SQLite nommée **ma_base_de_donnee.db**, le contenu de cette dernière est ensuite print sur le terminale.

### Lancement des tests ###
Pour lancer les tests, il faut exécuter la commande "**python -m pytest test/**" à la racine du projet (_exécuter uniquement pytest à la racine du projet ne fonctionnait pas pour moi_).

## Questions (étapes 4 à 7)

### Étape 4
![image](https://github.com/user-attachments/assets/c5a8b8d2-a4e3-4c00-adaa-067ede7051e0)

Pour stocker les informations retournées par l'API, je recommande l'utilisation d'une base de données relationnelle de diagramme UML ci-dessus. J'ai fait ce choix parceque, dans ce context, l'utilisation des relations entre les tables est indispensable : les historiques sont liés aux utilisateurs.

### Étape 5

Pour surveiller la santé du pipeline, il faudrait ajouter des logs (avec timestamps) à chaque accès de la base de données, de ce fait, la moindre erreur ou bug serait identifiable. Les métrique clés sont la quantité de données dans la table 'Historique' et le temps d'exécution du pipeline. Les entrées de cette table sont une corrélation direct entre les tables Utilisateurs et Musiques, ce qui signifie que plus il y a d'utilisateurs et de musiques, plus la table Historique à une forte probabilité d'avoir un nombre d'entrées bien supérieur à ces deux tables. De plus, si le temps d'execution du pipeline est anormalement rapide, cela signifirais que les données sont potentiellement mal récupérées et/ou mal formattées. Et s'il est anormalement long, cela signifirais qu'il y a un probleme au niveau de l'API.

### Étape 6

Pour automatiser le calcul des recommandations, j'utiliserais un modèle de recommandation qui se base sur l'historique (et potentiellement la géolocalisation) de l'utilisateur. On aurait donc un pipeline de données qui récupère les historiques stockés dans la base de données, qui les formatte pour qu'elle conviennent au modèle de recommandation, et qui recupère via une api les prédiciton du modèle.

### Étape 7

Pour automatiser le réentrainement, j'executerais un pipeline tous les X jours qui récupèrerais les différentes métriques et qui déterminerais l'éfficacité de la prédiction. Par exemple, si seulement un faible pourcentage des musiques suggérées ont été réellement écoutées, alors le réentrainement serait nécessaire. Le réentrainement se ferait donc avec une partie de ces métriques, et le reste serait utilisé pour le tester.

