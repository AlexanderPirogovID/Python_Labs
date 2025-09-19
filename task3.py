import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore


data = {
    'Товар': ['Яблоки', 'Бананы', 'Апельсины', 'Груши', 'Яблоки', 'Бананы'],
    'Цена': [50, 80, np.nan, 70, 55, 85],
    'Количество': [100, 50, 200, -5, 150, 2000]
}

df = pd.DataFrame(data)


median_price = df['Цена'].median()
df['Цена'] = df['Цена'].fillna(median_price)


df = df[(df['Количество'] >= 1) & (df['Количество'] <= 1000)]


df['Общая_стоимость'] = df['Цена'] * df['Количество']


revenue_by_product = df.groupby('Товар')['Общая_стоимость'].sum()


plt.figure(figsize=(10, 6))
revenue_by_product.plot(kind='bar', color=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
plt.title('Выручка по товарам')
plt.xlabel('Товар')
plt.ylabel('Выручка (руб)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Итоговый DataFrame:")
print(df)
print("\nВыручка по товарам:")
print(revenue_by_product)