from flask import Flask, render_template, jsonify, request
import nfl_data_py as nfl
import pandas as pd
import ssl
import traceback

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load and preprocess NFL data
def load_nfl_data():
    try:
        # Specify the year of schedule data
        years = [2024]

        print("Attempting to import team descriptions...")
        teams = nfl.import_team_desc()

        print(f"Attempting to import schedules for year(s): {years}")
        schedules = nfl.import_schedules(years=years)

        # Additional checks for data retrieval
        if teams is None or teams.empty:
            print("Error: No team data retrieved.")
            return None

        if schedules is None or schedules.empty:
            print("Error: No schedule data retrieved.")
            return None

        schedules = schedules[schedules['game_type'] == 'REG']

        if 'home_score' in schedules.columns and 'away_score' in schedules.columns:
            schedules['result'] = schedules.apply(
                lambda row: 'W' if row['home_score'] > row['away_score'] else 'L',
                axis=1
            )
        else:
            raise ValueError("Scores are missing from the schedules data.")

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

        standings = pd.merge(home_results, away_results, 
                              left_on='home_team', 
                              right_on='away_team', 
                              how='outer').fillna(0)

        standings['team'] = standings['home_team'].combine_first(standings['away_team'])
        standings['total_wins'] = standings['home_wins'] + standings['away_wins']
        standings['total_losses'] = standings['home_losses'] + standings['away_losses']
        standings['total_ties'] = standings['ties_x'] + standings['ties_y']

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

        standings = standings[['team', 'division', 'total_wins', 'total_losses', 'total_ties']].sort_values(
            by=['division', 'total_wins'], ascending=[True, False]
        )

        return {
            "teams": teams,
            "standings": standings,
            "games": schedules
        }
    except Exception as e:
        print("Comprehensive Error Loading NFL Data:")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")
        print("\nDetailed Traceback:")
        traceback.print_exc()
        return None

nfl_data = load_nfl_data()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/standings', methods=['GET'])
def standings():
    if nfl_data and 'standings' in nfl_data:
        return jsonify(nfl_data['standings'].to_dict(orient='records'))
    else:
        return jsonify({"error": "Standings data not available."}), 500

@app.route('/past_games', methods=['GET'])
def past_games():
    if nfl_data and 'games' in nfl_data:
        past_games = nfl_data['games'][nfl_data['games']['result'].notna()]
        return jsonify(past_games[['home_team', 'away_team', 'home_score', 'away_score', 'result']].to_dict(orient='records'))
    else:
        return jsonify({"error": "Past games data not available."}), 500

@app.route('/predict', methods=['GET'])
def predict():
    if nfl_data and 'games' in nfl_data and 'standings' in nfl_data:
        upcoming_games = nfl_data['games'][nfl_data['games']['result'].isna()]
        standings = nfl_data['standings']

        predictions = []
        for _, game in upcoming_games.iterrows():
            home_team = game['home_team']
            away_team = game['away_team']

            home_stats = standings[standings['team'] == home_team].iloc[0]
            away_stats = standings[standings['team'] == away_team].iloc[0]

            home_total_games = home_stats['total_wins'] + home_stats['total_losses'] + home_stats['total_ties']
            away_total_games = away_stats['total_wins'] + away_stats['total_losses'] + away_stats['total_ties']

            home_win_rate = home_stats['total_wins'] / home_total_games if home_total_games > 0 else 0
            away_win_rate = away_stats['total_wins'] / away_total_games if away_total_games > 0 else 0

            home_probability = home_win_rate / (home_win_rate + away_win_rate) if (home_win_rate + away_win_rate) > 0 else 0.5
            away_probability = 1 - home_probability

            predicted_winner = home_team if home_probability > away_probability else away_team

            predictions.append({
                'home_team': home_team,
                'away_team': away_team,
                'predicted_winner': predicted_winner,
                'win_probability': max(home_probability, away_probability)
            })

        return jsonify(predictions)
    else:
        return jsonify({"error": "Prediction data not available."}), 500

if __name__ == '__main__':
    app.run(debug=True)