import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans,AgglomerativeClustering,MeanShift
from sklearn.metrics import silhouette_score,calinski_harabasz_score,davies_bouldin_score
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv("Wholesale customers data.csv")

data=data.drop(["Channel","Region"],axis=1)

def preprocess_data(input_data,steps_to_apply):
    new_data=input_data.copy()

    if "log" in steps_to_apply:
        new_data=np.log1p(new_data)

    if "normalize" in steps_to_apply:
        scaler=MinMaxScaler()
        new_data=scaler.fit_transform(new_data)

    elif "standardize" in steps_to_apply:
        scaler=StandardScaler()
        new_data=scaler.fit_transform(new_data)

    else:
        new_data=new_data.values

    if "pca" in steps_to_apply:
        pca=PCA(n_components=2)
        new_data=pca.fit_transform(new_data)

    return new_data

def apply_clustering(X,algorithm_name,num_clusters=None):
    if algorithm_name=="kmeans":
        model=KMeans(n_clusters=num_clusters,random_state=42)
        labels=model.fit_predict(X)

    elif algorithm_name=="agglo":
        model=AgglomerativeClustering(n_clusters=num_clusters)
        labels=model.fit_predict(X)

    elif algorithm_name=="meanshift":
        model=MeanShift()
        labels=model.fit_predict(X)
        num_clusters=len(np.unique(labels))

    else:
        print("Unknown clustering algorithm.")
        return None,num_clusters

    if len(set(labels))<=1:
        return {"silhouette":-1,"calinski":-1,"davies":-1},num_clusters

    scores={
        "silhouette":silhouette_score(X,labels),
        "calinski":calinski_harabasz_score(X,labels),
        "davies":davies_bouldin_score(X,labels)
    }

    return scores,num_clusters

preprocessing_methods={
    "No Processing":[],
    "Using Normalization":["normalize"],
    "Using Transform":["log","standardize"],
    "Using PCA":["pca"],
    "Using T+N":["log","normalize"],
    "Using T+N+PCA":["log","normalize","pca"]
}

clustering_methods={
    "KMeans":"kmeans",
    "Hierarchical":"agglo",
    "KMeans Shift":"meanshift"
}

all_results=[]

for prep_name,prep_steps in preprocessing_methods.items():
    for cluster_name,cluster_type in clustering_methods.items():

        if cluster_type=="meanshift":
            processed_data=preprocess_data(data,prep_steps)
            scores,final_k=apply_clustering(processed_data,cluster_type)

            result={
                "Preprocessing":prep_name,
                "Algorithm":cluster_name,
                "Clusters":final_k,
                "Silhouette":round(scores["silhouette"],3),
                "Calinski-Harabasz":round(scores["calinski"],2),
                "Davies-Bouldin":round(scores["davies"],3)
            }
            all_results.append(result)

        else:
            for k in range(3,6):
                processed_data=preprocess_data(data,prep_steps)
                scores,_=apply_clustering(processed_data,cluster_type,k)

                result={
                    "Preprocessing":prep_name,
                    "Algorithm":cluster_name,
                    "Clusters":k,
                    "Silhouette":round(scores["silhouette"],3),
                    "Calinski-Harabasz":round(scores["calinski"],2),
                    "Davies-Bouldin":round(scores["davies"],3)
                }
                all_results.append(result)

results_df=pd.DataFrame(all_results)

final_csv_blocks=[]

for algorithm in clustering_methods.keys():
    filtered=results_df[results_df["Algorithm"]==algorithm].copy()
    filtered=filtered.drop(columns="Algorithm")
    filtered=filtered.sort_values(by=["Preprocessing","Clusters"])

    title_row=pd.DataFrame([[f"{algorithm} Clustering Results","","","",""]],
                            columns=filtered.columns)

    final_csv_blocks.append(title_row)
    final_csv_blocks.append(filtered)
    final_csv_blocks.append(pd.DataFrame([[""]*len(filtered.columns)],columns=filtered.columns))

final_output=pd.concat(final_csv_blocks,ignore_index=True)
final_output.to_csv("clustering_results.csv",index=False)
print("Results saved to 'clustering_results.csv'")

# Plotting
sns.set(style="whitegrid")
metrics=["Silhouette","Calinski-Harabasz","Davies-Bouldin"]

for metric in metrics:
    plt.figure(figsize=(14,6))
    sns.barplot(data=results_df,x="Preprocessing",y=metric,hue="Algorithm")
    plt.title(f"{metric} Score by Clustering Algorithm and Preprocessing Method")
    plt.xticks(rotation=45)
    plt.legend(title="Algorithm")
    plt.tight_layout()
    plt.show()
