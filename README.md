# Sello API

Backend de Sello (front en Vue, repositorio aparte): login con JWT y administración de usuarios por perfiles. Django + Django REST Framework.

Cada **perfil** define qué **herramientas** (pestañas del front) puede usar; cada **usuario** tiene un perfil. Los superusuarios ven todo. Todo se administra en `/admin/`.

## Desarrollo

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver 0.0.0.0:8000   # admin en http://localhost:8000/admin/
.venv/bin/python manage.py test
```

Sin `DATABASE_URL` se usa SQLite local.

## API

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/login/` | `{username, password}` → `{access, refresh, usuario}` |
| POST | `/api/auth/refresh/` | `{refresh}` → `{access}` |
| GET | `/api/auth/yo/` | Usuario actual con su perfil y herramientas (requiere `Authorization: Bearer <access>`) |

El slug de cada Herramienta debe coincidir con el `id` de la pestaña en `src/App.vue` del front (`marca`, `ocr`).

## Despliegue en Vercel

1. Importa el repo en Vercel con Framework Preset **Other**.
2. Storage → crea una base **Neon (Postgres)** y conéctala (agrega `DATABASE_URL`).
3. Variables de entorno:
   - `DJANGO_SECRET_KEY`: `python3 -c "import secrets;print(secrets.token_urlsafe(50))"`
   - `DJANGO_DEBUG=0`
   - `DJANGO_ALLOWED_HOSTS`: dominio del backend, p. ej. `sello-api.vercel.app`
   - `CORS_ALLOWED_ORIGINS`: URL del front, p. ej. `https://sello.vercel.app`
4. Crea las tablas y el admin desde tu máquina:
   ```bash
   DATABASE_URL='postgresql://...' .venv/bin/python manage.py migrate
   DATABASE_URL='postgresql://...' .venv/bin/python manage.py createsuperuser
   ```
5. En el proyecto del front define `VITE_API_URL` con la URL del backend y vuelve a desplegar.
