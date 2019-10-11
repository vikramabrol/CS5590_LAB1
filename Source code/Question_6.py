import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
#dataset from Kaggle (https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data)
dataset = pd.read_csv('AB_NYC_2019.csv')

##Null values
nulls = pd.DataFrame(dataset.isnull().sum().sort_values(ascending=False)[:25])
nulls.columns = ['Null Count']
nulls.index.name = 'Feature'
print(nulls)

#Drop nulls
data = dataset.select_dtypes(include=[np.number]).interpolate().dropna()
print(sum(data.isnull().sum() != 0))
print("\n")

#Setup x values off of dataset
x = data.select_dtypes(include=[np.number])
print(x.shape)

numeric_features = dataset.select_dtypes(include=[np.number])
corr = numeric_features.corr()
print(corr['reviews_per_month'].sort_values(ascending=False)[:10], '\n')


sns.FacetGrid(dataset, hue="neighbourhood_group", height=4).map(plt.scatter, "number_of_reviews","price").add_legend()
sns.FacetGrid(dataset, hue="neighbourhood_group", height=4).map(plt.scatter, "reviews_per_month","price").add_legend()
sns.FacetGrid(dataset, hue="neighbourhood_group", height=4).map(plt.scatter, "number_of_reviews","availability_365").add_legend()
sns.FacetGrid(dataset, hue="neighbourhood_group", height=4).map(plt.scatter, "calculated_host_listings_count","price").add_legend()
plt.show()

nclusters = 3  # this is the k in kmeans
km = KMeans(n_clusters=nclusters)
km.fit(x)
y_cluster_kmeans = km.predict(x)

from sklearn import metrics
score = metrics.silhouette_score(x, y_cluster_kmeans)
print("\n Silhoutte Score after applying KMeans")
print(score)
wcss= []
##elbow method to know the number of clusters
for i in range(1,8):
    kmeans= KMeans(n_clusters=i,init='k-means++', max_iter=500,random_state=0)
    kmeans.fit(x)
    wcss.append(kmeans.inertia_)
plt.plot(range(1,8),wcss, '-o')
plt.title('the elbow method')
plt.xlabel('Number of Clusters')
plt.ylabel('Wcss')
plt.show()

# We found k = 3 to be the best
from sklearn import preprocessing
scaler = preprocessing.StandardScaler()
scaler.fit(x)
X_scaler = scaler.transform(x)
X_scaled = pd.DataFrame(X_scaler, columns=x.columns)

from sklearn.decomposition import PCA
# Make an instance of the Model
pca= PCA(2)
X_pca= pca.fit_transform(X_scaler)

#Apply kmeans algorithm on the PCA result and report your observation if the score improved or not?
km_p = KMeans(n_clusters=3)
km_p.fit(X_pca)
y_cluster_kmeansp= km_p.predict(X_pca)

score_p = metrics.silhouette_score(X_pca, y_cluster_kmeansp)
print("\n Silhoutte Score after applying KMeans on PCA result dataset")
print(score_p)
