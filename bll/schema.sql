-- (c) Copyright 2015-2016 Hewlett Packard Enterprise Development LP

CREATE TABLE IF NOT EXISTS `preferences` (
    `username`   VARCHAR(255) NOT NULL,
    `prefs`      TEXT         NOT NULL,

    PRIMARY KEY (`username`)
);

CREATE TABLE IF NOT EXISTS `eula` (
    `accepted`   TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS `jobs` (
    `id`                VARCHAR(255) NOT NULL,
    `updated_at`        DATETIME     NOT NULL,
    `status`            TEXT         NOT NULL,

    PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `install`;

DROP TABLE IF EXISTS `plugin`;
