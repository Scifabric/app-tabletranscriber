===================================================================
Instalação do Memória Estatística do Brasil (app-tabletranscriber)
===================================================================


   A aplicação Memória Estatística do Brasil é uma aplicação desenvolvida
   com a finalidade de indexar, transcrever e disponibilizar para pesquisadores
   e o público em geral, tabelas dos livros da Biblioteca do Ministério da Fazenda
   no Rio de Janeiro.
   
   Os livros são digitalizados e colocados no _archive.org, de onde, por meio
   da API disponibilizada, fazemos o download dos livros que serão utilizados na
   nosssa aplicação. Amostras de livros que estão no archive.org podem ser visualizadas
   aqui: http://memoria.org.br/. Essas primeiras amostras são a origem do atual projeto
   Memória Estatística do Brasil, cuja localização atual é: http://alfa.pybossa.socientize.eu/mb

Pré-requisitos (instalados via pip):

    * Flask-0.9_ - framework para criação de aplicações web em python
    * Jinja2 - framework para renderização de templates para aplicações web
    * Flask-Testing - framework para teste de aplicações Flask
    * Flask-SQLAlchemy_ - interface entre o framework Flask e o SQLAlchemy para utilização de esquemas objeto-relacionais em python
    * Flask-Migrate_ - extensão que manipula migrações de banco de dados utilizando SQLALchemy e Flask
    * Psycopg2_ - biblioteca para consultas a banco de dados usando python
    * Celery_ - enfileirados de tasks (sentido mais genérico) usado em aplicações distribuídas
    * Python >= 2.7, <3.0 - linguagem usada para desenvolver o app-tabletranscriber
    * PIP - instalador de bibliotecas para python
    * SQLALchemy-0.9_: kit de ferramentas Python SQL e Object Relational Mapper que dá aos desenvolvedores de aplicativos o poder e a flexibilidade do SQL.
    * Alembic_ - ferramenta para criação de scripts de migração de banco de dados em python, que utiliza SQLAlchemy-0.9_
    * PyLucene_ - wrapper para python da máquina de busca feita em java da apache.org (Lucene_) utilizada na indexação e busca de resultados do app-tabletranscriber
    * PyBossa_ - Framework para criar aplicações de crowdsource
    
Instalados junto com o PyBossa:
    
    * PostgreeSQL 9.1 - sgbd utilizado pelo pybossa e pelo app-tabletranscriber
    * Supervisor 3.0 - sistema cliente-servidor que permite ao usuário controlar processos em sistemas unix-like
    * Apache 2.2 - servidor utilizado para rodar o pybossa
    * Apache Mod_WSGI - plugin do apache para interface universal para aplicações web em python
    * Virtualenv - ambiente virtual para rodar aplicações python com libs com diferentes versões simultaneamente na mesma máquina
    * Redis - silo de dados não estruturados (key-value) para gerenciamento e utilização de cache no pybossa
    * RabbitMQ - é um broker de mensagens. Ele dá a seus aplicativos uma plataforma comum para enviar e receber mensagens, e às mensagens um lugar seguro para viver até que sejam entregues

Recomendável:
    * PhpPgAdmin_ - interface web para gerenciamento de banco de dados
    * Sphinx_ - biblioteca para criação de documentação, como esta

.. _archive.org: https://archive.org    
.. _PhpPgAdmin: http://phppgadmin.sourceforge.net/doku.php
.. _Flask-0.9: http://flask.pocoo.org/docs/
.. _Flask-SQLAlchemy: http://pythonhosted.org/Flask-SQLAlchemy/
.. _Flask-Migrate: http://flask-migrate.readthedocs.org/en/latest/
.. _Psycopg2: http://initd.org/psycopg/docs/
.. _Alembic: http://alembic.readthedocs.org/en/latest/tutorial.html
.. _SQLAlchemy-0.9: http://docs.sqlalchemy.org/en/rel_0_9/
.. _PyLucene: http://lucene.apache.org/pylucene/
.. _Lucene: http://lucene.apache.org/core/4_8_1/index.html
.. _Sphinx: http://sphinx-doc.org/

.. note::

    Nós recomendamos a utilização do virtualenv_ que
    possui a característica de criar ambientes virtuais para rodar aplicações
    python com diferentes versões de bibliotecas simultaneamente na mesma máquina.

    .. _virtualenv: http://pypi.python.org/pypi/virtualenv

.. note::
    O Memória Brasil possui aplicações crowdsource que ficam localizadas dentro de um
    servidor PyBossa_. Portanto um servidor rodando esse framework
    é necessário, esse servidor pode ser instalado na mesma máquina ou estar
    localizado remotamente.


    .. _PyBossa: http://github.com/pybossa/pybossa


Preparando o ambiente
=====================

Para instalarmos o Memória Brasil precisamos preparar o ambiente de instalação, instalando
algumas ferramentas necessárias. O sistema operacional utilizado
nesse guia é o Ubuntu_

    .. _Ubuntu: http://www.ubuntu.com/


[Opcional] Instalando o PyBossa
===============================

A instalação do PyBossa necessita de vários componentes, acesse o `guia completo
de instalação do Pybossa`_ e realize a sua instalação.

.. _`guia completo de instalação do Pybossa`: http://docs.pybossa.com/en/latest/install.html

.. note::
    Para criar aplicações no PyBossa uma Api-Key é necessária, ela deve ser
    obtida criando um usuário no PyBossa.


Configurando o Celery
=====================

O celery_ é um enfileirador de tarefas baseado em troca de mensagens que utilizamos para criar
o workflow desejado entre as várias aplicações crowdsource que rodam no PyBossa.

Para que o celery funcione é necessário que seja instalado um broker de mensagens.
Nesse projeto utilizamos o RabbitMQ_, que provê uma plataforma comum para
enviar e receber mensagens. Portanto precisaremos instalar e configurar o RabbitMQ começando
com o seguinte::

    $ sudo apt-get install rabbitmq-server

Agora para usar o celery precisamos criar um host virtual no rabbitMQ e um usuário para utilizá-lo

Criando o vhost no RabbitMQ::
    
    $ sudo rabbitmqctl add_vhost <host>

Criando um usuário RabbitMQ::
    
    $ sudo rabbitmqctl add_user <user> <password>

Adicionando permissões de usuário para o host criado::
    
    $ sudo rabbitmqctl set_permissions -p <host> <user> ".*" ".*" ".*"


Por fim, inicialize o broker e guarde o usuário e senha criados::

 $ sudo rabbitmq-server


.. _celery: http://www.celeryproject.org/
.. _RabbitMQ: http://www.rabbitmq.com/


Configurando o BD do Memória Estatística do Brasil
==================================================

Agora vamos criar a base de dados para a nossa aplicação.
Para alterar as configurações do SGBD execute::

    $ sudo su postgres

Agora precisamos criar um usuário que utilizará o BD da aplicação::

    $ createuser -P <user>

Após executar o comando e digitar a senha responda as perguntas que
apareceração da seguinte forma:

    * Shall the new role be a super user? (y/n) responda **n**.
    * Shall the new role be allowed to create databases? (y/n) responda **y**.
    * Shall the new role be allowed to create more new roles? (y/n) responda **n**.

Com o usuário criado, agora é só criar o BD::

    $ createdb mbdb -O <user>

Pronto, o BD foi criado, agora saia do usuário postgres::
    
    $ exit

Agora com o BD criado e estando com o ambiente virtual ativo e no folder app-tabletranscriber::

    $ python app_tt/core.py mbdb upgrade

Note que com esse comando o esquema estará criado automaticamente, ele funciona basicamente em cima de uma interface
própria do Flask com o gerenciador de versões de esquemas Alembic.


Instalando o Memória Brasil
===========================

Baixando e instalando os componentes python da aplicação::

    $ git clone --recursive https://github.com/Jeymisson/app-tabletranscriber
    #acesse a pasta onde o projeto foi baixado
    $ cd app-tabletranscriber
    #crie um virtualenv
    virtualenv env
    #ative o virtualenv criado
    $ . env/bin/activate
    #instale a aplicação
    $ pip install -e .


Em seguida realizaremos as configurações necessárias para que o Memória Brasil
funcione, ainda no diretório atual faça::
    
    $ cp settings_local.py.template settings_local.py
    # edite o arquivo arquivo de configuração
    $ vim settings_local.py

Edite esse arquivo de configurações inserindo as informações necessárias
obtidas nos passos anteriores.


Celery e Redis-Sentinel como Daemons
====================================

Para que o celery e o redis sentinel (para o PyBossa) funcione como um daemons, 
utilizamos o `supervisor`_ que é software em python que permite monitorar e 
controlar processos unix.

Para instalar o supervisor execute o seguinte::

    sudo apt-get install supervisor

Em seguida adicione as configurações necessárias para que ele sempre execute
o celery instalado::
   
    sudo vim /etc/supervisor/supervisord.conf

Adicione as configurações abaixo no final do arquivo supervisord.conf
substitua <env-dir> pelo caminho do diretório do virtualenv criado::
    
    [program:celeryd]
    command=<env-dir>/bin/celery worker --app=app_tt.engine.tasks -l info
    stdout_logfile=/tmp/celeryd.log
    stderr_logfile=/tmp/celeryd.log
    autostart=true
    autorestart=true
    startsecs=10
    stopwaitsecs=600
    
    [program:redis]                                                               
    command=redis-server <path to pybossa>/contrib/redis/sentinel.conf --sentinel               
    autostart=true
    autorestart=true                                                              
    user=<user>                                                               
    stdout_logfile=<path to pybossa>/log/redis/stdout.log         
    stderr_logfile=<path to pybossa>/log/redis/stderr.log


.. note::
	
	Note que os arquivos stdout.log e stderr.log devem existir e root
	deve ser capaz de escrever neles.

Reinicie o supervisor::

    sudo /etc/init.d/supervisor stop
    sudo /etc/init.d/supervisor start


.. _supervisor: http://supervisord.org


Instalando e configurando o Apache2
===================================

.. note::
    Como essa aplicação possui alguns componentes estaticos que precisam ser
    acessados pelas aplicaçães crowdsource que ficam no PyBossa. Portanto a instalação
    e configuração do apache é necessária


Para instalar o apache2 execute o seguinte comando::

    sudo apt-get install apache2

Em seguida configure o apache para listar os arquivos estáticos que estão no
diretório <diretorio-mb>/app_tt/pb_apps/tt_apps/static/::

    Acrescentando o seguinte Alias no arquivo /etc/apache2/sites-available/mb-site:
    
    # substitua <diretorio-mb> pelo diretorio onde o memória brasil foi instalado
    Alias /mb-static <diretorio-mb>/app_tt/pb_apps/tt_apps/static


Por fim recarregue o apache para que as configurações sejam iniciadas::    
    
    sudo service apache2 reload


Instalando e configurando o PhpPgAdmin
======================================

Para instalar o phppgadmin, faça::
   
   sudo apt-get install phppgadmin


.. note::
   Para permitir o login com o usuário padrão do PostgresSQL (usuário postgres)
   na interface web, modifique a variável $conf['extra-login-security'] para false
   no arquivo /etc/phppgadmin/config.ini.php.


Instalando o Sphinx
===================

Para instalar o Sphincx, faça::

	sudo apt-get install python-sphinx
