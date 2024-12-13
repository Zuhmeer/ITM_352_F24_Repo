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

        # Standardize team names for matching
        team_mapping = {
            "ARI": "Arizona Cardinals", "ATL": "Atlanta Falcons", "BAL": "Baltimore Ravens",
            "BUF": "Buffalo Bills", "CAR": "Carolina Panthers", "CHI": "Chicago Bears",
            "CIN": "Cincinnati Bengals", "CLE": "Cleveland Browns", "DAL": "Dallas Cowboys",
            "DEN": "Denver Broncos", "DET": "Detroit Lions", "GB": "Green Bay Packers",
            "HOU": "Houston Texans", "IND": "Indianapolis Colts", "JAX": "Jacksonville Jaguars",
            "KC": "Kansas City Chiefs", "LA": "Los Angeles Rams", "LAC": "Los Angeles Chargers",
            "LV": "Las Vegas Raiders", "MIA": "Miami Dolphins", "MIN": "Minnesota Vikings",
            "NE": "New England Patriots", "NO": "New Orleans Saints", "NYG": "New York Giants",
            "NYJ": "New York Jets", "PHI": "Philadelphia Eagles", "PIT": "Pittsburgh Steelers",
            "SEA": "Seattle Seahawks", "SF": "San Francisco 49ers", "TB": "Tampa Bay Buccaneers",
            "TEN": "Tennessee Titans", "WAS": "Washington Commanders"
        }
        standings['team'] = standings['team'].map(team_mapping)

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

        standings['division'] = standings['team'].apply(
            lambda team: next((div for div, teams in divisions.items() if team in teams), "Unknown")
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
