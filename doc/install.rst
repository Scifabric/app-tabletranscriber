============================
Instalação do Memória Brasil
============================


A aplicação Memória Brasil é uma aplicação desenvolvida
utilizando o micro-framework Flask e componentes de aplicações
crowdsource para o PyBossa.

Pré-requisitos:

    * Python >= 2.7, <3.0
    * SGBD PostgreeSQL 9.1
    * pip - instalador de bibliotecas para python
    * PyBossa_ - Framework para criar aplicações de crowdsource

    .. _PyBossa: http://github.com/pybossa/pybossa

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
    
    $ rabbitmqctl add_vhost myvhost

Criando um usuário RabbitMQ::
    
    $ rabbitmqctl add_user myuser mypassword

Adicionando permissões de usuário para o host criado::
    
    $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"


Por fim, inicialize o broker e guarde o usuário e senha criados::

 $ sudo rabbitmq-server


.. _celery: http://www.celeryproject.org/
.. _RabbitMQ: http://www.rabbitmq.com/


Configurando o BD do Memória Brasil
===================================

Agora vamos criar a base de dados para a nossa aplicação.
Para alterar as configurações do SGBD execute::

    $ sudo su postgres

Agora precisamos criar um usuário que utilizará o BD da aplicação::

    $ createuser -P mbuser

Após executar o comando e digitar a senha responda as perguntas que
apareceração da seguinte forma:

    * Shall the new role be a super user? (y/n) responda **n**.
    * Shall the new role be allowed to create databases? (y/n) responda **y**.
    * Shall the new role be allowed to create more new roles? (y/n) responda **n**.

Com o usuário criado, agora é só criar o BD::

    $ createdb mbdb -O mbuser

Pronto, o BD foi criado, agora saia do usuário postgres::
    
    $ exit

Agora com o BD criado execute o script que criará as tabelas necessárias::

    $ python create_db.py


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


Celery como Daemon
==================
Para que o celery funcione como um Daemon, utilizamos o `supervisor`_ que
é software em python que permite monitorar e controlar processos unix.

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

Reinicie o supervisor::

    sudo /etc/init.d/supervisor restart


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

    sudo touch /etc/apache2/sites-enable/mb-static
    sudo vim /etc/apache2/sites-enabled/mb-static
    #Cole o código abaixo no arquivo mb-static e substitua <diretorio-mb> pelo
    #diretorio onde o memória brasil foi instalado
    Alias /mb-static <diretorio-mb>/app_tt/pb_apps/tt_apps

Por fim reinicie o apache para que as configurações sejam iniciadas::

    sudo /etc/init.d/apache2 restart

.. 
    instalação sem o pybossa ###############
    Instalando o Git
    ================

    O git_ é um sistema de controle de versão distribuído e gerenciamento de código.

    .. _git: http://git-scm.com/

     Para instalá-lo basta executar o comando::

    sudo apt-get install git
