#!/bin/bash

# Atencao para os seguintes pontos:
# 1. Execute com virtualenv desativado
# 2. Garanta que o ant, java e gcc estao instalados
# 3. Garanta que a localizacao da java jdk indicada no arquivo
#    setup.py em jcc estah correspondente a que voce possui na sua maquina
# 4. modifique a localizacao do seu projeto MEB/TT no Makefile do lucene

echo "----- Installing PyLucene 4.8.0 ------------"

. env/bin/activate

svn co http://svn.apache.org/repos/asf/lucene/pylucene/tags/pylucene_4_8_0

cd pylucene_4_8_0/jcc

python setup.py build
sudo python setup.py install

cd ..

make
sudo make install

echo "------ PyLucene 4.8.0 installed with success ----------"
