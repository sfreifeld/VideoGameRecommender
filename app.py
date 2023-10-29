from flask import Flask, request, jsonify, render_template, session
import requests
import json
import openai
import time


app = Flask(__name__)
app.secret_key = 'yMk1vNu3muhFd4QzvcNYhhlYLXU'





@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search_game')
def search_game():
    query = request.args.get('query')
    response = requests.get(f"https://api.mobygames.com/v1/games?format=normal&title={query}&api_key=moby_yMk1vNu3muhFd4QzvcNYhhlYLXU")
    data = response.json()
    if 'games' in data:
        games = [{'label': game['title'], 'value': game['title'], 'sample_cover': game['sample_cover']['image'] if game['sample_cover'] else None} for game in data['games']]
    else:
        games = []
    return jsonify(games)

@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    '''data = request.get_json()
    prompt = data['prompt']

    
    with open('./secrets.json') as f:
        secrets = json.load(f)

    apiKey = secrets['API_KEY']
    openai.api_key = apiKey

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=100
    )'''

    # Extract the list of game names from the response
    #recommendation = response.choices[0].text.strip()
    #start = recommendation.find('[')
    #end = recommendation.find(']') + 1
    #games = json.loads(recommendation[start:end])
    games = ["Super Mario Odyssey", "Dark Souls: Remastered", "Undertale"]

    game_details = []
    for game in games:
        response = requests.get(f"https://api.mobygames.com/v1/games?format=normal&title={game}&api_key=moby_yMk1vNu3muhFd4QzvcNYhhlYLXU")
        data = response.json()
        if 'games' in data and len(data['games']) > 0:
            game_data = data['games'][0]
            game_info = {
                'name': game_data['title'],
                'cover': game_data['sample_cover']['image'] if game_data['sample_cover'] else '',
                'description': game_data['description'] if 'description' in game_data else 'No description available.',
                'genres': game_data['genres'],
                'platforms': game_data['platforms'],
                'moby_score': game_data['moby_score']
            }
            game_details.append(game_info)
        else:
            game_details.append({
                'name': game,
                'cover': '',
                'description': 'No details available for this game.'
            })
        time.sleep(1)

    # Store the game details in the user's session
    session['game_details'] = game_details

    return jsonify({'recommendations': game_details})




@app.route('/game_info/<game_name>')
def game_info(game_name):
    # Retrieve the game details from the API
    game_details = session.get('game_details', []) # Replace this with your actual function

    for game in game_details:
        if game['name'] == game_name:
            return render_template('game_info.html', game=game)

    # Pass the game details to the template
    return render_template('game_info.html', game={'name': game_name, 'cover': '', 'description': 'No details available for this game.'})


@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return "500 error"

if __name__ == '__main__':
    app.run(debug=True)