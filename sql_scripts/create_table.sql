USE `mystery_house`;

CREATE TABLE IF NOT EXISTS `players` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `user_id` INT(11) NOT NULL,
    `name` VARCHAR(50),
    `progress` VARCHAR(20),
    `events` VARCHAR(50),
    PRIMARY KEY(`id`)
);