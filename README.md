
# SIGED - Sistema de Gestión de Delegaciones Municipales

## Proyecto Integrado - Evaluación Sumativa N.º 3

- **Asignatura:** Programación Back End (TI3041)
- **Institución:** INACAP, sede La Serena
- **Carrera:** Analista Programador
- **Estudiante:** José Ignacio Villalobos
- **Periodo académico:** Primavera 2026
## 1. Descripción del proyecto

SIGED es una aplicación web desarrollada con Django Framework para la gestión de delegaciones municipales y funcionarios.

El sistema permite administrar información mediante interfaces propias desarrolladas con Django Templates, Bootstrap, formularios Django y Django ORM.

El proyecto corresponde a la evolución de la aplicación desarrollada en la Evaluación Sumativa N.º 2.

En la Evaluación Sumativa N.º 3 se incorporaron:

- Autenticación de usuarios.
- Gestión de roles y permisos.
- Dashboards diferenciados por perfil.
- Mantenedores CRUD completos.
- Gestión de usuarios.
- Recuperación de contraseñas por correo electrónico.
- Una transacción operacional entre dos entidades.
- Validaciones de formularios.
- Despliegue funcional en AWS EC2.

Las operaciones principales se realizan desde las interfaces del sistema, sin depender de Django Admin.

---

## 2. Objetivo del proyecto

Desarrollar una aplicación web que permita consultar y administrar delegaciones municipales y sus funcionarios, incorporando mecanismos de seguridad, control de acceso y persistencia de datos.

### Objetivos específicos

- Centralizar información de las delegaciones.
- Administrar funcionarios y sus asignaciones.
- Implementar operaciones CRUD.
- Controlar el acceso mediante perfiles.
- Proteger las funcionalidades según permisos.
- Permitir recuperar contraseñas de forma segura.
- Ejecutar operaciones sobre entidades relacionadas.
- Mantener los datos en una base de datos relacional.
- Desplegar la aplicación en AWS EC2.

---

## 3. Tecnologías utilizadas

### Backend

- Python.
- Django Framework.
- Django ORM.
- Formularios Django.
- Sistema de autenticación y permisos de Django.

### Frontend

- HTML5.
- CSS3.
- JavaScript.
- Bootstrap.
- Django Templates.

### Base de datos

- MySQL en desarrollo local.
- MariaDB en AWS.
- Motor de almacenamiento InnoDB.

### Infraestructura

- AWS EC2.
- Amazon Linux.
- Gunicorn.
- Nginx.
- HTTPS para el acceso al servidor.

### Herramientas

- Git.
- GitHub.
- Visual Studio Code.
- Entorno virtual de Python.
- Herramientas de inteligencia artificial como apoyo al desarrollo.

---

## 4. Estructura general

El proyecto incluye las siguientes aplicaciones Django:

### delegacionesApp

Permite gestionar delegaciones municipales mediante:

- Registro.
- Listado.
- Búsqueda.
- Consulta de detalles.
- Modificación.
- Eliminación.
- Registro opcional de un funcionario inicial.

### funcionariosApp

Permite gestionar funcionarios mediante:

- Registro.
- Listado.
- Búsqueda.
- Consulta de detalles.
- Modificación.
- Eliminación.
- Asignación de una delegación.
- Gestión de metas y avances.

### config

Contiene la configuración principal de Django, las rutas generales y las funcionalidades de autenticación y navegación correspondientes.

### templates

Contiene las páginas utilizadas por la aplicación, incluyendo:

- Inicio de sesión.
- Recuperación de contraseña.
- Dashboards.
- Gestión de delegaciones.
- Gestión de funcionarios.
- Gestión de usuarios.
- Formularios del sistema.

---

## 5. Autenticación y seguridad

SIGED utiliza el sistema de autenticación proporcionado por Django.

Las funcionalidades implementadas incluyen:

- Inicio de sesión con usuario y contraseña.
- Cierre de sesión.
- Protección de vistas.
- Restricción de acceso según permisos.
- Asignación de grupos.
- Gestión de usuarios desde interfaces propias.
- Recuperación de contraseñas mediante correo electrónico.

Las operaciones sensibles comprueban los permisos en el servidor.

No se depende únicamente de ocultar botones en la interfaz.

---

## 6. Perfiles de usuario

El sistema utiliza tres perfiles principales.

### Administrador

Dispone de acceso completo a las funcionalidades de gestión autorizadas.

Puede:

- Consultar registros.
- Crear delegaciones.
- Modificar delegaciones.
- Eliminar delegaciones.
- Crear funcionarios.
- Modificar funcionarios.
- Eliminar funcionarios.
- Gestionar usuarios.
- Utilizar la transacción operacional.

### Supervisor

Dispone de permisos intermedios.

Puede:

- Consultar delegaciones.
- Registrar delegaciones.
- Modificar delegaciones.
- Consultar funcionarios.
- Registrar funcionarios.
- Modificar funcionarios.
- Ejecutar la transacción operacional.

No dispone de permisos para eliminar delegaciones ni funcionarios.

### Administrativo

Dispone de permisos de consulta.

Puede:

- Consultar delegaciones.
- Consultar funcionarios.
- Visualizar la información correspondiente a su perfil.

No puede crear, modificar ni eliminar registros de esos mantenedores.

---

## 7. Dashboards por perfil

Después de iniciar sesión, el usuario puede acceder al panel correspondiente a sus permisos.

### Dashboard Administrador

Incluye acceso a la administración general y a las funcionalidades de gestión.

### Dashboard Supervisor

Permite acceder a los mantenedores y operaciones autorizadas.

### Dashboard Administrativo

Presenta las opciones de consulta permitidas.

Las restricciones también se aplican en las vistas del servidor.

---

## 8. Mantenedores CRUD

La aplicación dispone de dos mantenedores principales.

### Mantenedor de Delegaciones

Permite:

1. Crear delegaciones.
2. Buscar delegaciones por nombre o sector.
3. Listar las delegaciones existentes.
4. Consultar sus detalles.
5. Modificar su información.
6. Eliminar registros cuando la operación está permitida.

### Mantenedor de Funcionarios

Permite:

1. Crear funcionarios.
2. Buscar por nombre, cargo o delegación.
3. Listar funcionarios.
4. Consultar sus detalles.
5. Modificar su información.
6. Eliminar registros según los permisos correspondientes.

Los formularios incorporan validaciones para evitar datos incorrectos.

---

## 9. Transacción operacional

SIGED implementa una transacción entre dos entidades relacionadas:

- Delegación.
- Funcionario.

### Funcionamiento

Al seleccionar la opción **Agregar delegación**, el usuario puede registrar una delegación de manera individual.

También puede activar la opción:

**Registrar también un funcionario inicial.**

Al activarla, se solicitan los datos del funcionario.

El sistema:

1. Valida los datos de la delegación.
2. Valida los datos del funcionario.
3. Inicia una transacción mediante `transaction.atomic()`.
4. Registra la delegación.
5. Asocia el funcionario a la nueva delegación.
6. Registra el funcionario.
7. Confirma la operación si ambas entidades se guardan correctamente.

### Integridad de datos

Si ocurre un error durante el registro conjunto, la transacción se revierte.

De esta manera, se evita que una delegación quede registrada parcialmente cuando falla el registro del funcionario.

### Pruebas realizadas

La operación se comprobó en:

- MySQL local.
- MariaDB en AWS.

Se verificaron:

- Registro individual de delegaciones.
- Registro conjunto.
- Relación entre entidades.
- Validación de formularios.
- Permisos de usuario.
- Rollback ante errores simulados.

Los registros temporales utilizados durante las pruebas fueron revertidos.

---

## 10. Modelo de datos

### Delegacion

Entidad que almacena:

- Nombre.
- Sector.
- Descripción.

### Funcionario

Entidad que almacena:

- Nombre.
- Cargo.
- Delegación asignada.
- Meta.
- Avance.

### Relación

Cada funcionario pertenece a una delegación.

La relación se implementa mediante una clave foránea (`ForeignKey`).

Una delegación puede tener varios funcionarios asociados.

La relación utiliza `on_delete=PROTECT` para evitar eliminaciones que comprometan la integridad de los registros asociados.

### Usuarios y permisos

La autenticación utiliza los modelos de usuarios, grupos y permisos de Django.

---

## 11. Validaciones

Entre las validaciones implementadas se encuentran:

- Comprobación de campos obligatorios.
- Validación de nombres y cargos.
- Validación de datos numéricos.
- Restricción de valores negativos mediante los campos correspondientes.
- Impedimento de que el avance supere la meta.
- Validación de formularios antes de guardar.
- Verificación de permisos por operación.
- Protección de operaciones de eliminación mediante solicitudes POST.
- Protección de registros relacionados.

---

## 12. Recuperación de contraseña

SIGED incorpora recuperación de contraseña mediante correo electrónico.

El proceso permite:

1. Solicitar recuperación con un correo registrado.
2. Generar un enlace de recuperación con token.
3. Enviar el enlace mediante correo electrónico.
4. Validar el enlace recibido.
5. Establecer una nueva contraseña.
6. Confirmar el cambio.
7. Iniciar sesión con la nueva contraseña.

El flujo fue probado en el entorno AWS.

---

## 13. Configuración del proyecto

El proyecto utiliza variables de entorno para separar los datos sensibles del código fuente.

Entre las configuraciones necesarias se encuentran:

- Clave secreta de Django.
- Modo DEBUG.
- Hosts permitidos.
- Configuración de base de datos.
- Credenciales de conexión.
- Configuración del servicio de correo.

Los nombres exactos de las variables deben coincidir con la configuración de Django del proyecto.

El archivo `.env` contiene información privada y está excluido de Git mediante `.gitignore`.

No se deben publicar claves ni contraseñas en el repositorio.

---

## 14. Instalación en desarrollo

### Clonar repositorio

```bash
git clone https://github.com/CHINO-gift/Proyecto_Integrado_Backend.git
cd Proyecto_Integrado_Backend
```

### Crear entorno virtual

```bash
python -m venv venv
```

Activar el entorno según el sistema operativo.

En Linux:

```bash
source venv/bin/activate
```

En Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

Crear el archivo `.env` con las variables requeridas por la configuración del proyecto.

Configurar la conexión a MySQL o MariaDB.

### Aplicar migraciones

```bash
python manage.py migrate
```

### Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

Los usuarios, grupos y permisos deben estar configurados en la base de datos correspondiente.

---

## 15. Rutas principales

Las rutas principales de la aplicación incluyen:

| Funcionalidad | Ruta |
|---|---|
| Inicio de sesión | `/acceso/` |
| Dashboard | `/panel/` |
| Delegaciones | `/delegaciones/` |
| Crear delegación | `/delegaciones/crear/` |
| Funcionarios | `/funcionarios/` |
| Crear funcionario | `/funcionarios/crear/` |
| Gestión de usuarios | `/usuarios/` |
| Recuperación de contraseña | `/recuperar-contrasena/` |

El acceso a cada ruta depende de los permisos del usuario.

---

## 16. Despliegue en AWS EC2

La aplicación se encuentra desplegada en una instancia AWS EC2.

La infraestructura utiliza:

- Amazon Linux.
- Python y entorno virtual.
- Django.
- Gunicorn.
- Nginx.
- MariaDB.
- GitHub.

### Funcionamiento

Nginx recibe las solicitudes del navegador y las dirige a Gunicorn.

Gunicorn ejecuta la aplicación Django.

Django utiliza el ORM para acceder a la base de datos relacional.

### Servicio de aplicación

Gunicorn se administra mediante `systemd`.

Para comprobar su estado:

```bash
sudo systemctl is-active gunicorn
```

### Control de versiones

El código fuente se mantiene en GitHub.

Las actualizaciones se prueban primero en el entorno local antes de incorporarlas al servidor AWS.

---

## 17. Pruebas realizadas

Se han realizado pruebas funcionales sobre:

- Autenticación.
- Acceso por perfiles.
- Gestión de usuarios.
- Recuperación de contraseña.
- CRUD de Delegaciones.
- CRUD de Funcionarios.
- Validaciones de formularios.
- Transacción entre Delegación y Funcionario.
- Rollback de operaciones.
- Integridad de registros.
- Acceso a rutas protegidas.
- Funcionamiento del servidor AWS.

Las pruebas de base de datos se realizaron utilizando registros temporales y transacciones reversibles para conservar los datos existentes.

---

## 18. Control de versiones

El proyecto utiliza Git y GitHub.

El historial del repositorio registra avances progresivos sobre:

- Autenticación.
- Dashboards.
- Perfiles.
- Permisos.
- Recuperación de contraseña.
- Gestión de usuarios.
- Mantenedores.
- Transacciones.
- Correcciones.
- Despliegue en AWS.

### Repositorio

https://github.com/CHINO-gift/Proyecto_Integrado_Backend

---

## 19. Uso de inteligencia artificial

Durante el desarrollo se utilizaron herramientas de inteligencia artificial como apoyo para:

- Analizar requisitos de la evaluación.
- Proponer soluciones técnicas.
- Revisar código Django.
- Implementar formularios y validaciones.
- Diseñar mecanismos de permisos.
- Preparar pruebas funcionales.
- Analizar errores.
- Comprender transacciones y rollback.
- Apoyar la documentación.

Las soluciones propuestas se integraron y comprobaron mediante pruebas locales y en AWS.

Las evidencias concretas del uso de IA se incluirán en el documento técnico de la evaluación.

---

## 20. Autor

**José Ignacio Villalobos**

Carrera de Analista Programador.

INACAP, sede La Serena.

Asignatura: Programación Back End (TI3041).

Proyecto académico SIGED - Evaluación Sumativa N.º 3.
