INSERT INTO categories (name) VALUES ('default') ON CONFLICT (name) DO NOTHING;

INSERT INTO public.users(
	name, last_name, email, password, role)
	VALUES ('admin', 'admin', 'alejovillores@gmail.com', encode(sha256('admin123'), 'hex'), 'ADMIN')
    ON CONFLICT (id) DO NOTHING;;