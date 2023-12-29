import pandas as pd
import numpy as np


colspecs = [
    (0, 35),
    (36, 48),
    (49, 70),
    (71, 74), 
    (75, 100),  
    (101, 105),
    (106, 120),  
    (121, 135)  
]


column_names = [
    'identifier',
    'part_number',
    'name',
    'type_indicator',
    'extended_name',
    'unit_type',
    'price_field',
    'quantity_field'
]

df = pd.read_fwf('PP0006_MULTI.txt', colspecs=colspecs, header=None, encoding='ISO-8859-1')
df.columns = column_names

df['price_field'] = df['price_field'].str.extract('(\d+,\d+|\d+)')[0]


df['price_field'] = df['price_field'].str.replace(',', '.').astype(float) / 100  

df['manufacturer'] = df['part_number'].str[:3]

df['part_number'] = df['part_number'].str[3:]

df['quantity_field'] = pd.to_numeric(df['quantity_field'], errors='coerce').fillna(0).astype(int)

df = df[['part_number', 'manufacturer', 'price_field', 'quantity_field']]

df = df[df['quantity_field'] > 0]

df.to_csv('processed_data.csv', index=False)

print("Data processing complete. Output saved to 'processed_data.csv'.")

