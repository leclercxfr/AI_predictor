import pandas as pd

df = pd.read_csv('data/basket_raw.csv', parse_dates=['GAME_DATE'])
df = df.sort_values(['TEAM_ID', 'GAME_DATE']).reset_index(drop=True)
df['win'] = (df['WL'] == 'W').astype(int)
# 'Lakers vs. Celtics' = home game, 'Lakers @ Celtics' = away game
df['is_home'] = df['MATCHUP'].str.contains('vs.', regex=False).astype(int)
df['rest_days'] = (df.groupby(['TEAM_ID', 'season'])['GAME_DATE']
                     .diff().dt.days.fillna(7).clip(upper=7))

# Form = point margin averaged over EARLIER games only (shift(1) drops the current game).
team = df.groupby('TEAM_ID')
for n in (5, 10, 20):
    df[f'margin_{n}'] = team['PLUS_MINUS'].transform(lambda s: s.shift(1).rolling(n, min_periods=1).mean())
df['season_win'] = (df.groupby(['TEAM_ID', 'season'])['win']
                      .transform(lambda s: s.shift(1).expanding().mean()).fillna(0.5))
df = df.dropna(subset=['margin_5'])           # a team's very first game has no history

# Put the opponent next to each row (same GAME_ID, other team) and keep the DIFFERENCE.
stats = ['rest_days', 'margin_5', 'margin_10', 'margin_20', 'season_win']
opp = df[['GAME_ID', 'TEAM_ID'] + stats].rename(columns={'TEAM_ID': 'OPP_ID', **{c: 'opp_' + c for c in stats}})
df = df.merge(opp, on='GAME_ID')
df = df[df['TEAM_ID'] != df['OPP_ID']]
for c in stats:
    df['diff_' + c] = df[c] - df['opp_' + c]

cols = ['season', 'GAME_DATE', 'TEAM_ABBREVIATION', 'MATCHUP', 'is_home'] + ['diff_' + c for c in stats] + ['win']
df[cols].to_csv('data/clean_basket_real.csv', index=False)
print(df[cols].shape, f"win rate: {df['win'].mean():.1%}")