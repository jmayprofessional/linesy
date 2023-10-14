import requests
from prettytable import PrettyTable

# Function to get NHL teams from the API
def get_nhl_teams():
    response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    if response.status_code == 200:
        teams_data = response.json()["teams"]
        return teams_data
    else:
        return None

# Function to get team roster based on team ID
def get_team_roster(team_id):
    url = f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}/roster"
    response = requests.get(url)
    if response.status_code == 200:
        roster_data = response.json()["roster"]
        return roster_data
    else:
        return None

# Function to get player's individual stats based on player ID and season
def get_player_stats(player_id):
    url = f"https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season=20222023"
    response = requests.get(url)
    if response.status_code == 200:
        player_stats = response.json()
        return player_stats
    else:
        return None

# List to store selected players' data
selected_players = []

# Maximum allowed players
MAX_PLAYERS = 5

# Create a PrettyTable object to display selected players
table = PrettyTable()
table.field_names = ["Player", "Position", "Goals", "Assists", "Points", "Games Played"]

while True:
    # Display options and selected players to the user
    print("Choose an option:")
    print("1. View NHL Teams")
    print("2. Option Two")
    print("3. View Selected Players")
    print("4. Exit")
    
    # Get user input
    user_choice = input("Enter the number of your choice: ")

    if user_choice == "1":
        # Get NHL teams from the API
        teams = get_nhl_teams()

        if teams:
            print("NHL Teams:")
            for index, team in enumerate(teams, start=1):
                print(f"{index}. {team['name']} ({team['abbreviation']})")
            
            # Prompt user to select a team by number
            while True:
                try:
                    team_number = int(input("Enter the number of the NHL team: "))
                    if 1 <= team_number <= len(teams):
                        selected_team = teams[team_number - 1]
                        print(f"You selected: {selected_team['name']} ({selected_team['abbreviation']})")
                        break
                    else:
                        print("Invalid team number. Please enter a valid number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                
                # Get and display team roster
            team_roster = get_team_roster(selected_team['id'])
            if team_roster:
                print("Team Roster:")
                for index, player in enumerate(team_roster, start=1):
                    print(f"{index}. {player['person']['fullName']} ({player['position']['abbreviation']})")
                    
                # Prompt user to select a player from the roster
                while True:
                    try:
                        player_number = int(input("Enter the number of the player: "))
                        if 1 <= player_number <= len(team_roster):
                            selected_player = team_roster[player_number - 1]
                            player_id = selected_player['person']['id']
                            break
                        else:
                            print("Invalid player number. Please enter a valid number.")
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                        
                    # Get and display player's individual stats
                player_stats = get_player_stats(player_id)
                if player_stats:
                    print(f"Player: {selected_player['person']['fullName']} ({selected_player['position']['abbreviation']})")
                    
                    # Add player data to the PrettyTable
                    stats = player_stats['stats'][0]['splits'][0]['stat']
                    table.add_row([selected_player['person']['fullName'], selected_player['position']['abbreviation'],
                                   stats.get('goals', 0), stats.get('assists', 0), stats.get('points', 0), stats.get('games', 0)])
                    
                    # Check if the player is already in the selected players list
                    player_found = False
                    for player_data in selected_players:
                        if player_data['name'] == selected_player['person']['fullName']:
                            player_found = True
                            # Update the player's data
                            player_data['position'] = selected_player['position']['abbreviation']
                            player_data['goals'] = stats.get('goals', 0)
                            player_data['assists'] = stats.get('assists', 0)
                            player_data['points'] = stats.get('points', 0)
                            player_data['games'] = stats.get('games', 0)
                            break
                    
                    # If the player is not found and total players are less than MAX_PLAYERS, add them to the selected players list
                    if not player_found and len(selected_players) < MAX_PLAYERS:
                        player_data = {
                            'name': selected_player['person']['fullName'],
                            'position': selected_player['position']['abbreviation'],
                            'goals': stats.get('goals', 0),
                            'assists': stats.get('assists', 0),
                            'points': stats.get('points', 0),
                            'games': stats.get('games', 0)
                        }
                        selected_players.append(player_data)
                        print("Player added to the line!")
                    elif len(selected_players) >= MAX_PLAYERS:
                        print("You have reached the maximum limit of players (5). Cannot add more players.")
                    else:
                        print("Player already in the list.")
                else:
                    print("Failed to retrieve player stats.")
            else:
                print("Failed to retrieve team roster.")
        else:
            print("Failed to retrieve NHL teams data.")
    elif user_choice == "2":
        print("You chose Option Two")
        # Perform actions for Option Two
    elif user_choice == "3":
        # Display selected players and their stats using PrettyTable
        print("Selected Players:")
        print(table)
    elif user_choice == "4":
        print("Exiting. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
