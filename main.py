from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# store the characters in lists
lower_chars = ['a','b','c','d','e','f','g','h','i','j',
                'k','l','m','n','o','p','q','r','s','t','u',
                'v','w','x','y','z']
upper_chars = ['A', 'B', 'C', 'D','E','F','G','H','I','J',
                'K','L','M','N','O','P','Q','R','S','T','U',
                'V','W','X','Y','Z']
numbers = ['0','1','2','3','4','5','6','7','8','9']
special_chars = ['!', '@','#','$','%','&','*']

# default password generator function
def default_password_generator():
    password = random.choice(lower_chars) + random.choice(upper_chars) + random.choice(numbers) + random.choice(
        special_chars)
    password += ''.join(random.choices(lower_chars + upper_chars + numbers + special_chars, k=4))
    return ''.join(random.sample(password, len(password)))

# custom password generator function
def custom_password_generator(lower_count, upper_count, number_count, special_count):
    password = ''
    password += ''.join(random.choices(lower_chars, k=lower_count))
    password += ''.join(random.choices(upper_chars, k=upper_count))
    password += ''.join(random.choices(numbers, k=number_count))
    password += ''.join(random.choices(special_chars, k=special_count))
    return ''.join(random.sample(password, len(password)))

@app.route('/')
def index():
    return render_template('index.html')

# API route for generating the password
@app.route('/generate-password', methods=['GET'])
def generate_password():
    data = request.json
    if data['type'] == 'default':
        password = default_password_generator()
    elif data['type'] == 'custom':
        lower_count = data['lower_count']
        upper_count = data['upper_count']
        number_count = data['number_count']
        special_count = data['special_count']
        password = custom_password_generator(lower_count, upper_count, number_count, special_count)
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)