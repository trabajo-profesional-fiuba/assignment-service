INSERT INTO categories (name) VALUES ('default') ON CONFLICT (name) DO NOTHING;

INSERT INTO public.users (
    name, last_name, email, password, role
)
SELECT 'admin', 'admin', 'alejovillores@gmail.com', encode(sha256('admin123'), 'hex'), 'ADMIN'
WHERE NOT EXISTS (
    SELECT 1
    FROM public.users
    WHERE email = 'alejovillores@gmail.com'
);
