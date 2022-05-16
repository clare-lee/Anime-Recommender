CREATE TABLE `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(150) DEFAULT NULL,
  `first_name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
);

CREATE TABLE `Log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` text,
  `date` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `log_user_fk_idx` (`user_id`),
  CONSTRAINT `log_user_fk` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
);

CREATE TABLE `Favs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data` text COLLATE utf32_unicode_ci,
  `date` datetime DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fav_user_fk_idx` (`user_id`),
  CONSTRAINT `fav_user_fk` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
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

commit;

