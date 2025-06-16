from django.db import models

# Model untuk Sales Performance (Total Penjualan per Produk)
class SalesPerformance(models.Model):
    product_name = models.CharField(max_length=255)
    sales = models.FloatField()
    profit = models.FloatField()

    def __str__(self):
        return self.product_name


# Model untuk Discount Impact (Dampak Diskon terhadap Penjualan)
class DiscountImpact(models.Model):
    discount = models.FloatField()
    sales = models.FloatField()
    average_sales = models.FloatField()

    def __str__(self):
        return f"Discount: {self.discount}%"
        

# Model untuk Customer Behavior (Prediksi Laju Pembelian Pelanggan)
class CustomerBehavior(models.Model):
    customer_id = models.CharField(max_length=255)
    order_date = models.DateField()
    quantity = models.IntegerField()
    total_spend = models.FloatField()

    def __str__(self):
        return f"Customer {self.customer_id} on {self.order_date}"
