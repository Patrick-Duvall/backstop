INSERT INTO user (username, email, id)
VALUES
  ('test', 'test@test.com', 'abc123'),
  ('test2', 'test2@test.com', 'abcd123');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');

INSERT INTO alert (title, email, message, schedule, author_id, created, sent)
VALUES
  ('test title', 'test@test.com', 'test message', '2020-01-01 00:00:00', 'abc123', '2018-01-01 00:00:00', false);