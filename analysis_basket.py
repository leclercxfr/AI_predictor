import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('charts', exist_ok=True)

df = pd.read_csv('data/practice_basket.csv')
print(df.groupby('win')[['points_for']].mean())

wins = df[df['win'] == 1]
losses = df[df['win'] == 0]
avg_loss = losses['points_for'].mean()
avg_win = wins['points_for'].mean()

plt.figure(figsize=(6, 5))
plt.bar(['Loss', 'Win'], [avg_loss, avg_win])
plt.xlabel('Hasil laga')
plt.ylabel('Rata-rata poin')
plt.savefig('charts/avg_points.png', dpi=150)
plt.show()