from flask import Flask, request, jsonify, render_template
import requests
import json
import openai

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
    data = request.get_json()
    prompt = data['prompt']

    openai.api_key = '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'

    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=100
    )

    # Extract the list of game names from the response
    recommendation = response.choices[0].text.strip()
    start = recommendation.find('[')
    end = recommendation.find(']') + 1
    games = json.loads(recommendation[start:end])

    return jsonify({'recommendation': games})


@app.errorhandler(500)
def internal_error(exception):
    app.logger.error(exception)
    return "500 error"

if __name__ == '__main__':
    app.run(debug=True)