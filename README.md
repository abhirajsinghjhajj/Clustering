# 🧪 Clustering Analysis on Wholesale Customers Dataset

This project performs a **comparative performance study** of different clustering algorithms using various **preprocessing techniques**, **cluster counts**, and **evaluation metrics** on a dataset from the **UCI Machine Learning Repository**.

## 📌 Objective

The goal is to explore how different combinations of preprocessing steps and clustering algorithms affect the quality of clusters, using the **Wholesale customers dataset**.

---

## 📊 Dataset Information

- **Features used:** Fresh, Milk, Grocery, Frozen, Detergents_Paper, Delicassen
- **Removed:** 'Channel' and 'Region' columns (non-informative for clustering)

---

## 🧹 Preprocessing Techniques Used

We tried various preprocessing combinations:
- **None**
- **Normalization (Min-Max Scaling)**
- **Log Transformation + Standardization**
- **PCA (Principal Component Analysis)**
- **Log Transformation + Normalization**
- **Log Transformation + Normalization + PCA**

---

## 🤖 Clustering Algorithms Applied

- **KMeans**
- **Hierarchical Clustering (Agglomerative)**
- **Mean Shift**

KMeans and Hierarchical clustering were tested with **3 to 5 clusters**. Mean Shift automatically determines the number of clusters.

---

## 📏 Evaluation Metrics

We evaluated cluster quality using:
- **Silhouette Score** (higher = better)
- **Calinski-Harabasz Index** (higher = better)
- **Davies-Bouldin Index** (lower = better)

---

## 📈 Results & Visualizations

The notebook includes:
- Tables comparing performance across methods
- Bar plots for each metric (Silhouette, Calinski-Harabasz, Davies-Bouldin)
- Observations on which combinations work best

---

## ✅ Key Observations

- Preprocessing **significantly affects** clustering results.
- Using **log + normalization + PCA** often leads to better scores.
- **KMeans** generally performs well but may depend on initial cluster count.
- **Mean Shift** can automatically find clusters but may be slower.

---
