docker run --name mysql57 -d --restart unless-stopped -p 3306:3306 ibex/debian-mysql-server-5.7
echo "Run Command to enter mysql database: docker exec -it mysql57 "mysql" -u root"
echo "CREATE USER 'root'@'%' IDENTIFIED by 'cloud123';"
