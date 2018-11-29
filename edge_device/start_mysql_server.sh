docker run --name mysql57 -d --restart unless-stopped -p 127.0.0.1:3306:3306 ibex/debian-mysql-server-5.7
echo "Run Command to enter mysql database: docker exec -it mysql57 "mysql" -uroot"
echo "CREATE USER 'root'@'192.168.%' IDENTIFIED by 'cloud123';"
echo "CREATE USER 'root'@'172.%' IDENTIFIED by 'cloud123';"
