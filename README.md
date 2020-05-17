# Utilisez les données publiques de l'OpenFoodFacts

La Startup **Pur Beurre** travaille connait bien les habitudes alimentaires françaises. Leur restaurant, Ratatouille, remporte un succès croissant et attire toujours plus de visiteurs sur la butte de Montmartre.

L'équipe a remarqué que leurs utilisateurs voulaient bien changer leur alimentation mais ne savaient pas bien par quoi commencer. Remplacer le Nutella par une pâte aux noisettes, oui, mais laquelle ? Et dans quel magasin l'acheter ? Leur idée est donc de créer un programme qui interagirait avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

## Base de données "Pur_beurre"

Pour ce projet, le choix du **SGBDR** s'est porté sur **MySQL**. Dans le cas présent, la base nommée "**pur_beurre**" est stockée sur une machine virtuelle Linux (**Ubuntu Server 18.04**), hébergée elle-même sur un serveur **HP Proliant** (accessible depuis mon réseau local). Bien entendu, il est possible d'utiliser l'application avec une base de donnée stockée localement, il faudra alors le spécifier dans les constantes (**./constants.py**).

### Structure :

![MPD.PNG](https://github.com/Eidocode/OC_Project5/blob/bdd/Ressources/MPD.png)

La base de données est composée de 3 tables : 

 - **Categories** : Contient les catégories récupérées depuis la base OpenFoodFacts et selon les critères définis dans le code

|Field           |Type                   |NULL  | KEY    |DEFAULT |EXTRA          |
|----------------|-----------------------|------|--------|--------|---------------|
|id              |INT(10), Unsigned      |NO    |PRI     |NULL    |Auto_increment |
|name            |TINYTEXT               |NO    |        |NULL    |               |
|json_id         |VARCHAR(45)            |YES   |        |NULL    |               |
|url             |VARCHAR(90)            |YES   |        |NULL    |               |

 - **Products** : Contient les produits récupérés contenus dans les différentes catégories de la table précédente.

|Field           |Type                   |NULL  | KEY    |DEFAULT |EXTRA          |
|----------------|-----------------------|------|--------|--------|---------------|
|id              |INT(10), Unsigned      |NO    |PRI     |NULL    |Auto_increment |
|name            |TINYTEXT               |NO    |        |NULL    |               |
|brand           |TINYTEXT               |YES   |        |NULL    |               |
|description     |TEXT                   |YES   |        |NULL    |               |
|nutriscore      |CHAR(1)                |YES   |        |NULL    |               |
|category_id     |INT(10), Unsigned      |NO    |MUL     |NULL    |               |
|places          |VARCHAR(90)            |YES   |        |NULL    |               |
|stores          |VARCHAR(90)            |YES   |        |NULL    |               |
|barcode         |VARCHAR(45)            |NO    |        |NULL    |               |

 - **Favoris** : Cette base contiendra principalement l'ID des produits ajoutés en tant que Favoris par l'utilisateur final. 

|Field           |Type                   |NULL  | KEY    |DEFAULT |EXTRA          |
|----------------|-----------------------|------|--------|--------|---------------|
|id              |INT(10), Unsigned      |NO    |PRI     |NULL    |Auto_increment |
|added_date      |DATE                   |NO    |        |NULL    |               |
|product_id      |INT(10), Unsigned      |NO    |MUL     |NULL    |               |

Deux clés étrangères sont créées pour lier nos différentes tables : 

 - **fk_categories_id** :  Lie la valeur **category_id** de la table **Products** à la valeur référence **id** de la table **Categories**.
 - **fk_products_id** :  Lie la valeur **product_id** de la table **Favoris** à la valeur référence **id** de la table **Products**.

### Script :

Un script **SQL** comportant la création de la structure est accessible depuis ("**./SQL/pur_beurre_struct.sql**"). Ce script est autonome mais nécessite d'être exécuté depuis un compte possédant les droits en écriture sur "**pur_beurre.***".

Attribuer les droits sur la base pur_beurre depuis la console **MySQL** : 

    GRANT ALL PRIVILEGES ON pur_beurre.* TO '[login]'@'localhost' IDENTIFIED BY '[password]' WITH GRANT OPTION;
Si la base est hébergée sur une machine différente, il faudra remplacer '**localhost**' par '**%**'.

Exécution du script **SQL** depuis la console **MySQL** :

    SOURCE pur_beurre_struct.sql

Cela implique que la console **MySQL** soit lancée depuis le même chemin que le script **SQL**. Sinon, il faudra spécifier le chemin lors de l'exécution.

### Ajout des catégories dans la base :

L'ajout des catégories dans la base se fait par l'intermédiaire de deux fichiers python "**./category.py**" et "**./inject_categories.py**".

 - **./category.py** : 
 Contient la classe **Category**, utilisée pour sélectionner les catégories qui seront injectées dans la Table **Categories** de la base. La méthode **_get_categories** se charge de récupérer la liste des différentes catégories depuis l'URL https://fr.openfoodfacts.org/categories.json. Les catégories sont ici filtrées, notamment pour ne garder que celles dont la clé ['id'] commence par '**fr**' et également celles qui ont un total de produits minimum (il est de 100 par défaut, à voir si nous le rendrons plus dynamique par la suite dans l'application). Une fois filtrées, la méthode **get_random_categories** sélectionne (aléatoirement) un nombre de catégorie défini en paramètre lors de l'instanciation de la classe.  
 
 - **./inject_categories.py** :
 C'est dans ce fichier que se fait l'instanciation de la classe **Category**, c'est également par l'intermédiaire de celui-ci que nous pouvons nous connecter à la base et y injecter les catégories par l'intermédiaire de requêtes SQL. 

### Ajout des produits dans la base :

A l'instar des catégories, l'ajout des produits se fait par l'intermédiaire de deux fichiers python "**./products.py**" et "**./inject_products.py**".

 - **./products.py** : 
Contient la classe **Product**, utilisée pour retourner un produit lors de l'instanciation qui pourra par la suite être injecté dans la Table **Products** de la base. La méthode **_get_products** se charge de récupérer les produits contenus visibles depuis l'URL (**exemple** :  https://fr.openfoodfacts.org/categorie/sauces-tomates-au-basilic.json) renseignée en paramètre lors de l'instanciation de la classe. 
Les produits sont affichés par 20, pour accéder aux suivants, il est nécessaire de changer de page (l'exemple ci-dessus permet d'accéder à la première page). Pour cela, il est nécessaire de modifier l'URL pour indiquer une page différente, si nous reprenons l'exemple précédent, il faudra ajouter "**/2**" avant "**.json**". L'algorithme se charge donc de récupérer le nombre de produits total contenus dans la catégorie que l'on divise par 20. L'arrondi supérieur du résultat obtenu permet alors d'obtenir le nombre de page que la catégorie contient. Un numéro de page est alors défini aléatoirement afin de récupérer la liste des produits qu'elle contient. Un produit est alors sélectionné (également aléatoirement) dans cette liste.

 - **./inject_products.py** : 
L'instanciation de la classe **Product** se fait dans ce fichier. Ce fichier se connecte à la base pour notamment récupérer la liste des catégories préalablement injectées. Le champ **url** des catégories est utilisé lors de l'instanciation de la classe, les produits récupérés sont alors injectés dans la base.
Plusieurs tests sont effectués dans ce fichier, notamment pour vérifier que le produit n'est pas déjà présent dans la base pour éviter les doublons. Certains produits (très peu) sont apparus sans nom dans le **JSON**, ce qui peut poser problème pour l'application... Ces produits sont donc filtrés pour éviter un problème éventuel. 
Le nombre de produits à injecter dans la base est maintenant défini dans ce fichier (dans la version précédente, c'était géré par la classe **Products**). 
Lorsque le script rencontre une erreur dans les tests, il essaye de trouver un autre produit "éventuellement" conforme. Au bout de 3 essais, l'itération est passée. Si le script devait récupérer 10 produits, il y en aura donc un de moins etc...