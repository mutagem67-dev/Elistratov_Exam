import pandas as pd

i = pd.read_csv('Order_items_analytics.csv')
m = pd.read_csv('Shoe_models_analytics.csv')

# Умный поиск ID товара в обоих файлах
i_id = next(c for c in i.columns if 'id' in c.lower() or 'товар' in c.lower() or 'product' in c.lower())
m_id = next(c for c in m.columns if 'id' in c.lower() or 'товар' in c.lower() or 'product' in c.lower())

# Поиск категории и количества
cat_col = next(c for c in m.columns if 'cat' in c.lower() or 'кат' in c.lower())
qty_col = next(c for c in i.columns if 'qty' in c.lower() or 'quant' in c.lower() or 'кол' in c.lower())

mm = i.merge(m, left_on=i_id, right_on=m_id)
print("5.6:", mm.groupby(cat_col)[qty_col].sum().idxmax())
