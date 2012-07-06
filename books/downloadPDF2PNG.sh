# Copyright 2011 (C) Daniel Lombraña González 
# This program is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA)

# REQUIREMENTS: In order to run this script you will need:
# - pdfimages
# - convert from imagemagick package

# RUN IT: ./downloadPDF2PNG.sh PDFNUMBER

# The next URL is the download URL for any PDF document from INPE

URL="http://memoria.nemesis.org.br/trf_arq.php?a="

# Download a file from URL
wget "$URL$1" -O "$1.pdf"

# Create a folder for that document
mkdir $1
mkdir $1/baixa_resolucao
mkdir $1/alta_resolucao
mkdir $1/metadados

# Get the PBM native images from the PDF
pdfimages "$1.pdf" $1/$1

# Convert them to PNG
for f in $1/*.pbm
do
    convert $f $f.png
    rm $f
done

for i in $1/*.png
do

   newname=$(echo $i |sed s/-/_/| sed s/.pbm//| sed s/$1//)
   echo $newname
   cp $i $1/alta_resolucao$newname
   convert -resize "550x700!" $i $1/baixa_resolucao$newname
   rm $i

done


rm "$1.pdf"
