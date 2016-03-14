# pythontab

nginx.conf
##################
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
