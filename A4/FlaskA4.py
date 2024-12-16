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
        lambda row: 'W' if row['home_score'] > row['away_score'] else ('L' if row['home_score'] < row['away_score'] else 'TBD'),
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
    "AFC East": ["BUF", "MIA", "NYJ", "NE"],
    "AFC North": ["PIT", "BAL", "CIN", "CLE"],
    "AFC South": ["HOU", "IND", "TEN", "JAX"],
    "AFC West": ["KC", "LAC", "DEN", "LV"],
    "NFC East": ["PHI", "WAS", "DAL", "NYG"],
    "NFC North": ["DET", "MIN", "GB", "CHI"],
    "NFC South": ["ATL", "TB", "NO", "CAR"],
    "NFC West": ["SEA", "ARI", "LA", "SF"]
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
print(nfl_data)

@app.route('/standings2')
def standings2():
    if nfl_data and 'standings' in nfl_data and 'teams' in nfl_data:
        return render_template('standings2.html', standings=nfl_data['standings'].to_dict(orient='records'), team=nfl_data['teams'].to_dict(orient='records'))
    else:
        return jsonify({"error": "Standings or teams data not available."}), 500
    
    
@app.route('/pastgames2')
def pastgames2():
    if nfl_data and 'games' in nfl_data:
        games = nfl_data['games']
        past_games = games[games['result'].notna()]
        
        return render_template('pastgames2.html', games=games.to_dict(orient='records'), past_games=past_games.to_dict(orient='records'))
    else:
        return jsonify({"error": "Games or past games data not available."}), 500


@app.route('/predict2')
def predict2_page():
    return render_template('predict2.html')  # Serve the predictions page


@app.route('/predict2-data', methods=['GET'])
def predict2_data():
    if nfl_data and 'games' in nfl_data and 'standings' in nfl_data:
        upcoming_games = nfl_data['games'][nfl_data['games']['result'].isna()]
        standings = nfl_data['standings']

        predictions = []
        for _, game in upcoming_games.iterrows():
            home_team = game['home_team']
            away_team = game['away_team']

            # Defensive check for standings lookup
            if home_team not in standings['team'].values or away_team not in standings['team'].values:
                continue

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


@app.route('/teams')
def teams():
    if nfl_data and 'standings' in nfl_data:
        teams = nfl_data['standings']['team'].tolist()
        return jsonify({"teams": teams})
    else:
        return jsonify({"error": "Team data not available."}), 500


@app.route('/predict2-custom', methods=['GET'])
def predict2_custom():
    home_team = request.args.get('home_team')
    away_team = request.args.get('away_team')

    if not home_team or not away_team:
        return jsonify({"error": "Both teams must be selected."}), 400

    if home_team == away_team:
        return jsonify({"error": "Teams must be different."}), 400

    if nfl_data and 'standings' in nfl_data:
        standings = nfl_data['standings']
        if home_team not in standings['team'].values or away_team not in standings['team'].values:
            return jsonify({"error": "Selected teams are not valid."}), 400

        home_stats = standings[standings['team'] == home_team].iloc[0]
        away_stats = standings[standings['team'] == away_team].iloc[0]

        home_total_games = home_stats['total_wins'] + home_stats['total_losses'] + home_stats['total_ties']
        away_total_games = away_stats['total_wins'] + away_stats['total_losses'] + away_stats['total_ties']

        home_win_rate = home_stats['total_wins'] / home_total_games if home_total_games > 0 else 0
        away_win_rate = away_stats['total_wins'] / away_total_games if away_total_games > 0 else 0

        home_probability = home_win_rate / (home_win_rate + away_win_rate) if (home_win_rate + away_win_rate) > 0 else 0.5
        away_probability = 1 - home_probability

        predicted_winner = home_team if home_probability > away_probability else away_team

        return jsonify({
            "home_team": home_team,
            "away_team": away_team,
            "predicted_winner": predicted_winner,
            "win_probability": max(home_probability, away_probability) * 100
        })
    else:
        return jsonify({"error": "Prediction data not available."}), 500


@app.route('/teams', methods=['GET'])
def get_teams():
    nfl_teams = [
        "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", "DET", "GB", 
        "HOU", "IND", "JAX", "KC", "LV", "LAC", "LA", "MIA", "MIN", "NE", "NO", "NYG", "NYJ", 
        "PHI", "PIT", "SF", "SEA", "TB", "TEN", "WAS"
    ]
    return jsonify({"teams": nfl_teams})

if __name__ == '__main__':
    app.run(debug=True)



