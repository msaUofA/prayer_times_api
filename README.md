api to fetch prayer times for a given day in edmonton

example: http://nasif.ca/prayer-times?month=10&day=8 (domain will be changed eventually)

run with gunicorn -w 4 -b 0.0.0.0:80 api:app
