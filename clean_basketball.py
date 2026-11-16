import pandas as pd

df = pd.read_csv('data/basketball_teams.csv')

# 1. Numbers stored as text: '-' becomes NaN
num = ['Points', 'Games', 'Wins', 'Draws', 'Losses', 'Scored', 'Conceded']
df[num] = df[num].apply(pd.to_numeric, errors='coerce')

# 2. A team with no games has nothing to analyse: drop it
print('Teams without games:', df['Games'].isna().sum())
df = df.dropna(subset=['Games'])

# 3. In these two columns '-' means "never": that is 0, not missing
for col in ['Titles', 'RunnerUp']:
    df[col] = df[col].replace('-', 0).astype(int)

# 4. Mixed formats ('1946-47', '1947to48'): keep the first 4 digits as the founding year
df['Founded'] = df['Founded'].astype(str).str[:4].astype(int)

df['win_rate'] = (df['Wins'] / df['Games']).round(3)
print(df.sort_values('win_rate', ascending=False)[['Team', 'win_rate', 'Titles']].head(5))
print(df.groupby(df['Titles'] > 0)['win_rate'].mean().round(3))
df.to_csv('data/clean_basketball_teams.csv', index=False)