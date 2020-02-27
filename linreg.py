import numpy as np
import pandas as pd
from io import StringIO
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

# data=np.genfromtxt('train.csv',dtype=None, delimiter=',',names=True)

# # print(x)

# define the data/predictors as the pre-set feature names  
data = pd.read_csv('train.csv').values
y_actual= data[:, 3]
x=data[:, 0:3].astype(int)
# print(type(y_actual))
print(x)
# print(x[1])
# print(x[1][1])
# print(x[1,1])

regr = linear_model.LinearRegression()
regr.fit(x,y_actual)
tmp=np.array([[1,0,1]])
y_pred=regr.predict(tmp)
print(y_pred)
print('Coefficients: \n', regr.coef_)
