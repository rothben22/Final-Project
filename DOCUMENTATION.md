# Final Project Documentation

## Data Sources
    1. Data scraped from www.fangraphs.com and www.baseball-reference.com
        - URLs constructed within program, depending on player name, team name, associated year, and/or associated statistic being searched. Unique to all situations, and constructed accordingly.
    2. Formatting:
        - scraped data: HTML
        - cached data: CSV (two separate documents, 'pitchers.csv' and 'position_players.csv', depending on positionality, in order to keep associated statistics together.)
        - DB data: sqlite
            - this data mirrors that within the csvs, and is similarly broken up into separate tables for pitchers and position players to maintain statistical relevance
        - summary of data:
            -pitchers:
                - accesses player's career statistics (from Baseball Reference)
                - grabs WAR, W, L, ERA, GP, GS, and Saves
                - caches data in 'pitchers.csv' and in Pitchers table within MLB database
                - number of records available: thousands (every pitcher ever)
                - number of records retrieved: up to user, one per search
            -position players
                - accesses player's career statistics (from Baseball Reference)
                - grabs WAR, AB, H, HR, RBI, and SB
                - caches data in 'position_players.csv' and in PositionPlayers table within 
                MLB database
                - number of records available: thousands (every position player ever)
                - number of records retrieved: up to user, one per search
            -teams
                - grabs entire roster from previous season (from Fangraphs)
                - number of records available: 30 teams, plus entire roster (over 40 per team)
                - number of records retrieved: up to user, one team per search
            -leaderboards
                - grabs top 5 players per chosen stat from any season with available statistics
                    - seasons include 1871 through 2019
                - stats available (from Fangraphs):
                    -WAR
                    -HR
                    -RBI
                    -SB
                    -BABIP
                    -AVG
                    -OBP
                    -SLG
                    -wOBA
                    -wRC+
                    -W
                    -L
                    -SV
                    -IP
                    -K
                    -BB
                    -ERA
                    -FIP
                    -xFIP
                - number of records retrieved: up to user, one season, stat per search
    3. Database Specifics
        -pitchers
            - Generates unique ID for each given pitcher
            - populates table with WAR, W, L, ERA, GP, GS, and Saves
        -position players
            - Generates unique ID for each given position player
            - Populates table with WAR, AB, H, HR, RBI, and SB