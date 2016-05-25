mysql -u panda --password=weizoom panda < rebuild_database.sql
python manage.py syncdb --noinput