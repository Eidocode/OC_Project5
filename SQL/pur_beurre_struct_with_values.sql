SET NAMES utf8;

-- -------------------------
-- -- Database pur_beurre --
-- -------------------------

CREATE DATABASE IF NOT EXISTS pur_beurre;
USE pur_beurre;

ALTER TABLE Products DROP FOREIGN KEY fk_categories_id;
ALTER TABLE Favoris DROP FOREIGN KEY fk_products_id;

DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Favoris;


-- ----------------------
-- -- Table Categories --
-- ----------------------

CREATE TABLE Categories (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  json_id VARCHAR(45) NULL,
  url VARCHAR(90) NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB AUTO_INCREMENT = 6 DEFAULT CHARSET=utf8;

LOCK TABLES Categories WRITE;
INSERT INTO Categories VALUES
	(1, 'macaroni', 'fr:macaroni', 'https://fr.openfoodfacts.org/categorie/macaroni'),
	(2, 'jus-d-orange-sans-pulpe', 'fr:jus-d-orange-sans-pulpe', 'https://fr.openfoodfacts.org/categorie/jus-d-orange-sans-pulpe'),
	(3, 'Filets de harengs', 'fr:filets-de-harengs', 'https://fr.openfoodfacts.org/categorie/filets-de-harengs'),
	(4, 'Sauces tomates au basilic', 'fr:sauces-tomates-au-basilic', 'https://fr.openfoodfacts.org/categorie/sauces-tomates-au-basilic'),
	(5, 'Compotes pommes banane', 'fr:compotes-pommes-banane', 'https://fr.openfoodfacts.org/categorie/compotes-pommes-banane');
UNLOCK TABLES;


-- --------------------
-- -- Table Products --
-- --------------------

CREATE TABLE Products (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  brand VARCHAR(45) NULL,
  description TEXT NULL,
  nutriscore CHAR(1) NULL,
  category_id INT UNSIGNED NOT NULL,
  location VARCHAR(90) NULL,
  barcode VARCHAR(45) NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB AUTO_INCREMENT = 13 DEFAULT CHARSET=utf8;

LOCK TABLES Products WRITE;
INSERT INTO Products VALUES
	(1, 'Pâtes Maccheroni', 'Barilla', 'Pâtes alimentaires au blé dur', 'A', 1, 'Plaisir,France,Paris', '8076808050440'),
	(2, 'Macaroni (Maxi Format)', 'Panzani', 'Pâtes alimentaires au blé dur de qualité supérieure', 'A', 1, 'Villers Bocage 80260,France', '3038350023100'),
	(3, 'Macaroni coupés', 'Tous les jours', 'Pâtes alimentaires', 'A', 1, 'Seynod,France', '3700311800227'),
	(4, 'Macaroni aux œufs frais', 'Lustucru', 'Pâtes alimentaires aux œufs frais', 'A', 1, 'Belle-Epine', '3073190101069'),
	(5, 'Jus d\'orange sans pulpe', 'Franprix', 'Jus d\'orange du matin sans pulpe', 'C', 2, '', '3263858459810'),
	(6, 'Jus d\'orange du matin sans pulpe', 'Joker', 'Jus D\'orange 100% Sans Pulpe', 'B', 2, 'Bordeaux,France', '3123349013870'),
	(7, 'Filets de hareng à la crème', 'Baltic', 'Filets de hareng à la crème, Recette traditionnelle d\'Alsace', 'D', 3, 'Leclerc, France', '3052420004004 '),
	(8, 'Filets De Hareng Fumes', 'Simon', NULL, 'D', 3, NULL, '3262335000088'),
	(9, 'Tomate, Ricotta, Basilic', 'Monoprix Gourmet', 'Sauce Tomate, Ricotta, Basilic', 'D', 4, 'Monoprix, France', '3350033419391'),
	(10, 'Pasta sauce', 'Grand Jury', 'Sauce tomate cuisinée au basilic', 'A', 4, 'Carrefour, Proxi, 8 à Huit, France', '3560070674558'),
	(11, 'Assortiment de compotes multi variétés', 'Douceur du Verger', 'Compote de pommes allegee en sucres*: purée de pommes 96%, sucre, antioxydant: acide ascorbique. dessert de fruits pomme - peche: purée de pommes 73%, purée de pêches 19%, sucre, antioxydant: acide ascorbique. dessert de fruits pomme - banane: purée de pommes 73%, purée de bananes 22%, sucre, antioxydant: acide ascorbique, correcteur d\'acidité: acide citrique. specialite de fruits pomme - abricot, aromatisée : purée de pommes 72%, purée d\'abricots concentrée 25%, sucre, antioxydant: acide ascorbique, arôme naturel.', 'A', 5, 'Leclerc, France', '3564700750186 '),
	(12, 'Compote Pomme Banane', 'Andros', 'Pommes 75 %, bananes 20 %, antioxydant : acide ascorbique', 'A', 5, NULL, '3608580006664');
UNLOCK TABLES;


-- -------------------
-- -- Table Favoris --
-- -------------------

CREATE TABLE Favoris (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  added_date DATE NOT NULL,
  product_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB AUTO_INCREMENT = 2 DEFAULT CHARSET=utf8;

LOCK TABLES Favoris WRITE;
INSERT INTO Favoris VALUES
	(1, '2020-05-01', 2);
UNLOCK TABLES;


-- ------------------
-- -- FOREIGN KEYS --
-- ------------------

ALTER TABLE Products
	ADD CONSTRAINT fk_categories_id
	FOREIGN KEY (category_id)
	REFERENCES Categories (id)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION;

ALTER TABLE Favoris
	ADD CONSTRAINT fk_products_id
	FOREIGN KEY (product_id)
	REFERENCES Products (id)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION;