Requerimientos:

- MongoDB (http://www.mongodb.org/)
- django (http://django-project.com)
- mongoengine (http://mongoengine.org/)

Opcional, para servir archivos desde el gridfs:

- nginx (http://nginx.org/)
- nginx-gridfs (https://github.com/mdirolf/nginx-gridfs)

Instalación en Ubuntu:
====================

Instalar MongoDB:

    $ sudo apt-get install mongodb

Establecer el entorno para django:

    $ virtualenv --no-site-packages sitseg
    $ cd sitseg
    $ . bin/activate 
    $ git clone git@github.com:Inventta/sitseg.docus.git docus


Correr el servidor de desarrollo
-----------------------

    $ cd docus
    $ git checkout dev
    $ pip install -r docus/requirements.txt
    $ ./manage.py runserver

Crear usuario inicial (necesario para poder usar el formulario)
-----------------------
    $ ./manage.py shell
    >>> from mongoengine.django.auth import User
    >>> User.create_user('nombre', 'pass')

Correr mongodb en el entorno local
-----------------------
Si es la primera vez que se corre:    
    $ mkdir db

Para correrlo:
    
    $ mongod --dbpath=./db
    Sun May  8 16:55:15 MongoDB starting : pid=17436 port=27017 dbpath=./db 32-bit 

Esto permite tener la base de datos aislada en la carpeta db, para luego poder hacer
backups o levantar un entorno con datos cargados.


Correr el servidor de produccion
-----------------------
TBD



Configurar nginx para servir los archivos desde el GridFS
-----------------------
NOTA: Para el sitio en desarrollo no es necesario utilizarlo.


Obtener dependencias y las fuentes de nginx

    $ sudo apt-get install libpcre3-dev
    $ wget http://nginx.org/download/nginx-1.0.0.tar.gz
    $ tar nginx-1.0.0.tar.gz 


Obtener el módulo que da soporte para servir archvios directamente desde el 
GridFS de MongoDB
    
    $ git clone https://github.com/mdirolf/nginx-gridfs.git
    $ cd nginx-gridfs
    $ git submodule init
    $ git submodule update
    
Compilar nginx con soporte para GridFS

    # en el dir donde bajamos las fuentes de nginx
    $ ./configure prefix=</path/to/virtualenv/>/nginx --add-module=/path/to/nginx-gridfs
    $ make
    $ make install
    
> Esto instala nginx en el virtualenv para facilitar la explicación de la 
> configuración más adelante, probablemente quieras hacer algo más cómodo.


Modificar la configuración del servidor
    
    $ cd /path/to/nginx
    $ nano conf/ngnix.conf

Esta es una configuración para servir sólo archivos del gridfs

    events {
        worker_connections  1024;
    }


    http {
        include       mime.types;
        default_type  application/octet-stream;

        server {
            listen       9000;
            server_name  gridfs.sitseg;


            location /gridfs {
                gridfs sitseg field=filename type=string;
            }
        }

    }
    

> Notar que server_name está definido como gridfs.sitseg, probablemente te haga
> falta modificar /etc/hosts para agregar este subdominio


