USE `mystery_house`;

CREATE VIEW `users_quantity` AS SELECT COUNT(1) AS `count` FROM `players`;