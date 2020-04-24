# Final-Project

## To use this program, ensure you have installed:
    sqlite3
    BeautifulSoup
    plotly

## imported directories within this program:
    BeautifulSoup
    requests
    time
    webbrowser
    sqlite3
    csv
    plotly

## To initialize this program:
    from terminal, python/python3 fg.py

## What does this program do?
### 1) Allows user to search Fangraphs for a given player
        - scrapes Fangraphs and Baseball Reference for player statistics
        - caches player data within associated csv
        - writes player data to associated sqlite database
        - allows user to open associated Fangraphs player page
        - Allows user to compare said player to another player (limitation: pitcher compared to pitcher, offensive player to offensive player. No cross comparisons, for obvious reasons)
            1. opens comparative graph of appropriate statistics within web browser
### 2) Allows user to search any MLB team for its most recent roster
        - PRINTS roster within terminal window
        - allows user to select given player
        - scrapes Fangraphs and Baseball Reference for player statistics
        - caches player data within associated csv
        - allows user to open associated Fangraphs player page
        - Allows user to compare said player to another player (limitation: pitcher compared to pitcher, offensive player to offensive player. No cross comparisons, for obvious reasons)
            1. opens comparative graph of appropriate statistics within web browser
### 3) Allows user to view stat-specific leaderboards for any completed MLB season
        - asks user for a year
        - asks user for comparative statistic
        - uses input to find associated Fangraphs page
        - scrapes Fangraphs for specific statistic
        - PRINTS top 5 players from associated statistic's leaderboard
            1. handles each statistic differently, depending on associated position, league averages, and statistical meaning.
    