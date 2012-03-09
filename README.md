Requerimientos:
==================

* django
* postgreSQL - postgis
* R


Instalación en Ubuntu Oneiric Ocelot:
====================

Instalar dependencias de los repositorios de ubuntu:

        $ sudo apt-get install gdal-bin postgresql-9.1-postgis

Postgis 
--------------------

Crear el template_postgis y permitir que otros usuarios puedan crear bases 
de datos con este:
    
        $ sudo su - postgres

        $ createdb -E UTF8 template_postgis
        $ psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"

Cargar las rutinas PostGIS SQL:

        $ locate postgis.sql
        /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql # puede traer varios resultados
        $ psql -d template_postgis -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql
        $ psql -d template_postgis -f /usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql

Darle permisos a todos los usuarios de alterar columnas de geometría:

        $ psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
        $ psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
        $ psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

Configuración del proyecto
-------------------
Luego podés crear una base de datos que pueda almacenar las columnas de postgis utilizando el template_postgis:

        $ psql
        postgres=# CREATE DATABASE sitseg WITH OWNER=sitseg TEMPLATE=template_postgis;

Establecer el entorno para el proyecto:

        $ virtualenv --no-site-packages sitseg
        $ cd sitseg
        $ . bin/activate 
        $ git clone git@github.com:Inventta/sitseg.docus.git docus
        $ cd docus
        $ git checkout dev
        $ pip install -r docus/requirements.txt
    
Crear un archivo `local_settings.py` y ajustar la configuración a nuestro 
entorno:

        $ vim local_settings.py
        DATABASES = {
           'default': {
               'ENGINE': 'django.contrib.gis.db.backends.postgis',
               'NAME': 'sitseg',
               'USER': 'sitseg',
               'PASSWORD': 'sitseg',
               'HOST':'localhost',
               'PORT':'5432'
           },
        }
        INTERNAL_IP="127.0.0.1"
    
Instalacion de R

Editar el archivo de configuracion (/etc/apt/sources.list) 

        $ sudo gedit /etc/apt/sources.list

Agregar la siguiente linea al mismo

        deb http://cran.cnr.berkeley.edu/bin/linux/ubuntu oneiric/

Damos clic en “Guardar” y cerramos el archivo. En la terminal ejecutamos lo siguiente:

        $ gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
        $ gpg -a --export E084DAB9 | sudo apt-key add -

Actualizamos los paquetes de Ubuntu para poder instalar R. En la terminal ejecutamos:
        
        $ sudo apt-get update
        $ sudo apt-get install r-base

Hacen falta instalar algunos paquetes extra para R. Para ello, es necesario entrar en la terminal de R como superusuario

        $ sudo R
        $ install.packages('PBSmapping');        
    
Ahora podemos sincronizar y correr el servidor de desarrollo:

        $ ./manage.py syncdb
        $ ./manage.py runserver

Abrir google-chrome con la direccion para entrar en la aplicacion

        http://localhost:8000



