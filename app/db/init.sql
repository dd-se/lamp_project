CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `firstname` varchar(20) NOT NULL,
  `lastname` varchar(20) NOT NULL,
  `password` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO users (username, firstname, lastname, password) VALUES('marcusg', 'Marcus', 'Gustavsson', 's3cr3t+notreallyhashed');
INSERT INTO users (username, firstname, lastname, password) VALUES('alexd', 'Alex', 'Davidsson', 's3cr3t+notreallyhashed');
INSERT INTO users (username, firstname, lastname, password) VALUES('patrikh', 'Patrik', 'Hansson', 's3cr3t+notreallyhashed');