sudo rm /var/lib/postgresql/12/main/postgresql.auto.conf
sleep 2
su - postgres -c  '/usr/lib/postgresql/12/bin/pg_ctl restart -D /var/lib/postgresql/12/main -o "-c config_file=/etc/postgresql/12/main/postgresql.conf"'