api to fetch prayer times for a given day in edmonton

example: http://msauofa.ca/prayer-times?month=10&day=8 (domain will be changed eventually)

do `sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python3.x` first
run with `gunicorn -w 4 -b 0.0.0.0:80 api:app`
