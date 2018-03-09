import re # regex
import requests
from bs4 import BeautifulSoup # scraper library

import pandas as pd # tables
from collections import OrderedDict

# Config
base_page_url = 'https://www.teamrankings.com/ncaa-basketball/stat/'
date_range = pd.date_range(pd.datetime(2018, 1, 1), periods=59).tolist()

stat_types = [
        'points-per-game'
        ]
stats_urls = [ base_page_url + stat for stat in stat_types ]

def scrape_stats(page_url):
    stats_df = None
    stats = {}

    for date in date_range:
        url = page_url + '?date=' + str(date.date())

        print(url)

        page = requests.get(url) # load page
        soup = BeautifulSoup(page.text, 'html5lib') # parse
        table = soup.find('table', class_='datatable').find('tbody')
        rows = table.find_all('tr')

        # Go through rows
        for i in range(351):
            row = rows[i].find_all('td')
            team_name = row[1].get_text()
            stat_val = row[2].get_text()

            # Add to stats
            if team_name not in stats:
                stats[team_name] = {}

            stats[team_name][str(date.date())] = stat_val

        stats_df_data = [ [ team_name, *v.values() ] for team_name,v in stats.items() ]
        stats_df_columns = ['Team Name'] + list(stats[list(stats.keys())[0]].keys())
        stats_df = pd.DataFrame(data = stats_df_data, columns = stats_df_columns)

        print(stats_df)

    return stats_df

scrape_stats('https://www.teamrankings.com/ncaa-basketball/stat/points-per-game')


# Scrape some data!
# Load game stats and season stats tables
# game_stats_el, season_stats_el = soup.find_all('table', attrs={'class': 'tablehead'})

# def scrape_stats(table_el):
#     stats = []
# 
#     # Get column names
#     colhead_el = table_el.find('tr', attrs={'class': 'colhead'})
#     col_names = [ col.text for col in colhead_el.children ]
# 
#     # Get player and total stats
#     players_els = table_el.find_all('tr', attrs={'class': re.compile('(^player-)|(^total$)')})
#     for player_el in players_els: # each player is represented by one table row
#         player = OrderedDict() # empty initially
#         for col_idx, col_el in enumerate(player_el.children):
#             col_name = col_names[col_idx]
#             player[col_name] = col_el.text # fill in stat
#         stats.append(player) # add to list
# 
#     return stats

# # Lo and behold
# game_stats = scrape_stats(game_stats_el)
# season_stats = scrape_stats(season_stats_el)
# 
# # Put these into some pandas dataframes
# game_stats = pd.DataFrame.from_dict(game_stats)
# season_stats = pd.DataFrame.from_dict(season_stats)
# 
# print(game_stats)
# print(season_stats)
# 
# # Export to csv
# game_stats.to_csv('game_stats.csv')
# season_stats.to_csv('season_stats.csv')
