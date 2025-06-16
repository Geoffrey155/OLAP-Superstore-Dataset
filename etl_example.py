from airflow import DAG 
from airflow.operators.python import PythonOperator  # type: ignore
from datetime import datetime
import pandas as pd
import os

dag_path = os.path.dirname(__file__)

# 1. Extract Data untuk Sales Performance
def extract_sales_data():
    csv_path = os.path.join(dag_path, 'Sample - Superstore.csv')

    # Membaca dataset CSV
    df = pd.read_csv(csv_path)
    
    # Ekstrak kolom yang relevan untuk Sales Performance
    df_sales = df[['Product Name', 'Sales', 'Profit']]
    
    # Pastikan tidak ada data NaN atau nilai yang tidak relevan
    df_sales = df_sales.dropna(subset=['Sales', 'Profit'])

    # Menyimpan data hasil ekstraksi ke file sementara
    df_sales.to_csv('/tmp/extracted_sales_data.csv', index=False)

# 2. Extract Data untuk Discount Impact 
def extract_discount_data():
    csv_path = os.path.join(dag_path, 'Sample - Superstore.csv')
    df = pd.read_csv(csv_path)

    # Mengambil data diskon , penjualan , dan menghitung total penjualan per tingkat diskon
    df_discount = df.groupby(['Discount'])['Sales'].sum().reset_index()
    
    # Menyimpan data hasil ekstraksi ke file sementara
    df_discount.to_csv('/tmp/extracted_discount_data.csv', index=False)

# 3. Extract Data untuk Customer Behavior
def extract_customer_behavior_data():
    csv_path = os.path.join(dag_path, 'Sample - Superstore.csv')
    df = pd.read_csv(csv_path)
    
    # Menyimpan data hasil ekstraksi ke file sementara
    df.to_csv('/tmp/extracted_customer_behavior_data.csv', index=False)

# 4. Transform Data untuk Sales Performance 
def transform_sales_data():
    df = pd.read_csv('/tmp/extracted_sales_data.csv')
    
    df.to_csv('/tmp/transformed_sales_data.csv', index=False)

# 5. Transform Data untuk Discount Impact 
def transform_discount_data():
    df = pd.read_csv('/tmp/extracted_discount_data.csv')
    
    # Transformasi untuk menghitung rata-rata penjualan per tingkat diskon
    df['Average_Sales'] = df['Sales'] / df['Discount']

    df.to_csv('/tmp/transformed_discount_data.csv', index=False)

# 6. Transform Data untuk Customer Behavior 
def transform_customer_behavior_data():

    df = pd.read_csv('/tmp/extracted_customer_behavior_data.csv')
     

    # Mengelompokkan data berdasarkan Region dan menghitung total profit per region
    df_grouped = df.groupby('Region')['Profit'].sum().reset_index() 

    df_grouped.to_csv('/tmp/transformed_customer_behavior_data.csv', index=False)

# 7. Load Data untuk Sales Performance
def load_sales_data():
    df = pd.read_csv('/tmp/transformed_sales_data.csv')

    df.to_csv(os.path.join(dag_path, 'OLAP_sales_data.csv'), index=False)

# 8. Load Data untuk Discount Impact
def load_discount_data():
    df = pd.read_csv('/tmp/transformed_discount_data.csv')

    df.to_csv(os.path.join(dag_path, 'OLAP_discount_data.csv'), index=False)

# 9. Load Data untuk Customer Behavior
def load_customer_behavior_data():
    df = pd.read_csv('/tmp/transformed_customer_behavior_data.csv')

    df.to_csv(os.path.join(dag_path, 'OLAP_customer_behavior.csv'), index=False)

# Mendefinisikan DAG
with DAG(
    dag_id='etl_superstore',
    start_date=datetime(2023, 1, 1),
    #schedule_interval='@daily',  
    schedule='@daily',
    catchup=False,
    tags=['etl', 'superstore']
) as dag:
    
    # Task untuk Sales Performance
    t1 = PythonOperator(
        task_id='extract_sales_data',
        python_callable=extract_sales_data
    )
    t2 = PythonOperator(
        task_id='transform_sales_data',
        python_callable=transform_sales_data
    )
    t3 = PythonOperator(
        task_id='load_sales_data',
        python_callable=load_sales_data
    )

    # Task untuk Discount Impact
    t4 = PythonOperator(
        task_id='extract_discount_data',
        python_callable=extract_discount_data
    )
    t5 = PythonOperator(
        task_id='transform_discount_data',
        python_callable=transform_discount_data
    )
    t6 = PythonOperator(
        task_id='load_discount_data',
        python_callable=load_discount_data
    )

    # Task untuk Customer Behavior
    t7 = PythonOperator(
        task_id='extract_customer_behavior_data',
        python_callable=extract_customer_behavior_data
    )
    t8 = PythonOperator(
        task_id='transform_customer_behavior_data',
        python_callable=transform_customer_behavior_data
    )
    t9 = PythonOperator(
        task_id='load_customer_behavior_data',
        python_callable=load_customer_behavior_data
    )


    t1 >> t2 >> t3
    t4 >> t5 >> t6
    t7 >> t8 >> t9
