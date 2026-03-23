import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("../data/enhanced_data.csv")

# Select features
features = ['Recency', 'Frequency', 'Monetary']
X = df[features]


# K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X)


# Save Results
df.to_csv("../data/segmented_data.csv", index=False)

print("✅ Segmentation completed and saved!")

# Visualize Clusters
plt.scatter(df['Frequency'], df['Monetary'], c=df['Cluster'])
plt.xlabel("Frequency")
plt.ylabel("Monetary")
plt.title("Customer Segmentation")
plt.show()

print("\nCluster Summary:\n")
print(df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean())

def label_cluster(cluster):
    if cluster == 0:
        return "High Value"
    elif cluster == 1:
        return "Low Value"
    else:
        return "Medium Value"

df['Customer_Segment'] = df['Cluster'].apply(label_cluster)

df.to_csv("../data/segmented_data.csv", index=False)