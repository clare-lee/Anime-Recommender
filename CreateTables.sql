CREATE DATABASE Recommender; 
USE Recommender;

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `first_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) AUTO_INCREMENT = 50;

CREATE TABLE `log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` text,
  `date` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `log_user_fk_idx` (`user_id`),
  CONSTRAINT `log_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
);

CREATE TABLE `favs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` text COLLATE utf32_unicode_ci,
  `date` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fav_user_fk_idx` (`user_id`),
  CONSTRAINT `fav_user_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
);

CREATE TABLE `anime` (
  `anime_id` int NOT NULL,
  `name` varchar(250) NOT NULL,
  `genre` varchar(250) NOT NULL,
  `medium` varchar(150) NOT NULL,
  `episodes` varchar(45) NOT NULL,
  `rating` float NOT NULL,
  `binary_genres` varchar(150) NOT NULL,
  `members` int NOT NULL,
  PRIMARY KEY (`anime_id`)
);

Create TABLE `rating` (
  `user_id` int NOT NULL,
  `anime_id` int NOT NULL,
  `rating` int NOT NULL,
  PRIMARY KEY(`user_id`, `anime_id`)
);

commit;

INSERT INTO `user`(`email`,`password`,`first_name`) VALUES('testuser@test.com', 'sha256$EcUXHo7fqvRSjuq3$d9e050dd4f2d03eb536161d1d98e16e3eaa365d6e100c333df555851b1fe247d', 'Test');

LOAD DATA LOCAL INFILE 'anime.csv' INTO TABLE anime FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
LOAD DATA LOCAL INFILE 'ratings.csv' INTO TABLE rating FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 LINES;
