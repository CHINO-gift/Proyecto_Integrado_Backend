# Sistema de Gestión de Delegaciones Municipales

Proyecto desarrollado en Django para la gestión y visualización de delegaciones municipales y sus funcionarios.

El sistema permite administrar la información mediante Django Admin y visualizar los registros almacenados en una base de datos relacional mediante templates de Django y Bootstrap.

## Tecnologías utilizadas

- Python 3.14
- Django 6.1
- MySQL / MariaDB
- Django ORM
- Bootstrap
- Gunicorn
- Nginx
- phpMyAdmin
- Git y GitHub
- AWS EC2

## Aplicaciones Django

El proyecto está compuesto por dos aplicaciones principales:

- `delegacionesApp`: gestión de las delegaciones municipales.
- `funcionariosApp`: gestión de funcionarios y su relación con las delegaciones.

## Modelo de datos

### Delegación

Almacena:
- Nombre
- Sector
- Descripción

### Funcionario

Almacena:
- Nombre
- Cargo
- Delegación
- Meta
- Avance

Cada funcionario pertenece a una delegación mediante una relación `ForeignKey`.

## Configuración

El proyecto utiliza variables de entorno para proteger información sensible.

Se incluye `.env.example` como referencia para configurar:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- Motor de base de datos
- Nombre de base de datos
- Usuario
- Contraseña
- Host
- Puerto

El archivo `.env` real está excluido del repositorio mediante `.gitignore`.

## Instalación

Clonar el repositorio:

    git clone https://github.com/CHINO-gift/Proyecto_Integrado_Backend.git
    cd Proyecto_Integrado_Backend

Crear y activar el entorno virtual:

    python3 -m venv venv
    source venv/bin/activate

Instalar dependencias:

    pip install -r requirements.txt

Configurar el archivo `.env` utilizando `.env.example` como referencia.

Aplicar las migraciones:

    python manage.py migrate

## Carga de datos

Los datos utilizados originalmente en archivos JSON pueden migrarse a la base de datos relacional mediante:

    python cargar_datos.py

## Django Admin

Para crear un administrador:

    python manage.py createsuperuser

Django Admin permite realizar operaciones CRUD sobre las entidades del sistema, además de búsqueda y filtrado de registros.

## Ejecución en desarrollo

    python manage.py runserver

## Despliegue en AWS

La aplicación fue desplegada en una instancia AWS EC2 utilizando:

- Amazon Linux
- Python y entorno virtual
- Gunicorn como servidor WSGI
- Nginx como servidor web y proxy inverso
- MariaDB como base de datos
- phpMyAdmin para administración y verificación de la base de datos

Gunicorn se ejecuta mediante `systemd` y Nginx recibe las solicitudes HTTP y las redirige hacia la aplicación Django.

## Funcionalidades

- Visualización de delegaciones.
- Visualización de funcionarios.
- Consultas mediante Django ORM.
- Relación entre funcionarios y delegaciones.
- Administración de registros mediante Django Admin.
- Operaciones CRUD.
- Búsqueda y filtrado.
- Interfaz desarrollada con Bootstrap.
- Visualización de metas y avances.
- Persistencia en base de datos relacional.

## Autor

José Ignacio Villalobos

Proyecto académico desarrollado para la asignatura de Backend.
