# Validater-Microservice

Validater es un microservicio que permite validar la información de un usuario.
Consta de 2 modulos, el primero es el de Usuarios, el cual permite crear, editar, eliminar y listar Clientes.
También cuenta con el modulo Auth de la librería Djoser, el cual permite el registro de usuarios y la autenticación de los mismos.
Por ultimo, tenemos el modulo de Transacciones, el cual permite Listar, Obtener y Eliminar transacciones. Además tiene un endpoint especial para validar la información de un Cliente

## Instalación

1. Clona el repositorio con el comando:

```bash
git clone git@github.com:allanos94/darient_test.git
```

2. Configura las variables de entorno en el archivo `.env`:

```bash
cp .env.example .env
```

3. Se debe instalar la librería Poetry para poder instalar las dependencias del proyecto:

```bash
pip install poetry
```

4. Se debe instalar las dependencias del proyecto:

```bash
poetry install
```

5. Debes crear un superusuario para poder acceder a los endpoints del microservicio:

```bash
python manage.py createsuperuser
```

6. Con esto ya podrás ejecutar el proyecto:

```bash
python manage.py runserver
```

7. Para ejecutar con docker-compose:

```bash
docker-compose -f docker-compose.yml  --env-file=.env up
```

8. Te recomendamos apoyarte en el modo debug para poder ejecutar los comandos de Django de manera más sencilla y con la funcionalidad del Debugger.

## Uso

1. Con el proyecto corriendo en la dirección `http://0.0.0.0:8000/` ya podrás hacer uso de los endpoints.
