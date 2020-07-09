# Utilisez les données publiques de l'OpenFoodFacts

La Startup **Pur Beurre** travaille connait bien les habitudes alimentaires françaises. Leur restaurant, Ratatouille, remporte un succès croissant et attire toujours plus de visiteurs sur la butte de Montmartre.

L'équipe a remarqué que leurs utilisateurs voulaient bien changer leur alimentation mais ne savaient pas bien par quoi commencer. Remplacer le Nutella par une pâte aux noisettes, oui, mais laquelle ? Et dans quel magasin l'acheter ? Leur idée est donc de créer un programme qui interagirait avec la base Open Food Facts pour en récupérer les aliments, les comparer et proposer à l'utilisateur un substitut plus sain à l'aliment qui lui fait envie.

## Base de données "Pur_beurre"

Pour ce projet, le choix du **SGBDR** s'est porté sur **MySQL**. Dans le cas présent, la base nommée "**pur_beurre**" est stockée sur une machine virtuelle Linux (**Ubuntu Server 18.04**), hébergée elle-même sur un serveur **HP Proliant** (accessible localement). Bien entendu, il est possible d'utiliser l'application avec une base de donnée stockée localement, il faudra alors le spécifier dans les constantes (**./constants.py**).

### Structure :

![MPD.PNG](https://github.com/Eidocode/OC_Project5/blob/master/ressources/MPD.png)

La base de données est composée de 3 tables : 

 - **Categories** : Contient les catégories récupérées depuis la base OpenFoodFacts et selon les critères définis dans le code

|Field           |Type                   |NULL  | KEY    |DEFAULT |EXTRA          |
|----------------|-----------------------|------|--------|--------|---------------|
|id              |INT(10), Unsigned      |NO    |PRI     |NULL    |Auto_increment |
|name            |TINYTEXT               |NO    |        |NULL    |               |
|json_id         |VARCHAR(90)            |YES   |        |NULL    |               |
|url             |VARCHAR(150)           |YES   |        |NULL    |               |

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
|added_date      |DATETIME               |NO    |        |CUR_TIME|               |
|product_id      |INT(10), Unsigned      |NO    |UNI     |NULL    |               |

Deux clés étrangères sont créées pour lier nos différentes tables : 

 - **fk_categories_id** :  Lie la valeur **category_id** de la table **Products** à la valeur référence **id** de la table **Categories**.
 - **fk_products_id** :  Lie la valeur **product_id** de la table **Favoris** à la valeur référence **id** de la table **Products**.

### Script :

Un script **SQL** comportant la création de la structure est accessible depuis ("**./SQL/pur_beurre_struct.sql**"). Ce script est autonome mais nécessite d'être exécuté depuis un compte possédant les droits en écriture sur "**pur_beurre.***".
m
Attribuer les droits sur la base pur_beurre depuis la console **MySQL** : 

    GRANT ALL PRIVILEGES ON pur_beurre.* TO '[login]'@'localhost' IDENTIFIED BY '[password]' WITH GRANT OPTION;
Si la base est hébergée sur une machine différente, il faudra remplacer '**localhost**' par '**%**'.

Exécution du script **SQL** depuis la console **MySQL** :

    SOURCE pur_beurre_struct.sql

Cela implique que la console **MySQL** soit lancée depuis le même chemin que le script **SQL**. Sinon, il faudra spécifier le chemin lors de l'exécution.


## Application

_Les dépendances nécessaires à l'exécution de l'application se trouvent dans le fichier **./requirements.txt**. Elles peuvent être installées automatiquement (de préférence dans un environnement virtuel python) de la façon suivante :_

	pip3 install -r requirements.txt

### Packages :

L'application est composée de 3 différents packages **Api**, **Model** et **Database**.

- **Api** :  Contient deux classes **Api_Handler_Categories** et **Api_Handler_Products** dédiées à la manipulation des catégories et produits  côté API.

- **Model** :  Contient deux classes **Category** et **Product** chargées de la gestion des catégories et produits côté base de données. Elles permettent notamment de retourner un ou plusieurs éléments de la base de données (Get), voir d'ajouter un ou plusieurs éléments à celle-ci (Set) selon certains critères définis.

- **Database** :  Contient une classe **DatabaseManager** qui sera instanciée lorsqu'il sera nécessaire de communiquer avec la base SQL pour récupérer des éléments (méthode **get_query**) ou en ajouter (méthode **set_query**).


### Controller : 

Le controller **./controller.py** est constitué d'une classe chargée de faire communiquer tous les éléments de l'application. Il s'occupe par exemple de récupérer les éléments de l'Api (par l'intermédiaire du package **Api**), puis de les injecter dans la base de données (par l'intermédiaire des packages **Model** et **Database**). Toute la logique nécessaire au fonctionnement de l'application s'y trouve.


### State : 

Cette classe (en plus de la classe **State_machine** située dans le même fichier) est utilisée pour faciliter la gestion des états dans l'application et notamment la transition entre celles-ci. On peut retrouver les états suivants : **IDLE**, **SHOW_CATEGORIES**, **SHOW_PRODUCTS**, **SHOW_FAVORITES**.


### Interfaces : 

L'application contient deux interfaces utilisateurs qui, se reposant sur le controller, proposent les mêmes fonctionnalités. Une première en mode **"terminal"** (**./terminal_view.py**) , et une autre, **"graphique"** (**./ui_view.py**).

- **Terminal** :  Depuis cette interface, l'utilisateur interagit grâce aux touches de son clavier. Le menu lui indique quelles sont ses possibilités, il saisit alors son choix qui se fait exclusivement via le pavé numérique.

- **GUI** :  L'interface graphique propose donc, par l'intermédiaire d'une classe **Application**,  les mêmes fonctionnalités que la version **terminal**. La différence étant qu'elle est affichée dans une fenêtre à l'image du système d'exploitation. L'utilisateur interagit ici majoritairement avec sa souris grâce à des boutons et des listes à parcourir notamment. La bibliothèque **Tkinter** (intégrée nativement à Python) est utilisée ici pour dessiner et disposer les éléments de l'interface graphique.

- **Main** :  L'exécution de l'application s'effectue par l'intermédiaire du fichier **./main.py**. Un menu propose ici, à l'utilisateur, de choisir entre la version "**Terminal**" ou "**Graphique**" de l'application. L'action est exécutée selon le choix effectué.

