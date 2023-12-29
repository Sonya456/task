import pandas as pd
import sqlite3

filtered_df = pd.read_csv('processed_price_list.csv')


sample_supplier_df = pd.read_csv('sample_supplier.csv', delimiter='\t')


conn = sqlite3.connect(':memory:')

filtered_df.to_sql('current_prices', conn, index=False, if_exists='replace')
sample_supplier_df.to_sql('sample_supplier', conn, index=False, if_exists='replace')

query = """
SELECT
    cp.part_number,
    cp.manufacturer,
    cp.price AS current_price,
    ss.price AS sample_price,
    CASE
        WHEN cp.price <= ss.price THEN 'Current'
        ELSE 'Sample'
    END AS better_price
FROM current_prices cp
INNER JOIN sample_supplier ss
    ON cp.part_number = ss.part_number AND cp.manufacturer = ss.manufacturer
"""
with open('/home/sonya/new_task/task_2/price_comparison_query.txt', 'w') as file:
    file.write(query)



better_prices_df = pd.read_sql_query(query, conn)

better_prices_df.to_csv('/home/sonya/new_task/task_2/price_comparison.csv', index=False)

print(better_prices_df.head())

conn.close()

