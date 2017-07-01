# blog_on_django

## System requirements:
```
$ sudo apt-get install -y python  python3-dev  python3-setuptools python3-pip
$ sudo pip3 install virtualenv```
$ sudo apt-get install -y graphviz libgraphviz-dev pkg-config libenchant1c2a
$ sudo apt-get install mysql-server mysql-client
$ sudo apt-get install libjpeg8-dev zlib1g-dev libfreetype6-dev
$ sudo apt-get install libmysqlclient-dev
```
## Install
```
$ mkdir blog
$ cd blog
$ virtualenv --no-site-packages --distribute -p /usr/bin/python3 virtualenv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ cd web-application
$ ./manage.py makemigrations thumbnail
$ ./manage.py migrate
