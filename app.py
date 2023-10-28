from flask import Flask, request, jsonify, render_template
import requests
import json
import openai
import time


app = Flask(__name__)





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
    games = ["The Legend of Zelda: Breath of the Wild", "Super Mario Odyssey", "Dark Souls: Remastered", "Bloodstained: Curse of the Moon", "Undertale"]


    # Query MobyGames API for each game and get their covers
    
    game_covers = []
    for game in games:
        response = requests.get(f"https://api.mobygames.com/v1/games?format=normal&title={game}&api_key=moby_yMk1vNu3muhFd4QzvcNYhhlYLXU")
        data = response.json()
        print(data)
        if 'games' in data and len(data['games']) > 0:
            game_covers.append(data['games'][0]['sample_cover']['image'] if data['games'][0]['sample_cover'] else '')
            print(game_covers)
        else:
            game_covers.append('')
        print(game_covers)
        time.sleep(1)
    return jsonify({'recommendation': games, 'covers': game_covers})

'''
The Legend of Zelda: Breath of the Wild

Super Mario Odyssey

Dark Souls: Remastered

Bloodstained: Curse of the Moon

Undertale

'''




@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return "500 error"

if __name__ == '__main__':
    app.run(debug=True)