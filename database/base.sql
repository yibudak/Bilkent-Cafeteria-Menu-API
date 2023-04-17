-- Adminer 4.8.1 MySQL 5.5.5-10.6.12-MariaDB-0ubuntu0.22.04.1 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE DATABASE `bilkentkafemud_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `bilkentkafemud_db`;

DROP TABLE IF EXISTS `daily_menus`;
CREATE TABLE `daily_menus` (
  `create_date` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `english_name` varchar(50) DEFAULT NULL,
  `nutrition_facts` text DEFAULT NULL,
  `menu_type` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `meals`;
CREATE TABLE `meals` (
  `create_date` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text DEFAULT NULL,
  `english_name` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `meal_menu_rel`;
CREATE TABLE `meal_menu_rel` (
  `meal_id` int(11) DEFAULT NULL,
  `menu_id` int(11) DEFAULT NULL,
  KEY `meal_id` (`meal_id`),
  KEY `menu_id` (`menu_id`),
  CONSTRAINT `meal_menu_rel_ibfk_1` FOREIGN KEY (`meal_id`) REFERENCES `meals` (`id`),
  CONSTRAINT `meal_menu_rel_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `daily_menus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2023-04-17 23:02:18
