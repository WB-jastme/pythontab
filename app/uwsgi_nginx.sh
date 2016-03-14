#!/bin/sh
pid=`sudo netstat -ntpl | grep uwsgi | awk '{print $NF}'|awk -F'/' '{print $1}'`
echo $pid

while [ -n "$1" ]  
do  
case "$1" in   
    start)  
        sudo uwsgi -x app.xml
        sudo /etc/init.d/nginx start
        shift
        ;;  
    stop)  
        sudo kill -9 $pid
        sudo /etc/init.d/nginx stop
        shift  
        ;;  
    restart)  
        sudo kill -9 $pid
        sudo uwsgi -x app.xml
        sudo /etc/init.d/nginx restart
        shift  
        ;;  
     *)  
         echo "use start|stop|restart to execute the bash script"  
        ;;  
esac
done
