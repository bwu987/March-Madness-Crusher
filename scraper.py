import sys, os
import requests
from bs4 import BeautifulSoup # scraper library

import pandas as pd # tables
from collections import OrderedDict

# Config
base_page_url = 'https://www.teamrankings.com/ncaa-basketball/stat/'
date_range = pd.date_range(pd.datetime(2018, 1, 1), periods=59).tolist()

# dictionary: output_name: url
stat_types = {
        'pts_per_game': 'points-per-game',
        'pos_per_game': 'possessions-per-game',
        'field_goals_attempted': 'field-goals-attempted-per-game',
        'field_goals_made': 'field-goals-made-per-game',
        '3pt_attempted': 'three-pointers-attempted-per-game',
        '3pt_made': 'three-pointers-made-per-game',
        'ft_per_100_pos': 'ftm-per-100-possessions',
        'off_rebounds': 'offensive-rebounds-per-game',
        'ast_per_game': 'assists-per-game',
        'to_per_game': 'turnovers-per-game',
        'fouls_per_game': 'personal-fouls-per-game',
        'opp_pts_per_game': 'opponent-points-per-game',
        'opp_pts_from_3pt': 'opponent-points-from-3-pointers',
        'opp_pts_from_2pt': 'opponent-points-from-2-pointers',
        'def_rebounds': 'defensive-rebounds-per-game',
        'blocks_per_game': 'blocks-per-game',
        'steals_per_game': 'steals-per-game',
        'opp_to_per_game': 'opponent-turnovers-per-game',
        'opp_ast_per_game': 'opponent-assists-per-game',
        }

def scrape_stats(page_url, output_name):
    stats_df = None
    stats = {}

    for date_i, date in enumerate(date_range):
        date = str(date.date())
        url = page_url + '?date=' + date

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

            stats[team_name][date] = stat_val

        print(f"{output_name}: Fetching date: {date} [{date_i+1}/{len(date_range)}]", end='\r')

    print()

    # Convert to pandas dataframe
    stats_df_data = [ [ team_name, *v.values() ] for team_name,v in stats.items() ]
    stats_df_columns = ['Team Name'] + list(stats[list(stats.keys())[0]].keys())
    stats_df = pd.DataFrame(data = stats_df_data, columns = stats_df_columns)

    return stats_df

# def main():
#     scrape_stats('https://www.teamrankings.com/ncaa-basketball/stat/points-per-game', 'pts_per_game')

def main():
    for (output_name, stat_url) in stat_types.items():
        # Check if file exists so we don't have to reparse the data
        if os.path.isfile(output_name + '.csv'):
            print(f"{output_name}: File exists. Skipping...")
            continue

        page_url = base_page_url + stat_url
        
        print(f"{output_name}: Parsing from `{page_url}`...")

        stat = scrape_stats(page_url, output_name)
        stat.to_csv(output_name + '.csv')
        print(f"{output_name}: Done.")
        print()

if __name__ == '__main__':
    main()
