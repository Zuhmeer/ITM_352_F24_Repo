import nfl_data_py as nfl
import pandas as pd
import sys
import ssl

ssl._create_default_https_context = ssl._create_unverified_context 

# Load and preprocess to NFL data
def load_nfl_data():
    try:
        # Specify the year of schedule data
        years = [2024]
        teams = nfl.import_team_desc()
        schedules = nfl.import_schedules(years=years)

        # Filter data for regular season games only
        schedules = schedules[schedules['game_type'] == 'REG']

        # Ensure 'home_score' and 'away_score' columns exist for the 'result' column
        if 'home_score' in schedules.columns and 'away_score' in schedules.columns:
            schedules['result'] = schedules.apply(
                lambda row: 'W' if row['home_score'] > row['away_score'] else 'L',
                axis=1
            )
        else:
            print("Error: Scores are missing from the schedules data.")
            sys.exit(1)

        # Process wins, losses, and ties for home and away teams
        schedules['home_win'] = schedules['home_score'] > schedules['away_score']
        schedules['away_win'] = schedules['away_score'] > schedules['home_score']
        schedules['tie'] = schedules['home_score'] == schedules['away_score']

        home_results = schedules.groupby('home_team').agg(
            home_wins=('home_win', 'sum'),
            home_losses=('away_win', 'sum'),
            ties=('tie', 'sum')
        ).reset_index()

        away_results = schedules.groupby('away_team').agg(
            away_wins=('away_win', 'sum'),
            away_losses=('home_win', 'sum'),
            ties=('tie', 'sum')
        ).reset_index()

        # Combine home and away game results
        standings = pd.merge(home_results, away_results, 
                              left_on='home_team', 
                              right_on='away_team', 
                              how='outer').fillna(0)

        standings['team'] = standings['home_team'].combine_first(standings['away_team'])
        standings['total_wins'] = standings['home_wins'] + standings['away_wins']
        standings['total_losses'] = standings['home_losses'] + standings['away_losses']
        standings['total_ties'] = standings['ties_x'] + standings['ties_y']

        # Correspond teams to their divisions
        divisions = {
    "AFC East": ["Buffalo Bills", "Miami Dolphins", "New York Jets", "New England Patriots"],
    "AFC North": ["Pittsburgh Steelers", "Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns"],
    "AFC South": ["Houston Texans", "Indianapolis Colts", "Tennessee Titans", "Jacksonville Jaguars"],
    "AFC West": ["Kansas City Chiefs", "Los Angeles Chargers", "Denver Broncos", "Las Vegas Raiders"],
    "NFC East": ["Philadelphia Eagles", "Washington Commanders", "Dallas Cowboys", "New York Giants"],
    "NFC North": ["Detroit Lions", "Minnesota Vikings", "Green Bay Packers", "Chicago Bears"],
    "NFC South": ["Atlanta Falcons", "Tampa Bay Buccaneers", "New Orleans Saints", "Carolina Panthers"],
    "NFC West": ["Seattle Seahawks", "Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers"],
}
        
# In case the teams dont correspond with their division
        standings['division'] = standings['team'].apply(
    lambda team: next((div for div, teams in divisions.items() if team in teams), "Division")
)

        # Select and sort through the columns
        standings = standings[['team', 'division', 'total_wins', 'total_losses', 'total_ties']].sort_values(
            by=['division', 'total_wins'], ascending=[True, False]
        )

        print("NFL data loaded successfully!")
        return {
            "teams": teams,
            "standings": standings,
            "games": schedules
        }
    except Exception as e:
        print(f"Error loading NFL data: {e}")
        sys.exit(1)

# Display standings grouped by division
def display_division_standings(standings):
    # Get unique division names from standings
    divisions = standings['division'].unique()

    # Loop through each division and display team standings
    for division in divisions:
        print(f"\n{division.upper()}")
        print(f"{'Team':<25}{'Wins':<10}{'Losses':<10}{'Ties':<10}")
        print("-" * 50)

        # Filter teams in the current division
        div_teams = standings[standings['division'] == division]

        # Display each team's record
        for _, row in div_teams.iterrows():
            print(f"{row['team']:<25}{row['total_wins']:<10}{row['total_losses']:<10}{row['total_ties']:<10}")

# Predict game outcomes
def predict_game(data):
    print("\nGame Predictions:")

    # Fetch upcoming games
    upcoming_games = data["games"][data["games"]["result"].isna()]
    
    if upcoming_games.empty:
        print("No upcoming games found for prediction.")
        return

    # Get standings for win probabilities
    standings = data["standings"]

    print(f"{'Home Team':<20}{'Away Team':<20}{'Predicted Winner':<20}{'Win Probability':<20}")
    print("-" * 80)

    for _, game in upcoming_games.iterrows():
        home_team = game['home_team']
        away_team = game['away_team']

        # Team statistics from standings
        home_stats = standings[standings['team'] == home_team].iloc[0]
        away_stats = standings[standings['team'] == away_team].iloc[0]

        # Calculate win probabilities (basic example: ratio of wins to total games)
        home_total_games = home_stats['total_wins'] + home_stats['total_losses'] + home_stats['total_ties']
        away_total_games = away_stats['total_wins'] + away_stats['total_losses'] + away_stats['total_ties']

        home_win_rate = home_stats['total_wins'] / home_total_games if home_total_games > 0 else 0
        away_win_rate = away_stats['total_wins'] / away_total_games if away_total_games > 0 else 0

        # Assign probabilities to teams 
        home_probability = home_win_rate / (home_win_rate + away_win_rate) if (home_win_rate + away_win_rate) > 0 else 0.5
        away_probability = 1 - home_probability

        # Predict the winner
        predicted_winner = home_team if home_probability > away_probability else away_team
        win_probability = max(home_probability, away_probability)

        # Display the prediction
        print(f"{home_team:<20}{away_team:<20}{predicted_winner:<20}{win_probability:.2%}")

 #View past games
def view_past_games(data):
    past_games = data['games'][data['games']['result'].notna()]
    if past_games.empty:
        print("No past games available.")
    else:
        print(past_games[['home_team', 'away_team', 'home_score', 'away_score', 'result']].head(10))

# Main menu
def display_menu(data):
    while True:
        print("\nNFL Standings Menu:")
        print("1. View Team Standings by Division")
        print("2. View Past Games")
        print("3. Predict Upcoming Games")
        print("4. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            display_division_standings(data['standings'])
        elif choice == '2':
            view_past_games(data)
        elif choice == '3':
            predict_game(data)
        elif choice == '4':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

# Main program
if __name__ == "__main__":
    nfl_data = load_nfl_data()
    display_menu(nfl_data)
