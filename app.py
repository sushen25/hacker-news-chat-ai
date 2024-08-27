from flask import Flask, render_template, jsonify
from myHackerNews import get_top_news

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-top-news', methods=['GET'])
def get_message():
    result = get_top_news()
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)