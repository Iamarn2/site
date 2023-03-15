release: yes "yes" | python manage.py migrate
web: uwsgi --http-socket=:$PORT --master --workers=2 --threads=8 --die-on-term --wsgi-file=slides/wsgi.py  --static-map /media/=/app/slides/media/ --offload-threads 1
