# pythontab

###install packages

```
apt-get install nginx nmap python-dev ipython mysql-server libmysqld-dev ansible;
pip install uwsgi;
pip install django==1.7;
pip install pykafka;
pip install numpy;
pip install matplotlib;
pip install pandas;
pip install nmap;
pip install linaro_django_pagination;
pip install mysql-python;

```
###step if you clone the project
#####mysql
```
CREATE DATABASE `jastme` /*!40100 DEFAULT CHARACTER SET utf8 */;
GRANT ALL PRIVILEGES ON jastme.* TO 'jastme'@'127.0.0.1' IDENTIFIED BY 'jastme';
```
#####ubuntu server

```
cd /pythontab/app;
python manage.py syncdb
```
###nginx.conf

###---------------------------------------
```
server {  

    listen   80;
    server_name  your sitename;
    access_log /var/log/nginx/access.log ;
    error_log /var/log/nginx/error.log ;

    location / {
            uwsgi_pass 127.0.0.1:8630;
            include uwsgi_params;
    }

    location ~/static/ {
            root  /var/www/jastme/;
            index  index.html;
    }  

}
```

##the demo
```
http://52.79.111.129
```
