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
    $ pip install -r docus/requirements.txt

Correr el servidor de desarrollo
-----------------------

    $ cd docus
    $ git checkout dev
    $ ./manage.py runserver
    
Configurar nginx para servir los archivos desde el GridFS
-----------------------

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


