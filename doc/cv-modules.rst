======================================
Instalando e configurando o cv-modules
======================================

O cv-modules é um conjunto de componentes, escritos em c++ para tratar da 
parte de visão computacional do projeto Memória Estatística do Brasil.
	
Os seguintes módulos compõem o cv-modules:

* TableTranscriber2: módulo responsável por identificar linhas e colunas das tabelas.

* TesseractExecutor: módulo responsável por passar o OCR Tesseract nas células da tabela identificadas pelos usuários.

* ZoomingSelector: módulo responsável por identificar as coordenadas de corte da tabela, no caso em que o uso da tabela toda gera uma tarefa muito grande para apenas um usuário.

* QualityMeasuererTT: módulo usado para medição da qualidade dos layouts feitos pelo TableTranscriber2.

* QualityMeasuererTE: módulo usado para medição da qualidade das transcrições feitas pelo TesseractExecutor.


Instalando as dependências
==========================

Para instalar as dependências do cv-modules basta executar o script
INSTALL2.sh que se encontra na pasta resources da pasta cv-modules, 
atente para o fato de que o script precisa ser executado numa pasta
em que root tenha permissão de escrita::

	$ sudo sh INSTALL2.sh

.. note::
	
	O INSTALL2.sh irá criar uma pasta srcCV_MODULES na qual estarão os
	códigos das bibliotecas necessárias a todos os componentes do cv-modules.
	Não delete esta pasta após a instalação.

.. note::
	
	Caso a versão do image-magick não for encontrada, atualize o script para a versão
	atual, encontrada em http://www.imagemagick.org/download/


Compilando o código do cv-modules
=================================

Para compilar o código dos cv-modules e obter os executáveis de cada 
componente, basta executar o script script_compilacao_cvmodules.sh que
se encontra na pasta cv-modules::

	$ sh script_compilacao_cvmodules.sh
	

Executando o cv-modules
=======================

Todos os componentes do cv-modules compartilham de uma estrutura de diretórios,
a qual é descrita em resources/ESTRUTURA_DE_DIRETORIOS, ela deve ser respeitada
estritamente para funcionamento dos componentes.

Cada componente é executado separadamente e mais detalhes sobre a execução de
cada um deles pode ser encontrados no resources/README.md de cada.


Código do cv-modules
====================

O código do cv-modules se encontra no seguinte repositório::
	
	http://code.google.com/p/tabletranscriber/source/browse/

	