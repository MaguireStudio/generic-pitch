from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/some-endpoint', methods=['GET'])
def some_endpoint():
    # Handle requests here
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    SHEET_API_URL = os.getenv('SHEET_API_URL')
    if SHEET_API_URL:
        print('SHEET_API_URL is set')
    else:
        print('SHEET_API_URL is not set, the app will run without it')
    app.run(host='0.0.0.0', port=5000)