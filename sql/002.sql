BEGIN;
CREATE TABLE `Chapter` (
    `id` varchar(32) NOT NULL PRIMARY KEY,
    `title` varchar(255) NOT NULL UNIQUE,
    `create` integer UNSIGNED NOT NULL,
    `update` integer UNSIGNED NOT NULL,
    `status` smallint NOT NULL,
    `content` text
)
ENGINE=InnoDB DEFAULT CHARSET=utf8
;
CREATE INDEX `chapter_title` ON `Chapter` (`title`);
CREATE INDEX `chapter_create` ON `Chapter` (`create`);
CREATE INDEX `chapter_update` ON `Chapter` (`update`);
CREATE INDEX `chapter_status` ON `Chapter` (`status`);
COMMIT;