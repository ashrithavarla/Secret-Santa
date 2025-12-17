from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import random
import secrets
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

ASSIGNMENTS_FILE = 'secret_santa_assignments.xlsx'

# Load employee data
def load_employees():
    data = {
        'Full Name': ['name1', 'name2', 'name3', 'name4', 'name5', 'name6', 'name7', 'name8'],
        'Email': ['email1', 'email2', 'email3', 'email4', 'email5', 'email6', 'email7', 'email8']
    }
    return pd.DataFrame(data)

def load_assignments():
    if os.path.exists(ASSIGNMENTS_FILE):
        return pd.read_excel(ASSIGNMENTS_FILE)
    return pd.DataFrame(columns=['Email', 'Name', 'Assigned_To', 'Timestamp'])

def save_assignment(email, name, assigned_to):
    df = load_assignments()
    new_row = pd.DataFrame({
        'Email': [email],
        'Name': [name],
        'Assigned_To': [assigned_to],
        'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(ASSIGNMENTS_FILE, index=False)

employees_df = load_employees()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reveal')
def reveal():
    return render_template('reveal.html')

@app.route('/verify_email', methods=['POST'])
def verify_email():
    email = request.json.get('email', '').strip().lower()
    
    # Check if email exists
    if email not in employees_df['Email'].str.lower().values:
        return jsonify({'success': False, 'message': 'Email not found in the list'})
    
    # Check if already used
    assignments_df = load_assignments()
    if email in assignments_df['Email'].str.lower().values:
        return jsonify({'success': False, 'message': 'You have already participated'})
    
    # Get person's name
    person_name = employees_df[employees_df['Email'].str.lower() == email]['Full Name'].values[0]
    
    # Store in session
    session['email'] = email
    session['name'] = person_name
    
    return jsonify({'success': True})

@app.route('/get_numbers', methods=['GET'])
def get_numbers():
    if 'email' not in session:
        return jsonify({'success': False, 'message': 'Session expired'})
    
    email = session['email']
    person_name = session['name']
    
    # Get available names
    assignments_df = load_assignments()
    available_names = list(employees_df['Full Name'].values)
    available_names.remove(person_name)
    
    for assigned in assignments_df['Assigned_To'].values:
        if assigned in available_names:
            available_names.remove(assigned)
    
    if not available_names:
        return jsonify({'success': False, 'message': 'No more assignments available'})
    
    # Create random numbers list
    random.shuffle(available_names)
    numbers = list(range(1, len(available_names) + 1))
    random.shuffle(numbers)
    
    # Store in session
    session['available_names'] = available_names
    session['numbers'] = numbers
    
    return jsonify({'success': True, 'numbers': numbers})

@app.route('/flip_card', methods=['POST'])
def flip_card():
    if 'email' not in session or 'available_names' not in session:
        return jsonify({'success': False, 'message': 'Session expired'})
    
    number = request.json.get('number')
    email = session['email']
    person_name = session['name']
    available_names = session['available_names']
    
    # Random assignment
    assigned_name = random.choice(available_names)
    
    # Save to Excel
    save_assignment(email, person_name, assigned_name)
    
    # Clear session
    session.clear()
    
    return jsonify({'success': True, 'name': assigned_name})

if __name__ == '__main__':
    app.run(debug=False)