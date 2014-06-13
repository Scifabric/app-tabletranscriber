===================================================================
Instalando e configurando o PyLucene
===================================================================

	O pylucene é um wrapper para python da máquina de busca open-source
	da apache.org Lucene, que é escrita em java.
	
	No projeto, o pylucene é usado para indexar e fazer busca pelos
	resultados do projeto, especificamente as tabelas transcritas com o apoio
	da comunidade de usuários.


Instalando o pylucene
=====================

Para instalar o pylucene basta executar o script install_pylucene.sh,
que se encontra na pasta pylucene, ele irá instalar as dependências do pylucene
na máquina e disponibilizar o módulo para importação via código no ambiente
virtual env::

	$ sudo sh install_pylucene.sh
	

Código e documentação da api
============================

O código e a documentação da api do pylucene pode ser encontrada no seguinte
site:
	
	http://lucene.apache.org/pylucene/
	
.. note::
	
	A maior parte dos exemplos encontrados, até mesmo na pasta samples do pylucene
	está em java, mas pode ser traduzida facilmente para python.