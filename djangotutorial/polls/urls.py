from django.urls import path
from . import views

urlpatterns = [
    # URL untuk visualisasi clustering produk
    path('cluster_products/', views.cluster_products_view, name='cluster_products'),
    
    # URL untuk visualisasi dampak diskon terhadap penjualan dengan regresi linear
    path('discount_impact/', views.discount_impact_view, name='discount_impact'),
    
    # URL untuk analisis tren pembelian pelanggan dengan linear regression
    path('customer_behavior_trend/', views.customer_behavior_trend_view, name='customer_behavior_trend'),
]
