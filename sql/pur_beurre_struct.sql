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
  name TINYTEXT NOT NULL,
  json_id VARCHAR(45) NULL,
  url VARCHAR(90) NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET=utf8;


-- --------------------
-- -- Table Products --
-- --------------------

CREATE TABLE Products (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name TINYTEXT NOT NULL,
  brand TINYTEXT NULL,
  description TEXT NULL,
  nutriscore CHAR(1) NULL,
  category_id INT UNSIGNED NOT NULL,
  places VARCHAR(90) NULL,
  stores VARCHAR(90) NULL,
  barcode VARCHAR(45) NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET=utf8;


-- -------------------
-- -- Table Favoris --
-- -------------------

CREATE TABLE Favoris (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  added_date DATE NOT NULL,
  product_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET=utf8;


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