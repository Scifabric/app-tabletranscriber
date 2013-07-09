========================
Fazendo Deploy no Apache
========================

O Memória Brasil é uma aplicação web desenvolvida utilizando
o micro-framework Flask_. Para fazer o seu deploy no apache é necessário um
script wsgi_ que é um script de especificação para comunicação entre servidores
de aplicação e aplicações web.

.. _wsgi: http://pt.wikipedia.org/wiki/Web_Server_Gateway_Interface
.. _Flask: http://flask.pocoo.org/

Pré-requisitos:

    * Memória Brasil
    * Apache 2
    * mod_wsgi

Instalando o Apache2 e wsgi
===========================

Para instalar o apache2 e o wsgi em um sistema operacional Debian/Ubunto faça:

    $ sudo apt-get install apache2
    $ sudo apt-get install libapache2-mod-wsgi

Após instalá-los abilite a biblioteca mod_wsgi no apache e depois
reinicie-o::

    $ sudo a2enmod wsgi
    $ sudo /etc/init.d/apache2 restart


Criando um VirtualHost no Apache2 para rodar a aplicação
========================================================

Dentro da instalação do Memória Brasil copie o arquivo contrib/app_tt.wsgi.template para contrib/app_tt.wsgi e adapte-o para as diretrizes das sua instalação.

Adapte o arquivo de virtual host **contrib/apache2/mb-site** que está da seguinte
forma::

    <VirtualHost *:80>
        ServerName example.com

        DocumentRoot /home/user/mb
        WSGIDaemonProcess mb user=user1 group=group1 threads=5
        WSGIScriptAlias /mb /home/user/app-tabletranscriber/contrib/app_tt.wsgi

        <Directory /home/user/app-tabletranscriber>
            WSGIProcessGroup mb
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

Em seguida copie o arquivo contrib/apache2/mb-site para a pasta::

    /etc/apache2/sites-available/

Habilite o site::

     $ sudo a2ensite mb-site

Reinicie o Apache para que as configurações tenham efeito::

    $ sudo /etc/init.d/apache2 restart


Configurando o Apache para servir duas aplicações wsgi
======================================================

.. note:: 
    
    Caso seja necessário ter duas aplicacões wsgi rodando no mesmo
    Virtual Host, como por exemplo o PyBossa e o Memória Brasil.

Nesse caso o que muda é apenas a configuração do virtual host no apache. Abaixo um exemplo desssa configuração para o PyBossa + Memória Brasil::

    <VirtualHost *:80>
        ServerName example.com
        DocumentRoot /home/user/pybossa/pybossa
        WSGIDaemonProcess pybossa user=user1 group=group1 threads=5
        WSGIScriptAlias /pybossa /home/user/pybossa/contrib/pybossa.wsgi

        <Directory /home/user/pybossa>
            WSGIProcessGroup pybossa
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>

            WSGIDaemonProcess mb user=user1 group=group1 threads=5
            WSGIScriptAlias /mb /home/user/app-tabletranscriber/contrib/app_tt.wsgi

        <Directory /home/user/app-tabletranscriber>

            WSGIProcessGroup mb
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>

    </VirtualHost>
