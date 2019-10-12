import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import seaborn as sns
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier

# Data from https://www.kaggle.com/rajeevw/ufcdata
train_df = pd.read_csv('ufcData.csv')
# train_df = pd.DataFrame(train)
# print(train_df.head())
nulls = pd.DataFrame(train_df.isnull().sum().sort_values(ascending=False))
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
print(nulls)

# Fill the rest of the columns with most frequent values
train_df = train_df.fillna(train_df.mode().iloc[0])
train_df['R_Stance'] = train_df['R_Stance'].map(
    {'Open Stance': 0, 'Orthodox': 1, 'Sideways': 2, 'Southpaw': 3, 'Switch': 4}).astype(int)

# Handle Nulls if any
data = train_df.select_dtypes(include=[np.number]).interpolate().dropna()
print(sum(data.isnull().sum() != 0))
print("\n")

# Nulls after last step
nulls = pd.DataFrame(data.isnull().sum().sort_values(ascending=False))
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
print(nulls)

# train_df = train_df.fillna(dataset.mode().iloc[0])

numeric_features = train_df.select_dtypes(include=[np.number])
corr = numeric_features.corr()
print(corr['R_wins'].sort_values(ascending=False)[:10], '\n')

sns.heatmap(corr,
            xticklabels=corr.columns,
            yticklabels=corr.columns)
plt.show()

# Assigning x and y for test and train data
# Since there are a lot of fields, consider only R_ category
data = data[
    ['R_wins', 'R_total_rounds_fought', 'R_longest_win_streak', 'R_win_by_Decision_Unanimous', 'R_win_by_KO/TKO',
     'R_losses', 'R_win_by_Submission', 'R_total_title_bouts', 'R_Stance']]
y = data['R_wins']
x = data.drop(['R_wins'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=42, test_size=0.33)

# Apply Naive Bayes
gaussian = GaussianNB()

gaussian.fit(X_train, y_train)
future_y_g = gaussian.predict(X_test)
acc_g = round(gaussian.score(X_test, y_test) * 100, 2)
print("Naive Bayes accuracy is:", acc_g)

# print("classification accuracy for Naive Bayes\n *******************")
# model_accuracy_nb = metrics.classification_report(y_test, future_y_g)
# print(model_accuracy_nb)

# Apply SVM
svm = svm.SVC(kernel='rbf', gamma='auto')

svm.fit(X_train, y_train)
future_y_svm = svm.predict(X_test)
acc_svm = round(svm.score(X_test, y_test) * 100, 2)
print("SVM accuracy is:", acc_svm)

# print("classification accuracy for SVM\n *******************")
# model_accuracy_svm = metrics.classification_report(y_test, future_y_svm)
# print(model_accuracy_svm)


# Apply KNN
knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(X_train, y_train)
future_y_knn = knn.predict(X_test)
acc_knn = round(knn.score(X_test, y_test) * 100, 2)
print("KNN accuracy is:", acc_knn)

# print("classification accuracy for KNN\n *******************")
# model_accuracy_svm = metrics.classification_report(y_test, future_y_knn)
# print(model_accuracy_knn)
