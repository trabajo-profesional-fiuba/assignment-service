/*=================================================================================
Este script se utiliza para inializar algunos valores por default
Como una categoria y crear un admin.

Este script crea un "superadmin" por default, lo cual DEBE MODIFICARSE LA CONTRASEÑA
una vez que la aplicacion se encuentra en produccion para evitar problemas de 
seguridad en la aplicacion

===================================================================================*/

INSERT INTO categories (name) VALUES ('default') ON CONFLICT (name) DO NOTHING;

INSERT INTO public.users (
    name, last_name, email, password, role
)
SELECT 'admin', 'admin', 'admin@fiuba.com', encode(sha256('admin123'), 'hex'), 'ADMIN'
WHERE NOT EXISTS (
    SELECT 1
    FROM public.users
    WHERE email = 'admin@fiuba.com'
);
