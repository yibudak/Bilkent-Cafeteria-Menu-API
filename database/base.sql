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
  `date` date DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `english_name` varchar(50) DEFAULT NULL,
  `menu_type` text DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `meals`;
CREATE TABLE `meals` (
  `name` text DEFAULT NULL,
  `english_name` text DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `meal_menu_rel`;
CREATE TABLE `meal_menu_rel` (
  `meal_id` int(11) DEFAULT NULL,
  `menu_id` int(11) DEFAULT NULL,
  `sequence` int(11) DEFAULT NULL,
  KEY `meal_id` (`meal_id`),
  KEY `menu_id` (`menu_id`),
  CONSTRAINT `meal_menu_rel_ibfk_1` FOREIGN KEY (`meal_id`) REFERENCES `meals` (`id`),
  CONSTRAINT `meal_menu_rel_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `daily_menus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `nutrition_facts`;
CREATE TABLE `nutrition_facts` (
  `energy` varchar(50) DEFAULT NULL,
  `fat` varchar(50) DEFAULT NULL,
  `carbohydrate` varchar(50) DEFAULT NULL,
  `protein` varchar(50) DEFAULT NULL,
  `menu_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_id` (`menu_id`),
  CONSTRAINT `nutrition_facts_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `daily_menus` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `uid` varchar(16) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `user_meal_rel`;
CREATE TABLE `user_meal_rel` (
  `meal_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  KEY `meal_id` (`meal_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_meal_rel_ibfk_1` FOREIGN KEY (`meal_id`) REFERENCES `meals` (`id`),
  CONSTRAINT `user_meal_rel_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- 2023-04-24 18:34:39