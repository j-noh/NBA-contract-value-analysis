# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 14:25:27 2026

@author: junji
"""

import pandas as pd

seasons = ["2022-2023","2023-2024", "2024-2025", "2025-2026"]
all_seasons = []

for season in seasons:
    url = f"https://www.nbastuffer.com/{season}-nba-player-stats/"
    
    df = pd.read_html(url)[0]
    
    # Standardize column names
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace('%', 'pct')
          .str.replace('/', '_', regex=False)
          .str.replace(' ', '_')
    )
    
    # Normalize semantic differences
    df = df.rename(columns={
        "topg": "tpg"
    })
    
    # Drop junk
    df = df.drop(columns=["rank", "cur"], errors="ignore")
    
    # Add season
    df["season"] = season
    
    all_seasons.append(df)

nba_df = pd.concat(all_seasons, ignore_index=True)

#nba_df.to_csv('nba_stats_multiyear.csv', index=False)

