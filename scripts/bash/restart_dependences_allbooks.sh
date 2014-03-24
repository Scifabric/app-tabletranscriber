#!/bin/bash

#reload templates
. ../../env/bin/activate

for book in "anuario1916pb" "MemmoriaParaiba1841A1847" "estatisticasdodi1950depa" "rpparaiba1918" "caracterizaoeten2001bras" "mensagemdogovern1912gove"; do
   for ext in "_tt1" "_tt2" "_tt3" "_tt4"; do
       python ../python/update_pyb_apps.py -u $book$ext
   done
done

deactivate

