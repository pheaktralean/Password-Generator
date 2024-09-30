from flask import Flask, render_template, jsonify, request
import random
import string
import json
app = Flask(__name__)

# Load Configuration from JSON file
with open('password_generator_config.json') as config_file:
    config = json.load(config_file)

# Store the characters in string from the config file
lower_chars = config['character_sets']['lowercase']['chars']
upper_chars = config['character_sets']['uppercase']['chars']
numbers = config['character_sets']['numbers']['chars']
symbols = config['character_sets']['symbols']['chars']


# default password generator function
def password_generator(length=8, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True):
    char_pool = ''
    if use_uppercase:
        char_pool += upper_chars
    if use_lowercase:
        char_pool += lower_chars
    if use_numbers:
        char_pool += numbers
    if use_symbols:
        char_pool += symbols

    password = ''.join(random.choice(char_pool) for _ in range(length))
    return password


# (password_generator(length=12, use_uppercase=True, use_lowercase=True, use_numbers=True, use_symbols=True))


@app.route('/')
def index():
    return render_template('index.html')


# API route for generating the password
@app.route('/generate-password', methods=['POST'])
def generate_password():
    data = request.json
    length = data.get('length', config['default_settings']['length'])  # Use default from config

    # Get character type preferences by user
    use_uppercase = data.get('use_uppercase', config['default_settings']['use_uppercase'])
    use_lowercase = data.get('use_lowercase', config['default_settings']['use_lowercase'])
    use_numbers = data.get('use_numbers', config['default_settings']['use_numbers'])
    use_symbols = data.get('use_symbols', config['default_settings']['use_symbols'])

    try:
        # Generate the password
        password = password_generator(length, use_uppercase, use_lowercase, use_numbers, use_symbols)
        return jsonify({'password': password})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
