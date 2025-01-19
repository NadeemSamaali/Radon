from generator import generate_doc
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

difficulty = 0.0
language = ''

@app.route('/')
def home():
    return render_template('RadonMainPage.html')  # Main page

@app.route('/done')
def worksheet_page():
        # Generate the worksheet content first
    worksheet = generate_doc(language, round(float(difficulty) * 15))
    
    # Pass the generated worksheet to the template
    return render_template('RadonExercise.html', worksheet=worksheet)

@app.route('/your-endpoint', methods=['POST'])
def handle_json():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Access the data sent from the client
    global difficulty, language
    difficulty = data.get('difficulty')
    language = data.get('language')

    # Respond with a JSON message (optional)
    response = {"status": "success", "message": "Data received successfully!"}
    return jsonify(response)

@app.route('/get-worksheet')
def get_workshet():
    # String to be sent to JavaScript
    worksheet = generate_doc('fr', 5)
    return jsonify({"message": worksheet})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
