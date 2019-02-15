from database import connection
from flask import Flask, render_template
import mysql.connector
import MySQLdb
import yaml
import datetime
import time

app = Flask(__name__)

### Read config parameters for mysql
with open('config.yaml') as f:
	cloud_config = yaml.safe_load(f)
	cloud_host = cloud_config['cloud_mysql_hostname']
	cloud_username = cloud_config['cloud_mysql_username']
	cloud_password = cloud_config['cloud_mysql_password']
	cloud_database = cloud_config['cloud_mysql_database']
	cloud_port = cloud_config['cloud_mysql_port']

### Connect to mysql database and get cursor
cloud_mydb = mysql.connector.connect(
  host=cloud_host,
  user=cloud_username,
  passwd=cloud_password,
  database=cloud_database,
  port = cloud_port
)
cloud_mycursor = cloud_mydb.cursor()
cloud_mydb.commit()

### Read config parameters for mysql
with open('config.yaml') as f:
	edge_config = yaml.safe_load(f)
	edge_host = edge_config['edge_mysql_hostname']
	edge_username = edge_config['edge_mysql_username']
	edge_password = edge_config['edge_mysql_password']
	edge_database = edge_config['edge_mysql_database']
	edge_port = edge_config['edge_mysql_port']

### Connect to mysql database and get cursor
edge_mydb = mysql.connector.connect(
  host=edge_host,
  user=edge_username,
  passwd=edge_password,
  database=edge_database,
  port = edge_port
)
edge_mycursor = edge_mydb.cursor()
edge_mydb.commit()

@app.route('/')
def sensor_data():
	global total_time_batch, total_time_speed, count
	while(1):
		query = "SELECT * FROM (SELECT * FROM temps_predicted ORDER BY\
		time_stamp DESC LIMIT 5000) sub ORDER BY time_stamp ASC;"

		cloud_mycursor.execute(query)
		cloud_data = cloud_mycursor.fetchall()
		start_time = cloud_data[0][-2]
		end_time = cloud_data[-1][-2]
		total_time_batch = (end_time-start_time)/len(cloud_data)


		cloud_times = []
		cloud_temps = []
		for row in cloud_data:
			print(row[3].timestamp())
			cloud_times.append(row[3].timestamp()) 
			cloud_temps.append(row[1])

		cloud_out = []
		for time_, temp in zip(cloud_times,cloud_temps):
			cloud_out.append({'x': time_, 'y': temp})
		cloud_out = str(cloud_out).replace('\'', '')


		query = "SELECT * FROM (SELECT * FROM temps_found ORDER BY\
		time_stamp DESC LIMIT 20000) sub ORDER BY time_stamp ASC;"

		edge_mycursor.execute(query)
		edge_data = edge_mycursor.fetchall()
		start_time = edge_data[0][-2]
		end_time = edge_data[-1][-2]
		total_time_speed = (end_time-start_time)/len(edge_data)

		edge_times = []
		edge_temps = []
		for row in edge_data:
			edge_times.append(row[3].timestamp()) 
			edge_temps.append(row[1])

		edge_out = []
		for time_, temp in zip(edge_times,edge_temps):
			edge_out.append({'x': time_, 'y': temp})
		edge_out = str(edge_out).replace('\'', '')

		edge_mydb.commit()
		cloud_mydb.commit()
		
		time_stamps = range(0,len(cloud_data+edge_data))
		print(time_stamps)
		#cloud_data = edge_data+cloud_data
		return render_template("index2.html", data_cloud=cloud_out, data_edge=edge_out, speed_hz=1/(total_time_speed.total_seconds()), batch_hz=1/(total_time_batch.total_seconds()))


if(__name__ == '__main__'):
	app.debug = True
	app.env = ""
	app.run('0.0.0.0', port=5000)

