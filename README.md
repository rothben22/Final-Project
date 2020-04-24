# Final-Project

To use this program, ensure you have installed:
    sqlite3
    BeautifulSoup
    plotly

imported directories within this program:
    BeautifulSoup
    requests
    time
    webbrowser
    sqlite3
    csv
    plotly

To initialize this program:
    from terminal, python/python3 fg.py

What does this program do?
    1) Allows user to search Fangraphs for a given player
        a) scrapes Fangraphs and Baseball Reference for player statistics
        b) caches player data within associated csv
        c) writes player data to associated sqlite database
        d) allows user to open associated Fangraphs player page
        e) Allows user to compare said player to another player (limitation: pitcher compared to pitcher, offensive player to offensive player. No cross comparisons, for obvious reasons)
            I) opens comparative graph of appropriate statistics within web browser
    2) Allows user to search any MLB team for its most recent roster
        a) PRINTS roster within terminal window
        b) allows user to select given player
        c) scrapes Fangraphs and Baseball Reference for player statistics
        d) caches player data within associated csv
        e) allows user to open associated Fangraphs player page
        f) Allows user to compare said player to another player (limitation: pitcher compared to pitcher, offensive player to offensive player. No cross comparisons, for obvious reasons)
            I) opens comparative graph of appropriate statistics within web browser
    3) Allows user to view stat-specific leaderboards for any completed MLB season
        a) asks user for a year
        b) asks user for comparative statistic
        c) uses input to find associated Fangraphs page
        d) scrapes Fangraphs for specific statistic
        e) PRINTS top 5 players from associated statistic's leaderboard
            I) handles each statistic differently, depending on associated position, league averages, and statistical meaning.
    