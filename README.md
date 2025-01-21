# Radon

Radon is a Flask-based web application designed to create customized language learning worksheets. These worksheets contain vocabulary exercises, translation tasks, and sentence-building activities, which are dynamically generated based on user preferences.

## Features

- **Dynamic Worksheet Generation**: Create language exercises tailored to the desired difficulty level and target language.
- **Multilingual Support**: Translate and generate exercises in multiple languages using Google Translate.
- **Engaging Activities**: Includes vocabulary banks, fill-in-the-blank exercises, translation matching, and sentence unscrambling.
- **Interactive Frontend**: A user-friendly interface powered by Flask and HTML templates.

## Application Structure

### File Overview

1. **app.py**:  
   The main Flask application, which handles routes, user input, and rendering of HTML templates.
2. **generator.py**:  
   The core logic for generating worksheets, including vocabulary selection, translations, and exercise formatting.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd Radon
   ```

2. **Install Dependencies**: 
    Make sure you have Python 3.7 or later installed. Then, install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
3. **Setup API key** :
    Replace the placeholder API key in `generator.py` with your Google Generative AI key:
    ```python
    genai.configure(api_key="YOUR_GOOGLE_GENERATIVE_AI_KEY")
    ```

4. **Run the Application**:
    ```bash
    python app.py
    ```
    The application will run on http://localhost:7116.

## Acknowledgements

* NLTK for the comprehensive natural language tools.
* Google Translate API for multilingual support.
* Flask for its simplicity in building web applications
