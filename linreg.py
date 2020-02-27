import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from sklearn import metrics
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

def train_dataset():
    global regr, y_actual
    # print(type(y_actual)
    # print(x)
    # print(x[1])
    # print(x[1][1])
    # print(x[1,1])
    # tmp=np.array()
    header = list(pd.read_csv('train.csv').columns)
    data = pd.read_csv('train.csv').values
    y_actual= data[:, 3]
    x=data[:, 0:3].astype(int)
    regr = linear_model.LinearRegression()
    regr.fit(x,y_actual)

def linearreg(test):
    train_dataset()
    y_pred=regr.predict(test)
    # df = pd.DataFrame({'Actual': y_actual, 'Predicted': y_pred})
    # coeff_df = pd.DataFrame(regr.coef_, header[: -1], columns=['Coefficient'])  
    # df1 = df.head(18)
    # df1.plot(kind='bar',figsize=(16,10))
    # plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
    # plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    print(y_pred)
    # print(coeff_df)
    print('Regression Intercept :',regr.intercept_)
    # print('Mean Absolute Error:', metrics.mean_absolute_error(y_actual, y_pred))  
    # print('Mean Squared Error:', metrics.mean_squared_error(y_actual, y_pred))  
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_actual, y_pred)))
    print('Coefficients: \n', regr.coef_)
    return(y_pred)
    # plt.show()