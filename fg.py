from bs4 import BeautifulSoup
import requests
import time
import webbrowser
import sqlite3
import csv
import plotly.graph_objs as go

base_url = 'https://www.fangraphs.com/players.aspx'

position_players = []
pitchers = []


with open('positionplayers.csv', 'a+'):
    pass
with open('pitchers.csv', 'a+'):
    pass
def context():
    print('''
Enter [1] to search for a player 
Enter [2] to view a team's most recent roster
Enter [3] to search leaderboards
    ''')
    user_input = input('''
You can also type 'Quit' or 'Exit' to exit the program.
    
''')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    if user_input == '1':
        find_player()
    elif user_input == '2': 
        find_team()
    elif user_input == '3':
        find_leaders()
    elif user_input in quit_strings:
        quit
    else:
        print('''
Oops, you entered an invalid command. Please try again.''')
        time.sleep(2)
        context()


def find_player():
    '''
    Asks user for player name

    finds player name on player listings

    updates player_url to reflect player's unique page
    '''
    player_url = ''
    back_strings = ('Back', 'back')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    open_strings = ('open', 'Open')
    graph_strings = ('compare', 'Compare')
    player_name = input("Please enter the name of a player: ")
    if player_name in back_strings:
        context()
    elif player_name in quit_strings:
        quit
    else:
        try:
            player_name_string = player_name.lower()
            player_name_split = player_name_string.split()
            search_query_init = player_name_split[1]
            search_query = search_query_init[0]
            player_name_first = player_name_split[0].capitalize()
            player_name_second = player_name_split[1].capitalize()
        except:
            print("Oops, that didnt work. Make sure you entered a valid player!")
            find_player()
        construct_url = f"https://www.baseball-reference.com/players/{search_query}/"
        response = requests.get(construct_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
        for a in player_listing:
            player_url = a['href']
        player_page_url = f"https://www.baseball-reference.com/{player_url}"
        response = requests.get(player_page_url)
        positionsearch = BeautifulSoup(response.text, 'html.parser')
        positionalarg = positionsearch.findAll('p')
        pos = positionalarg[0].text
        if 'Pitcher' in pos:
            response = requests.get(player_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                find_chart = soup.find(class_="p1")
                stats = find_chart.find_all('p')
                find_second = soup.find(class_='p2')
                stats2 = find_second.find_all('p')
            except:
                print("Oops, that didn't work. Make sure you spelled the player's name correctly!")
                find_player()
            try:
                attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[1].text}", f"{stats[3].text}", f"{stats[5].text}", f"{stats[7].text}", f"{stats2[1].text}", f"{stats2[3].text}", f"{stats2[5].text}"]
                if attempt not in pitchers:
                    pitchers.append(attempt)
            except:
                attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[0].text}", f"{stats[1].text}", f"{stats[2].text}", f"{stats[3].text}", f"{stats2[0].text}", f"{stats2[1].text}", f"{stats2[2].text}"]   
                if attempt not in pitchers:
                    pitchers.append(attempt)
            with open("pitchers.csv", "r") as target:
                reader = csv.reader(target)
                if attempt not in reader:
                    with open("pitchers.csv", mode='a+') as pitchercsv:
                        writer = csv.writer(pitchercsv, delimiter=',')
                        writer.writerow(attempt)
                else:
                    pass
            build_db_pitcher()
            openWeb = input(f'''

Successfully accessed {player_name}'s career statistics. 
They are now present within the cache csv and populated 
within the sqlite database. These files are located within 
the same directory as this program. 

To compare his statistics to a different player, type 'Compare'.

If you would like to open {player_name}'s Fangraphs page, type 'Open'.

Otherwise, you may go 'Back' or 'Quit.'
''')
            if openWeb in open_strings:
                player_name_string = player_name.lower()
                player_name_split = player_name_string.split()
                search_query_init = player_name_split[1]
                search_query = search_query_init[0:2]
                construct_url_fg = f"{base_url}?letter={search_query}"
                response = requests.get(construct_url_fg)
                soup = BeautifulSoup(response.text, 'html.parser')
                player_name_first = player_name_split[0].capitalize()
                player_name_second = player_name_split[1].capitalize()
                player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
                for a in player_listing:
                    player_url = a['href']
                player_page_url_fg = f"https://www.fangraphs.com/{player_url}"
                webbrowser.open(player_page_url_fg)
                context()
            elif openWeb in back_strings:
                find_player()
            elif openWeb in quit_strings:
                quit
            elif openWeb in graph_strings:
                graph_pitcher(player_name, attempt[2:])
            else:
                print("Oops, that didnt work. Let's try again.")
                find_player()

        else:
            try:
                response = requests.get(player_page_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                find_chart = soup.find(class_="p1")
                stats = find_chart.find_all('p')
                find_second = soup.find(class_='p2')
                stats2 = find_second.find_all('p')
            except:
                print("Oops, that didnt work. Make sure you entered a valid player!")
                find_player()
            try:
                attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[1].text}", f"{stats[3].text}", f"{stats[5].text}", f"{stats[7].text}", f"{stats2[3].text}", f"{stats2[5].text}", f"{stats[9].text}"]
                if attempt not in position_players:
                    position_players.append(attempt)
            except:
                attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[0].text}", f"{stats[1].text}", f"{stats[2].text}", f"{stats[3].text}", f"{stats2[1].text}", f"{stats2[2].text}", f"{stats[4].text}"]
                if attempt not in position_players:
                    position_players.append(attempt)
            with open("positionplayers.csv", "r") as target:
                reader = csv.reader(target)
                if attempt not in reader:
                    with open("positionplayers.csv", mode='a') as posplr:
                        writer = csv.writer(posplr, delimiter=',')
                        writer.writerow(attempt)
                else:
                    pass
            build_db_player()

            openWeb = input(f'''

Successfully accessed {player_name}'s career statistics. 
They are now present within the cache csv and populated 
within the sqlite database. These files are located within 
the same directory as this program. 

To compare his statistics to a different player, type 'Compare'.

Instead, if you would like to open {player_name}'s Fangraphs page, type 'Open.' 

Otherwise, you may go 'Back' or 'Quit.'
''')
            if openWeb in open_strings:
                player_name_string = player_name.lower()
                player_name_split = player_name_string.split()
                search_query_init = player_name_split[1]
                search_query = search_query_init[0:2]
                construct_url_fg = f"{base_url}?letter={search_query}"
                response = requests.get(construct_url_fg)
                soup = BeautifulSoup(response.text, 'html.parser')
                player_name_first = player_name_split[0].capitalize()
                player_name_second = player_name_split[1].capitalize()
                player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
                for a in player_listing:
                    player_url = a['href']
                player_page_url_fg = f"https://www.fangraphs.com/{player_url}"
                webbrowser.open(player_page_url_fg)
                context()
            elif openWeb in back_strings:
                find_player()
            elif openWeb in quit_strings:
                quit
            elif openWeb in graph_strings:
                graph_posplr(player_name, attempt[2:-1])
            else:
                print("Oops, that didnt work. Let's try again.")
                find_player()
            

def find_team():
    '''
    Asks user for team name

    finds team name on team page

    updates team_url to reflect team's unique page

    returns most recent roster

    players denominated by numbers incremented by 1 in descending order

    asks whether user would like to open associated player page in fangraphs

    if valid input entered, player is passed to find_established_player()

    '''
    back_strings = ('Back', 'back')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    team_name = input("Please enter a team: ")
    if team_name in back_strings:
        context()
    elif team_name in quit_strings:
        quit
    else:
        team_name_string = team_name.lower()
        team_name_fixed = team_name_string.replace(' ', '-')
        construct_url = f"https://www.fangraphs.com/teams/{team_name_fixed}"
        b = []
        i = 0
        try:
            response = requests.get(construct_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            find_chart = soup.find_all('td')
            for a in find_chart:
                j = a.find('a')
                if j is not None:
                    b.append(j.text)
            print("Finding all MLB Players from previous season")
            time.sleep(2)
        except:
            print("Oops, that didnt work. Make sure you entered a valid team!")
            find_team()
        for a in b[86:]:
            i += 1
            print(f"[{i}] {a}")
        next_input = input('''
You may select a player by typing their associated number.

Otherwise, you may type 'back' to go back, or 'quit' to quit.
''')
        if next_input in back_strings:
            find_team()
        elif next_input in quit_strings:
            quit
        else:
            c = int(next_input) + 85
            find_established_player(b[c])

def find_leaders():
    '''
    Asks user for year

    finds year stats

    asks user for stat

    sorts stats based on position and stat

    returns top 5 players for given stat
    '''
    
    back_strings = ('Back', 'back')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    year = input("Please enter a year to search the associated leaderboards: ")
    if year in back_strings:
        context()
    elif year in quit_strings:
        quit
    elif int(year)>2019:
        print('''

The year you entered was invalid. Make sure you are searching for a completed season.

''')
        find_leaders()
    else:
        print('''
You may choose from any of the following statistics:
------Batting Statistics------

HR (Home Runs)
RBI (Runs Batted In)
SB (Stolen Bases)
BABIP (Batting Average on Balls in Play)
AVG (Batting Average)
OBP (On-Base Percentage)
SLG (Slugging Percentage)
wOBA (Weighted On-Base Average)
wRC+ (Weighted Runs Created Plus (Park-Adjusted))
bWAR  (Wins Above Replacement for Batters)

------Pitching Statistics------

W (Pitching Wins)
L (Pitching Losses)
SV (Saves)
IP (Innings Pitched)
K (Strikeouts)
BB (Walks)
ERA (Earned Run Average)
FIP (Fielding-Independent Pitching)
xFIP (Park-Adjusted Fielding-Independent Pitching)
pWAR (Wins Above Replacement for Pitchers)

''')
        all_stats = ('W', 'L', 'SV', 'IP', 'K', 'BB', 'ERA', 'FIP', 'xFIP', 'bWAR', 'pWAR', 'HR', 'RBI', 'SB', 'BABIP', 'AVG', 'OBP', 'SLG', 'wOBA', 'wRC+')
        pitching_stats = ('W', 'L', 'SV', 'IP', 'K', 'BB', 'ERA', 'FIP', 'xFIP', 'pWAR')
        batting_stats = ('HR', 'RBI', 'SB', 'BABIP', 'AVG', 'OBP', 'SLG', 'wOBA', 'wRC+', 'bWAR')
        stat = input("Please enter the statistic for which you would like to see the leaderboard: ")
        if stat not in back_strings:
            if stat not in quit_strings:
                if stat not in all_stats:
                    print("Please enter a valid statistic.")
                    find_leaders()
                else:
                    if stat in pitching_stats:
                        position = 'p'
                    elif stat in batting_stats:
                        position = 'b'
                    else:
                        find_leaders()
                    get_board(stat, year, position)
                    time.sleep(3)
                    context()
            else:
                exit
        else:
            context()

def get_board(stat, year, position):
    '''
    parameters: stat (string), year (string), position ('p' or 'b')

    given position and year, searches appropriate leaderboards for stat leaders

    returns player name, team, and stat value
    '''
    if position == 'p':
        if stat == 'W':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=3,d'
            most_stats(base_url)
        elif stat == 'L':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=4,d'
            most_stats(base_url)
        elif stat == 'SV':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=5,d'
            most_stats(base_url)
        elif stat == 'IP':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=8,d'
            most_stats(base_url)
        elif stat == 'K':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate=-12-31&sort=9,d'
            break_stats(base_url)
        elif stat == 'BB':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=10,a'
            most_stats(base_url)
        elif stat == 'ERA':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=16,a'
            break_stats(base_url)
        elif stat == 'FIP':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=17,a'
            most_stats(base_url)
        elif stat == 'xFIP':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=18,a'
            most_stats(base_url)
        elif stat == 'pWAR':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=19,d'
            break_stats(base_url)
    elif position == 'b':
        if stat == 'HR':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=5,d'
            most_stats(base_url)
        elif stat == 'RBI':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=7,d'
            most_stats(base_url)
        elif stat == 'SB':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=8,d'
            most_stats(base_url)
        elif stat == 'BABIP':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=12,d'
            most_stats(base_url)
        elif stat == 'AVG':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=13,d'
            break_stats(base_url)
        elif stat == 'OBP':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=14,d'
            most_stats(base_url)
        elif stat == 'SLG':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=15,d'
            most_stats(base_url)
        elif stat == 'wOBA':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=16,d'
            most_stats(base_url)
        elif stat == 'wRC+':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=17,d'
            most_stats(base_url)
        elif stat == 'bWAR':
            base_url = f'https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=y&type=8&season={year}&month=0&season1={year}&ind=0&team=0&rost=0&age=0&filter=&players=0&startdate={year}-01-01&enddate={year}-12-31&sort=21,d'
            most_stats(base_url)
    else:
        print("Error encountered")

def most_stats(base_url):
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_rank_parent = soup.find(class_="rgMasterTable")
        player_rank = player_rank_parent.find('tbody')
        for a in player_rank:
            player_data = player_rank.find_all('a', text=True)
        for b in player_rank:
            player_stat = player_rank.find_all(class_="grid_line_regular rgSorted")
        print(f'''
[1] {player_data[0].text}, {player_data[1].text}, {player_stat[0].text}
[2] {player_data[2].text}, {player_data[3].text}, {player_stat[1].text}
[3] {player_data[4].text}, {player_data[5].text}, {player_stat[2].text}
[4] {player_data[6].text}, {player_data[7].text}, {player_stat[3].text}
[5] {player_data[8].text}, {player_data[9].text}, {player_stat[4].text}
            ''')

def break_stats(base_url):
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_rank_parent = soup.find(class_="rgMasterTable")
        player_rank = player_rank_parent.find('tbody')
        for a in player_rank:
            player_data = player_rank.find_all('a', text=True)
        for b in player_rank:
            player_stat = player_rank.find_all(class_="grid_line_break rgSorted")
        print(f'''
[1] {player_data[0].text}, {player_data[1].text}, {player_stat[0].text}
[2] {player_data[2].text}, {player_data[3].text}, {player_stat[1].text}
[3] {player_data[4].text}, {player_data[5].text}, {player_stat[2].text}
[4] {player_data[6].text}, {player_data[7].text}, {player_stat[3].text}
[5] {player_data[8].text}, {player_data[9].text}, {player_stat[4].text}
            ''')

def find_established_player(player_input):
    '''
    takes player from find_team()
    
    treats input similar to find_player()

    asks user whether they'd like to compare the player to another player

    if yes, additional player is recieved, and both are passed to the appropriate graph constructor
    '''

    player_url = ''
    back_strings = ('Back', 'back')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    open_strings = ('open', 'Open')
    graph_strings = ('compare', 'Compare')
    player_name_string = player_input.lower()
    player_name_split = player_name_string.split()
    search_query_init = player_name_split[1]
    search_query = search_query_init[0]
    construct_url = f"https://www.baseball-reference.com/players/{search_query}/"
    response = requests.get(construct_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    player_name_first = player_name_split[0].capitalize()
    player_name_second = player_name_split[1].capitalize()
    player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
    for a in player_listing:
        player_url = a['href']
    player_page_url = f"https://www.baseball-reference.com/{player_url}"
    response = requests.get(player_page_url)
    positionsearch = BeautifulSoup(response.text, 'html.parser')
    positionalarg = positionsearch.findAll('p')
    pos = positionalarg[0].text
    if 'Pitcher' in pos:
        response = requests.get(player_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        find_chart = soup.find(class_="p1")
        stats = find_chart.find_all('p')
        find_second = soup.find(class_='p2')
        stats2 = find_second.find_all('p')
        try:
            attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[1].text}", f"{stats[3].text}", f"{stats[5].text}", f"{stats[7].text}", f"{stats2[1].text}", f"{stats2[3].text}", f"{stats2[5].text}"]
            if attempt not in pitchers:
                pitchers.append(attempt)
        except:
            attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[0].text}", f"{stats[1].text}", f"{stats[2].text}", f"{stats[3].text}", f"{stats2[0].text}", f"{stats2[1].text}", f"{stats2[2].text}"]   
            if attempt not in pitchers:
                pitchers.append(attempt)
        with open("pitchers.csv", "r") as target:
            reader = csv.reader(target)
            if attempt not in reader:
                with open("pitchers.csv", mode='a+') as pitchercsv:
                    writer = csv.writer(pitchercsv, delimiter=',')
                    writer.writerow(attempt)
            else:
                pass
        build_db_pitcher()
        openWeb = input(f'''

Successfully accessed {player_input}'s career statistics. 
They are now present within the cache csv and populated 
within the sqlite database. These files are located within 
the same directory as this program. 

To compare his statistics to a different player, type 'Compare'.

If you would like to open {player_input}'s Fangraphs page, type 'Open'.

Otherwise, you may go 'Back' or 'Quit.'
''')
        if openWeb in open_strings:
            player_name_string = player_input.lower()
            player_name_split = player_name_string.split()
            search_query_init = player_name_split[1]
            search_query = search_query_init[0:2]
            construct_url_fg = f"{base_url}?letter={search_query}"
            response = requests.get(construct_url_fg)
            soup = BeautifulSoup(response.text, 'html.parser')
            player_name_first = player_name_split[0].capitalize()
            player_name_second = player_name_split[1].capitalize()
            player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
            for a in player_listing:
                player_url = a['href']
            player_page_url_fg = f"https://www.fangraphs.com/{player_url}"
            webbrowser.open(player_page_url_fg)
        elif openWeb in back_strings:
            find_player()
        elif openWeb in quit_strings:
            quit
        elif openWeb in graph_strings:
            graph_pitcher(player_input, attempt[2:])

    else:
        response = requests.get(player_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        find_chart = soup.find(class_="p1")
        stats = find_chart.find_all('p')
        find_second = soup.find(class_='p2')
        stats2 = find_second.find_all('p')
        try:
            attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[1].text}", f"{stats[3].text}", f"{stats[5].text}", f"{stats[7].text}", f"{stats2[3].text}", f"{stats2[5].text}", f"{stats[9].text}"]
            if attempt not in position_players:
                position_players.append(attempt)
        except:
            attempt = [f"{player_name_second}", f"{player_name_first}", f"{stats[0].text}", f"{stats[1].text}", f"{stats[2].text}", f"{stats[3].text}", f"{stats2[1].text}", f"{stats2[2].text}", f"{stats[4].text}"]
            if attempt not in position_players:
                position_players.append(attempt)
        with open("positionplayers.csv", "r") as target:
            reader = csv.reader(target)
            if attempt not in reader:
                with open("positionplayers.csv", mode='a') as posplr:
                    writer = csv.writer(posplr, delimiter=',')
                    writer.writerow(attempt)
            else:
                pass
        build_db_player()

        openWeb = input(f'''

Successfully accessed {player_input}'s career statistics. 
They are now present within the cache csv and populated 
within the sqlite database. These files are located within 
the same directory as this program. 

To compare his statistics to a different player, type 'Compare'.

Instead, if you would like to open {player_input}'s Fangraphs page, type 'Open.' 

Otherwise, you may go 'Back' or 'Quit.'
''')
        if openWeb in open_strings:
            player_name_string = player_input.lower()
            player_name_split = player_name_string.split()
            search_query_init = player_name_split[1]
            search_query = search_query_init[0:2]
            construct_url_fg = f"{base_url}?letter={search_query}"
            response = requests.get(construct_url_fg)
            soup = BeautifulSoup(response.text, 'html.parser')
            player_name_first = player_name_split[0].capitalize()
            player_name_second = player_name_split[1].capitalize()
            player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
            for a in player_listing:
                player_url = a['href']
            player_page_url_fg = f"https://www.fangraphs.com/{player_url}"
            webbrowser.open(player_page_url_fg)
        elif openWeb in back_strings:
            find_player()
        elif openWeb in quit_strings:
            quit
        elif openWeb in graph_strings:
            graph_posplr(player_input, attempt[2:-1])

def build_db_pitcher():
    pitchers_cached = []
    conn = sqlite3.connect("MLB.sqlite")
    cur = conn.cursor()
    drop_players = '''
        DROP TABLE IF EXISTS "Pitchers";
    '''
    create_players = '''
        CREATE TABLE IF NOT EXISTS "Pitchers" (
            "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "LastName"  TEXT NOT NULL,
            "FirstName" TEXT NOT NULL,
            "WAR" TEXT NOT NULL,
            "Wins"  TEXT,
            "Losses" TEXT,
            "ERA" TEXT,
            "Games Pitched" TEXT,
            "Games Started" TEXT,
            "Saves" TEXT
        );
    '''
    cur.execute(drop_players)
    cur.execute(create_players)
    conn.commit()
    insert_players = '''
        INSERT INTO Pitchers
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    with open('pitchers.csv', 'r') as temp:
        reader = csv.reader(temp)
        for line in reader:
            pitchers_cached.append(line)
            cur.execute(insert_players, line)
    conn.commit()


def build_db_player():
    position_players_cached = []
    conn = sqlite3.connect("MLB.sqlite")
    cur = conn.cursor()
    drop_players = '''
        DROP TABLE IF EXISTS "PositionPlayers";
    '''
    create_players = '''
        CREATE TABLE IF NOT EXISTS "PositionPlayers" (
            "Id"        INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            "LastName"  TEXT,
            "FirstName" TEXT,
            "WAR" TEXT NOT NULL,
            "At Bats"  TEXT,
            "Hits" TEXT,
            "Home Runs" TEXT,
            "RBI" TEXT,
            "Stolen Bases" TEXT,
            "Batting Average" TEXT
        );
    '''
    cur.execute(drop_players)
    cur.execute(create_players)
    conn.commit()
    insert_players = f'''
        INSERT INTO PositionPlayers
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    with open('positionplayers.csv', 'r') as temp:
        reader = csv.reader(temp)
        for line in reader:
            position_players_cached.append(line)
            cur.execute(insert_players, line)

    conn.commit()

def graph_posplr(player_name1, player_data):
    player_url = ''
    back_strings = ('Back', 'back')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    second = input(f"Please enter a player to compare to {player_name1}:  ")
    if second in back_strings:
        context()
    elif second in quit_strings:
        quit
    else:
        player_name_string = second.lower()
        player_name_split = player_name_string.split()
        search_query_init = player_name_split[1]
        search_query = search_query_init[0]
        construct_url = f"https://www.baseball-reference.com/players/{search_query}/"
        response = requests.get(construct_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_name_first = player_name_split[0].capitalize()
        player_name_second = player_name_split[1].capitalize()
        player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
        for a in player_listing:
            player_url = a['href']
        player_page_url = f"https://www.baseball-reference.com/{player_url}"
        response = requests.get(player_page_url)
        positionsearch = BeautifulSoup(response.text, 'html.parser')
        positionalarg = positionsearch.findAll('p')
        pos = positionalarg[0].text
        if 'Pitcher' in pos:
            print('''
Sorry! That didnt work. Make sure youre not trying to compare a pitcher to a position player!

''')
            context()
        else:
            response = requests.get(player_page_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            find_chart = soup.find(class_="p1")
            stats = find_chart.find_all('p')
            find_second = soup.find(class_='p2')
            stats2 = find_second.find_all('p')
            try:
                attempt2 = [f"{player_name_second}", f"{player_name_first}", f"{stats[1].text}", f"{stats[3].text}", f"{stats[5].text}", f"{stats[7].text}", f"{stats2[3].text}", f"{stats2[5].text}", f"{stats[9].text}"]
                if attempt2 not in position_players:
                    position_players.append(attempt2)
            except:
                attempt2 = [f"{player_name_second}", f"{player_name_first}", f"{stats[0].text}", f"{stats[1].text}", f"{stats[2].text}", f"{stats[3].text}", f"{stats2[1].text}", f"{stats2[2].text}", f"{stats[4].text}"]
                if attempt2 not in position_players:
                    position_players.append(attempt2)
            with open("positionplayers.csv", "r") as target:
                reader = csv.reader(target)
                if attempt2 not in reader:
                    with open("positionplayers.csv", mode='a') as posplr:
                        writer = csv.writer(posplr, delimiter=',')
                        writer.writerow(attempt2)
                else:
                    pass
            build_db_player()
            stats = ['Wins Above Replacement', 'At Bats', 'Hits', 'Home Runs', 'RBI', 'Stolen Bases']
            fig = go.Figure(data=[
                go.Bar(name=f'{second}', x=stats, y=attempt2[2:-1]),
                go.Bar(name=f'{player_name1}', x=stats, y=player_data)
            ])
            # Change the bar mode
            fig.update_layout(barmode='group')
            fig.show()
            context()

def graph_pitcher(player_name1, player_data):
    del player_data[3]
    player_url = ''
    back_strings = ('Back', 'back')
    quit_strings = ('quit', 'Quit', 'exit', 'Exit')
    second = input(f"Please enter a player to compare to {player_name1}:  ")
    if second in back_strings:
        context()
    elif second in quit_strings:
        quit
    else:
        player_name_string = second.lower()
        player_name_split = player_name_string.split()
        search_query_init = player_name_split[1]
        search_query = search_query_init[0]
        construct_url = f"https://www.baseball-reference.com/players/{search_query}/"
        response = requests.get(construct_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        player_name_first = player_name_split[0].capitalize()
        player_name_second = player_name_split[1].capitalize()
        player_listing = soup.find_all('a', text=f'{player_name_first} {player_name_second}')
        for a in player_listing:
            player_url = a['href']
        player_page_url = f"https://www.baseball-reference.com/{player_url}"
        response = requests.get(player_page_url)
        positionsearch = BeautifulSoup(response.text, 'html.parser')
        positionalarg = positionsearch.findAll('p')
        pos = positionalarg[0].text
        try:
            if 'Pitcher' in pos:
                response = requests.get(player_page_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                find_chart = soup.find(class_="p1")
                stats = find_chart.find_all('p')
                find_second = soup.find(class_='p2')
                stats2 = find_second.find_all('p')
                try:
                    attempt2 = [f"{player_name_second}", f"{player_name_first}", f"{stats[1].text}", f"{stats[3].text}", f"{stats[5].text}", f"{stats[7].text}", f"{stats2[1].text}", f"{stats2[3].text}", f"{stats2[5].text}"]
                    if attempt2 not in pitchers:
                        pitchers.append(attempt2)
                except:
                    attempt2 = [f"{player_name_second}", f"{player_name_first}", f"{stats[0].text}", f"{stats[1].text}", f"{stats[2].text}", f"{stats[3].text}", f"{stats2[0].text}", f"{stats2[1].text}", f"{stats2[2].text}"]   
                    if attempt2 not in pitchers:
                        pitchers.append(attempt2)
                with open("pitchers.csv", "r") as target:
                    reader = csv.reader(target)
                    if attempt2 not in reader:
                        with open("pitchers.csv", mode='a+') as pitchercsv:
                            writer = csv.writer(pitchercsv, delimiter=',')
                            writer.writerow(attempt2)
                    else:
                        pass
                build_db_pitcher()
                stats = ['Wins Above Replacement', 'Wins', 'Losses', 'Games Pitched', 'Games Started', 'Saves']
                at2 = attempt2[2:]
                del at2[3]
                fig = go.Figure(data=[
                    go.Bar(name=f'{second}', x=stats, y=at2),
                    go.Bar(name=f'{player_name1}', x=stats, y=player_data)
                ])
                fig.update_layout(barmode='group')
                fig.show()
                context()
            else:
                print('''
Sorry! That didnt work. Make sure youre not trying to compare a pitcher to a position player!

''')
                context()
        except:
            print('''
Sorry! That didnt work. Make sure youre not trying to compare a pitcher to a position player!

''')
            context()

context()
