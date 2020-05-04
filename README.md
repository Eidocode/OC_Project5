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
|name            |VARCHAR(45)            |NO    |        |NULL    |               |
|json_id         |VARCHAR(45)            |YES   |        |NULL    |               |
|url             |VARCHAR(90)            |YES   |        |NULL    |               |

 - **Products** : Contient les produits récupérés contenus dans les différentes catégories de la table précédente.

|Field           |Type                   |NULL  | KEY    |DEFAULT |EXTRA          |
|----------------|-----------------------|------|--------|--------|---------------|
|id              |INT(10), Unsigned      |NO    |PRI     |NULL    |Auto_increment |
|name            |VARCHAR(45)            |NO    |        |NULL    |               |
|brand           |VARCHAR(45)            |YES   |        |NULL    |               |
|description     |TEXT                   |YES   |        |NULL    |               |
|nutriscore      |CHAR(1)                |YES   |        |NULL    |               |
|category_id     |INT(10), Unsigned      |NO    |MUL     |NULL    |               |
|location        |VARCHAR(90)            |YES   |        |NULL    |               |
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

Execution du script **SQL** depuis la console **MySQL** :

    SOURCE pur_beurre_struct.sql

Cela implique que la console **MySQL** soit lancée depuis le même chemin que le script **SQL**. Sinon, il faudra spécifier le chemin lors de l'exécution.