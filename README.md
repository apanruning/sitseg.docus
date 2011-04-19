Requerimientos:

- MongoDB (http://www.mongodb.org/)
- django-nonrel (https://bitbucket.org/wkornewald/django-nonrel/overview)
- django-mongodb-engine (http://django-mongodb-engine.github.com/mongodb-engine/)
- django-permission-backend-nonrel (https://bitbucket.org/fhahn/django-permission-backend-nonrel)


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

Iniciar mongoengine como usuario
-----------------------

    $ mkdir db #si no existe ya
    $ mongod --dbpath=./db

Correr el servidor de desarrollo
-----------------------

    $ cd docus
    $ git checkout dev
    $ ./manage.py runserver    
