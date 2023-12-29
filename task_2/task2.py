import pandas as pd
import sqlite3

# Load your existing price list DataFrame (assuming it's already been created)
# If 'filtered_df' is not yet defined, you would need to create it using the merging and filtering code from earlier
filtered_df = pd.read_csv('processed_price_list.csv')


# Load the sample_supplier.csv file
sample_supplier_df = pd.read_csv('sample_supplier.csv', delimiter='\t')
# Make sure the 'price' column is in the correct format, if not you'll need to convert it
# sample_supplier_df['price'] = ...

# Create a connection to an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Load DataFrames into the database
filtered_df.to_sql('current_prices', conn, index=False, if_exists='replace')
sample_supplier_df.to_sql('sample_supplier', conn, index=False, if_exists='replace')

# Perform an SQL query to find better prices
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
# Save the SQL query to a text file for task 2
with open('/home/sonya/new_task/task_2/price_comparison_query.txt', 'w') as file:
    file.write(query)



# Execute the query and put the result into a new DataFrame
better_prices_df = pd.read_sql_query(query, conn)

# Save the comparison result to a CSV file, formatted for Excel
better_prices_df.to_csv('/home/sonya/new_task/task_2/price_comparison.csv', index=False)

# Print the head of the resulting DataFrame to verify
print(better_prices_df.head())

# Close the SQL connection
conn.close()

