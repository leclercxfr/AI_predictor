# config.py: one place for every setting. Every script reads from here.
import pandas as pd

DATA_FILE = 'data/clean_basket_real.csv'
TARGET = 'win'
FEATURES = ['is_home', 'diff_rest_days', 'diff_margin_5', 'diff_margin_10', 'diff_season_win']
TEST_SEASONS = 2

TITLE = 'NBA Win Predictor'
DESCRIPTION = ('Compares two NBA teams (home advantage, rest, recent form, season record) and '
               'scores how likely the home team is to win, using only what is known before tip-off.')
LABELS = {
    'is_home': 'Playing at home',
    'diff_rest_days': 'Rest days (team minus opponent)',
    'diff_margin_5': 'Point margin, last 5 games (team minus opponent)',
    'diff_margin_10': 'Point margin, last 10 games (team minus opponent)',
    'diff_season_win': 'Season record so far (team minus opponent)',
}

def baseline_predict(df):
    return df['is_home']                   # baseline: the home team always wins

def load_splits():
    """train = old seasons, valid = last training season, test = newest seasons (final exam)."""
    df = pd.read_csv(DATA_FILE)
    valid_season = df['season'].max() - TEST_SEASONS
    return (df[df['season'] < valid_season], df[df['season'] == valid_season],
            df[df['season'] > valid_season])