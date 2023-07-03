import sys
import os
sys.path.append(os.getcwd())
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv(r'data\sales_data.csv', index_col = 0)
scaler = MinMaxScaler(feature_range=(10**-4, 1))
df['purchase_value_min_max'] = scaler.fit_transform(df[['purchase_value']])
y = df.groupby('product_id').agg(value_product = ('purchase_value_min_max', 'sum'))
y['target_q'] = pd.qcut(y['value_product'], q=4, labels=['Quartil 1', 'Quartil 2', 'Quartil 3', 'Quartil 4'])
df = df.merge(y.reset_index()[['product_id', 'target_q']], on=['product_id'], how='left')
df.to_csv(r'data\processed\dash_data.csv')