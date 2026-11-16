import pandas as pd

games = pd.read_csv('data/Games.csv', low_memory=False)
games['date'] = pd.to_datetime(games['gameDateTimeEst'])
# The NBA season starts in October: October 2024 to June 2025 is season 2024
games['season'] = games['date'].dt.year - (games['date'].dt.month < 10).astype(int)

REGULAR = ['Regular Season', 'NBA Emirates Cup', 'Emirates NBA Cup', 'NBA Cup']   # cup games count too
games = games[games['gameType'].isin(REGULAR)]
games = games[(games['season'] >= 2013) & (games['season'] <= 2025)]   # complete seasons only
games = games.dropna(subset=['homeScore', 'awayScore']).drop_duplicates('gameId')
games = games[games['homeScore'] != games['awayScore']]                # a tie is not a finished game

def one_side(home):
    own, other = ('home', 'away') if home else ('away', 'home')
    df = pd.DataFrame({'GAME_ID': games['gameId'], 'season': games['season'], 'GAME_DATE': games['date'].dt.strftime('%Y-%m-%d'),
                       'TEAM_ID': games[f'{own}teamId'], 'PTS': games[f'{own}Score'],
                       'PLUS_MINUS': games[f'{own}Score'] - games[f'{other}Score']})
    df['TEAM_ABBREVIATION'] = games[f'{own}teamName']
    df['MATCHUP'] = games[f'{own}teamName'] + (' vs. ' if home else ' @ ') + games[f'{other}teamName']
    df['WL'] = (df['PLUS_MINUS'] > 0).map({True: 'W', False: 'L'})
    return df

# One game becomes two rows (one per team): the shape the next script expects.
raw = pd.concat([one_side(True), one_side(False)], ignore_index=True)
raw.to_csv('data/basket_raw.csv', index=False)
print('Saved', raw.shape, '| seasons', raw['season'].min(), '-', raw['season'].max())