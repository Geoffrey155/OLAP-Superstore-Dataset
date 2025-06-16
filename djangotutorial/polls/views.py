from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.preprocessing import LabelEncoder

# 1. Clustering Produk - Sales Performance
def cluster_products_view(request):
    # Load df yang sudah diproses
    df = pd.read_csv('../OLAP_sales_data.csv')  # Ganti dengan path yang sesuai

    # Mengambil df untuk visualisasi
    products = df[['Product Name', 'Sales', 'Profit']]  # Menggunakan Sales dan Profit untuk clustering

    # Menggunakan K-Means untuk clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['Cluster'] = kmeans.fit_predict(products[['Sales', 'Profit']])

    # Kirim df ke template
    chart_data = {
        'sales': df['Sales'].tolist(),
        'profit': df['Profit'].tolist(),
        'cluster': df['Cluster'].tolist(),
    }

    return render(request, 'cluster_products.html', {'chart_data': chart_data})


# 2. Dampak Diskon terhadap Penjualan - Discount Impact dengan Regresi Linear
def discount_impact_view(request):
    # Load df yang sudah diproses
    df = pd.read_csv('../OLAP_discount_data.csv')  

    # Mengambil df untuk visualisasi
    discounts = df['Discount']
    sales = df['Sales']

    # Regresi Linear untuk menganalisis dampak diskon terhadap penjualan
    model = LinearRegression()
    X = discounts.values.reshape(-1, 1)
    y = sales
    model.fit(X, y)

    # Prediksi Trend Line
    trend_line = model.predict(X)

    chart_data = {
        'discounts': discounts.tolist(),
        'actual_sales': sales.tolist(),
        'trend_line': trend_line.tolist(),
    }

    return render(request, 'discount_impact.html', {'chart_data': chart_data})


# 3. Clustering Profit Per Region
def customer_behavior_trend_view(request):
    # Load df yang sudah diproses
    df = pd.read_csv('../OLAP_customer_behavior.csv')

    # Label Encoding untuk Region
    label_encoder = LabelEncoder()
    df['Region_encoded'] = label_encoder.fit_transform(df['Region'])

    # KMeans Clustering berdasarkan Profit dan Region_encoded
    kmeans = KMeans(n_clusters=3, random_state=42)  # Menggunakan 3 cluster
    df['Cluster'] = kmeans.fit_predict(df[['Profit', 'Region_encoded']])

    # Menyiapkan df untuk visualisasi
    chart_data = {
        'regions': df['Region'].tolist(),
        'profits': df['Profit'].tolist(),
        'clusters': df['Cluster'].tolist()
    }
    

    return render(request, 'customer_behavior.html', {'chart_data': chart_data})
