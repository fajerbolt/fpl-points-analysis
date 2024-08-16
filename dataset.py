import pandas as pd
import numpy as np

#Import all initial dataframes
players_raw = pd.read_csv('players_raw.csv')
players_cleaned = pd.read_csv('cleaned_players.csv')
gameweeks = pd.read_csv('merged_gw.csv')

#Points Breakdown
GK_DEF_GOAL = 6
MID_GOAL = 5
ATT_GOAL = 4
ASSIST = 3
GK_DEF_CLEAN_SHEET = 4
MID_CLEAN_SHEET = 1
PEN_SAVE = 5
PEN_MISS = -2
YC = -1
RC = -3
OWN_GOAL = -2

#Check for wrongly spelled names
#gameweeks[~gameweeks.name.isin(players_cleaned['first_name'] + ' ' + players_cleaned['second_name'])]
#Replace wrongly spelled names
gameweeks.replace({'Djordje Petrovic': 'Đorđe Petrović',
                   'Yegor Yarmolyuk': 'Yegor Yarmoliuk',
                   'Michale Olakigbe': 'Michael Olakigbe'}, inplace=True)

#Calculate points from minutes, saves and goals conceded
gameweeks['minutes_points'] = np.where(gameweeks['minutes'] ==0, 0, np.where(
    gameweeks['minutes'] >=60, 2, 1
))
gameweeks['saves_points'] = gameweeks['saves']//3
gameweeks['goals_conceded_points'] = np.where(gameweeks['position'].isin(['GK', 'DEF']), (gameweeks['goals_conceded']//2)*(-1), 0)

saves_gc_points = gameweeks.groupby('name').agg({'minutes_points': 'sum',
                                                'saves_points': 'sum',
                                                'goals_conceded_points': 'sum'})

#Merge dataframes
players_cleaned['full_name'] = players_cleaned['first_name'] + ' ' + players_cleaned['second_name']
players_cleaned = pd.merge(players_cleaned, saves_gc_points, left_on=['full_name'], right_index=True, validate='1:1')

additional_stats = players_raw[['own_goals', 'penalties_missed', 'penalties_saved', 'first_name', 'second_name']]
players_cleaned = pd.merge(players_cleaned, additional_stats, on=['first_name', 'second_name'], validate='1:1')

#Calculate points from stats
players_cleaned['assists_points'] = ASSIST*players_cleaned['assists']
players_cleaned['penalty_saves_points'] = PEN_SAVE*players_cleaned['penalties_saved']
players_cleaned['penalty_misses_points'] = PEN_MISS*players_cleaned['penalties_missed']
players_cleaned['yellow_cards_points'] = YC*players_cleaned['yellow_cards']
players_cleaned['red_cards_points'] = RC*players_cleaned['red_cards']
players_cleaned['own_goals_points'] = OWN_GOAL*players_cleaned['own_goals']



players_cleaned['goals_scored_points'] = np.where(
    players_cleaned['element_type'].isin(['GK', 'DEF']), GK_DEF_GOAL*players_cleaned['goals_scored'], np.where(
    players_cleaned['element_type']=='MID', MID_GOAL*players_cleaned['goals_scored'], ATT_GOAL*players_cleaned['goals_scored']
    )
)

players_cleaned['clean_sheet_points'] = np.where(
    players_cleaned['element_type'].isin(['GK', 'DEF']), GK_DEF_CLEAN_SHEET*players_cleaned['clean_sheets'], np.where(
    players_cleaned['element_type']=='MID', MID_CLEAN_SHEET*players_cleaned['clean_sheets'], 0
    )
)

#Select columns for dataset
player_points = players_cleaned[['full_name', 'element_type', 'now_cost',
                 'total_points', 
                 'minutes_points',
                 'bonus', 
                 'goals_scored_points', 'assists_points', 'penalty_misses_points', 'own_goals_points',
                 'goals_conceded_points','saves_points', 'penalty_saves_points', 'clean_sheet_points',
                 'yellow_cards_points', 'red_cards_points']]

#Validity check
validity_filter = player_points.iloc[:, 4:].sum(axis=1) == player_points.total_points
if not player_points[~validity_filter].empty:
    raise Exception('Some rows stats do not add up to total points')

#Export to csv
player_points.to_csv('player_points.csv', index=False)