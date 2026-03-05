# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 16:47:49 2026

@author: junji
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_nba_salaries(years):
    all_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Mapping dictionary for Full Names to Title-Cased Abbreviations
    team_map = {
        'Atlanta Hawks': 'Atl', 'Boston Celtics': 'Bos', 'Brooklyn Nets': 'Bkn',
        'Charlotte Hornets': 'Cha', 'Chicago Bulls': 'Chi', 'Cleveland Cavaliers': 'Cle',
        'Dallas Mavericks': 'Dal', 'Denver Nuggets': 'Den', 'Detroit Pistons': 'Det',
        'Golden State Warriors': 'Gsw', 'Houston Rockets': 'Hou', 'Indiana Pacers': 'Ind',
        'LA Clippers': 'Lac', 'Los Angeles Clippers': 'Lac', 'Los Angeles Lakers': 'Lal',
        'Memphis Grizzlies': 'Mem', 'Miami Heat': 'Mia', 'Milwaukee Bucks': 'Mil',
        'Minnesota Timberwolves': 'Min', 'New Orleans Pelicans': 'Nop', 'New York Knicks': 'Nyk',
        'Oklahoma City Thunder': 'Okc', 'Orlando Magic': 'Orl', 'Philadelphia 76ers': 'Phi',
        'Phoenix Suns': 'Phx', 'Portland Trail Blazers': 'Por', 'Sacramento Kings': 'Sac',
        'San Antonio Spurs': 'Sas', 'Toronto Raptors': 'Tor', 'Utah Jazz': 'Uta',
        'Washington Wizards': 'Was'
    }

    for year in years:
        print(f"\n--- Scraping Season {year-1}-{year} ---")
        page_num = 1
        
        while True:
            # 1. HANDLE URL LOGIC
            # If current year (2026), use the base salary path
            if year == 2026:
                if page_num == 1:
                    url = "https://www.espn.com/nba/salaries"
                else:
                    url = f"https://www.espn.com/nba/salaries/_/page/{page_num}"
            else:
                # If historical, use the /year/YYYY path
                if page_num == 1:
                    url = f"https://www.espn.com/nba/salaries/_/year/{year}"
                else:
                    url = f"https://www.espn.com/nba/salaries/_/year/{year}/page/{page_num}"
            
            print(f"Fetching: {url}")
            try:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    print(f"Status {response.status_code}. Moving to next season.")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table', class_='tablehead')
                
                if not table:
                    break
                    
                rows = table.find_all('tr')
                added_this_page = 0
                
                for row in rows:
                    cols = row.find_all('td')
                    # ESPN tables have 4 columns (Rank, Name, Team, Salary)
                    if len(cols) == 4 and cols[0].text.strip() != 'RK':
                        rk = cols[0].text.strip()
                        name_pos = cols[1].text.strip()
                        team_full = cols[2].text.strip()
                        salary_str = cols[3].text.strip()
                        
                        # 2. CLEAN NAME: Remove position (split at comma)
                        name_only = name_pos.split(',')[0]
                        
                        # 3. CONVERT TEAM: Map to Title-Cased Abbreviation
                        team_abbr = team_map.get(team_full, team_full)
                        
                        # 4. CLEAN SALARY: Remove $ and , then convert to float
                        salary_val = float(salary_str.replace('$', '').replace(',', ''))
                        
                        all_data.append([rk, name_only, team_abbr, salary_val, f"{year-1}-{year}"])
                        added_this_page += 1
                
                if added_this_page == 0:
                    break
                    
                page_num += 1
                time.sleep(0.5) # Prevent rate limiting

            except Exception as e:
                print(f"Error encountered: {e}")
                break

    # Create DataFrame and Export
    df = pd.DataFrame(all_data, columns=['Rank', 'Name', 'Team', 'Salary', 'Season'])
    return df

# Target years from 2022-23 (2023) to 2025-26 (2026)
target_years = [2023, 2024, 2025, 2026]
df_final = scrape_nba_salaries(target_years)

df_final.to_csv('nba_salaries_formatted.csv', index=False)
print(f"\nSaved {len(df_final)} records to nba_salaries_formatted.csv")

