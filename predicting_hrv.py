#Pull in the data from the spreadsheet that we built in the last blog
import pandas as pd
data = pd.read_csv("new_improved_metrics.csv")
print(data)

#Add tomorrow's HRV (the variable that we're going to try and predict) to the dataframe
data['tomorrows_hrv'] = data['HRV'].shift(-1)
print(data)

#Clean up the data by dropping any rows with NaN values
data.info()
data = data.dropna()
data.info()

#Separate the data into a Training set (80%) and a Test set (20%)
from sklearn.model_selection import train_test_split
data_train, data_test = train_test_split(data, test_size=0.2, random_state=42)
print(f"Training Data: {data_train}")
print(f"Test Data: {data_test}")

#Pick some good features to test in our model
corr_matrix = data.corr()
corr_matrix['tomorrows_hrv'].sort_values(ascending=False)

#Build the matrix of features that we want to test (X) and a vector of the variable that we want to predict(y)
X_train = data_train[['Sleep Quality', 'TSS', 'Stress']]
y_train = data_train['tomorrows_hrv']
X_test = data_test[['Sleep Quality', 'TSS', 'Stress']]
y_test = data_test['tomorrows_hrv']
print(X_train)
print(y_train)

#Fix typo in our feature names
print(data_train.columns)
data_train.rename(columns={'Sleep Qualilty':'Sleep Quality'}, inplace=True)
data_test.rename(columns={'Sleep Qualilty':'Sleep Quality'}, inplace=True)
print(data_train.columns)
X_train = data_train[['Sleep Quality','TSS', 'Stress']]
y_train = data_train['tomorrows_hrv']
X_test = data_test[['Sleep Quality','TSS', 'Stress']]
y_test = data_test['tomorrows_hrv']
print(X_train)
print(y_train)

#Build linear model
from sklearn.linear_model import LinearRegression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

#Make a prediction of HRV for sleep quality of 5, training load of 100TSS and stress of 1
prediction = linear_model.predict([[5, 100, 1]])
print(f"Predicted HRV: {prediction}")

#Look at the long term data to get some context on whether the prediction is a good or bad number
data['HRV'].describe()

#Make a prediction for a high stress, high training load, low sleep quality day
prediction = linear_model.predict([[5, 300, 1]])
print(f"Predicted HRV: {prediction}")

#Make a prediction for a rest day
prediction = linear_model.predict([[1, 0, 4]])
print(f"Predicted HRV: {prediction}")

#Test the error of our model on the test set
import numpy as np
from sklearn.metrics import mean_squared_error
predictions = linear_model.predict(X_test)
linear_model_mse = mean_squared_error(y_test, predictions)
linear_model_rmse = np.sqrt(linear_model_mse)
print(f"Error: {linear_model_rmse}")















