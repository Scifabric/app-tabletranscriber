app-tabletranscriber
====================

TableTranscriber (TT) is a PyBossa application that aims to take old books and use a series of crowd-sourcing tasks to transcribe data inside tables (which are poorly recognized by OCR processes).

In this first version we are using as a case books from the [Brazilian Statistical Memories](http://memoria.nemesis.org.br/) maintained by [IPEA](http://www.ipea.gov.br/portal/)

About
=====

In this first version TT has two main interdependent Tasks:
  * Finding tables and collecting its metadata
  * Transcribing found tables

Requirements
============

To use TT you will need:
  * A running PyBossa and a user key.
  * A webserver to suport TT tasks providing statical files (as images and some code).

To use Brazilian books first example you will need:
  * The "imagemagick" open software to deal with PDF books and create pages' images.

Running
=======

We are going to show how to create a transcription project using a Ubuntu platform. So, to pass the requirements you'll basically have:
  * Follow [PyBossa's installation guide](http://pybossa.readthedocs.org/en/latest/install.html);
  * Use the Apache probably already installed at your machine and the default "/var/www" folder to put TT static files;
  * Install "imagemagick" package using: sudo apt-get install imagemagick

Now, you'll need to:
  0. Start PyBossa and create your user;
  1. Download TT;
  2. Choose and prepare a book to have tables transcribed;
  3. Put static files at web server;
  4. Create tasks;
  5. Have fun!

Preparing a Book
================

Inside "<TT_folder>/books" you'll find a bash script that will help you downloading a book from (Brazilian Portal)[http://memoria.nemesis.org.br/], and creating images for each page.

To use it you will have to go to the book's portal and choose a book, and get its ID, for example: 00245000 (the ID is exactly the PDF name. You don't have to download it).

Execute the script:
```
./downloadPDF2PNG.sh 00245000
```
This will create a directory for the book and some some other inside it. For now the one that will be usefull will be the "baixa_resolucao". (ToDo: In newer versions we will translate everything to English).

Serving Static Files
====================

Go to the "/var/www" folder of your server (or any other folder that can serve static files) and do the following:
```
#1. create project folder
sudo mkdir app-tabletranscriber
cd app-tabletransciber
#2. make some important folder available - substitute <TT_folder> by the complete path of the application folder.
sudo cp -r <TT_folder>/css .
sudo cp -r <TT_folder>/images .
sudo cp -r <TT_folder>/js .
#3. make the downloaded book available
sudo mkdir books
sudo cp -r <TT_folder>/books/00245000/baixa_resolucao/ books/00245000
```

To make sure everything is OK, go to your browser and enter URL: http://YOUR.SERVER/app-tabletranscriber (we will call this <APP_URL> from now on). You should have the four directories available (books, css, images, js) and inside "books" you should have a book folder full of page images. If you have not, this may be problem with your server and its permissions.

Creating Tasks
==============

//Will be here SOON!