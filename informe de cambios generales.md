pip install django-cors-headers

NECESITAMOS ESA SUB LIBRERIRA DE DJANGO PARA QUE EL API NO RECHASE LAS PETICIONES AL FORNTED {REFLEX}




-----------------------------------------------------------------
# MODIFICACIONES QUE NECESTIO HAGAS EN SETTIGN

# En settings.py

INSTALLED_APPS = [
    # ... tus otras apps ...
    'corsheaders',  # <--- Agrega esto
    'inventario',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # <--- ¡Crucial! Antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ... resto de middleware ...
]

# Al final del archivo, permite el tráfico (para desarrollo):
CORS_ALLOW_ALL_ORIGINS = True