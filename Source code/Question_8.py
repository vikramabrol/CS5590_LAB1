import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(style='ggplot')
plt.rcParams['figure.figsize'] = (10, 6)

airfare = pd.read_csv("airq402.csv")
#show descriptive stats and skewness with average airfare as output variables
print(airfare.avrg_fare.describe())
print("skewness:", airfare.avrg_fare.skew())
plt.hist(airfare.avrg_fare)
plt.show()

#Correlation between X and Y variables
numeric_features = airfare.select_dtypes(include=[np.number])
corr = numeric_features.corr()
print (corr['avrg_fare'].sort_values(ascending=False)[:10], '\n')
plt.matshow(corr)
corr.style.background_gradient(cmap='coolwarm')
plt.show()

##check on null values
nulls = pd.DataFrame(airfare.isnull().sum().sort_values(ascending=False)[:25])
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
print(nulls)


##Build a linear model
data = airfare.select_dtypes(include=[np.number])
data_eda = data.drop(['mkt_share_h', 'mkt_share_l'], axis=1)

y = np.log(airfare.avrg_fare)
X = data.drop(['avrg_fare'], axis=1)
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
                                    X, y, random_state=42, test_size=.33)

#build multiple regression model
from sklearn import linear_model
mlr= linear_model.LinearRegression()
model= mlr.fit(X_train,y_train)

##Evaluate the performance and visualize results
print ("R^2 is: \n", model.score(X_test, y_test))
predictions = model.predict(X_test)
from sklearn.metrics import mean_squared_error
print ('RMSE is: \n', mean_squared_error(y_test, predictions))
print('coefficients: \n', mlr.coef_)

actual_values = y_test
plt.scatter(predictions, actual_values, alpha=.75,
            color='b')
plt.xlabel('Predicted')
plt.ylabel('Y_test')
plt.show()

### Scores after EDA

y_eda = np.log(airfare.avrg_fare)
X_eda = data_eda.drop(['avrg_fare'], axis=1)
X_train_eda, X_test_eda, y_train_eda, y_test_eda = train_test_split(
                                    X_eda, y_eda, random_state=42, test_size=.33)

#build multiple regression model
model_eda = mlr.fit(X_train_eda,y_train_eda)

##Evaluate the performance and visualize results
print ("R^2 after EDA is: \n", model_eda.score(X_test_eda, y_test_eda))
predictions_eda = model.predict(X_test_eda)
from sklearn.metrics import mean_squared_error
print ('RMSE after EDA is: \n', mean_squared_error(y_test_eda, predictions_eda))
print('coefficients after EDA: \n', mlr.coef_)

actual_values_eda = y_test_eda
plt.scatter(predictions_eda, actual_values_eda, alpha=.75,
            color='b')
plt.xlabel('Predicted_EDA')
plt.ylabel('Y_test_EDA')
plt.show()