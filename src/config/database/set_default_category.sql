INSERT INTO categories (name)
VALUES ('default')
ON CONFLICT (name) DO NOTHING;
