from matplotlib import pyplot
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import mysql.connector
import MySQLdb
import yaml
from database import connection
import numpy as np
import time
from datetime import datetime, timedelta

### Read config parameters for mysql
with open('config.yaml') as f:
	config = yaml.safe_load(f)
	host = config['cloud_mysql_hostname']
	username = config['cloud_mysql_username']
	password = config['cloud_mysql_password']
	database = config['cloud_mysql_database']
	port = config['cloud_mysql_port']

### Connect to mysql database and get cursor
mydb = mysql.connector.connect(
  host=host,
  user=username,
  passwd=password,
  database=database,
  port = port
)
mycursor = mydb.cursor()
mydb.commit()

while(1):
	query = "SELECT * FROM temps_found ORDER BY time_stamp ASC LIMIT 100000"
	mycursor.execute(query)
	temps_found = np.array(mycursor.fetchall())
	X = temps_found[:,1]
	size = int(len(X) * 0.99)
	train, test = X[0:size], X[size:len(X)]
	history = [x for x in train]
	predictions = list()
	#for t in range(100):
	model = ARIMA(history, order=(5, 1, 0))
	model_fit = model.fit(disp=0)
	output,stderr,conf_int = model_fit.forecast(steps=1000)
	yhat = output
	#history.append(yhat[0])
	#del history[0]
	# Save temp into mysql
	time_in = temps_found[-1,-2] #datetime.now()
	for delta,temp in enumerate(yhat):		
		sql = "INSERT INTO temps_predicted(temp, sensor_type,  time_stamp) VALUES (%s, %s, %s)"
		val = (float(temp), 4, time_in+timedelta(seconds=delta))
		print(time_in+timedelta(seconds=0.01*delta))
		mycursor.execute(sql, val)
		mydb.commit()
		# print('predicted=%f, expected=%f' % (yhat, obs))
	#error = mean_squared_error(test, predictions)
	#print('Test MSE: %.3f' % error)

	# Plotting the test/prediction results
	#pyplot.plot(test, color='blue')
	#pyplot.plot(predictions, color='red')
	#pyplot.show()

