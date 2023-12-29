import pandas as pd


prices_df = pd.read_csv('prices.csv', delimiter='\t')
data_df = pd.read_csv('data.csv', delimiter='\t')
quantity_df = pd.read_csv('quantity.csv', delimiter='\t')

prices_df.columns = ['part_number', 'price']
data_df.columns = ['part_number', 'manufacturer']
quantity_df.columns = ['part_number', 'quantity']

quantity_df['quantity'] = pd.to_numeric(quantity_df['quantity'].replace('>10', '11'), errors='coerce')

prices_df['price'] = prices_df['price'].str.replace(',', '.').astype(float)

quantity_df.dropna(subset=['quantity'], inplace=True)


prices_df['part_number'] = prices_df['part_number'].astype(str)
data_df['part_number'] = data_df['part_number'].astype(str)
quantity_df['part_number'] = quantity_df['part_number'].astype(str)


merged_df = pd.merge(data_df, prices_df, on='part_number', how='inner')
merged_df = pd.merge(merged_df, quantity_df, on='part_number', how='inner')



filtered_df = merged_df[(merged_df['price'] > 0) & (merged_df['quantity'] > 0)]


report = filtered_df['manufacturer'].value_counts().rename_axis('Manufacturer').reset_index(name='Number of Parts')


report = filtered_df['manufacturer'].value_counts().rename_axis('Manufacturer').reset_index(name='Number of Parts')


report.to_csv('/home/sonya/new_task/manufacturers_report.csv', index=False)


report_lines = [f"{row['Manufacturer']} - {row['Number of Parts']} rows" for index, row in report.iterrows()]


report_text = "\n".join(report_lines)


report_file_path = '/home/sonya/new_task/brands_report.txt'
with open(report_file_path, 'w') as report_file:
    report_file.write(report_text)





