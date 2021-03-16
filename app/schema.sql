-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;
-- DROP TABLE IF EXISTS alert;

-- CREATE TABLE user (
--   id TEXT PRIMARY KEY,
--   username TEXT NOT NULL,
--   email TEXT UNIQUE NOT NULL
-- );

-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );

-- CREATE TABLE alert (
--   id INTEGER PRIMARY KEY,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   email  TEXT NOT NULL,
--   title  TEXT NOT NULL,
--   message TEXT NOT NULL,
--   schedule DATETIME NOT NULL,
--   sent BOOLEAN DEFAULT FALSE,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );